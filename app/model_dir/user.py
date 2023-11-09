from .. import db
from .mymixin import MyMixin
from flask_bcrypt import generate_password_hash, check_password_hash



# ToDo : essayer ca plutot https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935
class User(db.Model, MyMixin):
    __tablename__ = 'users'
   
    email       = db.Column(db.String(100), unique=True)
    password    = db.Column(db.String(100))
    firstname   = db.Column(db.String(100))
    lastname    = db.Column(db.String(100))
    company_id  = db.Column(db.String(36), db.ForeignKey("companies.id"))
    company     = db.relationship("Company", viewonly=True)

    def to_json(self):
        return {
            'id':           self.id,
            '_internal' :   self.get_internal(),
            'email':        self.email,
            'password':     self.password,
            'company_id':   self.company_id,
            'firstname':    self.firstname,
            'lastname':     self.lastname,
            'company':      self.company.to_json_light()
            
        }

    def to_json_light(self):
        return {
            'id':           self.id,
            'email':        self.email,
            'company_id':   self.company_id,
            'firstname':    self.firstname,
            'lastname':     self.lastname,
            'company':      self.company.to_json_light()
            
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
