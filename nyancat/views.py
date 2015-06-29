from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.http import (HttpResponse, 
        HttpResponseRedirect, HttpResponseForbidden) # PEP 0328
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Person, Video
from .forms import VideoForm


ONE_HOUR = 60 * 60
ONE_DAY = ONE_HOUR * 24
ONE_YEAR = ONE_DAY * 365


def index(request):
    #TODO: make this more secure
    person = None
    password = request.COOKIES.get('password', None)
    if password:
        person = Person.objects.get(password=password)

    response = render(request, 'nyancat/index.html', {'person': person})
    return response


def get_edit_person(request):
    '''Helper function to reduce boilerplate in edit views'''
    password = request.COOKIES.get('password', None)
    if not password:
        raise HttpResponseForbidden()
    return Person.objects.get(password=password)


class UpdatePerson(UpdateView):
    model = Person
    fields = ('email',)
    def get_object(self):
        return get_edit_person(self.request)


def my_videos(request, person_url):
    person = get_object_or_404(Person, url=person_url)
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
        messages.info(request, _('%s videos removed.') % len(to_remove))
        return HttpResponseRedirect(person.get_absolute_url())
    else:
        context = {'video_list': person.videos.all()}
        return render(request, 'nyancat/remove_videos.html', context)


def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            video = Video.objects.get_or_create(url=form.cleaned_data['url'])
            video, video_is_new = video[0], video[1]

            # Person is created on first video upload. This serves as a
            # rudimentary rudimentary protection from crawler bots generating
            # billions of table rows.
            password = request.COOKIES.get('password', None)
            if password:
                person = Person.objects.get(password=password)
            else: 
                person = Person.objects.create()
                messages.info(request, _('Created a new person.'))

            if video_is_new:
                msg = _('Thanks for the new video!')
            elif video not in person.videos.all():
                msg = _('{} users already knew this video!'.format(
                        video.person_set.count()))
            else:
                msg = _('You already had this video.')
            messages.info(request, msg)

            person.videos.add(video)
            response = HttpResponseRedirect(person.get_absolute_url())
            response.set_cookie('password', person.password, max_age=ONE_YEAR)
            return response
    else:
        form = VideoForm()

    return render(request, 'nyancat/video_form.html', {'form': form})


class MostPopular(ListView):
    model = Video
    queryset = Video.objects.annotate(
            num_persons=Count('person')).order_by('-num_persons')
    template_name = 'nyancat/most_popular.html'


def restore_cookie(request, person_url, token):
    '''Sets the password cookie, equivalent to "lost password" links'''
    #TODO: insecure ?
    person = get_object_or_404(Person, url=person_url)
    response = HttpResponseRedirect(reverse('nyancat:my_videos',
        kwargs={'person_url': person.url}))
    if person.check_token(token):
        response.set_cookie('password', person.password, max_age=ONE_YEAR)
        messages.info(request, _('Cookie set.'))
    else:
        messages.info(request, _('Bad/expired link.'))
    return response


def send_password(request, person_url):
    from django.conf import settings
    person = get_object_or_404(Person, url=person_url)
    if not person.email:
        return
    subject = _('Nyancat password recovery')
    body = _("""
            Someone requested a password reminder for your nyancat page.
            You can use the link below to set the password cookie for
            your page, for example in another browser, on another
            device: \n
            {}\n
            If you don't know what this is about, ignore this message.
            """.format(request.build_absolute_uri(person.restore_cookie_url())))
    from_email = 'from@example.com'
    if hasattr(settings, 'NYANCAT_EMAIL'):
        from_email = settings.NYANCAT_EMAIL
    to = person.email
    send_mail(subject, body, from_email, [to], fail_silently=False)
    response = HttpResponseRedirect(reverse('nyancat:my_videos',
            kwargs={'person_url': person_url}))
    messages.info(request, _('Message sent. Check your mail.'))
    return response
