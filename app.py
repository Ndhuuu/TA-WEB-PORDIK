from flask import Flask, render_template, redirect, url_for, request
import pymysql
import config

connection = cursor = None
application = Flask(__name__)

connection = pymysql.connect(host = config.DB_HOST, user = config.DB_USER, password = config.DB_PASSWORD, database = config.DB_NAME)
cursor = connection.cursor()

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/beranda')
def beranda():
    return render_template('index.html')

@application.route('/tentang')
def tentang():
    return render_template('tentang.html')

@application.route('/layanan')
def layanan():
    return render_template('layanan.html')
	
if __name__ == '__main__':application.run(debug=True)