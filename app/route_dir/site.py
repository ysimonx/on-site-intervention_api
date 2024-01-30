from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.site import Site
from ..model_dir.mymixin         import User, Role
from ..model_dir.tenant import Tenant

from flask import jsonify, request, abort, g
from .. import db, getByIdOrEmail, getByIdOrByName

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_site = Blueprint('site',__name__)


@app_file_site.route("/site", methods=["GET"])
@jwt_required() 
def get_site_list():
    
    print(g.current_user)
    # TO DO
    # je dois trouver les sites pour lesquels j'ai des roles ...
    items = Site.query.all()
    return jsonify([item.to_json() for item in items])




@app_file_site.route('/site', methods=['POST'])
@jwt_required()
def create_site():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    site_name = request.json.get('name', None)
    if site_name is None:
        abort(make_response(jsonify(error="missing site_name parameter"), 400))

    _user = User.me()
     
    site = Site(
        name=site_name,
        tenant_id = _user.get_internal()["tenant_id"]
    )

    db.session.add(site)
    db.session.commit()
    return jsonify(site.to_json()), 201