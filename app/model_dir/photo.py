from .. import db
import datetime

from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM

class Photo(db.Model, MyMixin):
    __tablename__ = 'photos'
    
    field_id                    = db.Column(db.String(36),  db.ForeignKey("fields.id"), nullable=True)
    
    photo_on_site_uuid          = db.Column(db.String(36), unique=True)
    field_on_site_uuid          = db.Column(db.String(36),  index=True)
    report_on_site_uuid         = db.Column(db.String(36),  index=True)
    intervention_on_site_uuid   = db.Column(db.String(36),  index=True)
    
    filename            = db.Column(db.String(255))
    latitude            = db.Column(db.Float);
    longitude           = db.Column(db.Float);
    
    
    def to_json(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
            'photo_on_site_uuid':           self.photo_on_site_uuid,
            'field_on_site_uuid':           self.field_on_site_uuid,
            'report_on_site_uuid':          self.report_on_site_uuid,
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'filename':                     self.filename
        }
        
    def to_json_light(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
            'photo_on_site_uuid':           self.photo_on_site_uuid,
            'field_on_site_uuid':           self.field_on_site_uuid,
            'report_on_site_uuid':          self.report_on_site_uuid,
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'filename':                     self.filename
        }

    def get_attributes_for_thingsboard(self):
        dict_attributes=super().get_attributes_for_thingsboard()
        # remove relationships
        print(dict_attributes)
        for key in dict_attributes:
            print(key, "   =   ", dict_attributes[key], "     ", type( dict_attributes[key]), isinstance(dict_attributes[key],  (bool,str,int, float, datetime.datetime)))
        del dict_attributes["photos_backref"]
        return dict_attributes
        

from sqlalchemy import event
@event.listens_for(Photo, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
