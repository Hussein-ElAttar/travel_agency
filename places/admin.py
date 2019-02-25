from django.contrib import admin
from .models import Country, City, Location, Hotel, CityHotel
# Register your models here.
# Super User
# user: 'mohamed'
# email:'cap.mohamed.abdelhay@gmail.com'
# pass: 'Os@12345'


class CustomCountry(admin.ModelAdmin):
    fieldsets = [
        ['Country Info', {'fields': ['name', 'pic']}],
        ['Cities', {'fields': ['name']}]
    ]
    list_display = ['name', 'image_tag']
    list_filter = ['name']
    search_fields = ['name']


class CustomCity(admin.ModelAdmin):
    fieldsets = [
        ['City Info', {'fields': ['name', 'description', 'pic']}],
        ['Country', {'fields': ['name']}],
    ]
    list_display = ['name', 'description', 'name', 'image_tag']
    list_filter = ['name']
    search_fields = ['name', 'name__name']


class CustomLocation(admin.ModelAdmin):
    fieldsets = [
        ['Location Info', {'fields': ['loc_Name', 'loc_Description', 'loc_Pic']}],
        ['City', {'fields': ['name']}]
    ]
    list_display = ['loc_Name', 'loc_Description', 'name', 'image_tag']
    list_filter = ['name']
    search_fields = ['name__name', 'loc_Name']


class CustomHotel(admin.ModelAdmin):
    fieldsets = [
        ['Hotel Info', {'fields': ['hotel_Name']}],
        ['City', {'fields': ['name']}]
    ]
    list_display = ['hotel_id', 'city_id']
    list_filter = ['hotel_id__hotel_Name', 'city_id__name']
    search_fields = ['city_id', 'hotel_id']


# myModels = [Country, City]
admin.site.register(Country, CustomCountry)
admin.site.register(City, CustomCity)
admin.site.register(Location, CustomLocation)
admin.site.register(CityHotel, CustomHotel)





