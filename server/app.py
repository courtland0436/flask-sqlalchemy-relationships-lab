#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/events')
def get_events():
    events = Event.query.all()
    data = [{"id": e.id, "name": e.name, "location": e.location} for e in events]
    return make_response(jsonify(data), 200)

@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()
    if event:
        sessions_data = []
        for s in event.sessions:
            sessions_data.append({
                "id": s.id,
                "title": s.title,
                "start_time": s.start_time.isoformat()
            })
        return make_response(jsonify(sessions_data), 200)
    return make_response(jsonify({"error": "Event not found"}), 404)

@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    data = [{"id": s.id, "name": s.name} for s in speakers]
    return make_response(jsonify(data), 200)

@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()
    if speaker:
        return make_response(jsonify({
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
        }), 200)
    return make_response(jsonify({"error": "Speaker not found"}), 404)

@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    if session:
        speakers_data = []
        for s in session.speakers:
            speakers_data.append({
                "id": s.id,
                "name": s.name,
                "bio_text": s.bio.bio_text if s.bio else "No bio available"
            })
        return make_response(jsonify(speakers_data), 200)
    return make_response(jsonify({"error": "Session not found"}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)