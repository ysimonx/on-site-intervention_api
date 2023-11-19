from .. import db
from .mymixin import MyMixin
from sqlalchemy.orm import declarative_base, relationship, backref


class Role(db.Model, MyMixin):
    __tablename__ = 'roles'
   
   
    def to_json(self):
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':     self.name,
        }

    def to_json_light(self):
        return {
            'id':               self.id,
            'name':             self.name
        }
        
    def to_json_anonymous(self):
        return {
            'id':               self.id,
        }


from sqlalchemy import event
@event.listens_for(Role, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)

