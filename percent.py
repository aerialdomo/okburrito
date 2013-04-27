from flask import Flask, session, g
import model
from model import User, Burrito, Question, User_Choice, Choice, Restaurant
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
uid = 1

def get_data(session):
	#Get all question that have been answered

	max_cat_score = model.session.query(model.Question.category, func.count(Question.id)).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==uid).\
		group_by(model.Question.category).all()
	#currently getting total count of questions in category, which is also the max_cat_score
	#this is a list of tuples
	# print 'Maximum Category Score:', max_cat_score[0], max_cat_score[1], max_cat_score[2], max_cat_score[3]
	# print max_cat_score[0][0]

	#what is User score?
	user_cat_score = model.session.query(model.Question.category, func.sum(Choice.score)).\
		filter(model.User_Choice.choice_id==model.Choice.id).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==uid).\
		group_by(model.Question.category).all()
		
	# print'User_cat_score:',user_cat_score[0],user_cat_score[1],user_cat_score[2], user_cat_score[3]

	user_percent = []
	fields = []
	# score_dict={}
	for idx in range(len(user_cat_score)):
		# for inner_idx in range(len(idx)):
		score = user_cat_score[idx][1]/max_cat_score[idx][1]
		# print 'SCORE', user_cat_score[idx][0], 
		fields.append(user_cat_score[idx][0])
		user_percent.append(score)
		score_dict = dict(zip(fields, user_percent))
	return score_dict

def matcher(session, score_dict):
	#match burrito to user
	#get burrito number
	#do i need to turn it into a %
	#set user_percent == burrito percent

	burrito = model.session.query(model.Burrito_Attribute).all()

	for idx in range(len(burrito)): 
		b_percent = float(burrito[idx].spicy)/5
		if score_dict['spicy']<= b_percent - .2 and score_dict>= b_percent +.2:
			print burrito[idx].name
		


	# print score_dict



def main(session):
	# You'll call each of the load_* functions with the session as an argument
	score_dict = get_data(session)
	matcher(session, score_dict)


	


if __name__ == "__main__":
	s= model.connect()
	main(s)	


