import random,Scraping,os,wolframalpha,watson_developer_cloud,socket
from Global import Global as g
from Connector import Connector as c
from Details import Details as d
from flask import Flask, render_template, flash, redirect, url_for, session, request,Markup
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer,BadTimeSignature,SignatureExpired
from flask_cors import CORS
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField,SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from pymongo import MongoClient

socket.getaddrinfo('localhost', 8080)

client = MongoClient("mongodb+srv://Sanyog:Sanyog10@jarviscluster-inwgn.mongodb.net/test?retryWrites=true")

db = client.get_database('Jarvis')
records = db.ChatLog

wolfalpha = wolframalpha.Client("UPRE9P-WPWWUHQGEH")

app = Flask(__name__)
app.secret_key= os.urandom(5)
app.config.from_pyfile('config.cfg')
CORS(app)

mail = Mail(app)

emailKey = URLSafeTimedSerializer(app.config['SECRET_KEY'])


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


def sendMail(f_email,m_email,username):
	token = emailKey.dumps(username,salt = 'email-confirm')

	msg = Message('Verification Email',sender = 'jrjarvisverify@gmail.com',recipients = [f_email,m_email])
	link = url_for('confirm_email',token = token,_external = True)

	msg.body = """Thanks for registering on our website
	To login click the link below
	Click this link {}""".format(link)
	mail.send(msg)


def PassReset(f_email,m_email,username):
	token = emailKey.dumps(username,salt = 'email-confirm')
	msg = Message('Password Reset',sender = 'jrjarvisverify@gmail.com',recipients = [f_email,m_email])
	link = url_for('reset',token = token,_external = True)

	msg.body = """Click the link here to change the password {}""".format(link)
	mail.send(msg)	
# check login or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

def is_logged_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are already logged in', 'danger')
            return redirect(url_for('index'))
    return wrap

# games
@app.route('/games/<string:id>/')
@is_logged_in
def games(id):
	gm = "games/"+str(id)+".html"
	return render_template(gm)



@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/chat')
@is_logged_in
def chat():
    return render_template('chat.html')

# @app.route('/chatlog/<string:id>')
# @is_logged_in
# def ChatLogId(id):
# 	for ele in g.resultatlas:
# 		if ele['_id'] == id:
# 			chatlog = ele['Chat']
# 			return render_template('chatlog.html',chatlog=trim)		


@app.route('/chatlog')
@is_logged_in
def chatlog():
	logresult = records.find(filter = {'username': session['username']},batch_size = 10)
	sub = {}
	chat = []
	count = 1;
	# <li><a href="#section1">Section 1       12/11/18</a></li>
	for ele in logresult:
		if ele['date']:
			sub['id'] = count
			
			sub['date']=ele['date']
			sub['chat']=ele['Chat']
			# section = section + '<li><a href = #section'+str(count)+'>Section' +str(count)+ele['date']+'</a></li>' 
			count = count+1
			chat.append(sub)
			sub={}
	# section= Markup(section)
	chat=Markup(chat)
	return render_template('chatlog.html',chat =chat)


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
@is_logged_out
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
		cur.execute("INSERT INTO parent(`username`, `password`, `f_name`, `f_email`, `f_contact`, `m_name`, `m_email`, `m_contact`, `Sec_Q`, `Sec_A`,`address`,`verified`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,0)", (username, password, f_name, f_email, f_contact, m_name, m_email, m_contact, Sec_Q, Sec_A,Address))

		# Commit to DB
		mysql.connection.commit()

		# Close connection
		cur.close()
		
		sendMail(f_email,m_email,username)
		flash('Registration Succefully,Verify email within 30 min to login', 'success')
		return redirect(url_for('index'))
	else:
		if request.method == 'POST' and not form.validate():
			error = 'Some error occured'
			return render_template('register.html', form=form, error=error)
		return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
