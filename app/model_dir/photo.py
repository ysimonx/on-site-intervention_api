from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM

class Photo(db.Model, MyMixin):
    __tablename__ = 'photos'
    
    photo_uuid          = db.Column(db.String(255), unique=True)
    intervention_uuid   = db.Column(db.String(255))
    field_uuid          = db.Column(db.String(255))
    filename            = db.Column(db.String(255))
    latitude            = db.Column(db.Float);
    longitude           = db.Column(db.Float);
    
    
    def to_json(self):
        return {
            'id':           self.id,
            '_internal' :   self.get_internal(),
            'photo_uuid':   self.photo_uuid,
            'filename':     self.filename
        }
        
    def to_json_light(self):
        return {
            'id':           self.id,
            'photo_uuid':   self.photo_uuid, 
            'filename':     self.filename
        }


from sqlalchemy import event
@event.listens_for(Photo, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
