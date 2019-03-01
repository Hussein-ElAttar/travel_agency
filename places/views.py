from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Country, City, Location, Hotel, CityHotel,CityPics, UserCityRate, UserCarRent, UserHotelReservation
from .forms import UserCityRateForm, UserCarRentForm, HotelReservationForm
from .utils.crawler import Gretty_Image_Crawler, Yahoo_Image_Crawler
from .utils.CityHandler import CityHandler
from blog.forms import CommentForm, PostForm
from blog.models import Post, Comment
from django.http import JsonResponse
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
        country = Country.objects.get(name=countryName)
        cities  = City.objects.filter(country=country.id)
        context = {"country": country, "cities": cities, "countries":getAllCountries()}
        return render(request, "country.html", context)
    except:
        return HttpResponseRedirect("/")

def city_page(request, countryName, cityName):
    try:
        city_handler = CityHandler(request, countryName, cityName)
        context      = city_handler.get_context()
        context['countries'] = getAllCountries()
        return render(request, "city.html", context)
    except:
        return HttpResponseRedirect("/")

def homePage(request):
    countries = getAllCountries()
    top_cities = UserCityRate.objects.order_by('-rate')[:3]
    context = {"top_cities": top_cities,"countries":getAllCountries()}
    return render(request, 'homepage.html', context)


@login_required
def showUserReservations(request):   
    try:
        reservations=UserHotelReservation.objects.get(user=request.user.id) 
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
                user      =request.user.id,
                hotel     =request.POST.get('name'),
                rooms     =request.POST.get('rooms'),
                room_type =request.POST.get('room_type'),
                to_Date   =request.POST.get('to_Date'),
                from_Date =request.POST.get('from_Date')
            )
            return HttpResponseRedirect('/places/')
    else:
        form = HotelReservationForm()
        context = {'hotel_form': form}
    
        return render(request, 'hotelReservation.html', context)


def city_api(request,countryName, cityName):
    try:
        country = Country.objects.get(name = countryName)
        city    = City.objects.get(name = cityName, country = country)
        data = get_city_data(city)
        return JsonResponse({
            "city":data['city'],
            "urls":data['urls'],
            "description":data['description']
        })
    except:
        return JsonResponse({"status":"404","error":"not found"})

def country_api(request, countryName):
    try:
        country = Country.objects.get(name = countryName)
        country_cities    = City.objects.filter(country = country)
        random_valid_city_num = random.randint(0, len(country_cities)-1)
        city = country_cities[random_valid_city_num]
        data = get_city_data(city)
        return JsonResponse({
            "country":country.name,
            "urls":data['urls'],
        })
    except:
        return JsonResponse({"status":"404","error":"not found"})

def get_city_data(city):
    if city.is_crawled:
        urls = []
        desc = city.description
        city_pics_query = CityPics.objects.filter(city_id=city.id)
        for city_pic in city_pics_query:
            urls.append(city_pic.url)
    else:
        cr = Gretty_Image_Crawler(city.name)
        desc = cr.get_city_description()
        city.description = desc
        urls = cr.get_urls()[:10]
        for url in urls:
            CityPics.objects.create(url=url, city = city)
        city.is_crawled = True
        city.save()

    return {"city":city.name, "urls":urls, "description":desc}