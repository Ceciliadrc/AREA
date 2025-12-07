from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True) # nom technique
    display_name = Column(String) # nom affichage ex: "Google"

class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id")) # lien vers service
    name = Column(String, nullable=False) # nom de l'action

class Reaction(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    name = Column(String, nullable=False)  # nom de la reaction

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # nom donne pas l'utilisateur
    user_id = Column(Integer, ForeignKey("users.id")) # lien vers quel utilisateur possède cet AREA
    action_id = Column(Integer, ForeignKey("actions.id")) # l'action qui declenche
    reaction_id = Column(Integer, ForeignKey("reactions.id")) # reaction a executer

