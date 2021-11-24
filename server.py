from flask import Flask, render_template, flash, request, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from analyzer import review_analyser
from textcluster import text_clust

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 

client = MongoClient('localhost')
db = client.review
col = db.reviews

app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

 
class uploadForm(Form):
	
	name = TextAreaField('Review:', validators=[validators.required()])
  
 

@app.route("/", methods=['GET', 'POST'])
def hello():
    session['logged_in'] = False
    form = uploadForm(request.form)
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
            
        print (name)
 
        if form.validate():
            # Save the comment here.
            cat = text_clust(name)
            print(cat) 
            one,two,three= review_analyser(name)
            
            ini = db.reviews.insert({"review":name,"rating":one,"star":two, "category":cat,"type":three})
            
        else:
            flash('All the form fields are required.')
    avg,b = 0,0

    if db.reviews.count() == 0 :
    	stars = 0
    else :
	    for rev in db.reviews.find():
	        avg = avg + rev['rating']
	        b = b + 1
	    stars = avg / b
    rev = []
    for x in db.reviews.find():
        
        revs = x['review']
        rev.append(revs)
    flash(rev)
    return render_template('index1.html', form=form,star = stars)
@app.route('/admin', methods=['GET'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('admin.html')

@app.route('/admin/login', methods=['POST','GET'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
@app.route('/')
def logout():
   # remove the username from the session if it is there
   session.pop('username')
   
   return redirect(url_for('hello'))
   #return hello()
   #food
@app.route('/admin/food',methods=['GET','POST'])
def food():
    food = []
    for ff in db.reviews.find():
        if ff['category'] == "food":
            if ff['type'] == "negative":
                food.append(ff['review'])
    flash(food)

    return render_template('food.html')
    #rooms
@app.route('/admin/rooms',methods=['GET','POST'])
def rooms():
    rooms = []
    for ff in db.reviews.find():
        if ff['category'] == "rooms":
            if ff['type'] == "negative":
                rooms.append(ff['review'])
    flash(rooms)

    return render_template('rooms.html')
''' 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
'''
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,port=8080)
