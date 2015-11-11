from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^hotel/create/$', HotelCreateView.as_view(), name='hotel_create'),
    url(r'hotel/$', HotelListView.as_view(), name='hotel_list'),
    url(r'hotel/$', HotelListView.as_view(), name='hotel_list'),
    url(r'^hotel/(?P<pk>\d+)/$', HotelDetailView.as_view(), name='hotel_detail'),
    url(r'^hotel/update/(?P<pk>\d+)/$', HotelUpdateView.as_view(), name='hotel_update'),
    url(r'^hotel/delete/(?P<pk>\d+)/$', HotelDeleteView.as_view(), name='hotel_delete'),
    url(r'^hotel/(?P<pk>\d+)/review/create/$', ReviewCreateView.as_view(), name='review_create'),
    url(r'^hotel/(?P<hotel_pk>\d+)/review/update/(?P<review_pk>\d+)/$', ReviewUpdateView.as_view(), name='review_update'),
)