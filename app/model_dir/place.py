from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Place(db.Model, MyMixin):
    __tablename__ = 'places'
    
    place_uuid= db.Column(db.String(255), unique=True)
    average_latitude= db.Column(db.Float);
    average_longitude= db.Column(db.Float);
    
    interventions   = relationship("Intervention")
                                
                                
   
    def to_json(self):
        return {
            'id': self.id,
            'name':                 self.name,
            '_internal' : self.get_internal(),
            'place_uuid': self.place_uuid,
            'average_latitude': self.average_latitude,
            'average_longitude': self.average_longitude,
            'interventions':  [{"intervention": item.to_json()} for item in self.interventions] 
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'name':                 self.name,
            'place_uuid': self.place_uuid,
            'average_latitude': self.average_latitude,
            'average_longitude': self.average_longitude,
            # 'interventions':  [{"intervention": item.to_json_light()} for item in self.interventions] 
        }


from sqlalchemy import event
@event.listens_for(Place, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
