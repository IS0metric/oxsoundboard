from django.contrib import admin
from oxsoundboard_project.models import *

class SoundAdmin(admin.ModelAdmin):
    fields = ('filename', 'name', 'person', 'description', 'video_url')

admin.site.register(Sound, SoundAdmin)
