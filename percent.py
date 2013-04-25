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

	max_cat_score = model.session.query(model.Question.category, func.count(Question.id)).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==uid).\
		group_by(model.Question.category).all()
	#currently getting total count of questions in category, which is also the max_cat_score
	#this is a list of tuples
	print 'Maximum Category Score:', max_cat_score[0], max_cat_score[1], max_cat_score[2]

	#what is User score?
	user_cat_score = model.session.query(model.Question.category, func.sum(Choice.score)).\
		filter(model.User_Choice.choice_id==model.Choice.id).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==uid).\
		group_by(model.Question.category).all()
		
	print'User_cat_score:',user_cat_score[0],user_cat_score[1],user_cat_score[2]

	
	
# def calc_percent(session):
# 	max_category_score= #pull from question db
# 	percent = total_score/max_category_score


def main(session):
	# You'll call each of the load_* functions with the session as an argument
	get_data(session)
	


if __name__ == "__main__":
	s= model.connect()
	main(s)	


