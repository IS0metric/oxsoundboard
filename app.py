from flask import Flask, render_template, send_from_directory, jsonify, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy
import db_conf
import json
app = Flask(__name__)

db_string = 'mysql+pymysql://' + db_conf.DB_USERNAME + ':' + db_conf.DB_PASSWORD + '@' + db_conf.DB_HOST + '/' + db_conf.DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['APPLICAITON_ROOT'] = '/'
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = db_conf.SECRET_KEY
db = SQLAlchemy(app)


class Sound(db.Model):
    __tablename__ = 'oxsoundboard_project_sound'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    person = db.Column(db.String(255))
    description = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    num_plays = db.Column(db.Integer)
    rank = db.Column(db.Boolean)

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ('-num_plays',)

    def get_absolute_url(self):
        return reverse('oxsound', kwargs={'filename': self.filename})


class Randoms(db.Model):
    __tablename__ = 'oxsoundboard_project_randoms'

    id = db.Column(db.Integer, primary_key=True)
    sound_week = db.Column(db.Integer)
    sound_weekend = db.Column(db.Integer)


@app.route('/')
def home():
    sound_welcome = Sound.query.filter_by(filename="welcome").first()
    randoms = Randoms.query.filter().first()
    sound_week = Sound.query.filter_by(id=randoms.sound_week).first()
    sound_weekend = Sound.query.filter_by(id=randoms.sound_weekend).first()
    context = {
        "sound_welcome": sound_welcome,
        "file_welcome": "welcome",
        "sound_week": sound_week,
        "file_week": sound_week.filename,
        "sound_weekend": sound_weekend,
        "file_weekend": sound_weekend.filename,
    }
    return render_template("home.html", context=context)


@app.route('/myboard')
def personal_board():
    return render_template("personal_board.html")


@app.route('/library')
def library():
    sounds = Sound.query.all()
    js_sounds = []
    for sound in sounds:
        js_sounds.append(sound.filename)
    js_sounds = json.dumps(js_sounds)
    print(len(sounds))
    context = {"sounds":sounds, "js_sounds":js_sounds}
    return render_template("library.html", context=context)


@app.route('/library/<filename>')
def oxsound(filename):
    """Single sound - takes a filename as an argument, returning that sound and
    the filename (again, for JS to play nicely with)
    """
    sound = Sound.query.filter_by(filename=filename).first_or_404()
    context = {"sound": sound, "filename":filename}
    return render_template('oxsound.html', context=context)


@app.route('/api/update')
def update():
    """Update counter - used as a headless GET request. Given a filename, gets
    the corresponding sound and updates the play count
    """
    filename = request.args.get('filename', "")
    sound = Sound.query.filter_by(filename=filename).first_or_404()
    sound.num_plays+=1
    db.session.commit()
    # Needs to return SOMETHING, so return an empty response
    return jsonify("success")


@app.route('/suggest')
def suggest():
    return render_template("suggest.html")


@app.route("/api/get_top")
def get_top_played():
    """API call to get the top played sounds"""
    sounds = Sound.query.filter_by(rank=True)
    top_played = []
    for i in range(0, 10): #
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
    return jsonify(resp_dict)


@app.route("/api/stream/<filename>")
def stream(filename):
    sound = Sound.query.filter_by(filename=filename).first_or_404()
    def generate(f):
        if not db_conf.DEBUG:
            with app.app_context():
                sound = url_for("static", filename="".join(["audio/", f, ".mp3"]))
        else:
            sound = "".join(["static/audio/", f, ".mp3"])
        with open(sound, "rb") as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)
    return Response(generate(filename), mimetype="audio/mp3")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=db_conf.DEBUG)
