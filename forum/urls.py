from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^list/(\d+)/$',blog_list),
    url(r'get/(\d+)/$',blog_get),
    url(r'edit/$',blog_edit),
    url(r'save/$',save_blog),
    url(r'deploy/$',deploy_blog),
    url(r'list/type/(\d+)/(\d+)/$',blog_list_by_type),
)
