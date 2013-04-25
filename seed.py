import csv, sys

from flask import Flask, session, g
import model
from model import User, Burrito, Question, User_Choice, Choice, Restaurant
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

def import_resturant(session):

	with open('Hb_burrito.csv', 'rb') as csvfile:
		f = csv.reader(csvfile, delimiter=',')
		header_line = f.next()
		# print header_row
		# print f.read()
		# rest_reader = f.readlines()
		# print rest_reader
		for lines in f:
			add_object = get_or_create(model.session, model.Restaurant, name=lines[1], neighborhood=lines[2])
			# add_object = Resturant(name=lines[1], neighborhood=lines[2])
			# print add_object[1]
			# print add_object.name
			model.session.add(add_object)
		model.session.commit()

def import_burrito(session):
		
		with open('Hb_burrito.csv', 'rb') as csvfile:
		bu_reader = csv.reader(csvfile, delimiter=',')
		header_line = bu_reader.next()

		for lines in bu_reader:
			add_object = get_or_create

		


def main(session):
	import_resturant(session)


if __name__ == "__main__":
    s= model.connect()
    main(s)