from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'cityName/(.*)/$',getWeatherByCityName),
    url(r'login/$',to_login),
    url(r'login/valid/$',valid_login),
    url(r'logout/$',logout),
)
