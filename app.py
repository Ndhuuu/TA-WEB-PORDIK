from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


application = Flask(__name__)
application.secret_key = 'proyekspp'

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'keuangan'


mysql = MySQL(application)


@application.route('/')
def index():
    return render_template("beranda.html")


@application.route('/beranda')
def beranda():
    return redirect(url_for('index'))


@application.route('/tentang')
def tentang():
    return render_template('tentang.html')


@application.route('/layanan')
def layanan():
    return render_template('layanan.html')


@application.route('/masuk')
def masuk():
    return render_template('login.html')


@application.route('/admin')
def admin():
    return render_template('dashboard_admin.html')

@application.route('/mahasiswa')
def mahasiswa():
    return render_template('dashboard_mahasiswa.html')


@application.route('/autentifikasi', methods=['POST'])
def autentifikasi():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT role FROM user WHERE nim=%s AND password=%s", (nim, password))
        user_role = cur.fetchone()
        cur.close()
        if user_role:
            if user_role[0] == 'Admin':
                session['role'] = 'Admin'
                return redirect(url_for('admin'))
            elif user_role[0] == 'Mahasiswa':
                session['role'] = 'Mahasiswa'
                return redirect(url_for('mahasiswa'))
        else:
            return 'Nim atau password anda salah'



if __name__ == '__main__':
    application.run(debug=True)