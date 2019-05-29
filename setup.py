import watson_developer_cloud
import random
from Global import Global as g
from Connector import Connector as c
from Details import Details as d
from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField,SelectField
from passlib.hash import sha256_crypt
from functools import wraps
import Scraping,os,wolframalpha
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Sanyog:Sanyog10@jarviscluster-inwgn.mongodb.net/test?retryWrites=true")

db = client.get_database('Jarvis')
records = db.ChatLog

wolfalpha = wolframalpha.Client("UPRE9P-WPWWUHQGEH")

app = Flask(__name__)
app.secret_key= os.urandom(5)
CORS(app)


# Config MySQL
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'LpPJcmW4ti'
app.config['MYSQL_PASSWORD'] = 'jWPEOTGee7'
app.config['MYSQL_DB'] = 'LpPJcmW4ti'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

service = watson_developer_cloud.AssistantV2(
	username = d.username, 
	password = d.password,
	version = d.version
)
assistant_id = d.assistant_id

def createSession():
	global assistant_id
	g.session_id = service.create_session(
    	assistant_id = assistant_id
    	).get_result()['session_id']

	g.init_response = service.message(
		assistant_id,
		g.session_id,
		input = {
			'text': '',
			'options': {
				'return_context': True
			}
		},
	).get_result()

sec_q=[("phone no.","Which phone number do you remember most from your childhood?"),("place","What was your favorite place to visit as a child?"),("celib","Who is your favorite actor, musician, or artist?"),("pet","What is the name of your favorite pet?"),("city","In what city were you born?"),("high school","What high school did you attend?"),("first school","What is the name of your first school?"),("movie","What is your favorite movie?"),("maiden","What is your mother's maiden name?")]

# games
@app.route('/games/<string:id>/')
def games(id):
	gm = "games/"+str(id)+".html"
	return render_template(gm)


# @app.route('/g_sequence')
# def g_sequence():
#     return render_template('g_sequence.html')

# @app.route('/g_upbeat')
# def g_upbeat():
#     return render_template('g_up-beat.html')

# # games
# @app.route('/g_poll')
# def g_poll():
#     return render_template('g_poll.html')


# # games
# @app.route('/g_bloxorz')
# def g_bloxorz():
#     return render_template('g_bloxorz.html')




@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chatlog/<string:id>')
def ChatLogId(id):
	for ele in g.resultatlas:
		if ele['_id'] == id:
			# ele['Chat']
			pass


@app.route('/chatlog')
def chatlog():
	trim = []
	sub = {}
	for ele in g.resultatlas:
		if ele['date']:
			sub['_id'] = ele['_id']
			sub['date'] = ele['date']
			trim.append(sub)
			sub = {}
	# Trim has data
	return render_template('chatlog.html')

