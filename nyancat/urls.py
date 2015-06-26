from django.conf.urls import url

from . import views
from .forms import VideoForm 

urlpatterns = (
        url(r'^$', views.index, name='index'),
        url(r'^my_videos/(?P<person_pk>[a-zA-Z0-9]+)/$',
            views.my_videos, name='my_videos'),
        url(r'^add_video/$',
            views.add_video, name='add_video'),
        url(r'^remove_videos/$',
            views.remove_videos, name='remove_videos'),
        url(r'^most_popular/$',
            views.MostPopular.as_view(), name='most_popular'),
        )
