from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Country, City, Location, Hotel, CityHotel, UserCityRate, UserCarRent, UserHotelReservation
from .forms import UserCityRateForm, UserCarRentForm, HotelReservationForm
from pprint import *

# Create your views here.


# index Test :-
def index(request):
    countries = getAllCountries()
    context = {"countries": countries }
    return render(request, "index.html", context)


def country_page(request, countryName):
    try:
        country = Country.objects.get(country_Name=countryName)
        cities  = City.objects.filter(country_Name_id=country.id)
        context = {"country": country, "cities": cities}
        return render(request, "country.html", context)
    except:
        return HttpResponseRedirect("/places/")

def city_page(request, countryName, cityName):
    return city_handler.handle_request(request, countryName, cityName)

class city_handler:
    @staticmethod
    def handle_request(request, countryName,cityName):
        try:
            country = Country.objects.get(country_Name = countryName)
            city    = City.objects.get(city_Name = cityName, country_Name_id = country.id)

            if request.method == 'GET':
                form = city_handler.__get_saved_user_rating_form(request, city.id)

            if request.method == 'POST':
                form = UserCityRateForm(request.POST)
                city_handler.__rate_city(request, form, city.id)

            context = {"country": country, "city":city,"form": form}
            return render(request, "city.html", context) 
        except:
            return HttpResponseRedirect("/places/")

    @staticmethod
    def __get_saved_user_rating_form(request,cityId):
        if request.user.is_authenticated:
            try:
                rate_value = UserCityRate.objects.get(user_id = request.user.id, city_id = cityId).rate
                user_rating = {"rate":rate_value}
            except :
                user_rating = None
            finally:            
                return UserCityRateForm(user_rating)
        else:
            return None

    @staticmethod
    def __rate_city(request,form, cityId):
        if form.is_valid():
            rate = form.cleaned_data.get('rate')
            try:
                UserCityRate.objects.create(user_id = request.user.id, city_id = cityId, rate = rate)
            except:
                UserCityRate.objects.filter(user_id = request.user.id, city_id = cityId ).update(rate = rate)


# Country Methods :-
def getAllCountries():
    countries = Country.objects.all()
    return countries


# City Methods :-
def getAllCities(request):
    cities = City.objects.all()
    context = {"cities": cities}
    return render(request, "citiesPage.html", context)


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


# def handle_city_rate(request, cityId):
#     form_data = request.POST or None
#     form      = UserCityRateForm(form_data)

#     if request.method == 'POST':
#         if form.is_valid():
#             rate = form.cleaned_data.get('rate')
#             try:
#                 UserCityRate.objects.create(user_id = request.user.id, city_id = cityId, rate = rate)
#             except:
#                 UserCityRate.objects.filter(user_id = request.user.id, city_id = cityId ).update(rate = rate)
#         else:
#             form_data = None
    
#     return form_data


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


# def newCountry(request):
#     if request.method == 'POST':
#         form = CountryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/places/')
#     else:
#         form = CountryForm()
#         context = {"country_form": form}
#         return render(request, "newCountry.html", context)
#
#
# def editCountry(request, countryId):
#     country = Country.objects.get(id=eval(countryId))
#     if request.method == 'POST':
#         form = CountryForm(request.POST, instance=country)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/places/")
#     else:
#         form = CountryForm(instance=country)
#         context = {'country_form': form}
#         return render(request, "newCountry.html", context)
#
#
# def deleteCountry(request, countryId):
#     st = Country.objects.get(id=eval(countryId))
#     st.delete()
#     return HttpResponseRedirect("/places/")







# class city_handler:
#     @staticmethod
#     def handle_request(request, countryName,cityName):
#         try:
#             country = Country.objects.get(country_Name = countryName)
#             city    = City.objects.get(city_Name = cityName, country_Name_id = country.id)

#             if request.method == 'GET':
#                 form = city_handler.__get_saved_user_rating_form(request, city.id)

#             if request.method == 'POST':
#                 form = UserCityRateForm(request.POST)
#                 city_handler.__rate_city(request, form, city.id)

#             context = {"country": country, "city":city,"form": form}
#             return render(request, "city.html", context) 
#         except:
#             return HttpResponseRedirect("/places/")

#     @staticmethod
#     def __get_saved_user_rating_form(request,cityId):
#         if request.user.is_authenticated:
#             try:
#                 rate_value = UserCityRate.objects.get(user_id = request.user.id, city_id = cityId).rate
#                 user_rating = {"rate":rate_value}
#             except :
#                 user_rating = None
#             finally:            
#                 return UserCityRateForm(user_rating)
#         else:
#             return None

#     @staticmethod
#     def __rate_city(request,form, cityId):
#         if form.is_valid():
#             rate = form.cleaned_data.get('rate')
#             try:
#                 UserCityRate.objects.create(user_id = request.user.id, city_id = cityId, rate = rate)
#             except:
#                 UserCityRate.objects.filter(user_id = request.user.id, city_id = cityId ).update(rate = rate)

# def city_page(request, countryName, cityName):
#     return city_handler.handle_request(request, countryName, cityName)
    # try:
    #     country = Country.objects.get(country_Name = countryName)
    #     city    = City.objects.get(city_Name = cityName, country_Name_id = country.id)

    #     if request.user.is_authenticated:
    #         try:
    #             rate_value = UserCityRate.objects.get(user_id = request.user.id, city_id = (city.id)).rate
    #             form_data = {"rate":rate_value}
    #         except :
    #             pass
    #         form_data = handle_city_rate(request, city.id) or form_data
    #         form = UserCityRateForm(form_data)
    #         context = {"country": country, "city":city,"form":form}
    #     else:
    #         context = {"country": country, "city":city}

    #     return render(request, "city.html", context)
    
    # except:  # country or city is not valid
    #     return HttpResponseRedirect("/places/")
