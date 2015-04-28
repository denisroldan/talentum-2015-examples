# -*- coding: UTF-8 -*-
from create import Base, Character, Game
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///game_char.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Buscamos todos los personajes en la base de datos
session.query(Character).all()

# Obtenemos el primer personaje y mostramos su nombre
character = session.query(Character).first()
print character.name

# Buscamos aquellos juegos que contengan como personaje principal a nuestro personaje.
print session.query(Game).filter(Game.main_character == character).all()  # devuelve una queryset

# Obtenemos el primer juego que contiene a dicho personaje
game = session.query(Game).filter(Game.main_character == character).one()  # devuelve un objeto
# Lo mostramos por consola
print game.name