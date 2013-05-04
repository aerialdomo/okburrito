import csv, sys

from flask import Flask, session, g
import model 

from model import User, Burrito, Question, User_Choice, Choice, Restaurant
from collections import namedtuple
#create an object
#add object to db???? session
#commit
def get_or_create(session, model_class, **kwargs):
	instance = model.session.query(model_class).filter_by(**kwargs).first()
	if instance:
		return instance
	else:
		#this creates a new model object
		instance = model_class(**kwargs)
		return instance	

def import_restaurant(session):

	with open('Hb_burrito.csv', 'rb') as csvfile:
		f = csv.reader(csvfile, delimiter=',')
		header_line = f.next()
		# print header_row
		# print f.read()
		# rest_reader = f.readlines()
		# print rest_reader
		for lines in f:
			add_object = get_or_create(model.session, model.Restaurant, name=lines[1], neighborhood=lines[2])
			# print add_object[1]
			# print add_object.name
			model.session.add(add_object)
		model.session.commit()

def import_burrito(session):
		
	with open('Hb_burrito.csv', 'rb') as csvfile:
		bu_reader = csv.reader(csvfile, delimiter=',')
		header_line = bu_reader.next()

		#how to insert restaurant id

		for lines in bu_reader:
			r= model.session.query(model.Restaurant).filter(model.Restaurant.name==lines[1]).all()
			# print "RESTURANT ID", r[0].id

			add_burrito = get_or_create(model.session, model.Burrito, diet=lines[4], name=lines[0], 
				protien=lines[5], bean=lines[6], rice=lines[7], monies=lines[8], spicy=lines[9], 
				size=lines[10],structure=lines[11], special=lines[12], exotic=lines[13], 
				self_sum=lines[14], image=lines[15], restaurant_id=lines[16])
			
			model.session.add(add_burrito)
			model.session.commit()
			

		model.session.commit()	 

def import_questions(session):
	Choice = namedtuple('Choice', ['text', 'score', 'qid'])
	choices = []
	with open('Choices.csv', 'rb') as csvfile:
		c_reader = csv.reader(csvfile, delimiter=',')
	 	header_line = c_reader.next()
	 	for lines in c_reader:
	 		choice = Choice(lines[0], int(lines[1]), int(lines[2]))
	 		choices.append(choice)

	with open('Questions.csv', 'rb') as csvfile:
		table_reader = csv.reader(csvfile, delimiter=',')
		header_line = table_reader.next()

		for lines in table_reader:
			question_obj = get_or_create(model.session,
									 model.Question,
									 id=lines[0],
									 text=lines[1],
									 category=lines[2])
			#print question[0].text
			model.session.add(question_obj)	
			model.session.commit()	

			#import pdb
			#pdb.set_trace()
			question_choices = [choice for choice in choices if choice.qid == question_obj.id]
			for choice in question_choices:
				choice_obj = get_or_create(model.session, 
										   model.Choice, 
										   text=choice.text, 
										   score=choice.score,
										   question_id=question_obj.id,
										   question=question_obj)
				model.session.add(choice_obj)
				model.session.commit()	


	# with open('Choices.csv', 'rb') as csvfile:	
	# 	c_reader = csv.reader(csvfile, delimiter=',')
	# 	header_line = c_reader.next()
	# 	# i think the code is barfing b/c of add_questions[lines].id, 
	# 	# need to write the query that pulls the question id properly
	# 	for lines in c_reader:
	# 		add_choices = get_or_create(model.session, model.Choice, text=lines[0], 
	# 			score=lines[1], question_id=add_questions[lines].id)
	# 		# print add_choices.text	
	# 		model.session.add(add_choices)	

	#model.session.commit()	

# def import_choices(session):

# 		model.session.commit()	

def main(session):
	import_restaurant(session)
	import_burrito(session)
	import_questions(session)
	# import_choices(session)


if __name__ == "__main__":
    s= model.connect()
    main(s)