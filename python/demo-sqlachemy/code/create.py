# -*- coding: UTF-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Character(Base):
	__tablename__ = 'character'
	# Definimos las columnas de la tabla character
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)


class Game(Base):
	__tablename__ = 'game'
	# Definimos las columnas de la tabla game
	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	platform = Column(String(250), nullable=True)
	character_id = Column(Integer, ForeignKey('character.id'))  # Clave foránea
	main_character = relationship(Character)  # Relación

# Guardamos la base de datos, por comodidad, en sqlite
engine = create_engine('sqlite:///game_char.db')

# Creamos todas las tablas declaradas (El clásico CREATE TABLE de SQL)
Base.metadata.create_all(engine)