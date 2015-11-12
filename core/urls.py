from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^hotel/create/$', login_required(HotelCreateView.as_view()), name='hotel_create'),
    url(r'hotel/$', login_required(HotelListView.as_view()), name='hotel_list'),
    url(r'hotel/$', HotelListView.as_view(), name='hotel_list'),
    url(r'^hotel/(?P<pk>\d+)/$', login_required(HotelDetailView.as_view()), name='hotel_detail'),
    url(r'^hotel/update/(?P<pk>\d+)/$', login_required(HotelUpdateView.as_view()), name='hotel_update'),
    url(r'^hotel/delete/(?P<pk>\d+)/$', login_required(HotelDeleteView.as_view()), name='hotel_delete'),
    url(r'^hotel/(?P<pk>\d+)/review/create/$', login_required(ReviewCreateView.as_view()), name='review_create'),
    url(r'^hotel/(?P<hotel_pk>\d+)/review/update/(?P<review_pk>\d+)/$', login_required(ReviewUpdateView.as_view()), name='review_update'),
    url(r'^hotel/(?P<hotel_pk>\d+)/review/delete/(?P<review_pk>\d+)/$', login_required(ReviewDeleteView.as_view()), name='review_delete'),
    url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
)