from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

Engine = create_engine('sqlite:///gym.sqlite3')

Base.metadata.create_all(Engine)

Session = sessionmaker(bind=Engine)
session = Session()

def get_session():
    return session