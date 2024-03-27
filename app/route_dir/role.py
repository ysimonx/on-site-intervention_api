from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.mymixin import Role
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_role = Blueprint('role',__name__)


@app_file_role.route("/role", methods=["GET"])
def get_role_list():
    items = Role.query.all()
    return jsonify([item.to_json() for item in items])


    #@app_file_role.route('/role', methods=['POST'])
    #def create_user():
    # if not request.json:
    #    abort(make_response(jsonify(error="no json provided in request"), 400))
    #
    # role_name = request.json.get('name', None)
    # if role_name is None:
    #    abort(make_response(jsonify(error="missing role_name parameter"), 400))
    # 
    #role = Role(
    #    name=role_name
    #)
    #
    #db.session.add(role)
    # db.session.commit()
    #return jsonify(role.to_json()), 201