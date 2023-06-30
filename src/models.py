import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class   User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    suscription_date = Column(String(250), nullable=False)
    

    favorites = relationship("Favorites", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
            "suscription_date": self.suscription_date,
        }

class   Object(Base):
    __tablename__ = 'object'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    created = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    object_type = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'object',
        'polymorphic_on':object_type
    }
    def serialize(self):
        return {
            "id": self.id,
            "created": self.created,
            "name": self.name,
            "url": self.url,
            "object_type": self.object_type,
        }

class   Planet(Object):
    __tablename__ = 'planet'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, ForeignKey('object.id'), primary_key=True)
    climate = Column(String(250), nullable=False)
    diameter = Column(Integer, nullable=False)
    edited = Column(String(250), nullable=False)
    gravity = Column(Integer, nullable=False)
    orbital_period = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    residents = Column(String(250), nullable=False)
    rotation_period = Column(Integer, nullable=False)
    surface_water = Column(Integer, nullable=False)
    terrain = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'planet',
    }
    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            "name": self.name,
            "diameter": self.diameter,
            "edited": self.edited,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "residents": self.residents,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
        }

class   Character(Object):
    __tablename__ = 'character'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, ForeignKey('object.id'),primary_key=True)
    birth_year = Column(String(250), nullable=False)
    eye_color = Column(String(250), nullable=False)
    gender = Column(String(250), nullable=False)
    hair_color = Column(String(250), nullable=False)
    height = Column(Integer, nullable=False)
    homeworld = Column(String(250), nullable=False)
    mass = Column(Integer, nullable=False)
    skin_color = Column(String(250), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'character',
    }
    def serialize(self):
        return {
            "id": self.id,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "homeworld": self.homeworld,
            "mass": self.mass,
            "skin_color": self.skin_color,
        }


class Favorites(Base):
    __tablename__ = 'favorites'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    object_id = Column(Integer, ForeignKey('object.id'))
    objects = relationship(["Object"], )
    user = relationship("User", back_populates="favorites")

    def serialize(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "object_id": self.object_id,
    }
