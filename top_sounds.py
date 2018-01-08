import os
from django.core.wsgi import get_wsgi_application

def get_top_sounds():
    sounds = Sound.objects.all()
    header_string = "".join([
        "\n",
        "Plays",
        "\t",
        "Name"
    ])
    print(header_string)
    print("------------------------------------------------------------")
    for i in range(0, 10):
        sound = sounds[i]
        sound_string = "".join([
            str(sound.num_plays),
            "\t",
            sound.name
        ])
        print(sound_string)


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'oxsoundboard.settings'
    application = get_wsgi_application()
    from oxsoundboard_project.models import *
    get_top_sounds()
