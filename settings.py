import configparser
import typing
import enum
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, Enum


config = configparser.ConfigParser()
config.read("config.ini")
config_root = config["admin"]
password = config_root["password"]
config_jwt = config["jwt"]
SECRET = config_jwt["secret"]
# utilisateur admin est un compte mysql avec une limitation des privilèges sur 
# la BD epic_events(select, insert, update et delete)
ENGINE = create_engine(
    f"mysql+pymysql://admin:{password}@localhost/epic_events", echo=False
)
Session = sessionmaker(bind=ENGINE)
SESSION = Session()


class Base(DeclarativeBase):
    type_annotation_map = {
        enum.Enum: Enum(enum.Enum),
        typing.Literal: Enum(enum.Enum),
    }
