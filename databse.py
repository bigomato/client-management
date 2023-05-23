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
# from sqlalchemy.schema import CreateTable

# # get creation sql for the tables
# with open("database.sql", "w") as f:
#     for table in Base.metadata.sorted_tables:
#         copiled = CreateTable(table).compile(engine)
#         f.write(str(copiled) + "\n\n")
