from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from oxsoundboard_project import views

from . import views



urlpatterns = [
    url(r'^$', views.oxsoundboard, name='oxsoundboard'),
    url(r'^(?P<filename>[-\w]+)/$', views.oxsound, name='oxsound'),
    url(r'^update/(?P<filename>[-\w]+)/$', views.update_counter, name='update_counter'),
    url(r'^api/get_top/$', views.get_top_played, name="get_top_played"),
    url(r'^api/get_sound/(?P<filename>[-\w]+)/$', views.send_file, name="get_sound"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
