from flask import Blueprint, abort, make_response


from ..model_dir.place import Place
from flask import jsonify, abort
from flask_jwt_extended import jwt_required

from .. import db
app_file_place= Blueprint('place',__name__)




@app_file_place.route("/place", methods=["GET"])
def get_places():
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
        abort(make_response(jsonify(error="place is not found"), 404))
    return jsonify(place.to_json())

@app_file_place.route("/place/<id>", methods=["DELETE"])
@jwt_required()
def delete_place(id):
    place = Place.query.get(id)
    if place is None:
       abort(make_response(jsonify(error="place is not found"), 404))
    db.session.delete(place)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
