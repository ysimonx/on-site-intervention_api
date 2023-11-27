from .. import db
from .mymixin import MyMixin
from flask_bcrypt import generate_password_hash, check_password_hash



user_role = db.Table('users_roles',
                    db.Column('user_id', db.String(36), db.ForeignKey('users.id')),
                    db.Column('role_id', db.String(36), db.ForeignKey('roles.id'))
                    )
   


class Role(db.Model, MyMixin):
    __tablename__ = 'roles'
   
    
    def to_json(self):
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':             self.name,
        }

    def to_json_light(self):
        return {
            'id':               self.id,
            'name':             self.name,
            
        }
        
    def to_json_anonymous(self):
        return {
            'id':               self.id,
        }
    

# ToDo : essayer ca plutot https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935
class User(db.Model, MyMixin):
    __tablename__ = 'users'
   
    email       = db.Column(db.String(100), unique=True)
    password    = db.Column(db.String(100))
    firstname   = db.Column(db.String(100))
    lastname    = db.Column(db.String(100))
    company_id  = db.Column(db.String(36), db.ForeignKey("companies.id"))
    company     = db.relationship("Company", viewonly=True)

    roles = db.relationship('Role', secondary=user_role, backref='users')

    def to_json(self):
        
        tenants=[];
        dict_tenant_roles={}
        
        for item in self.roles:
            if not item.tenant_id in tenants:
                dict_tenant_roles[item.tenant_id] = {"roles":[]}
                tenants.append(item.tenant_id)
            dict_tenant_roles[item.tenant_id]["roles"].append(item.name)
        
        return {
            'id':           self.id,
            '_internal' :   self.get_internal(),
            'email':        self.email,
            'password':     self.password,
            'company_id':   self.company_id,
            'firstname':    self.firstname,
            'lastname':     self.lastname,
            'company':      self.company.to_json_light(),
            'tenant_ids':   dict_tenant_roles
            
        }

    def to_json_light(self):
        
        return self.to_json()
        
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

