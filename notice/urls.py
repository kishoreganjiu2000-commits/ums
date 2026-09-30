"""
URLs for the notice app.

Sits at /notice/ via the include in config/urls.py. Named so templates can use
{% url 'notice:notice_list' %}.

The download route is nested under the slug rather than pointing at MEDIA_URL
directly, so the URL stays self-describing and the storage backend can change
without touching a single template.
"""

from django.urls import path

from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('<slug:slug>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('<slug:slug>/download/', views.notice_download, name='notice_download'),
]
