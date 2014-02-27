from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'query/(.*)$',query_musiz),
    url(r'song/(\d*)$',get_song),
    url(r'song/data/?(.*)$',get_song_data),
    url(r'lrc/(.*)$',get_lrc),
    url(r'$',music_box),
)



