from .. import db

# from types import NoneType
import datetime


from sqlalchemy import event
from sqlalchemy.orm import declarative_base, relationship, declared_attr
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, verify_jwt_in_request
from flask_bcrypt import generate_password_hash, check_password_hash
import uuid
from datetime import date, datetime
from sqlalchemy import inspect
from .tenant import Tenant

NoneType = type(None)
NoneType = None.__class__

def formatted_date_iso(date):
    if date is None:
        return None
    return date.isoformat()
    

class MyMixin(object):
    id              = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name            = db.Column(db.String(255), index=True)

    time_created    = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated    = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    owner_user_id   = db.Column(db.String(36), nullable=True, index=True, default="")
    tenant_id       = db.Column(db.String(36), nullable=True, index=True)
    
    def map_owner(mapper, connect, target):
        
        # _tenant = Tenant.query.filter(Tenant.name=="sandbox").first()
        # if (not _tenant is None):
        #     target.tenant_id = _tenant.id
        
        verify_jwt_in_request(optional=True)
        current_user = get_jwt_identity()
        if (not current_user is None):
            target.owner_user_id = current_user

    @classmethod
    def my_query(cls):
        
        current_user = get_jwt_identity()
        _user = User.query.get(current_user)
        
        if _user.isSuperAdmin():
            print("is super admin")
            query = cls.query
        else:
            # return a query filtered by current tenant value (specified when logged in)
            print("is NOT super admin")
            query = cls.__class__.query.filter(__class__ .tenant_id == _user.get_internal()["tenant_id"])
        
        return query
    
    def get_internal(self):

        
        return {
                
                'time_created_utc': formatted_date_iso(self.time_created),
                'time_updated_utc': formatted_date_iso(self.time_updated),
                'owner_user_id':    self.owner_user_id,
                'tenant_id':    self.tenant_id
            }
        
        
    def get_attributes_for_thingsboard(self):
        
        # je prends tous les attributs d'une instance d'objets
        dict_attributes={}
        mapper = inspect(self)
        for column in mapper.attrs:
            # pour chaque colonne, je vérifie le type de l'attribut (pour éliminer les relationsship par exemple)
            if isinstance(column.value,  (NoneType, bool,str,int, float)):
                dict_attributes[column.key]=column.value
            if isinstance(column.value, (datetime)):
                 dict_attributes[column.key]=column.value
        return dict_attributes
        
        
"""        
@event.listens_for(MyMixin, 'before_insert')
def do_stuff(mapper, connect, target):


    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    if (not current_user is None):
        target.owner_user_id = current_user
""" 



user_role = db.Table('users_roles',
                    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True),
                    db.Column('role_id', db.String(36), db.ForeignKey('roles.id'), primary_key=True)
                    )
   


class Role(db.Model, MyMixin):
    __tablename__ = 'roles'
   
    site_id  = db.Column(db.String(36), db.ForeignKey("sites.id"))
    site        = relationship("Site", viewonly=True)
    
    
    def to_json(self):
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':             self.name,
            'site':     self.site.to_json(),
            'users':      [{"user": item.to_json_light()} for item in self.users] 
        }

    def to_json_light(self):
        return {
            'id':               self.id,
            'name':             self.name,
            'users':            [{"user": item.to_json_light()} for item in self.users] 
        }
        
    def to_json_anonymous(self):
        return {
            'id':               self.id,
        }
    

# ToDo : essayer ca plutot https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935
class User(db.Model, MyMixin):
    __tablename__ = 'users'
   
    email       = db.Column(db.String(100), index=True)
    password    = db.Column(db.String(100))
    firstname   = db.Column(db.String(100))
    lastname    = db.Column(db.String(100))
    phone       = db.Column(db.String(100))
    company_id  = db.Column(db.String(36), db.ForeignKey("companies.id"))
    company     = db.relationship("Company", viewonly=True)
    active      = db.Column(db.Boolean, nullable=False, default=True)

    roles = db.relationship('Role', secondary=user_role, backref='users')
    tenants_administrator = db.relationship('Tenant', foreign_keys="[Tenant.admin_tenant_user_id]")
    def me():
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        return user
    
    def isSuperAdmin(self):
        return True
    
    def to_json(self):
        
        sites=[];
        dict_site_roles={}
        
        for item in self.roles:
            # print(item.site.name)
            
            if not item.site_id in sites:
                dict_site_roles[item.site.name] = {"roles":[]}
                sites.append(item.site_id)
            dict_site_roles[item.site.name]["roles"].append(item.name)
        
        return {
            'id':           self.id,
            '_internal' :   self.get_internal(),
            'email':        self.email,
            'password':     self.password,
            'phone':        self.phone,
            'firstname':    self.firstname,
            'lastname':     self.lastname,
            'company':      self.company.name,
            'sites_roles':   dict_site_roles,
            'active':       self.active,
            
        }

    def to_json_light(self):
        
        return {
            'id':           self.id,
            'email':        self.email,
            'phone':        self.phone,
            'firstname':    self.firstname,
            'lastname':     self.lastname,
            'company':      self.company.name,
            'active':       self.active,
        }
    
    
    def to_json_ultra_light(self):
        
        
        return {
            'id':           self.id,
            'email':        self.email,
            'phone':        self.phone,
            'firstname':    self.firstname,
            'lastname':     self.lastname,
            'company':      self.company.name,
            'active':       self.active,
        }
        
        
    def to_json_anonymous(self):
        return {
            'id':           self.id,
        }


    def hash_password(self):
            self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
            return check_password_hash(self.password, password)








from sqlalchemy import event
@event.listens_for(User, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)


from sqlalchemy import event
@event.listens_for(Role, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)

