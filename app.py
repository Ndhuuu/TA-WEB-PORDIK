from flask import Flask, render_template, request, redirect, url_for, session
from flask import flash
from flask_mysqldb import MySQL
from functools import wraps


application = Flask(__name__)
application.secret_key = 'proyekspp'

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'keuangan'


mysql = MySQL(application)


# INDEX AREA
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


@application.route('/keluar')
def keluar():
    session.clear()
    return redirect(url_for('masuk'))


# RESTRICTION PAGE AREA
def login_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('masuk'))
            elif session['role'] != role:
                return "Anda tidak dapat mengakses halaman ini, karena anda tidak memiliki hak akses ke halaman ini.", 403
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# ADMIN AREA
@application.route('/admin')
@login_required('Admin')
def home_admin():
    return render_template('after login/dashboard/home_admin.html')


@application.route('/data-login-user')
def data_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nama, nim, password, role FROM tb_user")
    data_user = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_user.html', data_user=data_user)



@application.route('/data-mahasiswa')
@login_required('Admin')
def data_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_mahasiswa")
    mhs = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_mhs.html', mhs=mhs)


# @application.route('/tagihanmhs')
# @login_required('Admin')
# def lk_tagihanmhs_admin():
#     return render_template('after login/lk_tagihanmhs_admin.html')


# MAHASISWA AREA
@application.route('/mahasiswa')
@login_required('Mahasiswa')
def home_mahasiswa():
    return render_template('after login/dashboard/home_mahasiswa.html')


# @application.route('/tagihanmhs')
# @login_required('Mahasiswa')
# def lk_tagihanmhs_mahasiswa():
#     return render_template('after login/lk_tagihanmhs_mahasiswa.html')


# LOGIN AREA
@application.route('/autentifikasi', methods=['POST'])
def autentifikasi():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT role, nama FROM tb_user WHERE nim=%s AND password=%s", (nim, password))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            session['role'] = user_data[0]
            session['nama'] = user_data[1]
            if user_data[0] == 'Admin':
                flash('Anda berhasil masuk sebagai admin', 'success')
                return redirect(url_for('home_admin'))
            elif user_data[0] == 'Mahasiswa':
                flash('Anda berhasil masuk sebagai mahasiswa', 'success')
                return redirect(url_for('home_mahasiswa'))
        else:
            flash('Nim atau password anda salah!', 'danger')
            return redirect(url_for('masuk'))


if __name__ == '__main__':
    application.run(debug=True)