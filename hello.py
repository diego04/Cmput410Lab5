from flask import Flask, render_template, request, url_for, jsonify, g, redirect, url_for, session, flash   
import sqlite3
import os
from wtforms import Form, BooleanField, TextField, PasswordField, validators


app = Flask(__name__)


conn = sqlite3.connect('example.db')
c = conn.cursor()

c.executescript('drop table if exists test;')

c.execute('''CREATE TABLE test (category real, priority real, description real)''')

DATABASE='test.db'
DATABASE ='test.db'
USERNAME = 'admin'
PASSWORD = 'password'
SECRET_KEY = 'this is secrete key'


"""
app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',    
    PASSWORD='password',
    
    
))"""

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object(__name__)



app= Flask(__name__)
app.config.from_object(__name__)

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
    #return render_template('form_submit.html')
    return redirect(url_for('task'))

@app.route('/task', methods=['GET','POST'])
def task():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        addTask(category, priority, description)

        flash('New task added!')
        return redirect(url_for('task'))
    return render_template('show_entries.html', tasks=query_db('select * from tasks'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'invalid password'
        else:
            session['logged_in'] = True
            flash('authenticated')
            return redirect(url_for('task'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in')
    flash('You are logged out!')
    return redirect(url_for('task'))

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get('logged_in'):
        abort(401)
    removeTask(request.form['category'], request.form['priority'], request.form['description'])
    flash('Task was deleted successfully!')
    return redirect(url_for('task'))


def addTask(category, priority, description):
    query_db('insert into tasks values(?, ?, ?)', [category, int(priority), description], one=True)
    get_db().commit()

def removeTask(category, priority, description):
    query_db('delete from tasks where category = ? and priority  = ? and description= ?', [category, int(priority), description], one=True)
    get_db().commit()
    
def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        db = None
        
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