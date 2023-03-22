from flask import Flask, render_template, request
from flask_mysqldb import MySQL


application = Flask(__name__)
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'flask'


mysql = MySQL(application)


@application.route('/beranda')
def beranda():
    return render_template("index.html")


@application.route('/tentang')
def tentang():
    return render_template('tentang.html')


@application.route('/layanan')
def layanan():
    return render_template('layanan.html')


@application.route('/masuk')
def masuk():
    return render_template('login.html')


@application.route('/authenticate', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM user WHERE nim=%s AND password=%s", (nim, password))
        user = cur.fetchone()
        cur.close()
        if user:
            return render_template('dashboard.html')
        else:
            return 'Nim atau password anda salah'


if __name__ == '__main__':
    application.run(debug=True)