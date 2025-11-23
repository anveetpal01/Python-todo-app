# this file connects with database by using sqlalchemy

from sqlalchemy import create_engine # creates a connection engine that talks to your database.
from sqlalchemy.ext.declarative import declarative_base #create a base class that your models inherit from.
from sqlalchemy.orm import sessionmaker # creates a session class used to interact with the DB.

#using sqlite
'''
"sqlite:///./todo.db" - this is database connection url used by sqlalchemy
sqlite -> database engine we are using.
:// -> start of the URL and extra / ->means the database is a file on the local filesystem
./ -> relative path (current folder)
./todo.db -> . means current directory and todo.db is the database file that will be created/used.
'''
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# create engine / it starts database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# sessionLocal database de sath baat karne ka handle hai
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class jisse humare models inherit karenge
Base = declarative_base()