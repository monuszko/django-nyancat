from django.conf.urls import url
from django.views.decorators.cache import cache_page
#TODO: probably better to put stuff like ONE_HOUR in constants.py or something

from . import views
from .forms import VideoForm 

urlpatterns = (
        url(r'^$', views.index, name='index'),
        url(r'^my_videos/(?P<person_url>[a-zA-Z0-9]+)/$',
            views.my_videos, name='my_videos'),
        url(r'^add_video/$',
            views.add_video, name='add_video'),
        url(r'^update_person/$',
            views.UpdatePerson.as_view(), name='update_person'),
        url(r'^remove_videos/$',
            views.remove_videos, name='remove_videos'),
        url(r'^most_popular/$',
            cache_page(views.ONE_HOUR)(views.MostPopular.as_view()),
            name='most_popular'),
        url(r'^restore_cookie/(?P<person_url>[\w.@+-]+)/(?P<token>[\w.:_=-]+)$',
            views.restore_cookie, name='restore_cookie'),
        url(r'^send_password/(?P<person_url>[a-zA-Z0-9]+)/$',
            views.send_password, name='send_password'),
        )
