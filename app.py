from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

application = Flask(__name__)

@application.route('/')
def index():
	return render_template('login.html')
	
if __name__ == '__main__':application.run(debug=True)