from flask import Flask, render_template, redirect, url_for, request, session, g, flash
import model 
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://christinaliu@localhost/burrito"
db = SQLAlchemy(app)
app.secret_key = 'stuff'

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
	#?????????????????????
	check = model.session.query(model.User).filter_by(screenname = new_user.screenname, 
														email=new_user.email).all()
	# sn_check = model.session.query(model.User).filter_by(screenname=new_user.screenname).all()
	# e_check = model.session.query(model.User).filter_by(email=new_user.email).all()

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

	profile	= model.session.query(model.User).filter_by(id = session['uid']).all()
	print "This be my profile yo"
	return render_template('/my_profile.html', profile = profile)

@app.route('/show_question') #this is a GET request
def show_question():
	q_row = model.session.query(model.Question).all()
	#REMEMBER! q_row is a list
	#i need responses list to glom the c_row results together to pass into html
	# question= []
	responses = []
	for i in q_row:
		print i.text
		# question.append(q_row)
		# question = range(len(question))
		# print question
		c_row = model.session.query(model.Choice).filter_by(question_id = i.id).all()
		# print 'xxxxxxxxxxxxxxxxxxx',type(c_row), c_row
		responses.append(c_row)
		for j in range(len(c_row)):
			choice = c_row[j]
			# print type(choice)
			print c_row[j].text
			# print 'Running through show_question'
	return render_template('/question.html', responses=responses, q_row = q_row)

@app.route('/question', methods=['POST'])
def insert_score():
	#first get row
	row = model.session.query(model.Question).all()
	user_id = session['uid']
	#update row with user info
	new_row = Question(q_id=row.q_id, 
		text = row.text,
		category = row.category,
		user_id=session['uid'], 
		answer = answer)
	#make new database row
	session.add(new_row)
	session.commit()	
	return render_template('/question.html', new_row=question_list)

@app.route('/all_sexy_burrito')
def all_sexy_burrito():
	b_row = model.session.query(model.Burrito).all()
	return render_template('/all_sexy_burrito.html', burritrows=b_row) 

#id is included as part of hte url
@app.route('/one_sexy_burrito/<int:id>')
def one_sexy_burrito(id):
	sexy_b = model.session.query(model.Burrito).get(id)
	print 'vvvvvvvv', sexy_b.self_sum
	return render_template('/one_sexy_burrito.html', sexy_b=sexy_b)

if __name__ == "__main__":
	app.run(debug = True)