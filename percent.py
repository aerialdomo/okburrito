import model
from model import User, Burrito, Question, Answer, Choice

# remember that SQL Datatypes are INTEGERS!! NEED TO CHANGE TO DECIMAL!

# Category: Spicy
# "If I were a pokemon, I would be: " -pikachu -squirtle - charmander

#psuedo code .2
# opinion needs to get clicked via checkbox
# when opinion picked, needs to relate to -1 to 1
# insert opinion into db
# user needs to choose a weight, which spans 0-1 
# insert weight into database
# opinion * weight = score
# insert score into a Category in db
# Category needs to be displayed in bar graph

#pull question from questions table
#insert it into answers table with user_id, qestion_is and choice_id


# opinion = {'pikachu': 1,
# 		   'squirtle': 1,
# 		   'charmander': 1}

# get user_id via sessions instead of hard code
user_info = {'user_id':3, 'answer':1}
# opinion = [1]
# need to figure the decimal thing in database
# weight = [2, 1, 0]

def ask_question(session):
	#first get rows
	
	q_row = model.session.query(model.Question).all()
	#REMEMBER! q_row is a list
	for i in q_row:
		c_row = model.session.query(model.Choice).filter_by(question_id = i.id).all()
	# print 'Running through show_question'
	
	# q_row = session.query(model.Question).get(quid)
	# c_row = session.query(model.Choice).filter_by(question_id = q_row.id).all()
	# print q_row.text
	# # print 'TYPE', type(c_row)
	# for i in range(len(c_row)):
	# 	print c_row[i].text
	return (q_row, c_row)	

#need to call the db to insert my hard coded data
def insert_score(session, q_row, c_row):
	
	# update row with user info
	new_row = Answer(question_id = 'q_row.id', 
		#value will come in from radio button
		choice_id = 'c_row.id',
		# answer = 'c_weight',
		user_id=user_info['user_id'])
	print new_row
	#make new database row
	# session.add(new_row)
	# session.commit()

def main(session):
	# You'll call each of the load_* functions with the session as an argument
	ask_question(session)
	insert_score(session, q_row, c_row)


if __name__ == "__main__":
	s= model.connect()
	main(s)	


