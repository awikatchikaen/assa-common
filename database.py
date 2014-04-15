'''
Created on 8 avr. 2014

@author: fcs
'''
import os

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property, backref
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String, Boolean


Base = declarative_base()


    
class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    code = Column(String(50))
    type = Column(Integer)
    parent_id = Column(Integer, ForeignKey('location.id'))
    children = relationship("Location",
                backref=backref('parent', remote_side=[id]))
    
criteria_location = Table('criteria_location', Base.metadata,
    Column('location_id', Integer, ForeignKey('location.id')),
    Column('criteria_id', Integer, ForeignKey('criteria.id'))
)    


class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    config = Column(String(250))
    type = Column(String(50))
    success = Column(Integer, ForeignKey('action.id'))
    failure = Column(Integer, ForeignKey('action.id'))
    criteria_id = Column(Integer, ForeignKey('criteria.id'))
   


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
   
criteria_site = Table('criteria_site', Base.metadata,
    Column('site_id', Integer, ForeignKey('site.id')),
    Column('criteria_id', Integer, ForeignKey('criteria.id'))
)  

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
   
criteria_category = Table('criteria_category', Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id')),
    Column('criteria_id', Integer, ForeignKey('criteria.id'))
)  

class Criteria(Base):
    __tablename__ = 'criteria'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    name = Column(String(50))
    query = Column(String(120))
    
    #post_code = Column(String(250), nullable=False)
    #prices = column_property()
    
    #person = relationship(Person)
    locations = relationship("Location", secondary=criteria_location)
    sites = relationship("Site", secondary=criteria_site)
    categories = relationship("Category", secondary=criteria_category)
    categories = relationship("Category", secondary=criteria_category)
    action = relationship("Action", uselist=False, backref="criteria")
    #TODO : deplacer vers la table Search
    #site = Column(String(50))
    #site = Column('user_id', Integer, ForeignKey('users.user_id')),
    #self.actions=[]
    
    price_min = Column(Integer)
    price_max = Column(Integer)
    
    @property
    def prices(self):
        return {'min':self.price_min,'max':self.price_max}

def createCategories(session):
    session.add(Category(id=0,name="velo"))
    session.add(Category(id=1,name="venteImmo"))
    session.add(Category(id=2,name="electromenager"))
    session.add(Category(id=3,name="jeux"))
    session.add(Category(id=4,name="equipementBebe"))
    session.add(Category(id=5,name="equipementMoto"))
    session.add(Category(id=6,name="ameublement"))
    session.add(Category(id=7,name="equipementAuto"))
    session.add(Category(id=8,name="deco"))
    session.add(Category(id=9,name="jardinage"))
    session.add(Category(id=10,name="photo"))
    session.add(Category(id=11,name="informatique"))
    session.commit()

def createLocation(session):
    pibrac = Location(name='Pibrac', type='town')
    gragnague = Location(name='Gragnague', type='town')
    haute_garonne = Location(name='haute_garonne',code='haute_garonne', type='departement', children=[pibrac, gragnague])
    MI_PI = Location(name='midi_pyrenees',code='midi_pyrenees', type='region',children=[haute_garonne])
    session.add(MI_PI)
    
def createSites(session):
    LBC = Site(name='LBC')
    session.add(LBC)
    
def createTestDatas(session):
    mail = Action(config="{'mailadress':'awikatchikaen@free.fr'}", type="Mailer")
    push = Action(type="Pushover")
    
    c1 = Criteria(name="test search",
                      sites=[session.query(Site).filter_by(name='LBC').one()],
                      #locations=[session.query(Location).filter_by(name='Pibrac').one(),session.query(Location).filter_by(name='Gragnague').one()],
                      locations=[session.query(Location).filter_by(name='Pibrac').one()],
                      price_min=10,
                      price_max=90000,
                      categories=[session.query(Category).filter_by(name='venteImmo').one()],
                      query="Terrain",
                      action=push
                      );

    session.add(c1)
    
    
if __name__ == '__main__':
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    if os.path.exists("C:\Windows\Temp\sqlalchemy_example.db"):
        os.remove("C:\Windows\Temp\sqlalchemy_example.db")
        
    db = create_engine('sqlite:///C:\Windows\Temp\sqlalchemy_example.db')
    
    #engine = create_engine('sqlite', opts={'filename': 'C:\\Windows\\Temp\\sqlalchemy_example.db'})
     
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(db)
    
    Base.metadata.bind = db
 
    DBSession = sessionmaker(bind=db)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()
    createCategories(session)
    createLocation(session)
    createSites(session)
    createTestDatas(session)
    

    
    session.commit()
    