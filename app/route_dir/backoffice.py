from flask import Blueprint, render_template, redirect, session,abort, current_app, make_response

import uuid
import hashlib
import numpy
import os
import datetime
from config import config

from ..model_dir.intervention import Intervention
from ..model_dir.photo import Photo
from ..model_dir.place import Place
from ..model_dir.report import Report
from ..model_dir.field import Field
from ..model_dir.field_histo import FieldHisto
from ..model_dir.user import User
from ..model_dir.company import Company

from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_backoffice= Blueprint('backoffice',__name__)

import cv2
import json
from sqlalchemy import desc, text

# Setup upload folder
UPLOAD_FOLDER = config["upload_dir"]


@app_file_backoffice.route("/intervention/details", methods=["GET"])
def get_interventions_details_backoffice():
    
    users = User.query.all()
    dict_users = {}
    for user in users:
        dict_users[user.id] = user
        
        
    companies = Company.query.all()
    dict_companies = {}
    for company in companies:
        dict_companies[company.id] = company
    
    
    liste_controles = [
        "piece-identite",
        "ancienne-chaudiere",
        "plaque-signaletique-ancienne-chaudiere",
        "futur-emplacement-unite-exterieure",
        "facade-maison",
        "ajout-de-photo-avant-depose",
     
        "depose-ancienne-chaudiere",
        "vue-d-ensemble-unite-interieure",
        "fixation-unite-interieure",
        "plaque-signaletique-unite-interieure",
        "calorifuge-circuit-eau-chaude",
        "calorifuge-circuit-frigorigene",
        "dispositifs-reglage-equilibrage-reseau",
        "vue-d-ensemble-unite-exterieure",
        "unite-exterieure-aeration",
        "plaque-signaletique-unite-exterieure",
        "fixation-unite-exterieure",
        "radiateur",
        "ajout-de-photo-installation"
    ]
    
    users = User.query.all()
    dict_users = {}
    for user in users:
        dict_users[user.id] = user
        
        
    companies = Company.query.all()
    dict_companies = {}
    for company in companies:
        dict_companies[company.id] = company
    

    recordset = Intervention.query
    
    filter_controle_status = request.args.get("filter_controle_status")
    if filter_controle_status == None or filter_controle_status == "":
        filter_controle_status = 99
    else:
        filter_controle_status=int(filter_controle_status)
        recordset = recordset.filter(text("intervention_uuid in (select intervention_uuid from controle where controle_status='"+ dict_EnumInverse[filter_controle_status]+ "')"))
    
    filter_user_id =  request.args.get("user_id") 
    if filter_user_id is None or  filter_user_id== "" :
        recordset = recordset
    else:
        recordset = recordset.filter(text("owner_user_id = '" +filter_user_id +"'"))
        
    interventions = recordset.order_by(desc("time_created")).all()
    

    dict_intervention_controle_details = {}
    
    for intervention in interventions:
        dict_intervention_controle_field = {}
    
        print("----")
        fields=intervention.fields
        fields_histo=intervention.fields_histo
        for controle_name in liste_controles:
            # print(controle_name)
            dict_intervention_controle_field[controle_name]=dict_controle_field_for_export[0] # default value : non saisi

            for field in fields:
                if (field.name == controle_name):
                    # print(field.field_uuid)
                    for field_histo in fields_histo:
                        if field.field_uuid == field_histo.field_uuid:
                            if field.field_data_md5 == field_histo.field_data_md5:
                                # print("gotcha")
                                dict_intervention_controle_field[controle_name] = dict_controle_field_for_export[field_histo.controle_status.value];
                                # print(controle_name, dict_intervention_controle_field[controle_name])
        dict_intervention_controle_details[intervention.intervention_uuid] = dict_intervention_controle_field
    return render_template('interventions_details.html', dict_controle=dict_controle, dict_companies=dict_companies, dict_users= dict_users, interventions=interventions,liste_controles=liste_controles, dict_intervention_controle_details=dict_intervention_controle_details)
   


