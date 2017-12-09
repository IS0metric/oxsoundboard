import os
from django.core.wsgi import get_wsgi_application
#     ["","","","",""],

raw_list = [
    ["timcurry_space","Misc","Tim Curry - Space","SPAAICE","https://www.youtube.com/watch?v=g1Sq1Nr58hM"],
    ["timcurry_capitalism","Misc","Tim Curry - Capitalism","I'm going to the one place not corrupted by capitalsim... SPAAICE","https://www.youtube.com/watch?v=g1Sq1Nr58hM"],
]

def populate():
    for sound in raw_list:
        sound_filename = sound[0]
        sound_person = sound[1]
        sound_name = sound[2]
        sound_description = sound[3]
        sound_link = sound[4]
        Sound.objects.get_or_create(
            filename=sound_filename,
            description=sound_description,
            name=sound_name,
            person=sound_person,
            video_url=sound_link
        )

if __name__ == "__main__":
    print("Starting population script")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'oxsoundboard.settings'
    application = get_wsgi_application()
    from oxsoundboard_project.models import *
    populate()
    print("Done")
