from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///your_database.db',connect_args= {'check_same_thread':False})
sessionLocal = sessionmaker(bind= engine, autoflush= False, autocommit = False)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()