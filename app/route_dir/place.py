from flask import Blueprint, render_template, session,abort, current_app

import uuid
import numpy
import os
from config import config

from ..model_dir.intervention import Intervention
from ..model_dir.place import Place
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_place= Blueprint('place',__name__)

import cv2



@app_file_place.route("/place", methods=["GET"])
def get_placex():
    placex = Place.query.all()
    return jsonify([item.to_json() for item in placex])


@app_file_place.route('/place', methods=['POST'])
@jwt_required()
def create_place():
    return jsonify({ "message":"ok"}), 201


@app_file_place.route("/place/<id>", methods=["GET"])
@jwt_required()
def get_place(id):
    place = Place.query.get(id)
    if place is None:
        abort(404, "place is not found")
    return jsonify(place.to_json())

@app_file_place.route("/place/<id>", methods=["DELETE"])
@jwt_required()
def delete_place(id):
    place = Place.query.get(id)
    if place is None:
        abort(404, "place is not found")
    db.session.delete(place)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
