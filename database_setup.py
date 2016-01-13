# Udacity Full Stack Web Developer Nanodegree
# Project 3 - Item catalog
# Journal Catalog App
# by Federico Vasen
# File with the Database Schema
# Dec 23, 2015


import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Create tables


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


class Disciplines(Base):
    __tablename__ = 'disciplines'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
        }


class Journals(Base):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    issn = Column(String(9), nullable=False)
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

    # Adds property for JSON output
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'issn': self.issn,
            'publisher': self.publisher,
            'editor_in_chief': self.chief_editor,
            'issues_per_year': self.issues_per_year,
            'foundation_year': self.foundation_year,
            'description': self.description,
            'discipline_id': self.discipline_id,
        }

# Final steps
engine = create_engine('sqlite:///journals.db')

Base.metadata.create_all(engine)
