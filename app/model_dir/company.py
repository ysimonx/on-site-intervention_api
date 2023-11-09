from .. import db
from .mymixin import MyMixin
from sqlalchemy.orm import declarative_base, relationship, backref


class Company(db.Model, MyMixin):
    __tablename__ = 'companies'
   
    users   = relationship("User",   
                            cascade="all, delete", 
                            backref=backref("users",lazy="joined")
                            )
    
    def to_json(self):
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':     self.name,
            'users':  [{"user": item.to_json_light()} for item in self.users] 
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
@event.listens_for(Company, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)

