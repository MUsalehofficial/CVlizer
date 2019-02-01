import os
import warnings

import MySQLdb
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import IndexFunctions

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'CVs/'
app.secret_key = 'super secret key'  # I still don't know the actual usage of the Secret Key


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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _cv = filename

            # Open database connection
            db = MySQLdb.connect("localhost", "root", "123456789", "ACVAS")
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            # execute the cursor
            cursor.execute("""\
            INSERT INTO applicants(FName, LName, Email, Country, Phone, Birthdate, CV)
            VALUES (%s, %s, %s, %s, %s, %s, %s) """, (_fname, _lname, _email, _country, _phone, _birthdate, _cv))
            # commit
            db.commit()
            # disconnect from server
            db.close()

            return redirect(url_for('done_upload'))
    return render_template('index.html')


@app.route('/done')
def done_upload():
    # A redirection code to index page is add at done.html
    return render_template('done.html')


@app.route('/Admin/Login', methods=['GET', 'POST'])
def admin_login():
    error = None
    # global currentUser
    # if request.form['_username'] in session:
    #    return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        _username = request.form['_username']
        _password = request.form['_password']

        # Open database connection
        db = MySQLdb.connect("localhost", "root", "123456789", "ACVAS")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # execute the cursor
        cursor.execute("SELECT * from admin where Username='" + _username + "' and Password='" + _password + "'")
        data = cursor.fetchone()
        # print(data)
        if data is None:
            # print("Username or Password is wrong")
            error = 'Invalid username or password.'
        else:
            # print(data[0])  # This goes for Username
            # print(data[1])  # This goes for Password
            admin_login.currentUser = str(data[0])
            # print(admin_login.currentUser)
            session['_username'] = _username
            # session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
            # print("Logged in successfully")
    return render_template('AdminLogin.html', error=error)


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

        # if request.method == 'POST':
        #    _jobDescription = request.form['_jobDescription']
        #    if len(_jobDescription) <= 100:
        #        _jobDescription = _jobDescription
        #    else:
        #        _jobDescription = summarize(_jobDescription, word_count=100)

        return render_template('AdminDashboard.html', loggedInUser=loggedInUser)
    else:
        return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run()
