from flask import Blueprint, render_template, session,abort, current_app

import uuid
import numpy
import os
from config import config

from ..model_dir.controle import Controle
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_controle= Blueprint('controle',__name__)

import cv2



@app_file_controle.route("/controle/filter_by_interventions", methods=["POST"])
def get_controles_intervention():
    if not request.json:
        print("not json")
        abort(400)
    if not "interventions" in request.json:
        print("not interventions in json")
        abort(400)
        
    interventions = request.json.get("interventions")
      
    result=[]
    for intervention in interventions:
        intervention_uuid = intervention.get("intervention_uuid")
        controle = Controle.query.filter(Controle.intervention_uuid == intervention_uuid).first()
        if controle is None:
            print("pas encore de controle pour le intervention "+ intervention_uuid)
        else :
            result.append(controle.to_json())
            
    # controles = Controle.query.all()
    return jsonify(result)





@app_file_controle.route("/controle", methods=["GET"])
def get_controles():
    controles = Controle.query.all()
    return jsonify([item.to_json() for item in controles])


@app_file_controle.route("/controle/<id>", methods=["GET"])
@jwt_required()
def get_controle(id):
    controle = Controle.query.get(id)
    if controle is None:
        abort(404, "controle is not found")
    return jsonify(controle.to_json())

@app_file_controle.route("/controle/<id>", methods=["DELETE"])
@jwt_required()
def delete_controle(id):
    controle = Controle.query.get(id)
    if controle is None:
        abort(404, "controle is not found")
    db.session.delete(controle)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
