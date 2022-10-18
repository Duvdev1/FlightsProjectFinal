from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# user-name: postgres
# password: admin
# database: flights_db


config = ConfigParser()
config.read("config2.conf")
connection_string = config["db"]["connection_string"]

Base = declarative_base()

engine = create_engine(connection_string, echo=True)

Session = sessionmaker()

local_session = Session(bind=engine)


def create_all_entities():
    Base.metadata.create_all(engine)
