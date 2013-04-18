#database .3 beta
#ok.db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, VARCHAR #DECIMAl!!!
#sqlalchemy session is a handle to interact with db
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

#no longer need to instantiate Session class
engine = create_engine("mysql://christinaliu@localhost/burrito", echo=False)
session = scoped_session(sessionmaker(bind=engine, 
									autocommit = False, 
									autoflush = False))


ENGINE = None
Session = None

# OMFG remember to type in column names to the python to sql magic 
# ie) u = models.User(nickname='john', email='john@email.com')
Base = declarative_base()
# Base.metadata.create_all(engine)
Base.query = session.query_property()

class User(Base):
	__tablename__='users'

	id = Column(Integer, primary_key=True) 
	screenname = Column(String(64), nullable=False)
	email = Column(String(64), nullable=False)
	password = Column(String(64), nullable=False)
	diet = Column(String(64), nullable=True)
	# image 
	# location = Column(String(64), nullable=True)

class Resturant(Base):
	__tablename__='resturants'
	id = Column(Integer, primary_key=True)
	name = Column(String(56))
	neighborhood = Column(String(56)) 
	#image

class Burrito(Base):
	__tablename__='burritos'

	id = Column(Integer, primary_key=True) 
	diet = Column(String(64), nullable=True)
	resturant = Column(String(64), nullable=True)
	self_sum = Column(String(256), nullable=True)
	resturant_id = Column(Integer, ForeignKey('resturants.id'))

	image = Column(VARCHAR(512))
	resturant = relationship('Resturant', backref=backref('resturants'), order_by=id)

class Burrito_Attribute(Base):
	__tablename__='burrito_attributes'

	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	monies = Column(Integer, nullable=False)
	spicy = Column(Integer)
	# structure = Column(Integer)
	# exotic = Column(Integer)
	# size = Column(Integer)
	# meat = Column(String(64), nullable=True)

class Question(Base):	
	__tablename__='questions'

	id = Column(Integer, primary_key=True)
	q_id = Column(Integer)
	text = Column(String(256))
	category = Column(String(64))

class Choice(Base):
	__tablename__='choices'

	id = Column(Integer, primary_key=True)
	text = Column(String(256))
	score = Column(Integer) #(1, 0, -1)
	question_id = Column(Integer, ForeignKey('questions.id'))
	
	question = relationship('Question', backref=backref('choices'), order_by=id)

class User_Choice(Base): 
	__tablename__='user_choices'

	id = Column(Integer, primary_key=True)	
	# weight = Column(Integer)#Decimal(5,2) leave out atm for simplicity
	# score = Column(Integer)#Decimal(2,2)	
	question_id= Column(Integer, ForeignKey('questions.id'))
	choice_id = Column(Integer, ForeignKey('choices.id'))
	user_id = Column(Integer, ForeignKey('users.id'))

	choice = relationship('Choice', backref=backref('user_choices'), order_by=id)
	question = relationship('Question', backref=backref('user_choices'), order_by=id)
	user = relationship('User', backref=backref('user_choices'), order_by=id)

	
def connect():
	global ENGINE
	global Session

	ENGINE = create_engine('sqlite:///ok.db', echo = True)	
	#Session is a class generated by sqlalchemy, using sessionmaker
	Session = sessionmaker(bind=ENGINE)

	return Session()


def main():
   
    session = connect()

if __name__ == "__main__":
    main()