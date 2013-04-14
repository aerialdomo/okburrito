from flask import Flask, render_template, redirect, url_for, request, session, g
import model
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ok.db'
db = SQLAlchemy(app)
app.secret_key = 'stuff'

@app.route('/')
def index():
	return "FooF"

@app.route('/signup', methods=['POST'])
def  signup():
	pass

@app.route('/login')
def login():
	return	render_template('/login.html',)

@app.route('/authenticate', methods=['POST'])
def authenticate():
	form_screenname = request.form['screenname']
	form_password = request.form['password']
	#querying row from db so that we can compare form data to existing data
	row = model.session.query(model.User).filter_by(screenname = form_screenname).one()
	if (form_screenname == row.screenname) and (form_password == row.password):
		session['uid'] = row.id
		return redirect(url_for('my_profile',))	
	else:
		return 'Foof'	

@app.route('/my_profile')
def my_profile():
	uid = session['uid']
	profile	= model.session.query(model.User).filter_by(id = session['uid']).all()
	print "This be my profile yo"
	return render_template('/my_profile.html', profile = profile)

@app.route('/question')
def show_question():	
	question_list = model.session.query(model.Question).all()
	return render_template('/question.html', question_list = question_list)


if __name__ == "__main__":
	app.run(debug = True)