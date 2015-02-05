from flask import Flask, render_template, request, url_for, jsonify
import sqlite3

app = Flask(__name__)

from wtforms import Form, BooleanField, TextField, PasswordField, validators

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.executescript('drop table if exists test;')

c.execute('''CREATE TABLE test (category real, priority real, description real)''')

# Create table
#c.execute('''CREATE TABLE stocks
#    (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
#conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
#conn.close()


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password',[validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

@app.route('/')
def hello_world():
    return render_template('form_submit.html')

@app.route('/_add_numbers')
def add_numbers():
    category = request.args.get('category', "", type=str)
    priority = request.args.get('priority', 0, type=int)
    description = request.args.get('description', "", type=str)

#c.execute('''CREATE TABLE stocks
#    (date text, trans text, symbol text, qty real, price real)''')
#c.execute('''CREATE TABLE test (category real, priority real, description real)''')
    vals = [(category, priority, description)]
    c.executemany('INSERT INTO test VALUES (?,?,?)', vals)
    conn.commit()
    z = []
    for x in c.execute('select * from test'):
        z.append(x)

    return jsonify(result = z)
#return jsonify(result=category + priority+ description)

@app.route('/hello/', methods=['POST'])
def hello():
    name=request.form['yourname']
    email=request.form['youremail']
    return render_template('form_action.html', name=name, email=email)


#http://runnable.com/UhLMQLffO1YSAADK/handle-a-post-request-in-flask-for-python