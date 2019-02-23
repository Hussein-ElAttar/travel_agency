from array import array
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Country, City, Location, Hotel, CityHotel, UserCityRate, UserCarRent, UserHotelReservation
from .forms import UserCityRateForm, UserCarRentForm, HotelReservationForm
from pprint import *
from .utils.crawler import Gretty_Image_Crawler, Yahoo_Image_Crawler
from blog.forms import CommentForm, PostForm
from blog.models import Post, Comment
import json
# Create your views here.

# index Test :-


def getAllCountries():
    countries = Country.objects.all()[:30]
    return countries


def index(request):
    countries = getAllCountries()
    context = {"countries": countries}
    return render(request, "index.html", context)


def country_page(request, countryName):
    try:
        country = Country.objects.get(country_Name=countryName)
        cities  = City.objects.filter(country_Name_id=country.id)
        country_cr = Gretty_Image_Crawler(country.country_Name)
        country_img_url = country_cr.get_random_url()
        country.image = country_img_url
        context = {"country": country, "cities": cities,"countries":getAllCountries()}
        return render(request, "country.html", context)
    except:
        return HttpResponseRedirect("/places/")

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

                city_handler.__create_post(request, post_form, city.id)
                city_handler.__rate_city(request, form, city.id)

            cr = Gretty_Image_Crawler(cityName)
            city_img_url = cr.get_random_url()
            description = cr.get_city_description()
            
            context = {
                "country": country, 
                "city":city,
                "city_img_url":city_img_url,
                "description":description,
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

# Country Methods :-

def homePage(request):
    countries = getAllCountries()
    top_cities = UserCityRate.objects.order_by('-rate')[:3]
    context = {"top_cities": top_cities,"countries":getAllCountries()}
    return render(request, 'homepage.html', context)


# City Methods :-
def getAllCities(request):
    cities = City.objects.all()
    context = {"cities": cities}
    return render(request, "cityPage.html", context)


def getCityById(request, cityId):
    city = City.objects.get(id=eval(cityId))
    context = {"city": city}
    return render(request, "cityPage.html", context)


# Location Methods :-
def getAllLocations(request):
    locations = Location.objects.all()
    context = {"locations": locations}
    return render(request, "locationsPage.html", context)


def getLocationById(request, locationId):
    location = Location.objects.get(id=eval(locationId))
    context = {"location": location}
    return render(request, "locationPage.html", context)


# Hotel Methods :-
def getAllHotels(request):
    hotels = Hotel.objects.all()
    context = {"hotels": hotels}
    return render(request, "hotelsPage.html", context)


def getHotelById(request, hotelId):
    hotel = Hotel.objects.get(id=eval(hotelId))
    context = {"hotel": hotel}
    return render(request, "hotelPage.html", context)


# Services
def getUserCityRate(request, cityId):
    rate = UserCityRate.objects.filter(user_id = request.user.id, city_id = cityId)
    context = {"rate": rate}
    return context


@login_required
def getUserCarRentals(request, cityId):
    userCityRatentals = UserCarRent.objects.filter(user_id = request.user.id)
    context = {"rentals": userCityRatentals}
    return context


def showUserReservations(request):   
    try:
        reservations=UserHotelReservation.objects.get(user_Name=request.user.id) 
        rents=showUserRentals(request)     
        context={"reservations":reservations,"rents":rents}    
    except:
        context={"reservations":[],"rents":[]}
    return render(request,'single.html', context)


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

        return HttpResponseRedirect('/places/cities/rentCar/')

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
        cr = Gretty_Image_Crawler(cityName)
        obj = {"urls":cr.get_urls(),"url":cr.get_random_url(),"description":cr.get_city_description()}
        return HttpResponse(json.dumps(obj))
    except:
        return HttpResponse(json.dumps({"status":"404","error":"not found"}))

def country_api(request,countryName):
    try:
        country = Country.objects.get(country_Name = countryName)
        cr = Gretty_Image_Crawler(countryName)
        obj = {"urls":cr.get_urls(),"url":cr.get_random_url()}
        return HttpResponse(json.dumps(obj))
    except:
        return HttpResponse(json.dumps({"status":"404","error":"not found"}))