@app_file_backoffice.route("/field/histo_by_field_uuid/<field_uuid>", methods=["GET"])
def get_field_histo_by_uuid(field_uuid):
    fields_histo = FieldHisto.query.filter(FieldHisto.field_on_site_uuid == field_uuid).all()
    print(fields_histo)
    fields=[]
    for field_histo in fields_histo:
        print(field_histo.to_json())
        jsonField  = field_histo.to_json()
        # jsonField.controle_status = field_histo.controle_status
        fields.append(jsonField)
        
    # on recupere toutes les photos de ce intervention (y compris les obsoletes)
    photos = Photo.query.filter(Photo.field_uuid == field_uuid).all()
    map_photos={}    
    for photo in photos:
        map_photos[photo.photo_uuid] = photo

    
    return render_template('field.html', fields = fields, map_photos= map_photos, dict_controle_field=dict_controle_field)
    
@app_file_backoffice.route("/intervention", methods=["GET"])
def get_interventions_backoffice():
    users = User.query.all()
    dict_users = {}
    for user in users:
        dict_users[user.id] = user
        
        
    companies = Company.query.all()
    dict_companies = {}
    for company in companies:
        dict_companies[company.id] = company
    

    recordset = Intervention.query
    
    filter_controle_status = request.args.get("filter_controle_status")
    if filter_controle_status == None or filter_controle_status == "":
        filter_controle_status = 99
    else:
        filter_controle_status=int(filter_controle_status)
        recordset = recordset.filter(text("intervention_uuid in (select intervention_uuid from controle where controle_status='"+ dict_EnumInverse[filter_controle_status]+ "')"))
    
    filter_user_id =  request.args.get("user_id") 
    if filter_user_id is None or  filter_user_id== "" :
        recordset = recordset
    else:
        recordset = recordset.filter(text("owner_user_id = '" +filter_user_id +"'"))
        
    interventions = recordset.order_by(desc("time_created")).all()
    
    # interventions_json = jsonify([item.to_json() for item in interventions])
    
    return render_template('interventions.html', user_id=filter_user_id, interventions=interventions, dict_users=dict_users, dict_companies=dict_companies, dict_controle=dict_controle, filter_controle_status= filter_controle_status)


@app_file_backoffice.route("/users", methods=["POST"])
def create_or_update_user():
    
        
    message =  request.args.get("message")
    
    
    if "user_id" in request.form:
        print("update user")
        user = getByIdOrByName(obj=User, id=request.form.get("user_id"))
        if user is None:
             return redirect("/backoffice/v1/users?message=user%20non%20trouvé")
        user.password = request.form.get("password")
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return redirect("/backoffice/v1/users?message=password%20modifié")
    
    user = User(email= request.form.get("email"), password= request.form.get("password"), company_id = request.form.get("company_id"), firstname=request.form.get("firstname"), lastname=request.form.get("lastname"))
    user.hash_password()
    db.session.add(user)      
    db.session.commit()
    return redirect("/backoffice/v1/users?message=utilisateur créé")
    


@app_file_backoffice.route("/users", methods=["GET"])
def get_users():
    
    
    message =  request.args.get("message")
    
    
    users = User.query.order_by(User.lastname).all()
    
    companies = Company.query.order_by(Company.name).all()
    dict_companies = {}
    for company in companies:
        dict_companies[company.id] = company
    
    return render_template('users.html',users = users, dict_companies=dict_companies, message=message)


@app_file_backoffice.route("/companies", methods=["GET"])
def get_companies():
    
        
    message =  request.args.get("message")
    
    
    companies = Company.query.order_by(Company.name).all()
    dict_companies = {}
    for company in companies:
        dict_companies[company.id] = company
    
    return render_template('companies.html', companies=companies, message=message)


