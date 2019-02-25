from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Country, City, Location, Hotel, CityHotel,CityPics, UserCityRate, UserCarRent, UserHotelReservation
from .forms import UserCityRateForm, UserCarRentForm, HotelReservationForm
from pprint import *
from .utils.crawler import Gretty_Image_Crawler, Yahoo_Image_Crawler
from blog.forms import CommentForm, PostForm
from blog.models import Post, Comment
from django.http import JsonResponse
import json
import random

# Create your views here.


def getAllCountries():
    countries = Country.objects.all()[:30]
    return countries


def index(request):
    countries = Country.objects.all()
    context = {"countries": countries}
    return render(request, "index.html", context)


def country_page(request, countryName):
    try:
        country = Country.objects.get(country_Name=countryName)
        cities  = City.objects.filter(country_Name_id=country.id)
        context = {"country": country, "cities": cities, "countries":getAllCountries()}
        return render(request, "country.html", context)
    except:
        return HttpResponseRedirect("/")


def city_page(request, countryName, cityName):
    return city_handler.handle_request(request, countryName, cityName)


class city_handler:
    @staticmethod
    def handle_request(request, countryName, cityName):
        try:
            country = Country.objects.get(country_Name = countryName)
            city    = City.objects.get(city_Name = cityName, country_Name_id = country.id)
            posts   = city_handler.__get_city_posts(request, city.id)
            
            if request.method == 'GET':
                form  = city_handler.__get_saved_user_rating_form(request, city.id)

            if request.method == 'POST':
                form      = UserCityRateForm(request.POST)
                post_form = PostForm(request.POST)

                comment_form = CommentForm(request.POST)
                city_handler.__create_post(request, post_form, city.id)
                city_handler.__rate_city(request, form, city.id)
                city_handler.__create_comment(request, form, city.id)

            context = {
                "country": country, 
                "city":city,
                "form": form,
                "post": PostForm(),
                "posts": posts,
                "countries":getAllCountries()
            }
            return render(request, "city.html", context)
        except:
            return HttpResponseRedirect("/")

    @staticmethod
    def __get_saved_user_rating_form(request, cityId):
        if request.user.is_authenticated:
            try:
                rate_value = UserCityRate.objects.get(user_id = request.user.id, city_id = cityId).rate
                user_rating = {"rate": rate_value}
            except :
                user_rating = None
            finally:            
                return UserCityRateForm(user_rating)
        else:
            return None
    
    @staticmethod
    def __get_city_posts(request, cityId):
        try:
            posts = Post.objects.filter(city_Name_id=cityId)
            print(posts[0])
        except:
            posts = []
        return posts

    @staticmethod
    def __get_post_comments(request, cityId):
        all_posts_comments = []
        try:
            posts = Post.objects.filter(city_Name_id=cityId)
            for post in posts:
                comments = Comment.objects.filter(post_Id=post.id)
                post_comments = {'post_id': post.id, 'post_comments': comments}
                all_posts_comments.append(post_comments)
        except:
            all_posts_comments = []
        return all_posts_comments

    @staticmethod
    def __rate_city(request, form, cityId):
        if form.is_valid():
            rate = form.cleaned_data.get('rate')
            try:
                UserCityRate.objects.create(user_id = request.user.id, city_id = cityId, rate = rate)
            except:
                UserCityRate.objects.filter(user_id = request.user.id, city_id = cityId ).update(rate = rate)

    @staticmethod
    def __create_post(request, post_form, city_id):
        if post_form.is_valid():
            postText = post_form.cleaned_data.get('post_Text')
            Post.objects.create(user_Name = request.user , city_Name = City(id=city_id), post_Text = postText)

    def __create_comment(request, comment_form, city_id):
        if comment_form.is_valid():
            commentText = comment_form.cleaned_data.get('comment_Text')
            Comment.objects.create(user_Name = request.user , city_Name = City(id=city_id), comment_Text = commentText)

# Country Methods :-

def homePage(request):
    countries = getAllCountries()
    top_cities = UserCityRate.objects.order_by('-rate')[:3]
    context = {"top_cities": top_cities,"countries":getAllCountries()}
    return render(request, 'homepage.html', context)


@login_required
def showUserReservations(request):   
    try:
        reservations=UserHotelReservation.objects.get(user_Name=request.user.id) 
        rents=showUserRentals(request)     
        context={"reservations":reservations,"rents":rents}    
    except:
        context={"reservations":[],"rents":[]}
    return render(request,'single.html', context)

@login_required
def showUserRentals(request):
    rents=UserCarRent.objects.get(user=request.user.id)
    return rents


def rentCar(request):
    form = UserCarRentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # form.save()
            UserCarRent.objects.create(
                user_id        =request.user.id,
                pickup_loc_id  =request.POST.get('pickup_loc'),
                dropoff_loc_id =request.POST.get('dropoff_loc'),
                time           =request.POST.get('time')
            )

        return HttpResponseRedirect('/rentcar/')

    else:
        form = UserCarRentForm()
        context = {"form": form}
        return render(request, "rentCar.html", context)


def hotelReservation(request):
    if request.method == 'POST':
        form = HotelReservationForm(request.POST)
        if form.is_valid():
            UserHotelReservation.objects.create(
                user_Name =request.user.id,
                hotel_Name=request.POST.get('hotel_Name'),
                rooms     =request.POST.get('rooms'),
                room_type =request.POST.get('room_type'),
                to_Date  =request.POST.get('to_Date'),
                from_Date=request.POST.get('from_Date')
            )
            return HttpResponseRedirect('/places/')
    else:
        form = HotelReservationForm()
        context = {'hotel_form': form}
    
        return render(request, 'hotelReservation.html', context)


def city_api(request,countryName, cityName):
    try:
        country = Country.objects.get(country_Name = countryName)
        city    = City.objects.get(city_Name = cityName, country_Name_id = country.id)
        if city.city_is_crawled:
            urls = []
            desc = city.city_Description
            city_pics_query = CityPics.objects.filter(city_id=city.id)
            for city_pic in city_pics_query:
                urls.append(city_pic.url)
        else:
            cr = Gretty_Image_Crawler(cityName)
            desc = cr.get_city_description()
            city.city_Description = desc
            urls = cr.get_urls()[:10]
            for url in urls:
                CityPics.objects.create(url=url, city = city)
            city.city_is_crawled = True
            city.save()

        return JsonResponse({"city":city.city_Name, "urls":urls, "description":desc})
    except:
        return JsonResponse({"status":"404","error":"not found"})


def country_api(request, countryName):
    try:
        country = Country.objects.get(country_Name = countryName)
        country_cities    = City.objects.filter(country_Name_id = country.id)
        random_valid_city_num = random.randint(0, len(country_cities)-1)
        city = country_cities[random_valid_city_num]
        
        if city.city_is_crawled:
            urls = []
            desc = city.city_Description
            city_pics_query = CityPics.objects.filter(city_id=city.id)
            for city_pic in city_pics_query:
                urls.append(city_pic.url)
        else:
            cr = Gretty_Image_Crawler(city.city_Name)
            desc = cr.get_city_description()
            city.city_Description = desc
            urls = cr.get_urls()[:10]
            for url in urls:
                CityPics.objects.create(url=url, city = city)
            city.city_is_crawled = True
            city.save()

        return JsonResponse({"country":country.country_Name, "urls":urls, "description":desc})
    except:
        return JsonResponse({"status":"404","error":"not found"})