from flask import Blueprint, render_template, session,abort, current_app

import uuid
import numpy
import os
from config import config

from ..model_dir.photo import Photo
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_photo= Blueprint('photo',__name__)

import cv2

import piexif
from fractions import Fraction


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Setup upload folder
UPLOAD_FOLDER = config["upload_dir"]

# cf fileupload : https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/


def deg_to_dms(decimal_coordinate, cardinal_directions):
    """
    This function converts decimal coordinates into the DMS (degrees, minutes and seconds) format.
    It also determines the cardinal direction of the coordinates.

    :param decimal_coordinate: the decimal coordinates, such as 34.0522
    :param cardinal_directions: the locations of the decimal coordinate, such as ["S", "N"] or ["W", "E"]
    :return: degrees, minutes, seconds and compass_direction
    :rtype: int, int, float, string
    """
    if decimal_coordinate < 0:
        compass_direction = cardinal_directions[0]
    elif decimal_coordinate > 0:
        compass_direction = cardinal_directions[1]
    else:
        compass_direction = ""
    degrees = int(abs(decimal_coordinate))
    decimal_minutes = (abs(decimal_coordinate) - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = Fraction((decimal_minutes - minutes) * 60).limit_denominator(100)
    return degrees, minutes, seconds, compass_direction

def dms_to_exif_format(dms_degrees, dms_minutes, dms_seconds):
    """
    This function converts DMS (degrees, minutes and seconds) to values that can
    be used with the EXIF (Exchangeable Image File Format).

    :param dms_degrees: int value for degrees
    :param dms_minutes: int value for minutes
    :param dms_seconds: fractions.Fraction value for seconds
    :return: EXIF values for the provided DMS values
    :rtype: nested tuple
    """
    exif_format = (
        (dms_degrees, 1),
        (dms_minutes, 1),
        (int(dms_seconds.limit_denominator(100).numerator), int(dms_seconds.limit_denominator(100).denominator))
    )
    return exif_format


def add_geolocation(image_path, latitude, longitude):
    """
    This function adds GPS values to an image using the EXIF format.
    This fumction calls the functions deg_to_dms and dms_to_exif_format.

    :param image_path: image to add the GPS data to
    :param latitude: the north–south position coordinate
    :param longitude: the east–west position coordinate
    """
    # converts the latitude and longitude coordinates to DMS
    latitude_dms = deg_to_dms(latitude, ["S", "N"])
    longitude_dms = deg_to_dms(longitude, ["W", "E"])

    # convert the DMS values to EXIF values
    exif_latitude = dms_to_exif_format(latitude_dms[0], latitude_dms[1], latitude_dms[2])
    exif_longitude = dms_to_exif_format(longitude_dms[0], longitude_dms[1], longitude_dms[2])

    try:
        # Load existing EXIF data
        exif_data = piexif.load(image_path)

        # https://exiftool.org/TagNames/GPS.html
        # Create the GPS EXIF data
        coordinates = {
            piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
            piexif.GPSIFD.GPSLatitude: exif_latitude,
            piexif.GPSIFD.GPSLatitudeRef: latitude_dms[3],
            piexif.GPSIFD.GPSLongitude: exif_longitude,
            piexif.GPSIFD.GPSLongitudeRef: longitude_dms[3]
        }

        # Update the EXIF data with the GPS information
        exif_data['GPS'] = coordinates

        # Dump the updated EXIF data and insert it into the image
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, image_path)
        print(f"EXIF data updated successfully for the image {image_path}.")
    except Exception as e:
        print(f"Error: {str(e)}")




@app_file_photo.route("/photo", methods=["GET"])
def get_photos():
    photos = Photo.query.all()
    return jsonify([photo.to_json() for photo in photos])


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM
# flutter image upload exemple : https://www.youtube.com/watch?v=dsPdIdrgAD4
@app_file_photo.route('/photo', methods=['POST'])
@jwt_required()
def create_photo():

    if request.files.get("file") is None:
        abort(400, "miss file parameter")
        
    if not 'photo_uuid' in request.form:
        abort(400, "miss photo_uuid parameter")
        
    if not 'latitude' in request.form:
        abort(400,"miss latitude parameter")
        
    if not 'longitude' in request.form:
        abort(400,"miss longitude parameter")

    if not 'intervention_uuid' in request.form:
        abort(400,"miss intervention_uuid parameter")
       
    if not 'field_uuid' in request.form:
        abort(400,"miss field_uuid parameter")
       
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)  
    print(get_extension(filename))
    photo_uuid = request.form.get('photo_uuid')
    
    photo= Photo.query.filter(Photo.photo_uuid == photo_uuid).first()
    
    print(photo)
    if photo is not None:
        print("photo already uploaded")
        abort(400,"photo already uploaded")
    
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    intervention_uuid = request.form.get('intervention_uuid')
    field_uuid = request.form.get('field_uuid')
    
    newfilename = photo_uuid+get_extension(filename)
    
    file.save(os.path.join(UPLOAD_FOLDER, newfilename))
    
    
    add_geolocation(os.path.join(UPLOAD_FOLDER, newfilename), float(latitude), float(longitude))
    
    
    photo = Photo(  photo_uuid=photo_uuid, latitude=latitude, longitude=longitude, filename= newfilename, intervention_uuid = intervention_uuid, field_uuid=field_uuid )
    db.session.add(photo)
    db.session.commit() 
    return jsonify(photo.to_json()), 201


@app_file_photo.route("/photo/<id>", methods=["GET"])
@jwt_required()
def get_photo(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(404, "photo is not found")
    return jsonify(photo.to_json_to_root())

@app_file_photo.route("/photo/<id>", methods=["DELETE"])
@jwt_required()
def delete_photo(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(404, "photo is not found")
    db.session.delete(photo)
    db.session.commit()
    return jsonify({'result': True, 'id': id})

@app_file_photo.route("/photo/ready")
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
