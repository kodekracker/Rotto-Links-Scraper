#! /usr/bin/env python
# -*- coding : utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from settings import DATABASE_URI

# Create an engine that stores data file in the local directory's
engine = create_engine(DATABASE_URI)

# Define a Session class which will serve as a factory for new Session objects
Session = sessionmaker(bind=engine)

def create_db():
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    print DATABASE_URI
    Base.metadata.create_all(engine)
