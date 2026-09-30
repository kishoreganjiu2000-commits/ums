"""
URLs for the core app.

The homepage is a real view. Every other section exists as a route but has no
page built yet, so each one is served by ComingSoonView - a styled "under
development" page rather than a missing-template error. Swapping in a real page
later is a one-line change per section.

Namespaced as 'core' so {% url 'core:home' %} cannot collide with a similarly
named route in another app.
"""

from django.urls import path

from .views import ComingSoonView, HomeView

app_name = 'core'

# (url, route name, key in core.views.PENDING_SECTIONS)
STATIC_SECTIONS = [
    ('about/', 'about', 'about'),
    ('academics/', 'academics', 'academics'),
    ('admission/', 'admission', 'admission'),
    ('research/', 'research', 'research'),
    ('students/', 'students', 'students'),
    ('news-events/', 'news_events', 'news_events'),
    ('career/', 'career', 'career'),
    ('contact/', 'contact', 'contact'),
]

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]

urlpatterns += [
    path(route, ComingSoonView.as_view(), {'section': key}, name=name)
    for route, name, key in STATIC_SECTIONS
]
