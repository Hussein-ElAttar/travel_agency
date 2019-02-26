from django.contrib import admin
from .models import Country, City, Location, Hotel, CityHotel

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
        ['Location Info', {'fields': ['name', 'description', 'pic']}],
        ['City', {'fields': ['name']}]
    ]
    list_display = ['name', 'description', 'name', 'image_tag']
    list_filter = ['name']
    search_fields = ['name__name', 'name']


class CustomHotel(admin.ModelAdmin):
    fieldsets = [
        ['Hotel Info', {'fields': ['name']}],
        ['City', {'fields': ['name']}]
    ]
    list_display = ['hotel_id', 'city_id']
    list_filter = ['hotel_id__name', 'city_id__name']
    search_fields = ['city_id', 'hotel_id']


# myModels = [Country, City]
admin.site.register(Country, CustomCountry)
admin.site.register(City, CustomCity)
admin.site.register(Location, CustomLocation)
admin.site.register(CityHotel, CustomHotel)





