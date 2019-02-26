from django.db import models
from users.models import CustomUser
from places.models import City
# Create your models here.


class Post(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser)
    city = models.ForeignKey(City)

    class Meta:
        verbose_name_plural = "Posts"


class Comment(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser)
    post = models.ForeignKey(Post)

    class Meta:
        verbose_name_plural = "Comments"



