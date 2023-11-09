from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Report(db.Model, MyMixin):
    __tablename__ = 'reports'
    
    intervention_id     = db.Column(db.String(36), db.ForeignKey("interventions.id"))
    report_on_site_uuid = db.Column(db.String(255), unique=True)
    report_data         = db.Column(db.Text())
    report_data_md5     = db.Column(db.String(32))
    average_latitude    = db.Column(db.Float)
    average_longitude   = db.Column(db.Float)
    intervention_uuid   = db.Column(db.String(255))
   

    def to_json(self):
        return {
            'id': self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'report_on_site_uuid':  self.report_on_site_uuid,
            'report_data':          self.report_data,
            'report_data_md5':      self.report_data_md5,
            'intervention_id':      self.intervention_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
            
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'name':                 self.name,
            'report_on_site_uuid':  self.report_on_site_uuid,
            'report_data':          self.report_data,
            'report_data_md5':      self.report_data_md5,
            'intervention_id':      self.intervention_id,
            'intervention_uuid':    self.intervention_uuid,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
        }


from sqlalchemy import event
@event.listens_for(Report, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
