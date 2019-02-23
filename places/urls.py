from django.conf.urls import url
from places import views

urlpatterns = [
    url(r'^country/(?P<countryName>[a-zA-Z ]+)/$', views.country_page),
    url(r'^country/(?P<countryName>[a-zA-Z ]+)/city/(?P<cityName>[a-zA-Z ]+)/$', views.city_page),
    url(r'^rentcar/$', views.rentCar),
    url(r'^hotelres/$', views.hotelReservation),
    url(r'^user/$', views.showUserReservations),

    url(r'^api/country/(?P<countryName>[a-zA-Z ]+)/$', views.country_api),
    url(r'^api/country/(?P<countryName>[a-zA-Z ]+)/city/(?P<cityName>[a-zA-Z ]+)/$', views.city_api),
    url(r'^countries/$', views.index),
    url(r'^$', views.homePage),
    url(r'^', views.homePage),
]




