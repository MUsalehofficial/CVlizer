import os
import warnings
# import MySQLdb

from pymongo import MongoClient
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import IndexFunctions
import DashboardFunctions

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'CVs/'
app.secret_key = 'super secret key'  # I still don't know the actual usage of the Secret Key

client = MongoClient('mongodb://localhost:27017/')
db = client['ACVAS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Adding each value of text-boxes in the registration page into variables
        _fname = request.form['_fname']
        _lname = request.form['_lname']
        _email = request.form['_email']
        _country = request.form['_country']
        _phone = request.form['_phone']
        _birthdate = request.form['_birthdate']

        # check if the post request has the file part
        if '_cv' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['_cv']

        # if user does not select file, browser also
        # submit an empty part without filename
        # WE DONE THIS PART IN HTML
        # if file.filename == '':
        #   flash('No selected file')
        #   return redirect(request.url)

        if file and IndexFunctions.allowed_file(file.filename):
            # cwd = os.getcwd()
            # print(cwd)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _cv = filename

            # applicants = db['Applicants']
            db['Applicants'].insert_one({
                'FName': _fname,
                'LName': _lname,
                'Email': _email,
                'Country': _country,
                'Phone': _phone,
                'Birthdate': _birthdate,
                'CV': _cv,
                'CV_parsed': False
            })
            # applicant_id = applicants.insert_one(applicant).inserted_id
            # applicant_id
            # print('done to mongo..')

            # Open database connection
            # db = MySQLdb.connect("localhost", "root", "123456789", "ACVAS")
            # prepare a cursor object using cursor() method
            # cursor = db.cursor()
            # execute the cursor

            # cursor.execute("""\
            # INSERT INTO applicants(FName, LName, Email, Country, Phone, Birthdate, CV)
            # VALUES (%s, %s, %s, %s, %s, %s, %s) """, (_fname, _lname, _email, _country, _phone, _birthdate, _cv))
            # commit
            # db.commit()
            # disconnect from server
            # db.close()
            # index.fName = _fname
            return redirect(url_for('done_upload'))
    return render_template('index.html')


@app.route('/done')
def done_upload():
    # A redirection code to index page is add at done.html
    # print('Test GET: ', index.fName)
    return render_template('done.html')


@app.route('/Admin/Login', methods=['GET', 'POST'])
def admin_login():
    error = None
    # loggedOrNot = 0
    # global currentUser
    # if request.form['_username'] in session:
    #    return redirect(url_for('admin_dashboard'))
    admin_login.loggedOrNot = 0
    if request.method == 'POST':
        _username = request.form['_username']
        _password = request.form['_password']
        # user = User.get(_username)

        # client = MongoClient('mongodb://localhost:27017/')
        # db = client['ACVAS']
        data = db['Admins'].find_one({
            'Username': _username,
            'Password': _password
        })

        # Open database connection
        # db = MySQLdb.connect("localhost", "root", "123456789", "ACVAS")
        # prepare a cursor object using cursor() method
        # cursor = db.cursor()
        # execute the cursor
        # cursor.execute("SELECT * from admin where Username='" + _username + "' and Password='" + _password + "'")
        # data = cursor.fetchone()

        # print(data)
        if data is None:
            # print("Username or Password is wrong")
            error = 'Invalid username or password.'
        else:
            admin_login.currentUser = data['Username']
            # print(admin_login.currentUser)
            session['_username'] = _username
            # session['logged_in'] = True
            admin_login.loggedOrNot = 1

            return redirect(url_for('admin_dashboard'))
            # print("Logged in successfully")
    return render_template('AdminLogin.html', error=error, loggedOrNot=admin_login.loggedOrNot)


@app.route('/Admin/Logout', methods=['GET', 'POST'])
def admin_logout():
    session.pop('_username')
    # session.pop('logged_in', None)
    # print('You were logged out')
    return redirect(url_for('admin_login'))


@app.route('/Admin/Dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if '_username' in session:
        # noinspection PyBroadException
        try:
            loggedInUser = admin_login.currentUser
        except:
            loggedInUser = 'Null'

        totalApplicants = db['Applicants'].count()
        totalParsedCVs = db['CV_Content'].count()
        totalUnParsedCVs = db['Applicants'].find({
            'CV_parsed': False
        }).count()
        if request.method == 'POST':
            _jobDescription = request.form['_jobDescription']
            # if len(_jobDescription) <= 100:
            #    _jobDescription = _jobDescription
            # else:
            #    _jobDescription = summarize(_jobDescription, word_count=100)

        return render_template('AdminDashboard.html',
                               loggedInUser=loggedInUser,
                               totalApplicants=totalApplicants,
                               totalParsedCVs=totalParsedCVs,
                               totalUnParsedCVs=totalUnParsedCVs)
    else:
        return redirect(url_for('admin_login'))

@app.route('/Admin/Dashboard/Applicants')
def browse_applicants():
    if '_username' in session:
        # noinspection PyBroadException
        try:
            loggedInUser = admin_login.currentUser
        except:
            loggedInUser = 'Null'

        applicants = db['Applicants'].find()

        return render_template('Applicants.html',
                               loggedInUser=loggedInUser,
                               applicants=applicants)
    else:
        return redirect(url_for('admin_login'))

@app.route('/Admin/Dashboard/CVs')
def browse_cvs():
    if '_username' in session:
        # noinspection PyBroadException
        try:
            loggedInUser = admin_login.currentUser
        except:
            loggedInUser = 'Null'

        cvs = db['CV_Content'].find()

        return render_template('CVs.html',
                               loggedInUser=loggedInUser,
                               cvs=cvs)
    else:
        return redirect(url_for('admin_login'))


@app.route('/Admin/Dashboard/Search', methods=['GET', 'POST'])
def search_job():
    # search_job.jobDescription = ''
    # print('>> FUNCTION START')
    # print(request.method)
    # print(request.form)
    if '_username' in session:
        # noinspection PyBroadException
        try:
            loggedInUser = admin_login.currentUser
        except:
            loggedInUser = 'Null'

        if request.method == 'POST':
            # print(">> REQUEST FORM:", request.form)
            _jobDescription = request.form['_jobDescription']
            # print(_jobDescription)
            search_job.jobDescription = _jobDescription
            return redirect(url_for('results'))

        # search_job.jobDescription = _jobDescription
        return render_template('Search.html', loggedInUser=loggedInUser)
    else:
        return redirect(url_for('admin_login'))

@app.route('/Admin/Dashboard/Search/Results')
def results():
    if '_username' in session:
        # noinspection PyBroadException
        try:
            loggedInUser = admin_login.currentUser
        except:
            loggedInUser = 'Null'

        # noinspection PyBroadException
        try:
            res = DashboardFunctions.ranking_cvs(search_job.jobDescription)
            # print(res)
        except:
            print('Something error. Please, try again.')
            return redirect(url_for('search_job'))

        return render_template('Results.html',
                               loggedInUser=loggedInUser,
                               res=res)
    else:
        return redirect(url_for('admin_login'))

@app.route('/CVs/<path:filename>')
def custom_static(filename):
    return send_from_directory('./CVs', filename)


if __name__ == '__main__':
    app.run()