@is_logged_out
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
		data = cur.fetchone()
		if result > 0:
			# Get stored hash
			
			password = data['password']
			confirm = data['verified']
			if confirm:
				if sha256_crypt.verify(password_candidate, password):
					# Passed
					session['logged_in'] = True
					session['username'] = username
					createSession()

					flash('You are now logged in', 'success')
					return redirect(('chat'))
				else:
					error = 'Invalid Password'
					return render_template('login.html', error=error)
			else:
				#sendMail(data['f_email'],data['m_email'],username)
				error = 'Email not verified'
				return render_template('login.html', error=error)

			# Close connection
			cur.close()
		else:
			error = 'Username not found'
			return render_template('login.html', error=error)

	return render_template('login.html')

@app.route('/login/<string:token>')
def confirm_email(token):
	cur = mysql.connection.cursor()
	try:
		username = emailKey.loads(token, salt ='email-confirm', max_age = 3600)
	except SignatureExpired:
		result = cur.execute("SELECT f_email,m_email FROM parent WHERE username = %s", [username])
		cur.close()
		if result > 0:
			mails = cur.fetchone()
			sendMail(mails['f_email'],mails['m_email'],username)
		flash('Link has expired sending it again, Verify new link within 30 minutes','error')
		return redirect(url_for('home'))
	except BadTimeSignature:
		flash('Invalid link','error')
		return redirect(url_for('home'))
	cur.execute("UPDATE parent SET verified = 1 WHERE username = %s",[username])
	mysql.connection.commit()
	cur.close()
	flash('Linked verified login to continue', 'success')
	return redirect(url_for('login'))



# Logout
@app.route('/logout')
@is_logged_in
def logout():
	
	log = {
	'username': session['username'],
	'date':g.startTime,
	'Chat': g.chatArr
	}
	session.clear()
	records.insert_one(log)

	g.chatArr,g.startTime = [],''

	flash('You are now logged out', 'success')
	return redirect(url_for('login'))
# reset password
class resetpassword(Form):
	password = PasswordField(' Password', [
		validators.Length(min=4, max=20),
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField(' Confirm Password',[validators.DataRequired()])

@app.route('/resetMethod')
def resetMethod(name):
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT f_email,m_email FROM parent WHERE username = %s", [name])
	cur.close()
	if result > 0:
		mails = cur.fetchone()
		PassReset(mails['f_email'],mails['m_email'],name)

@app.route('/reset/<string:_id>')
@is_logged_out
def reset(_id):
	form = resetpassword(request.form)
	cur = mysql.connection.cursor()

	if request.method == 'POST' and form.validate():
		password = sha256_crypt.encrypt(str(form.password.data))
		try:
			username = emailKey.loads(_id, salt ='email-confirm', max_age = 300)
		except SignatureExpired:
			result = cur.execute("SELECT f_email,m_email FROM parent WHERE username = %s", [username])
			cur.close()
			if result > 0:
				mails = cur.fetchone()
				PassReset(mails['f_email'],mails['m_email'],username)
			flash('Link has expired, reset password with new link. Verify within 5 min.','error')
			return redirect(url_for('index'))
		except BadTimeSignature:
			flash('Invalid link','error')
			return redirect(url_for('index'))
		cur.execute("UPDATE parent SET password = %s WHERE username = %s",(password,username))
		mysql.connection.commit()
		cur.close()
		flash('Password reset Succefully, login to continue', 'success')
		return redirect(url_for('login'))		
	else:
		if request.method == 'POST' and not form.validate():
			error = 'Some error occured, please retry after some time'
			return render_template('reset.html', form=form, error=error)
		return render_template('reset.html', form=form)


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
	if response['context']['skills']['main skill']['user_defined']['foul']:
		respond= ['Did you understand champ?','Was this answer good enough','This is what i know, did you get the answer?']
		i = random.randint(0,len(respond)-1)
		if(response["output"]["entities"]):
			answer = Scraping.search( response )
			g.res += answer
			if (random.uniform(0,1) > 0.65):
				g.res += respond[i]
	response['context']['skills']['main skill']['user_defined']['foul'] = False


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
