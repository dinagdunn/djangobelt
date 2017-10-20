from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^main/(?P<user_id>\d+)/add$', views.add),
    url(r'^main/(?P<travel_id>\d+)/destination$', views.display),
    url(r'^main/(?P<user_id>\d+)/join$', views.join),
    url(r'^main/(?P<user_id>\d+)/logout$', views.logout)
]
