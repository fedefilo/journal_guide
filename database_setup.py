# configuracion

import sys

from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# crear tablas

# una clase por tabla, 
# con las columnas como atributos

class Disciplines(Base):
	__tablename__ = 'disciplines'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)


class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)	
	first_name = Column(String(100), nullable = False)
	last_name = Column(String(100), nullable = False)
	email = Column(String(100), nullable = False)
	picture = Column(String(100))
	

class Journals(Base):
	__tablename__ = 'journals'
	id = Column(Integer, primary_key = True)	
	title = Column(String(100), nullable = False)
	issn = Column(String(9), nullable = False)
	publisher = Column(String(250))
	chief_editor = Column(String(80))
	issues_per_year = Column(Integer)
	foundation_year = Column(Integer)
	description = Column(String(250))
	picture = Column(String(100))
	user_id = Column(Integer, ForeignKey('users.id'))
	discipline_id = Column(Integer, ForeignKey('disciplines.id'))	
	disciplines = relationship(Disciplines)
	users = relationship(Users)


## final

engine = create_engine('sqlite:///journals.db')

Base.metadata.create_all(engine)

