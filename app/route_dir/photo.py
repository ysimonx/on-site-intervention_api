from flask import Blueprint, abort, make_response, current_app
from PIL import Image, ImageOps
from resizeimage import resizeimage

import os
from config import config

from ..model_dir.photo import Photo
from ..model_dir.tenant import Tenant
from ..model_dir.mymixin import User
from ..model_dir.event import Event
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from .. import db, getByIdOrByName

from ..thingsboard.connector_thingsboard import ThingsboardConnector


app_file_photo= Blueprint('photo',__name__)


import piexif
from fractions import Fraction

# extension for file upload
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# Setup upload folder
UPLOAD_FOLDER = config["upload_dir"]

# resize width
RESIZE_WIDTH = 300

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
        current_app.logger.info(f"EXIF data updated successfully for the image {image_path}.")
    except Exception as e:
        print(f"Error: {str(e)}")

def resize_image(filename_source, filename_destination):
    fd_img = open(filename_source, 'rb')
    img = Image.open(fd_img)
    
    # cf https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    fixed_img = ImageOps.exif_transpose(img)
    
    fixed_img = resizeimage.resize_width(fixed_img, RESIZE_WIDTH)
    fixed_img.save(filename_destination, img.format)
    fd_img.close()

@app_file_photo.route("/photo", methods=["GET"])
@jwt_required()
def get_photos():
    _user = User.me()
    photos = Photo.query.filter(Photo.tenant_id == _user.get_internal()["tenant_id"]).all()
    return jsonify([photo.to_json() for photo in photos])


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM
# flutter image upload exemple : https://www.youtube.com/watch?v=dsPdIdrgAD4
@app_file_photo.route('/photo', methods=['POST'])
@jwt_required()
def create_photo():


    if not "file" in request.files:
        abort(make_response(jsonify(error="missing file parameter"), 400))
        
    if not 'photo_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing photo_on_site_uuid parameter"), 400))

    if not 'latitude' in request.form:
        abort(make_response(jsonify(error="missing latitude parameter"), 400))
        
    if not 'longitude' in request.form:
        abort(make_response(jsonify(error="missing longitude parameter"), 400))

    if not 'field_on_site_uuid' in request.form:
        abort(make_response(jsonify(error="missing field_on_site_uuid parameter"), 400))
       
    photo_on_site_uuid = request.form.get('photo_on_site_uuid')
    photo = Photo.query.filter(Photo.photo_on_site_uuid == photo_on_site_uuid).first()
    if photo is not None:
        current_app.logger.infos("photo already uploaded")
        abort(make_response(jsonify(error="photo already uploaded"), 400))
    
    
    _user = User.me()


    file                        = request.files['file']
    filename                    = secure_filename(file.filename)
    latitude                    = request.form.get('latitude')
    longitude                   = request.form.get('longitude')
    field_on_site_uuid          = request.form.get('field_on_site_uuid')
    intervention_values_on_site_uuid   = request.form.get('intervention_values_on_site_uuid')
    newfilename_fullsize        = photo_on_site_uuid+"_fullsize"+get_extension(filename)
    newfilename         = photo_on_site_uuid+get_extension(filename)

    # save image as full size
    file.save(os.path.join(UPLOAD_FOLDER, newfilename_fullsize))
    # copy image, and resize this copy to small width 
    resize_image(os.path.join(UPLOAD_FOLDER, newfilename_fullsize), os.path.join(UPLOAD_FOLDER, newfilename))
    
    add_geolocation(os.path.join(UPLOAD_FOLDER, newfilename), float(latitude), float(longitude))
    add_geolocation(os.path.join(UPLOAD_FOLDER, newfilename_fullsize), float(latitude), float(longitude))
    
    photo = Photo(  photo_on_site_uuid=photo_on_site_uuid,
                    latitude=latitude, 
                    longitude=longitude, 
                    filename= newfilename, 
                    filename_fullsize=newfilename_fullsize,
                    field_on_site_uuid=field_on_site_uuid, 
                    intervention_values_on_site_uuid = intervention_values_on_site_uuid,
                    tenant_id = _user.get_internal()["tenant_id"]
                )
    
    db.session.add(photo)
    
    
    event=Event(object=photo.__class__.__name__, object_id=photo.id, action="upload",  description="")
    db.session.add(event)
       
       
    db.session.commit() 

    # tb=ThingsboardConnector()
    # tb.syncAsset(photo)

    return jsonify(photo.to_json()), 201


@app_file_photo.route("/photo/<id>", methods=["GET"])
@jwt_required()
def get_photo(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(make_response(jsonify(error="photo is not found"), 404))

    return jsonify(photo.to_json_to_root())

@app_file_photo.route("/photo/<id>", methods=["DELETE"])
@jwt_required()
def delete_photo(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(make_response(jsonify(error="photo is not found"), 404))
    db.session.delete(photo)
    db.session.commit()
    return jsonify({'result': True, 'id': id})

"""
This endpoint is made for refreshing token (if needed) just before uploading photos
"""
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
