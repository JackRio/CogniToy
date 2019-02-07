from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'jarvis'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#Articles = Articles()

# Index
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


@app.route('/chatlog')
def chatlog():
    return render_template('chatlog.html')

# Register Form Class
class RegisterForm(Form):
    f_name = StringField('Father Name', [validators.Length( max=50)])
    f_contact = IntegerField('Father Contact No.')
    f_email = StringField('Father Email Id', [validators.Length( max=50)])
    
    m_name = StringField('Mother Name', [validators.Length( max=50)])
    m_contact = IntegerField('Mother Contact No.')
    m_email = StringField('Mother Email Id', [validators.Length( max=50)])
    
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=20)])
    password = PasswordField('Password', [
        validators.Length(min=4, max=20),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    
    Sec_Q = StringField('Security Question', [validators.Length(min=5, max=20)])
    Sec_A = StringField('Security Answer', [validators.Length(min=4, max=20)])

    Address = TextAreaField('Address')
    
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
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

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
                return redirect(url_for('chatlog'))
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
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
