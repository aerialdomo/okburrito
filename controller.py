from flask import Flask, render_template, redirect, url_for, request, session, g, flash
import model 
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ok.db'
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
	new_user = model.User(screenname = request.form['screenname'], email = request.form['email'],
							password = request.form['password'], diet = request.form['diet'])
	#checks to see if this user is already in the db
	if new_user.screenname != model.User.screenname and new_user.email != model.User.email :
		model.session.add(new_user)
		model.session.commit()
		session['uid']=new_user.id
		return redirect('my_profile', )
	else:
		print "Duplicate screenname || email"	
		return redirect('login')

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
		#write a thing that says if no screenname found its ok, just redirect to signup
		if (form_screenname == row.screenname) and (form_password == row.password):
				session['uid'] = row.id
				return redirect(url_for('my_profile',))	
	#else dosen't work yet	
	except NoResultFound:
		# flash('User not found. How about you give me your soul?')
		print 'Error biatchs!'
		return render_template('/signup.html')

@app.route('/my_profile')
def my_profile():

	profile	= model.session.query(model.User).filter_by(id = session['uid']).all()
	print "This be my profile yo"
	return render_template('/my_profile.html', profile = profile)

@app.route('/question', methods=['POST'])
def insert_score():
	#first get row
	row = session.query(model.Question).get(1)
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


if __name__ == "__main__":
	app.run(debug = True)