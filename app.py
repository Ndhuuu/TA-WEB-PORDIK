from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


application = Flask(__name__)
application.secret_key = 'proyekspp'

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'keuangan'


mysql = MySQL(application)


@application.route('/', methods=['GET', 'POST'])
@application.route('/beranda', methods=['GET', 'POST'])
def index():
    if request.path == '/beranda':
        return redirect('/')
    else:
        return render_template('before login/beranda.html')


@application.route('/pengumuman')
def pengumuman():
    return render_template('before login/pengumuman.html')


@application.route('/layanan')
def layanan():
    return render_template('before login/layanan.html')


@application.route('/masuk')
def masuk():
    return render_template('before login/login.html')


@application.route('/admin')
def home_admin():
    return render_template('after login/home_admin.html')


@application.route('/mahasiswa')
def home_mahasiswa():
    return render_template('after login/home_mahasiswa.html')


@application.route('/admin/tagihanmhs')
def lk_tagihanmhs_admin():
    return render_template('after login/lk_tagihanmhs_admin.html')


@application.route('/mahasiswa/tagihanmhs')
def lk_tagihanmhs_mahasiswa():
    return render_template('after login/lk_tagihanmhs_mahasiswa.html')


@application.route('/autentifikasi', methods=['POST'])
def autentifikasi():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT role FROM tb_user WHERE nim=%s AND password=%s", (nim, password))
        user_role = cur.fetchone()
        cur.close()
        if user_role:
            if user_role[0] == 'Admin':
                session['role'] = 'Admin'
                return redirect(url_for('home_admin'))
            elif user_role[0] == 'Mahasiswa':
                session['role'] = 'Mahasiswa'
                return redirect(url_for('home_mahasiswa'))
        else:
            return 'Nim atau password anda salah'


if __name__ == '__main__':
    application.run(debug=True)