# Register Form Class
class RegisterForm(Form):
    f_name = StringField(' Father Name', [validators.Length(min = 3, max=50,message="Invalid Name")])
    f_contact = IntegerField(' Father Contact No.')#,[validators.Length(min = 10, max=13,message="Enter valid Contact no.(10-13 digit)")])
    f_email = StringField(' Father Email Id', [validators.Email()])
    
    m_name = StringField(' Mother Name', [validators.Length(min = 3, max=50,message="Invalid Name")])
    m_contact = IntegerField(' Mother Contact No.')#,[validators.Length(min = 10, max=13,message="Enter valid Contact no.(10-13 digit)")])
    m_email = StringField(' Mother Email Id', [validators.Email()])
    
    username = StringField(' Username', [validators.DataRequired(),validators.Length(min=4, max=20)])
    password = PasswordField(' Password', [
        validators.Length(min=4, max=20),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField(' Confirm Password',[validators.DataRequired()])
    
    # Sec_Q = StringField('Security Question', [validators.Length(min=5, max=20)])
    Sec_A = StringField(' Security Answer', [validators.DataRequired(),validators.Length(min=4, max=20)])
    Sec_Q = SelectField(' Security Question', choices =sec_q)
    Address = TextAreaField(' Address',[validators.Length(min = 2,message="Enter Address")])
    
# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		f_name = form.f_name.data
		f_email = form.f_email.data
		f_contact = form.f_contact.data

		m_name = form.m_name.data
		m_email = form.m_email.data
		m_contact = form.m_contact.data

		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		Sec_Q = form.Sec_Q.data
		Sec_A = form.Sec_A.data

		Address =form.Address.data

		# Create cursor
		cur = mysql.connection.cursor()
		x = cur.execute("SELECT * FROM parent WHERE username = %s", [username])

		if x > 0:
		    error = "Username not available, please choose another"
		    return render_template('register.html',error = error,form=form)
		# Execute query
		cur.execute("INSERT INTO parent(`username`, `password`, `f_name`, `f_email`, `f_contact`, `m_name`, `m_email`, `m_contact`, `Sec_Q`, `Sec_A`,`address`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (username, password, f_name, f_email, f_contact, m_name, m_email, m_contact, Sec_Q, Sec_A,Address))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()

		flash('Registration Succefully, login to continue', 'success')

		return redirect(url_for('login'))
	else:
		if request.method == 'POST' and not form.validate():
			error = 'Some error occured'
			return render_template('register.html', form=form, error=error)
		return render_template('register.html', form=form)


# class ChildDetail(Form):
#     fname = StringField('First Name', [validators.Length(min =1, max=50)])
#     # lname = StringField('Last Name', [validators.Length(min =1, max=50)])
#     # #nickname = StringField('Nick Name', [validators.Length( max=50)])
#     # dob = DateTimeField('Birthday', format='%d/%m/%y')
#     # gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
#     # grade = SelectField('Grade', choices = [('KinderGarden'),('1st'),('2nd'),('3rd'),('4th'),('5th'),('6th'),('7th'),('8th'),('9th')])
# # User login

# @app.route('/childdetail', methods=['GET', 'POST'])
# def childdetail():
#     # render_template('childdetails.html')
#     form1 = ChildDetail(request.form)
#     if request.method == 'POST' and form.validate():
#         fname = form.fname.data
#         # lname = form.lname.data
#         # #nickname = form.nickname.data
#         # # dob = form.dob.data
#         # gender = form.gender.data
#         # grade = form.garde.data
#         return redirect(url_for('home')) 
#     return render_template('childdetails.html',form=form1)
# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        if len(username) == 0:
            error = 'Username is empty'
            return render_template('login.html', error=error)
        elif len(password_candidate) == 0:
            error = 'Password is empty'
            return render_template('login.html', error=error)
        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM parent WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(('chat'))
            else:
                error = 'Invalid Password'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
	log = {
	'username': session['username'],
	'date':g.startTime,
	'Chat': g.chatArr
	}
	records.insert_one(log)

	g.chatArr,g.startTime = [],''

	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


def tag_to_func(tag,response):
	switcher = {
		"Riddle" : askRiddle,
		"Defination" : giveDefine,
		"General_Jokes": tellJoke,
	}
	func = switcher.get(tag,False)
	if func:
		return func(response)

def tellJoke(response):
    respond= ['Do you want to hear another one?','How about one more?','Another joke?']
    c.mycursor.execute("SELECT * from jokes")
    result = c.mycursor.fetchall()
    num =random.sample(range(0,len(result)- 1), 2)
    response['context']['skills']['main skill']['user_defined']['answer'] = result[num[0]][0]
    g.res += result[num[1]][0]+ '$'
    i = random.randint(0,len(respond)-1)
    g.res += respond[i]
	
def solveMath(sentence):
	try:
		solve = wolfalpha.query(sentence)
		result = next(solve.results).text
		g.res += result + "$"
	except:
		g.res += "Brain is damaged did you ask correct question?" + '$'

def askRiddle(response):
	
	c.mycursor.execute("SELECT * from riddle")
	result = c.mycursor.fetchall()
	num = random.randint(0,len(result)-1)
	response['context']['skills']['main skill']['user_defined']['answer'] = result[num][1]
	g.res += result[num][0] +'$'

def giveDefine(response):

	respond= ['Did you understand champ?','Was this answer good enough','This is what i know, did you get the answer?']
	i = random.randint(0,len(respond)-1)
	if(response["output"]["entities"]):
		answer = Scraping.search( response )
		g.res += answer
		if (random.uniform(0,1) > 0.65):
			g.res += respond[i]


def appendChatLog(child,bot):
	chats = {'speaker': 'child','chat':child,'timestamp':datetime.now().strftime('%H:%M')}
	g.chatArr.append(chats)
	for _ in bot.split('$'):
		chats = {'speaker': 'Bot','chat':_,'timestamp':datetime.now().strftime('%H:%M')}
		g.chatArr.append(chats)

@app.route('/start')
def start():
	string = ''
	for text in g.init_response['output']['generic']: 
		string += text['text'] + '$'
	
	string_temp = string[:-1]
	
	for _ in string_temp.split('$'):
		chats = {'speaker': 'Bot','chat':_,'timestamp':datetime.now().strftime('%H:%M')}
		g.chatArr.append(chats)
	
	g.startTime = datetime.now().strftime('%d:%b:%Y %H:%M')

	return string_temp

@app.route('/conversation', methods = ['POST'])
def conversation():
	query = request.get_json()
	sentence = query['question']
	try:
		response = service.message(
			assistant_id,
			g.session_id,
			input = {
				'text': sentence,
				'options': {
					'return_context': True
				}
			},
			context = g.context
		).get_result()
	except:
		createSession()
		response = service.message(
			assistant_id,
			g.session_id,
			input = {
				'text': sentence,
				'options': {
					'return_context': True
				}
			},
			context = g.context
		).get_result()


	g.res = ""
	g.context = response['context']
	for ele in response['output']['generic']:
		if ele['response_type'] == 'text' and ele['text']:
			g.res += ele['text'] + '$'

	if(response["output"]["intents"]):
		tag_to_func(response["output"]["intents"][0]["intent"],response)
	
	if response['context']['skills']['main skill']['user_defined']['tag']:
		if response['context']['skills']['main skill']['user_defined']['tag'] == "maths":
			solveMath(sentence)
			response['context']['skills']['main skill']['user_defined']['tag'] = None
		if response['context']['skills']['main skill']['user_defined']['tag'] == "Task":
			for ele in response['output']['generic'][2]['options']:
				g.res += ele['label'] +"$"
				response['context']['skills']['main skill']['user_defined']['tag'] = None
	
	appendChatLog(sentence,g.res[:-1])
	return g.res[:-1]	

if __name__ == '__main__':

	app.run(debug = True)

	service.delete_session(
		assistant_id = assistant_id,
		session_id = g.session_id

	)
