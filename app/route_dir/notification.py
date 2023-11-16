from flask import Blueprint, abort, make_response

import os
from config import config

from ..model_dir.notification import Notification
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db


app_notification_notification= Blueprint('notification',__name__)







@app_notification_notification.route("/notification", methods=["GET"])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([notification.to_json() for notification in notifications])


# notification upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM
# flutter image upload exemple : https://www.youtube.com/watch?v=dsPdIdrgAD4
@app_notification_notification.route('/notification', methods=['POST'])
@jwt_required()
def create_notification():

    if not 'notification_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing notification_on_site_uuid parameter"), 400))
    
    notification_on_site_uuid = request.form.get('notification_on_site_uuid')
    notification = Notification.query.filter(Notification.notification_on_site_uuid == notification_on_site_uuid).first()
    if notification is not None:
        print("notification already uploaded")
        abort(make_response(jsonify(error="notification already uploaded"), 400))
    
    notification        = request.notifications['notification']
    
    notification = Notification(  notification_on_site_uuid=notification_on_site_uuid,
                    
                )
    db.session.add(notification)
    db.session.commit() 

    return jsonify(notification.to_json()), 201


@app_notification_notification.route("/notification/<id>", methods=["GET"])
@jwt_required()
def get_notification(id):
    notification = Notification.query.get(id)
    if notification is None:
        abort(make_response(jsonify(error="notification is not found"), 404))

    return jsonify(notification.to_json_to_root())

@app_notification_notification.route("/notification/<id>", methods=["DELETE"])
@jwt_required()
def delete_notification(id):
    notification = Notification.query.get(id)
    if notification is None:
        abort(make_response(jsonify(error="notification is not found"), 404))
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'result': True, 'id': id})

@app_notification_notification.route("/notification/ready")
@jwt_required()
def get_ready():
    return jsonify(message="ready");
    
    
def allowed_notification(notificationname):
    return '.' in notificationname and \
           notificationname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_extension(notificationname):
    return '.' in notificationname and \
           notificationname.rsplit('.', 1)[0].lower()

def get_extension(notificationname):
    fic, notification_extension = os.path.splitext(notificationname)
    return notification_extension.lower()
