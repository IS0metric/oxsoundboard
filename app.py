from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import db_conf
import json
app = Flask(__name__)

db_string = 'mysql://' + db_conf.DB_USERNAME + ':' + db_conf.DB_PASSWORD + '@' + db_conf.DB_HOST + '/' + db_conf.DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['APPLICAITON_ROOT'] = '/'
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = db_conf.SECRET_KEY
db = SQLAlchemy(app)


class Sound(db.Model):
    __tablename__ = 'oxsoundboard_project_sound'

    filename = db.Column(db.String(255))
    name = db.Column(db.String(255))
    person = db.Column(db.String(255))
    description = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    num_plays = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Boolean)

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ('-num_plays',)

    def get_absolute_url(self):
        return reverse('oxsound', kwargs={'filename': self.filename})



@app.route('/')
def home():
    sounds = Sound.query.all()

    js_sounds = []
    for sound in sounds:
        js_sounds.append(sound.filename)
    js_sounds = json.dumps(js_sounds)
    print(js_sounds)
    context = {"sounds":sounds, "js_sounds":js_sounds}
    return render_template("home.html", context=context)


@app.route('/<filename>')
def oxsound(filename):
    """Single sound - takes a filenme as an argument, returning that sound and
    the filename (again, for JS to play nicely with)
    """
    sound = Sound.query.filter_by(filename=filename).first_or_404()
    context = {"sound": sound, "filename":filename}
    return render_template('oxsound.html', context=context)


@app.route('/update/<filename>')
def update(filename):
    """Update counter - used as a headless GET request. Given a filename, gets
    the corresponding sound and updates the play count
    """
    sound = Sound.query.filter_by(filename=filename).first_or_404()
    sound.num_plays+=1
    db.session.commit()
    # Needs to return SOMETHING, so return an empty response
    return "success"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
