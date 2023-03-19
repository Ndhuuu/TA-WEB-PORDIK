from flask import Flask, render_template, redirect, url_for, request
# import pymysql
from flask_mysqldb import MySQL
import config

# connection = cursor = None
application = Flask(__name__)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


@application.route('/')
def index():
    return render_template("index.html")


@application.route('/tentang')
def tentang():
    return render_template('tentang.html')


@application.route('/layanan')
def layanan():
    return render_template('layanan.html')


@application.route('/login')
def login():
    return render_template('login.html')


@application.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    application.run(debug=True)
