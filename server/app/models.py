from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True) # nom technique
    display_name = Column(String) # nom affichage ex: "Google"
    oauth_config = relationship("ServiceOauth", uselist=False, backref="service")

class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id")) # lien vers service
    name = Column(String, nullable=False) # nom de l'action
    description = Column(String)

class Reaction(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    name = Column(String, nullable=False)  # nom de la reaction
    description = Column(String)

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # nom donne pas l'utilisateur
    user_id = Column(Integer, ForeignKey("users.id")) # lien vers quel utilisateur possède cet AREA
    action_id = Column(Integer, ForeignKey("actions.id")) # l'action qui declenche
    reaction_id = Column(Integer, ForeignKey("reactions.id")) # reaction a executer
    parameters = Column(String, nullable=True)

class ServiceOauth(Base):
    __tablename__ = "service_oauth"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)

class UserOauth(Base):
    __tablename__ = "user_oauth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
