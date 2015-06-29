=======
nyancat
=======

Nyancat is a cookie-based app allowing users to create their lists of favorite
Youtube videos.

Quick start
-----------

1. Add "nyancat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'nyancat',
    )

2. Include the anothercrm URLconf in your project urls.py like this::

    url(r'^nyancat/', include('nyancat.urls', namespace='nyancat')),

3. For password recovery, you will need to set up email backend. You will also
   need to set up the email password links will be sent from in settings.py::

    NYANCAT_EMAIL = 'dontreply@yourdomain.com'

3. Run `python manage.py migrate` to create the nyancat models.

4. Visit http://127.0.0.1:8000/nyancat/ to access the app.

5. You can build a package (installed via pip) issuing the command::

   python setup.py sdist
