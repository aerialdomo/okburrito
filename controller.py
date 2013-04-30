from flask import Flask, render_template, redirect, url_for, request, session, g, flash
#figure out what the g is for
from flaskext.gravatar import Gravatar 
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound


import model 
# from model import Burrito_Attribute

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://christinaliu@127.0.0.1/burrito"
db = SQLAlchemy(app)
app.secret_key = 'stuff'

def get_or_create(session, model_class, **kwargs):
	instance = model.session.query(model_class).filter_by(**kwargs).first()
	if instance:
		return instance
	else:
		#this creates a new model object
		instance = model_class(**kwargs)
		return instance	

@app.route('/')
def index():
	return "FooF"

@app.route('/signup.html')
def  signup():
	return render_template('/signup.html')

@app.route('/signup', methods=['POST'])	
def create_user():
	# pull query from db to see if this use exists
	# use if statements
	new_user = model.User(screenname = request.form['screenname'], email = request.form['email'],
							password = request.form['password'], diet = request.form['diet'])
	#is this query right for matching screenname or email???
	check = model.session.query(model.User).filter_by(screenname = new_user.screenname, 
														email=new_user.email).all()

	#check is a list, need check[0].screenname, check[0].email to access info in rows
	for i in range(len(check)):
		if new_user.screenname == check[i].screenname or new_user.email == check[i].email:
			#checks to see if this user is already in the 
			print "Duplicate screenname || email"	
			return redirect('login',)
			
	print 'things are A-OK'
	model.session.add(new_user)
	model.session.commit()
	session['uid']=new_user.id
	return redirect('my_profile', )
			
@app.route('/login')
def login():
	return	render_template('/login.html',)

@app.route('/logout')
def logout():
	session.pop('uid', None)
	#flash is not working!
	# flash('You were logged out')
	return redirect(url_for('login'))	

@app.route('/authenticate', methods=['POST'])
def authenticate():
	form_screenname = request.form['screenname']
	form_password = request.form['password']
	#checks to see if user even exists in db
	try:
		#querying row from db so that we can compare form data to existing data
		row = model.session.query(model.User).filter_by(screenname = form_screenname).one()
		if (form_screenname == row.screenname) and (form_password == row.password):
				session['uid'] = row.id
				return redirect(url_for('my_profile',))	
	except NoResultFound:
		flash('User not found. How about you give me your soul?')
		print 'Error, such poor unfortunate souls. In Pain! In Need!'
		return render_template('/signup.html')
	
	print 'Something has gone horribly wrong with authenticate!!!!!'	
	return	redirect('/')

@app.route('/my_profile')
def my_profile():

	profile	= model.session.query(model.User).filter_by(id=session['uid']).all()
	print "This be my profile yo"

	gravatar = Gravatar(app, 
						size=100)

	return render_template('/my_profile.html', profile=profile)

@app.route('/show_question') #this is a GET request
def show_question():
	q_row = model.session.query(model.Question).all()
	#REMEMBER! q_row is a list.
	# I need responses list to glom the c_row results together to pass into html.
	responses = []
	for i in q_row:
		print i.text
		c_row = model.session.query(model.Choice).filter_by(question_id=i.id).all()
		responses.append(c_row)
		# Created idx_c_row for for loop optimization.
		idx_c_row  = range(len(c_row))
		for j in idx_c_row:
			print c_row[j].text
	return render_template('/question.html', responses=responses, q_row=q_row)

#update answers REST api
@app.route('/insert_score', methods=['POST'])
#def update_answers()
def insert_score():
	# interitems() turns the immutable multidict into a something that is iterable
	for question_id, answer_id in request.form.iteritems():
		answer = get_or_create(model.session, model.User_Choice, question_id=question_id, user_id=session['uid'])  
		# import pdb   <--- Awesome debugger!!!
		# pdb.set_trace
		answer.choice_id = answer_id
		# adding entire answer object
		model.session.add(answer)
		model.session.commit()	
	return redirect('/')


def calculate_score():

	#Get all question that have been answered

	max_cat_score = model.session.query(model.Question.category, func.count(Question.id)).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==uid).\
		group_by(model.Question.category).all()
	#currently getting total count of questions in category, which is also the max_cat_score
	#this is a list of tuples
	print 'Maximum Category Score:', max_cat_score[0], max_cat_score[1], max_cat_score[2], max_cat_score[3]
	# print max_cat_score[0][0]

	#what is User score?
	user_cat_score = model.session.query(model.Question.category, func.sum(Choice.score)).\
		filter(model.User_Choice.choice_id==model.Choice.id).\
		filter(model.User_Choice.question_id==model.Question.id).\
		filter(model.User_Choice.user_id==uid).\
		group_by(model.Question.category).all()
		
	print'User_cat_score:',user_cat_score[0],user_cat_score[1],user_cat_score[2], user_cat_score[3]

	for idx in range(len(user_cat_score)):
		# for inner_idx in range(len(idx)):
		user_percent = user_cat_score[idx][1]/max_cat_score[idx][1]
		# if user_percent
		print idx, user_percent 
 
@app.route('/all_sexy_burrito')
def all_sexy_burrito():
	#getting burrito id
	burritrows = model.session.query(model.Burrito).all()
	
	return render_template('/all_sexy_burrito.html', burritrows=burritrows)

# id is included as part of hte url.
@app.route('/one_sexy_burrito/<int:id>')
def one_sexy_burrito(id):
	sexy_burrito = model.session.query(model.Burrito).get(id)

	return render_template('/one_sexy_burrito.html', sexy_burrito=sexy_burrito)


if __name__ == "__main__":
	app.run(debug = True)