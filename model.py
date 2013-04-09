#database .1 beta 
#ok.db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Decimal
from sqlalchemy.orm import sessionmaker, scoped_session

Engine = None
Session = None

engine = create_engine(#POSTGRES)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True) 
	screenname = Column(String(64), nullable=False)
	email = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)
	diet = Column(String(64), nullable=True)
	location = Column(String(64), nullable=True)

class Burrito(Base):
	__tablename__='burritos'

	id = Column(Integer, primary_key=True) 
	diet = Column(String(64), nullable=True)
	resturant = Column(Sting(64), nullable=True)
	self_sum = Column(String(256), nullable=True)
	monies = Column(String(64), nullable=False) #or do i want this to be a number
	spicy = Column(Integer)
	structure = Column(Integer)
	exotic = Column(Integer)
	size = Column(Integer)
	meat = Column(String(64), nullable=True)

class Question(Base):	
	__tablename__='questions'

	id = Column(Integer, primary_key=True)
	q_id = Column(Integer)
	score = Column(Decimal(5,2))
	weight = Column(Decimal(2,2))
	user_id = Column(Integer)
	burrito_id = Column(Integer)

def main():
	global ENGINE
	global Session

	Engine = create_engine(#POSTGRES)
	Session = sessionmaker(bind = ENGINE)

if __name__ == '__main__':
	main()	