@app_file_backoffice.route("/companies", methods=["POST"])
def create_or_update_company():
    
    if "company_id" in request.form:
        print("update")
        company = getByIdOrByName(obj=Company, id=request.form.get("company_id"))
        lastcompany_name = company.name
        company.name = request.form.get("company_name").lower()
        db.session.add(company)
        db.session.commit()
        return redirect("/backoffice/v1/companies?message=société%20modifiée%20"+lastcompany_name.upper()+"%20en%20"+company.name.upper())
        
    new_company = request.form.get("new_company").lower()
    company = getByIdOrByName(obj=Company, id=new_company)
    if company is None:
        if len(new_company) > 0:
            print("company '" + new_company +  "' n existe pas encore")
            company = Company(
                name=new_company
            )

            db.session.add(company)
            db.session.commit()
            return redirect("/backoffice/v1/companies?message=création%20société%20"+new_company.upper()+"%20effectuée")
    
    return redirect("/backoffice/v1/companies")
    


    
@app_file_backoffice.route("/photos", methods=["GET"])
def get_photos_backoffice():
    photos = Photo.query
    photos = photos.order_by(desc("time_created")).all()
    users = User.query.all()
    dict_users = {}
    for user in users:
        dict_users[user.id] = user
        
    companies = Company.query.all()
    dict_companies = {}
    for company in companies:
        dict_companies[company.id] = company
    
    photoTABCertigna = []
    
    for photo in photos:
        path = os.path.join(UPLOAD_FOLDER, "timestamps",  photo.filename)
        pathCertigna=path + ".certigna.tsr.txt"
        print(pathCertigna)
        if os.path.isfile(pathCertigna) and os.access(pathCertigna, os.R_OK):
            photoTABCertigna.append(photo.photo_uuid)
            print("exists")
        
    # print(photoTABCertigna)        
    return render_template('photos.html', photos=photos, photoTABCertigna=photoTABCertigna, dict_users=dict_users, dict_companies=dict_companies)


@app_file_backoffice.route("/controle", methods=["POST"])
def post_controle_backoffice():
    print(request.form)
    
    intervention_id  = request.form.get("intervention_id")
    
    intervention=Intervention.query.get(intervention_id)
    print(intervention.intervention_uuid)
    controle = Controle.query.filter(Controle.intervention_uuid == intervention.intervention_uuid).first()
    controle.adresse = request.form.get("place_address")
    controle.zip = request.form.get("place_zip")
    controle.ville = request.form.get("place_ville")
    controle.numero_fiscal_local= request.form.get("place_numero_fiscal_local")
    controle.attendus = request.form.get("controle-attendus")
    controle.controle_status = request.form.get("controle-status")
    controle.commentaires = request.form.get("controle-commentaires")
    
    db.session.add(controle)
    db.session.commit()
    
    for k, v in request.form.items():
        
        # sauvegarde du status de tous les champs du form post ... 
        # chaque field a une clé de la forme
        # field | 33f28eb3-15cc-11ee-b40c-fd0c80dc8a99 | 05af6be0c324f6fba4cb7184d773181b
        # field | field_uuid                           | field_data_md5
        # ce qui signifie que le controleur donne un status pour un champ donné pour un contenu (question ET reponses/photos/commentaires donnés)
        if (k.startswith("field|")): 
            field_entete, field_uuid, md5 = k.split("|")
            field_histo = FieldHisto.query.filter(FieldHisto.field_on_site_uuid == field_uuid).filter(FieldHisto.field_data_md5 == md5).first()
            field_histo.controle_status=v
            db.session.add(field_histo)
            db.session.commit()
            
    return redirect("/backoffice/v1/intervention/" + request.form.get("intervention_id") + "?message=données%20enregistrées")
     
   

