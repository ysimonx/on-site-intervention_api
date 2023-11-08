from flask import Blueprint, render_template, session,abort, current_app

import uuid
import numpy
import os
from config import config

from ..model_dir.intervention import Intervention
from ..model_dir.formulaire import Formulaire
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_formulaire= Blueprint('formulaire',__name__)

import cv2



@app_file_formulaire.route("/formulaire", methods=["GET"])
def get_formulaires():
    formulaires = Formulaire.query.all()
    return jsonify([item.to_json() for item in formulaires])


@app_file_formulaire.route("/formulaire/<id>", methods=["GET"])
@jwt_required()
def get_formulaire(id):
    formulaire = Formulaire.query.get(id)
    if get_formulaire is None:
        abort(404, "get_formulaire is not found")
    return jsonify(get_formulaire.to_json())

@app_file_formulaire.route("/formulaire/<id>", methods=["DELETE"])
@jwt_required()
def delete_formulaire(id):
    formulaire = Formulaire.query.get(id)
    if formulaire is None:
        abort(404, "formulaire is not found")
    db.session.delete(formulaire)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
