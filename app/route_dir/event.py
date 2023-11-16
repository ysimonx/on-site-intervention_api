from flask import Blueprint, abort, make_response

import os
from config import config

from ..model_dir.event import Event
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db


app_file_event= Blueprint('event',__name__)







@app_file_event.route("/event", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_json() for event in events])


# event upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM
# flutter image upload exemple : https://www.youtube.com/watch?v=dsPdIdrgAD4
@app_file_event.route('/event', methods=['POST'])
@jwt_required()
def create_event():

    if not 'event_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing event_on_site_uuid parameter"), 400))
    
    event_on_site_uuid = request.form.get('event_on_site_uuid')
    event = Event.query.filter(Event.event_on_site_uuid == event_on_site_uuid).first()
    if event is not None:
        print("event already uploaded")
        abort(make_response(jsonify(error="event already uploaded"), 400))
    
    event        = request.events['event']
    
    event = Event(  event_on_site_uuid=event_on_site_uuid,
                    
                )
    db.session.add(event)
    db.session.commit() 

    return jsonify(event.to_json()), 201


@app_file_event.route("/event/<id>", methods=["GET"])
@jwt_required()
def get_event(id):
    event = Event.query.get(id)
    if event is None:
        abort(make_response(jsonify(error="event is not found"), 404))

    return jsonify(event.to_json_to_root())

@app_file_event.route("/event/<id>", methods=["DELETE"])
@jwt_required()
def delete_event(id):
    event = Event.query.get(id)
    if event is None:
        abort(make_response(jsonify(error="event is not found"), 404))
    db.session.delete(event)
    db.session.commit()
    return jsonify({'result': True, 'id': id})

@app_file_event.route("/event/ready")
@jwt_required()
def get_ready():
    return jsonify(message="ready");
    
    
def allowed_event(eventname):
    return '.' in eventname and \
           eventname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_extension(eventname):
    return '.' in eventname and \
           eventname.rsplit('.', 1)[0].lower()

def get_extension(eventname):
    fic, event_extension = os.path.splitext(eventname)
    return event_extension.lower()
