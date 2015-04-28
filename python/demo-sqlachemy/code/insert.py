# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create import Base, Character, Game

engine = create_engine('sqlite:///game_char.db')
# Realizamos un binding de la clase Base para recuperar la instancia.
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# DBSession() establece todas las comunicaciones con la base de datos
# y representa una zona de "staging" para los objetos cargados en la sesión.
session = DBSession()

# Insertamos un nuevo personaje
new_char = Character(name='Snake')
session.add(new_char)
# Cualquier cambio hecho en los objetos de la sesión no serán persistentes
# hasta que llamemos al método commit del objeto sesión.
# En cualquier momento, podremos hacer rollback de los cambios con el método rollback
session.commit()

# Lo vinculamos a su juego
new_game = Game(name='Metal Gear Solid', main_character=new_char)
session.add(new_game)
session.commit()