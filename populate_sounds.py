import os
from django.core.wsgi import get_wsgi_application
#     ["","","","",""],

raw_list = [
    ["jane_locks", "Jane", "Locks, Caitlin", "Aha, it's not my fault if you're gonna cheap out on something as important as locks, Caitlin...", "https://www.youtube.com/watch?v=8TjuDKjAVkQ"],
    ["ellen_wonderwall", "Ellen", "Wonderwall", "Anway, here's Wonderwall", "https://www.youtube.com/watch?v=KGEsbXpyq6o"],


]

def populate():
    for sound in raw_list:
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
            video_url=sound_link
        )

if __name__ == "__main__":
    print("Starting population script")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'oxsoundboard.settings'
    application = get_wsgi_application()
    from oxsoundboard_project.models import *
    populate()
    print("Done")
