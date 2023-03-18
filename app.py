from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import pymysql
import config

connection = cursor = None

application = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

connection = pymysql.connect(host = config.DB_HOST, user = config.DB_USER, password = config.DB_PASSWORD, database = config.DB_NAME)
cursor = connection.cursor()

class User(UserMixin):
	def __init__(self, id, nim, password):
		self.id = id
		self.nim = nim
		self.password = password

	@staticmethod
	def get(user_id):
		with connection.cursor() as cursor:
			cursor.execute('select * from user where id = %s', (user_id,))
			user = cursor.fetchone()
			if not user:
				return None
			return User(user['id'], user['nim'], user['password'])

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/')
@login_required
def home():
	return render_template('home.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		nim = request.form['nim']
		password = request.form['password']
		with connection.cursor() as cursor:
			cursor.execute('select * from user where nim = %s and password = %s', (nim, password))
			user = cursor.fetchone()
			if user:
				user_obj = User(user['id'], user['nim'], user['password'])
				login_user(user_obj)
				return redirect(url_for('home'))
			else:
				return render_template('login.html', error='invalid nim or password')
	else:
		return render_template('login.html')
	
@application.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))
	
if __name__ == '__main__':application.run(debug=True)