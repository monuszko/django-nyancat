from django.conf.urls import url

from . import views
from .forms import VideoForm 

urlpatterns = (
        url(r'^$', views.index, name='index'),
        url(r'^myvideos/(?P<person_pk>[a-zA-Z0-9]+)/$',
            views.myvideos, name='myvideos'),
        url(r'^addvideo/$',
            views.addvideo, name='addvideo'),
        )
