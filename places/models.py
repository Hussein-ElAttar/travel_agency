from django.db import models
from users.models import CustomUser
from datetime import datetime

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='countries', max_length=250,null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return u'<img src="/media/%s" width=50 height=50/>' % self.pic

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,null=True, blank=True)
    pic = models.ImageField(upload_to='cities', max_length=250,null=True, blank=True)
    is_crawled = models.BooleanField(default=False)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name

    def image_tag(self):
        return u'<img src="/media/%s" width=50 height=50/>' % self.pic

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        verbose_name_plural = "Cities"

class CityPics(models.Model):
    city = models.ForeignKey(City)
    url = models.CharField(max_length=150)


class Location(models.Model):
    loc_Name = models.CharField(max_length=100)
    loc_Description = models.CharField(max_length=1000, null=True, blank=True)
    loc_Pic = models.ImageField(upload_to='locations', max_length=250)
    name = models.ForeignKey(City)

    def __str__(self):
        return self.loc_Name

    def image_tag(self):
        return u'<img src="/media/%s" width=50 height=50/>' % self.loc_Pic

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class Hotel(models.Model):
    hotel_Name = models.CharField(max_length=100)
    hotel_Pic = models.ImageField(upload_to='hotels', max_length=250)

    def __str__(self):
        return self.hotel_Name


class UserHotelReservation(models.Model):
    hotel_Name = models.ForeignKey(Hotel)
    user_Name = models.ForeignKey(CustomUser)
    rooms = models.IntegerField()
    room_type = models.IntegerField(choices=[(1, "Single"), (2, "Double"), (3, "Triple")])
    from_Date = models.DateTimeField(default=datetime.now)
    to_Date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "Hotel Reservation"


class CityHotel(models.Model):
    city_id = models.ForeignKey(City)
    hotel_id = models.ForeignKey(Hotel)

    class Meta:
        verbose_name_plural = "Hotels"


class UserCityRate(models.Model):
    user = models.ForeignKey(CustomUser)
    city = models.ForeignKey(City)
    rate = models.IntegerField(
        default=0,
        choices=(
            (0, '---'),
            (1, 'Bad'),
            (2, 'Below Average'),
            (3, 'Average'),
            (4, 'Very Good'),
            (5, 'Excellent'),
        )
    )

    class Meta:
        unique_together = (('user', 'city'),)

    def __str__(self):
        return "Rate"


class UserCarRent(models.Model):
    pickup_loc  = models.ForeignKey(Location, related_name='pickup_loc')
    dropoff_loc = models.ForeignKey(Location, related_name='dropoff_loc')
    user        = models.ForeignKey(CustomUser)
    time        = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.time

    def get_loc(self):
        return self.pickup_loc.city_Name
    #
    # def set_pickup(self, city_name):
    #     self.pickup_loc = city_name
    #
    # def set_dropoff(self, city_name):
    #     self.dropoff_loc = city_name



