import logging
from flask import Flask, render_template, request, redirect, session
import mysql.connector

# Configure the logging settings
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = 'Ka20s6480'


# MySQL database connection
db = mysql.connector.connect(
    host='dev-demo-rds.c4yrcdfixqfn.eu-west-1.rds.amazonaws.com',
    user='foo',
    password='foobarbaz',
    database='demo_db'
)

@app.route('/')
def home():
    app.logger.info('Home page accessed.')
    return 'Welcome to the login page Azam'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['logged_in'] = True
            app.logger.info(f'User {username} logged in.')
            return redirect('/dashboard')
        else:
            app.logger.warning(f'Failed login attempt for user {username}.')
            return 'Authentication failed'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    logged_in = session.get('logged_in', False)  # Get the session variable or default to False
    if logged_in:
        app.logger.info('Dashboard accessed.')
        return render_template('dashboard.html', logged_in=logged_in)  # Pass logged_in to the template
    else:
        app.logger.warning('Unauthorized access to dashboard.')
        return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)



