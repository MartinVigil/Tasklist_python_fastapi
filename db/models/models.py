from sqlalchemy import ForeignKey, Column, String,Integer,Boolean
from sqlalchemy.ext.declarative import declarative_base
from db.client import SessionLocal

Base = declarative_base()


class User(Base):
    __tablename__ = 'usuarios'

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    user = Column('user',String)
    disabled = Column('disabled',Boolean)
    hashed_password = Column('hashed_password',String)

class Task(Base):
    __tablename__ = 'tasks'   

    id = Column('id',Integer,primary_key=True,autoincrement=True)     
    task = Column('task',String)
    fk_user = Column('fk_user',Integer,ForeignKey('usuarios.id'))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

       
    
         

