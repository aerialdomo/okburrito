from flask import Flask, session, g
import model
from model import User, Burrito, Question, User_Choice, Choice, Resturant
from sqlalchemy.sql import func


#psuedo code .2
# opinion needs to get clicked via checkbox
# when opinion picked, needs to relate to -1 to 1
# insert opinion into db
# user needs to choose a weight, which spans 0-1 
# insert weight into database
# opinion * weight = score
# insert score into a Category in db
# Category needs to be displayed in bar graph

# opinion = {'pikachu': 1,
# 		   'squirtle': 1,
# 		   'charmander': 1}

# get user_id via sessions instead of hard code
user_info = {'user_id':3, 'answer':1}

# Braining-
# 	- burrito score goes in chuncks of 20's to get 100%
# 	- user data can then be a percentage, 
# 		- if 100% of 1 q is 100%, then what is 100% of 10 qs
# 		- 
# 	- match percentage
uid = 2

def get_data(session):
	#Get all question that have been answered

	q_answered = model.session.query(model.Question.category, func.count('*')).\
				filter(model.User_Choice.question_id==model.Question.id).\
				filter(model.User_Choice.user_id==uid).\
				group_by(model.Question.category).all()
	#currently getting total count of questions in category
	print q_answered		
	
	# q_answered = model.session.query(model.User_Choice).filter_by(user_id=uid).all()
	# print "LENGTH", len(q_answered)
	# for idx in range(len(q_answered)):
	# 	print 'question_id:', q_answered[idx].question_id, "User_ID:", q_answered[idx].user_id
	# 	print q_answered[idx].question.text
	# 	print q_answered[idx].choice.text
	# 	print q_answered[idx].choice.score
	# 	print q_answered[idx].question.category


	# 	q_category = model.session.query(model.Question).group_by(model.Question.category).all()
	# 	print "TROUBLE", type(q_category), q_category[idx].category


# def calc_percent(session):
# 	max_category_score= #pull from question db
# 	percent = total_score/max_category_score

def main(session):
	# You'll call each of the load_* functions with the session as an argument
	get_data(session)
	


if __name__ == "__main__":
	s= model.connect()
	main(s)	


