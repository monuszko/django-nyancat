from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import (HttpResponse, 
        HttpResponseRedirect, HttpResponseForbidden) # PEP 0328
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib import messages

from .models import Person, Video
from .forms import VideoForm


ONE_HOUR = 60 * 60
ONE_DAY = ONE_HOUR * 24
ONE_YEAR = ONE_DAY * 365


def index(request):
    # If user already 'registered', redirect him.
    password = request.COOKIES.get('password', None)
    if password:
        return HttpResponse('Use your bookmarks')


    person = Person.objects.create()
    response = HttpResponseRedirect(reverse('nyancat:my_videos',
        kwargs={'person_pk': person.pk}))
    response.set_cookie('password', person.password, max_age=ONE_YEAR)
    return response


def get_edit_person(request):
    '''Helper function to reduce boilerplate in edit views'''
    password = request.COOKIES.get('password', None)
    if not password:
        raise HttpResponseForbidden()
    return Person.objects.get(password=password)


def my_videos(request, person_pk):
    person = get_object_or_404(Person, pk=person_pk)
    password = request.COOKIES.get('password', None)
    is_owner = True if password == person.password else False

    context = {
            'person': person,
            'is_owner': is_owner,
            'video_list': person.videos.all(),
            }
    return render(request, 'nyancat/my_videos.html', context)


def remove_videos(request):
    person = get_edit_person(request)

    if request.method=='POST':
        to_remove = request.POST.getlist('to_remove')
        qs_to_remove = Video.objects.filter(id__in=to_remove)
        for vid in qs_to_remove:
            person.videos.remove(vid)
        messages.info(request, '%s videos removed.' % len(to_remove))
        return HttpResponseRedirect(person.get_absolute_url())
    else:
        context = {'video_list': person.videos.all()}
        return render(request, 'nyancat/remove_videos.html', context)


def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            video = Video.objects.get_or_create(url=form.cleaned_data['url'])
            video, is_new = video[0], video[1]

            person = get_edit_person(request)

            if is_new:
                msg = 'Thanks for the new video!'
            elif video not in person.videos.all():
                msg = '{} users already knew this video!'.format(
                        video.person_set.count())
            else:
                msg = 'You already had this video.'
            messages.info(request, msg)

            person.videos.add(video)
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        form = VideoForm()

    return render(request, 'nyancat/video_form.html', {'form': form})


class MostPopular(ListView):
    model = Video
    queryset = Video.objects.annotate(
            num_persons=Count('person')).order_by('-num_persons')
    template_name = 'nyancat/most_popular.html'
