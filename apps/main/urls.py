from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^add$', views.add),
    url(r'^newtrip$', views.newtrip),
    url(r'^main/destination/(?P<trip_id>\d+)$', views.destination),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^logout$', views.logout),
]