@app_file_backoffice.route("/intervention/<id>", methods=["GET"])
def get_intervention_backoffice(id):
    
    intervention = Intervention.query.get(id)
    
    if intervention is None:
        abort(make_response(jsonify(error="intervention is not found"), 404))

    
    # le owner_user_id est celui qui a créé ce intervention
    owner_user_id = intervention.get_internal()["owner_user_id"]
    user = User.query.filter(User.id ==owner_user_id).first()
    
    
    # un eventuel message à afficher 
    # exemple : http://localhost:4999/backoffice/v1/intervention/7e5fcd1f-636a-4e86-b5fa-2316372afc13?message=donn%C3%A9es%20enregistr%C3%A9es
    message =  request.args.get("message")
    
    
    # chargement du md5 de la valeur (Question ET reponses) de chaque champ de ce intervention (histoire de pouvoir controler la valeur de chaque champs)
    dict_field_md5 = {}
    fields_for_md5 = Field.query.filter(Field.intervention_uuid == intervention.intervention_uuid).all()
    for field_for_md5 in fields_for_md5:
        dict_field_md5[field_for_md5.field_uuid] = field_for_md5.field_data_md5

    
    # chargement de l'historique de chaque champ, avec le controle qui avait été donné à chaque fois
    dict_field_histo={}
    
    dict_field_histo_status = {}
    fields_historiques = FieldHisto.query.filter(FieldHisto.intervention_on_site_uuid == intervention.intervention_uuid).all()
    for field_historique in fields_historiques:
        l=[]
        if field_historique.field_uuid in dict_field_histo:
            l = dict_field_histo[field_historique.field_uuid]
            print(field_historique.field_name)
        l.append(field_historique)
        dict_field_histo[field_historique.field_uuid] = l
        
        dict_field_histo_status[field_historique.field_uuid+"|"+field_historique.field_data_md5] = field_historique
    
    print(dict_field_histo)
    # et bien la date de controle, c'est maintenant 
    date_controle=datetime.datetime.now()
    
    
    # chargement d'un controle précédent de ce intervention
    controle = Controle.query.filter(Controle.intervention_uuid == intervention.intervention_uuid).first()
    if controle is None:
            controle=Controle(intervention_uuid = intervention.intervention_uuid, controle_status='non_saisi')
            db.session.add(controle)
            db.session.commit()
                
    # on recupere toutes les photos de ce intervention (y compris les obsoletes)
    photos = Photo.query.filter(Photo.intervention_uuid == intervention.intervention_uuid).all()
    map_photos={}    
    for photo in photos:
        map_photos[photo.photo_uuid] = photo
    
    # preparation des photos à afficher sur la carte google maps
    list_photos_geoloc=[] 
    for photo in photos:
        img_tag="<img style='width:100px;' src='https://api-renovadmin.kysoe.com/static/photos/"+photo.filename+"' />"
        list_photos_geoloc.append({"external_id":photo.photo_uuid, "latitude":photo.latitude,"longitude":photo.longitude,"infoContent":img_tag})
     
    
    photoTABCertigna = []
       
    for photo in photos:
        map_photos[photo.photo_uuid] = photo
        path = os.path.join(UPLOAD_FOLDER, "timestamps", photo.filename)
        pathCertigna=path + ".certigna.tsr.txt"
        if os.path.isfile(pathCertigna) and os.access(pathCertigna, os.R_OK):
            photoTABCertigna.append(photo.photo_uuid)
            
    
    # re ordering des champs pour privilégier le formulaure avant-depose avant celui de l'installation
    reports=intervention.reports
    fields=[]
    ordre_reports=['Avant dépose','Installation']
    for ordre_report in ordre_reports:
        
        for report in reports:
            if report.formulaire_name == ordre_report:
                formulaire_data = report.formulaire_data
                formulaire_json=json.loads(formulaire_data)
                fields_json=formulaire_json["fields"]
                for field_json in fields_json:
                    field_json["md5"] = dict_field_md5[field_json["field_uuid"]]
                    controle_status =  dict_field_histo_status[field_json["field_uuid"] + "|" + field_json["md5"]].controle_status
                    
                    # ici on va changer le champs enum par une variable de type string plus facile à traiter dans le template
                    field_json["controle_status"] = dict_controle_field[controle_status.value]
                    fields.append(field_json)
            
    return render_template('intervention.html', message=message, 
                                         intervention=intervention,
                                         controle=controle,
                                         dict_controle_field=dict_controle_field,
                                         fields=fields,
                                         dict_field_md5=dict_field_md5,
                                         dict_field_histo_status=dict_field_histo_status,
                                         dict_field_histo=dict_field_histo,
                                         map_photos = map_photos,
                                         moe=user,
                                         date_controle=date_controle,
                                         list_photos_geoloc=list_photos_geoloc,
                                         photoTABCertigna=photoTABCertigna
                                        )

    

