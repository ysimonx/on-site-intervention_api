from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class ReportTemplate(db.Model, MyMixin):
    __tablename__ = 'report_templates'
    


    def to_json(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            
        }
        
    def to_json_light(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            
        }
       


from sqlalchemy import event
@event.listens_for(ReportTemplate, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
