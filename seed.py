import csv, sys

from flask import Flask, session, g
import model
from model import User, Burrito, Burrito_Attribute, Question, User_Choice, Choice, Restaurant
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
			
			add_object = get_or_create(model.session, model.Burrito, diet=lines[4], restaurant_id=r[0].id)
			model.session.add(add_object)

			add_bur_attribute = get_or_create(model.session, model.Burrito_Attribute, name=lines[0], 
				protien=lines[5], bean=lines[6], rice=lines[7], monies=lines[8], spicy=lines[9], 
				size=lines[10],structure=lines[11], special=lines[12], exotic=lines[13], 
				self_sum=lines[14], burrito_id=add_object.id)
			# print add_bur_attribute
			model.session.add(add_bur_attribute)

		model.session.commit()	

def import_questions(session):
	with open('Questions.csv', 'rb') as csvfile:
		table_reader = csv.reader(csvfile, delimiter=',')
		header_line = table_reader.next()

		for lines in table_reader:
			add_questions = get_or_create(model.session, model.Question, text=lines[0], category=lines[1])
			print add_questions.text
			model.session.add(add_questions)	

def main(session):
	# import_restaurant(session)
	# import_burrito(session)
	import_questions(session)


if __name__ == "__main__":
    s= model.connect()
    main(s)