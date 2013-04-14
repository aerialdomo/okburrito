import model
from model import User, Burrito, Question

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


# opinion = {'pikachu': 1,
# 		   'squirtle': 1,
# 		   'charmander': 1}

# get user_id via sessions instead of hard code
user_info = {'user_id':1, 'answer':1}
# opinion = [1]
# need to figure the decimal thing in database
# weight = [2, 1, 0]

#need to call the db to insert my hard coded data
def insert_score(session):
	#first get row
	row = session.query(model.Question).get(2)
	#update row with user info
	new_row = Question(q_id=row.q_id, 
		text = row.text,
		category = row.category,
		user_id=user_info['user_id'], 
		answer = user_info['answer'])
	#make new database row
	session.add(new_row)
	session.commit()

def main(session):
	# You'll call each of the load_* functions with the session as an argument
  insert_score(session)


if __name__ == "__main__":
	s= model.connect()
	main(s)	


