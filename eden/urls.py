from django.conf.urls import patterns, include, url
from django.contrib import admin
from eden.views import *

admin.autodiscover()

urlpatterns = patterns('',
       url(r'^$', main_page),
       url(r'^admin/', include(admin.site.urls)),
       url(r'^blog/', include('forum.urls')),
       url(r'^music/', include('music.urls')),
       url(r'^say/$', just_say),
       url(r'^about/$', about_me),
       url(r'^photo/wall/$', photo_wall),
       url(r'^message/$', message),
       url(r'^utente/', include('utente.urls')),
       url(r'^upload/', upload_file),
)