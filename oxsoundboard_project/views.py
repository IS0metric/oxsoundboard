from django.shortcuts import render, get_object_or_404
from oxsoundboard_project.models import Sound
from django.http import HttpResponse, JsonResponse
import json

def oxsoundboard(request):
    """Home page - gets all the sounds and creates a helpful list of all the
    filenames for JavaScript to play nicely with
    """
    sounds = Sound.objects.all()
    js_sounds = []
    for sound in sounds:
        js_sounds.append(sound.filename)
    context = {"sounds": sounds, "js_sounds": json.dumps(js_sounds)}
    return render(request, 'oxsoundboard/oxsoundboard.html', context)


def oxsound(request, filename):
    """Single sound - takes a filenme as an argument, returning that sound and
    the filename (again, for JS to play nicely with)
    """
    filename = get_object_or_404(Sound, filename=filename)
    sound = Sound.objects.get(filename=filename)
    context = {"sound": sound, "filename":filename}
    return render(request, 'oxsoundboard/oxsound.html', context)


def update_counter(request, filename):
    """Update counter - used as a headless GET request. Given a filename, gets
    the corresponding sound and updates the play count
    """
    sound = Sound.objects.get(filename=filename)
    sound.num_plays+=1
    sound.save()
    # Needs to return SOMETHING, so return an empty response
    return HttpResponse('')


def get_top_played(request):
    """API call to get the top played sounds, and idea for the soundboard"""
    sounds = Sound.objects.all()
    top_played = []
    for i in range(0, 4): #
        sound = sounds[i]
        sound_string = "".join([
            str(i+1),
            ". ",
            sound.name,
            " (",
            sound.person,
            ")"
        ])
        top_played.append(sound_string)
    resp_string = "".join(top_played)
    resp_dict = {"data": top_played}
    return JsonResponse(resp_dict)


def get_sound(request, filename):
    sound = Sound.objects.get(filename=filename)
    sound.num_plays+=1
    sound.save()
    return HttpResponse('')
