from flask import Flask, render_template, redirect, request, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_pymongo import PyMongo

app = Flask(__name__)

Bootstrap(app)
moment = Moment(app)

app.config['MONGO_URI'] = "mongodb+srv://SidAnand:Sid2004$@cluster0-csrmd.mongodb.net/test?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = "SomeSecretText"

mongo = PyMongo(app)

user = {}

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/classroom')
def classroom():
    return render_template('/classroom.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    username = session['username']
    classlist = mongo.db.AccountInformation.find_one({'username': username})['classes']

    #Post limiting feature
    if 'username' not in session:
        flash('Session Expired. Please Login Again')
        return redirect('/login')

    if request.method == 'POST':
        postentry = request.form['postentry']
        username = session['username']
        #Add time

        mongo.db.GlobalPost.insert_one({'username': username, 'postentry': postentry, 'timestamp': str(datetime.now())})
        return redirect('/home')

    else:
        allpost = mongo.db.GlobalPost.find()
        return render_template('home.html', allpost=allpost, role=session['role'], classlist=classlist)

@app.route('/manageclass', methods=['POST', 'GET'])
def manageclass():
    username = session['username']
    classlist = mongo.db.AccountInformation.find_one({'username': username})['classes']

    if request.method == 'POST':
        classid = request.form['classid']

        if 'leave' in request.form:

            mongo.db.AccountInformation.update({'username': username}, {'$pull': {'classes': {'classid': classid}}})
            mongo.db.Class.update({'classid': classid}, {'$pull': {'classes': {'username': username}}})

        elif 'delete' in request.form:

            mongo.db.AccountInformation.update_one({'username': username}, {'$pull': {'classes': {'classid': classid}}})
            mongo.db.ClassPost.delete_many({'classid': classid})
            studentlist = mongo.db.Class.find_one({'classid': classid})['classes']

            for x in studentlist:
                mongo.db.AccountInformation.update(x, {'$pull': {'classes': {'classid': classid}}})
            mongo.db.Class.delete_one({'classid': classid})


        else:
            classname = request.form['classname']
            if 'student' == session['role']:
                duplicatecheck = mongo.db.AccountInformation.find_one({'username':username})

                print(classid, duplicatecheck['classes'])
                if {'classname':classname, 'classid': classid} in duplicatecheck['classes']:
                    flash('Student is already in Class')
                    return redirect('/manageclass')

                dbclassid = mongo.db.Class.find_one({'classname': classname, 'classid': classid})
                print(dbclassid)


                if dbclassid:
                    mongo.db.AccountInformation.update_one({'username': username},
                                                       {'$push': {'classes': {'classname': classname,'classid': classid}}})
                    mongo.db.Class.update_one({'classid': dbclassid['classid']}, {'$push': {'classes': {'username': username}}}, upsert = True)
                else:
                    flash('Classroom does not exist.')

            elif 'teacher' == session['role']:
                mongo.db.AccountInformation.update({'username': username}, {'$push': {'classes': {'classname': classname,
                                                                                                  'classid': classid}}})
                mongo.db.Class.insert({'username': username, 'classname': classname, 'classid': classid})

        return redirect('/manageclass')



    classes = mongo.db.AccountInformation.find_one({'username': username})['classes']
    return render_template('manageclass.html', role=session['role'], classes=classes,classlist=classlist)

@app.route('/viewclass/<classid>', methods=['POST', 'GET'])
def viewclass(classid):
    username = session['username']
    classlist = mongo.db.AccountInformation.find_one({'username': username})['classes']

    for x in classlist:
        if x['classid'] == classid:
            classname = x['classname']
            print(classname)

    if request.method == "POST":
        postentry = request.form['postentry']
        mongo.db.ClassPost.insert_one({'username': username, 'postentry': postentry,'classid': classid,
                                       'timestamp': str(datetime.now())})
        return redirect('/viewclass/'+classid)

    allpost = mongo.db.ClassPost.find({'classid': classid})

    return render_template('viewclass.html', role=session['role'], classlist=classlist, classname=classname,
                           username=username, allpost=allpost)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='GET':
        if 'username' in session:
            return redirect('/home')
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        collection = mongo.db.AccountInformation
        user = collection.find_one({'username': username})

        if username == '' or password == '':
            flash('Username or Password Field is Required')
            return redirect('/login')
        elif user == None:
            flash('Account not found. Please Register')
            return redirect('/register')
        elif username != user['username'] or password != user['password']:
            flash('The Username or Password is Incorrect. Please Try Again')
            return redirect('/login')
        else:
            session['username'] = username
            session['role'] = user['role']
            return redirect('/home')

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/login')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        passwordrepeat = request.form['password-repeat']

        role = request.form['role']

        collection = mongo.db.AccountInformation
        user = collection.find_one({'username': username})

        # if email is not registered, runs inside
        if user == None:
            if password != passwordrepeat:
                flash('Your passwords do not match. Please Try Again')
                return redirect('/register')
            else:
                collection = mongo.db.AccountInformation
                usersDetails = {'username': username, 'password': password, 'role': role, 'classes':[]}
                collection.insert(usersDetails)
                flash('Successfully registered')
                return redirect('/login')
        else:
            flash('User Exists Please login')
            return redirect('/login')

    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
