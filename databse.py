from models import *
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

if os.path.exists("database.sqlite"):
    os.remove("database.sqlite")

# create an engine for the local sqlite database
engine = create_engine("sqlite:///database.sqlite")

# create all tables in the engine
Base.metadata.create_all(engine)

# create a session
Session = sessionmaker(bind=engine)
session = Session()
