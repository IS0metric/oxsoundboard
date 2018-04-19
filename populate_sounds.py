import os
from django.core.wsgi import get_wsgi_application
#     ["","","","",""],

raw_list = [
    ["welcome", "Misc", "Welcome To The Soundboard!", "Hello-welcome to the Outside Xbox-Xtra soundboard... soundboard... (Andy...)", "https://www.youtube.com/channel/UCKk076mm-7JjLxJcFSXIPJA"],

def populate():
    for sound in raw_list:
        sound_rank = False
        sound_filename = sound[0]
        sound_person = sound[1]
        sound_name = sound[2]
        sound_description = sound[3]
        sound_link = sound[4]
        print("\tAdding " + sound_filename)
        Sound.objects.get_or_create(
            filename=sound_filename,
            description=sound_description,
            name=sound_name,
            person=sound_person,
            video_url=sound_link,
            rank=sound_rank
        )

if __name__ == "__main__":
    print("Starting population script")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'oxsoundboard.settings'
    application = get_wsgi_application()
    from oxsoundboard_project.models import *
    populate()
    print("Done")
