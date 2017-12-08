from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from oxsoundboard_project import views

from . import views

urlpatterns = [
    url(r'^$', views.oxsoundboard, name='oxsoundboard'),
    url(r'^(?P<filename>[-\w]+)', views.oxsound, name='oxsound'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
