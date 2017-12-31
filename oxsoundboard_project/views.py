from django.shortcuts import render, get_object_or_404
from oxsoundboard_project.models import Sound
from django.http import HttpResponse
import json

def oxsoundboard(request):
    sounds = Sound.objects.all()
    js_sounds = []
    for sound in sounds:
        js_sounds.append(sound.filename)
    context = {"sounds": sounds, "js_sounds": json.dumps(js_sounds)}
    return render(request, 'oxsoundboard/oxsoundboard.html', context)


def oxsound(request, filename):
    filename = get_object_or_404(Sound, filename=filename)
    sound = Sound.objects.get(filename=filename)
    context = {"sound": sound, "filename":filename}
    return render(request, 'oxsoundboard/oxsound.html', context)


def update_counter(request, filename):
    filename = get_object_or_404(Sound, filename=filename)
    sound = Sound.objects.get(filename=filename)
    sound.num_plays+=1
    sound.save()
    return HttpResponse('')
