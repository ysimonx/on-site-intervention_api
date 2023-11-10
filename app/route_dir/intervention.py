from flask import Blueprint, render_template, session,abort, current_app, make_response

import uuid
import hashlib
import numpy
import os
from config import config

from ..model_dir.intervention import Intervention
from ..model_dir.place import Place
from ..model_dir.report import Report
from ..model_dir.field import Field
from ..model_dir.field_histo import FieldHisto
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_intervention= Blueprint('intervention',__name__)

import cv2
import json


@app_file_intervention.route("/intervention", methods=["GET"])
def get_interventions():
    interventions = Intervention.query.all()
    return jsonify([item.to_json() for item in interventions])


@app_file_intervention.route('/intervention', methods=['POST'])
@jwt_required()
def create_intervention():
    
    if not request.json:
        print("not json")
        abort(make_response(jsonify(error="no json provided in request"), 400))


    intervention_uuid = request.json.get('intervention_uuid')
    intervention_name = request.json.get('intervention_name')
    place_uuid = request.json.get('place_uuid')
    place_name = request.json.get('place_name')
    
    place = Place.query.filter(Place.place_uuid == place_uuid).first()
    if place is None:
        place = Place(place_uuid = place_uuid, name = place_name )
        db.session.add(place)
        db.session.commit()  
         
    md5Intervention = hashlib.md5(json.dumps(request.json).encode('utf-8')).hexdigest()
           
    intervention= Intervention.query.filter(Intervention.intervention_uuid == intervention_uuid).first()
    if intervention is None:
        intervention = Intervention(intervention_uuid = intervention_uuid,
                      name = intervention_name, 
                      intervention_data_md5 = md5Intervention,  
                      place_id = place.id)
        db.session.add(intervention)
        db.session.commit()  
    else:
        intervention.intervention_data_md5 = md5Intervention
        db.session.commit()  
         
    intervention_average_longitude = 0;
    intervention_average_latitude = 0;
    
    reports= request.json.get('reports') 
    # TODO : JL a envoyé un formulaire des 2 reports avec aucune photo ... du coup, l'average est = 0.0 et 0.0 et du coup, la moyenne de 2 reports n'est pas bonne
    
    print(len(reports))
    nb_formulaire_with_averagelocation=0
    for formulaire_json in reports:
        print(formulaire_json)
        print(formulaire_json.get("formulaire_uuid"))
        formulaire_uuid = formulaire_json.get("formulaire_uuid");
        formulaire_name = formulaire_json.get("formulaire_name");
        formulaire = Report.query.filter(Report.formulaire_uuid == formulaire_uuid).first()
        average_location = formulaire_json.get("average_location");
        average_latitude = average_location.get("latitude")
        average_longitude = average_location.get("longitude")
        
        if (average_longitude > 0.0 and average_latitude > 0.0):
            intervention_average_longitude = intervention_average_longitude + average_longitude 
            intervention_average_latitude = intervention_average_latitude + average_latitude
            nb_formulaire_with_averagelocation = nb_formulaire_with_averagelocation + 1   
        
        md5 = hashlib.md5(json.dumps(formulaire_json).encode('utf-8')).hexdigest()
            
            
        if formulaire is None:
            print("creation formulaire")
            formulaire = Report(formulaire_uuid = formulaire_uuid,
                                    intervention_id = intervention.id,
                                    name = formulaire_name,
                                    formulaire_data = json.dumps(formulaire_json),
                                    formulaire_data_md5 = md5,
                                    average_latitude = average_latitude,
                                    average_longitude = average_latitude)
            db.session.add(formulaire)
            db.session.commit()  
        else:
            print("updating formulaire")
            formulaire.formulaire_data = json.dumps(formulaire_json)
            formulaire.formulaire_data_md5 = md5
            formulaire.average_latitude = average_latitude
            formulaire.average_longitude = average_longitude
            db.session.commit()  
            
        fields=formulaire_json.get("fields")
        for field_json in fields:
            print()
            field_uuid = field_json.get("field_uuid")
            field_name = field_json.get("field_name")
            print(field_uuid)
            print(field_json)
            
            field = Field.query.filter(Field.field_uuid == field_uuid).first()
            md5 = hashlib.md5(json.dumps(field_json).encode('utf-8')).hexdigest()
            
            if field is None:
                print("creation field")
                
                field=Field(field_uuid = field_uuid, 
                            name=field_name, 
                            field_data=json.dumps(field_json), 
                            intervention_uuid= intervention_uuid,
                            field_data_md5=md5)
                
                db.session.add(field)
                db.session.commit()  
            else:
                print("update field")
                field.field_data=json.dumps(field_json)
                field.field_data_md5=md5
                field.intervention_uuid= intervention_uuid
                db.session.commit()  
                
            # si la valeur de ce champ n'a pas encore été archivée, je l'archive ! 
            # (field_uuid et field_data_md5)
            field_histo = FieldHisto.query.filter(FieldHisto.field_on_site_uuid == field.field_uuid).filter(FieldHisto.field_data_md5 == md5).first()
            if field_histo is None:
                  print("field_histo is none", field.field_uuid, md5 )
                  field_histo = FieldHisto(
                      field_uuid = field.field_uuid,
                      field_data = field.field_data,
                      field_data_md5 = md5,
                      name = field.field_name,
                      intervention_uuid=intervention_uuid,
                      controle_status='non_saisi' # TODO : dictionnaire des valeurs possibles
                  )
                  db.session.add(field_histo)
                  db.session.commit()  
          
                
    if nb_formulaire_with_averagelocation > 0:
        intervention.average_latitude = intervention_average_latitude / nb_formulaire_with_averagelocation
        intervention.average_longitude = intervention_average_longitude / nb_formulaire_with_averagelocation
    else:
        intervention.average_latitude = 0.0
        intervention.average_longitude = 0.0 
        
    db.session.commit()  
    return jsonify({ "intervention_id":intervention.id}), 201


@app_file_intervention.route("/intervention/<id>", methods=["GET"])
@jwt_required()
def get_intervention(id):
    intervention = Intervention.query.get(id)
    if intervention is None:
        abort(make_response(jsonify(error="intervention is not found"), 404))
    return jsonify(intervention.to_json())

@app_file_intervention.route("/intervention/<id>", methods=["DELETE"])
@jwt_required()
def delete_intervention(id):
    intervention = Intervention.query.get(id)
    if intervention is None:
        abort(make_response(jsonify(error="intervention is not found"), 404))
    db.session.delete(intervention)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
