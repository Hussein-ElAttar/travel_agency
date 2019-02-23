from django.conf.urls import url
from places import views

urlpatterns = [
    # Country Urls:-
    url(r'^country/(?P<countryName>[a-zA-Z ]+)/$', views.country_page),
    url(r'^country/(?P<countryName>[a-zA-Z ]+)/city/(?P<cityName>[a-zA-Z ]+)/$', views.city_page),
    # url(r'^(?P<countryId>[0-9]+)/$', views.getCountryById),
    # City Urls:-
    url(r'^cities/[0-9]/rentCar/$', views.rentCar),
    url(r'^cities/$', views.getAllCities),
    url(r'^(?P<cityId>[0-9]+)/$', views.getCityById),
    # Locations Urls:-
    url(r'^locations/$', views.getAllLocations),
    url(r'^(?P<locationId>[0-9]+)/$', views.getLocationById),
    # Hotels Urls:-
    url(r'^hotels/$', views.getAllHotels),
    url(r'^(?P<hotelId>[0-9]+)/$', views.getHotelById),
    url(r'^rentcar/$', views.rentCar),
    url(r'^hotelres/$', views.hotelReservation),
    url(r'^user/$', views.showUserReservations),

    url(r'^api/country/(?P<countryName>[a-zA-Z ]+)/$', views.country_api),
    url(r'^api/country/(?P<countryName>[a-zA-Z ]+)/city/(?P<cityName>[a-zA-Z ]+)/$', views.city_api),
    url(r'^$', views.homePage),

]




