from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^appointments$', views.appointments),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^update/(?P<id>\d+)$', views.update)
]
