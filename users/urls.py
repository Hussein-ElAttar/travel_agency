from django.conf.urls import url
from users import views
from django.http import HttpResponseRedirect

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^user/(?P<userId>[0-9]+)/$', views.getUserById),
    url(r'^edit/(?P<userId>[0-9]+)/$', views.editProfile),
]
