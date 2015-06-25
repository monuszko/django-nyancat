from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.http import (HttpResponse, 
        HttpResponseRedirect, HttpResponseForbidden) # PEP 0328
from django.core.urlresolvers import reverse

from .models import Person, Video
from .forms import VideoForm


ONE_HOUR = 60 * 60


def index(request):
    # If user already 'registered', redirect him.
    password = request.COOKIES.get('password', None)
    if password:
        return HttpResponse('Use your bookmarks')


    person = Person.objects.create()
    response = HttpResponseRedirect(reverse('nyancat:myvideos', kwargs={'person_pk': person.pk}))
    response.set_cookie('password', person.password, max_age=ONE_HOUR)
    return response


def myvideos(request, person_pk):
    person = get_object_or_404(Person, pk=person_pk)
    password = request.COOKIES.get('password', None)
    is_owner = True if password == person.password else False

    context = {
            'person': person,
            'is_owner': is_owner,
            'videos': person.videos.all(),
            }
    return render(request, 'nyancat/myvideos.html', context)


def addvideo(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            video = Video.objects.get_or_create(url=form.cleaned_data['url'])
            video = video[0] # get_or_create returns a tuple

            password = request.COOKIES.get('password', None)
            if not password:
                raise HttpResponseForbidden()

            person = Person.objects.get(password=password)
            person.videos.add(video)
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        form = VideoForm()

    return render(request, 'nyancat/video_form.html', {'form': form})
