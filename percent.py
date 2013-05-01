from flask import Flask, session, g
import model
from model import User, Burrito, Question, User_Choice, Choice, Restaurant
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from controller import *


def get_data(session):
	#Get all question that have been answered
	max_cat_score = model.session.query(model.Question.category, func.count(Question.id)).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==session['uid']).\
		group_by(model.Question.category).all()

	#what is User score?
	user_cat_score = model.session.query(model.Question.category, func.sum(Choice.score)).\
		filter(model.User_Choice.choice_id==model.Choice.id).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==session['uid']).\
		group_by(model.Question.category).all()
		
	user_percent = []
	fields = []
	score_dict={}
	for idx in range(len(user_cat_score)):
		score = user_cat_score[idx][1]/max_cat_score[idx][1]
		fields.append(user_cat_score[idx][0])
		user_percent.append(score)
		score_dict = dict(zip(fields, user_percent))
	
	return score_dict

def matcher(session, score_dict):

	user_diet = model.session.query(model.User).filter_by(id=session['uid']).one()
	burrito = model.session.query(model.Burrito).filter_by(diet=user_diet.diet).all()

	burritrows = []
	error_rate = .30
	burrito_max = 5
	for idx in range(len(burrito)):
		counter = 0

		monies_percent = float(burrito[idx].monies) / burrito_max
		spicy_percent = float(burrito[idx].spicy) / burrito_max
		size_percent = float(burrito[idx].size) / burrito_max
		structure_percent = float(burrito[idx].structure) / burrito_max

		if (score_dict['monies'] >= (monies_percent - error_rate)) and (score_dict['monies'] <= (monies_percent +error_rate)):
			counter += 1
		if (score_dict['spicy'] >= (spicy_percent - error_rate)) and (score_dict['spicy'] <= (spicy_percent +error_rate)):
			counter += 1
		if (score_dict['size'] >= (size_percent - error_rate)) and (score_dict['size'] <= (size_percent + error_rate)):
			counter += 1
		if (score_dict['structure'] >= (structure_percent - error_rate)) and (score_dict['structure'] <= (structure_percent + error_rate)): 		
			counter += 1
	
		if counter >= 2:
			burritrows.append(burrito[idx])

	return burritrows

def main(session):
	# You'll call each of the load_* functions with the session as an argument
	score_dict = get_data(session)
	matcher(session, score_dict)


if __name__ == "__main__":
	s= model.connect()
	main(s)	


