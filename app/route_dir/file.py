from flask import Blueprint, abort, make_response

import os
from config import config

from ..model_dir.file import File
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from .. import db

from ..thingsboard.connector_thingsboard import ThingsboardConnector


app_file_file= Blueprint('file',__name__)




ALLOWED_EXTENSIONS = {'pdf'}

# Setup upload folder
UPLOAD_FOLDER = config["upload_dir"]

# cf fileupload : https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/




@app_file_file.route("/file", methods=["GET"])
def get_files():
    files = File.query.all()
    return jsonify([file.to_json() for file in files])


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM
# flutter image upload exemple : https://www.youtube.com/watch?v=dsPdIdrgAD4
@app_file_file.route('/file', methods=['POST'])
@jwt_required()
def create_file():

    if request.files.get("file") is None:
        abort(make_response(jsonify(error="missing file parameter"), 400))
        
    if not 'file_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing file_on_site_uuid parameter"), 400))

    if not 'intervention_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing intervention_on_site_uuid parameter"), 400))

    if not 'report_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing report_on_site_uuid parameter"), 400))
       
    if not 'field_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing field_on_site_uuid parameter"), 400))
       
    if not 'file_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing file_on_site_uuid parameter"), 400))
    
    file_on_site_uuid = request.form.get('file_on_site_uuid')
    file = File.query.filter(File.file_on_site_uuid == file_on_site_uuid).first()
    if file is not None:
        print("file already uploaded")
        abort(make_response(jsonify(error="file already uploaded"), 400))
    
    file        = request.files['file']
    filename    = secure_filename(file.filename)
    latitude    = request.form.get('latitude')
    longitude   = request.form.get('longitude')
    field_on_site_uuid          = request.form.get('field_on_site_uuid')
    report_on_site_uuid         = request.form.get('report_on_site_uuid')
    intervention_on_site_uuid   = request.form.get('intervention_on_site_uuid')
    newfilename                 = file_on_site_uuid+get_extension(filename)
    
    file.save(os.path.join(UPLOAD_FOLDER, newfilename))
    
    file = File(  file_on_site_uuid=file_on_site_uuid,
                    filename= newfilename, 
                    field_on_site_uuid=field_on_site_uuid, 
                    report_on_site_uuid=report_on_site_uuid, 
                    intervention_on_site_uuid=intervention_on_site_uuid
                )
    db.session.add(file)
    db.session.commit() 

    tb=ThingsboardConnector()
    tb.syncAsset(file)

    return jsonify(file.to_json()), 201


@app_file_file.route("/file/<id>", methods=["GET"])
@jwt_required()
def get_file(id):
    file = File.query.get(id)
    if file is None:
        abort(make_response(jsonify(error="file is not found"), 404))

    return jsonify(file.to_json_to_root())

@app_file_file.route("/file/<id>", methods=["DELETE"])
@jwt_required()
def delete_file(id):
    file = File.query.get(id)
    if file is None:
        abort(make_response(jsonify(error="file is not found"), 404))
    db.session.delete(file)
    db.session.commit()
    return jsonify({'result': True, 'id': id})

@app_file_file.route("/file/ready")
@jwt_required()
def get_ready():
    return jsonify(message="ready");
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[0].lower()

def get_extension(filename):
    fic, file_extension = os.path.splitext(filename)
    return file_extension.lower()
