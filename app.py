from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask import flash
from flask_mysqldb import MySQL
from functools import wraps

application = Flask(__name__)
application.secret_key = 'portalakademik'

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'db_pordik'

mysql = MySQL(application)


# INDEX AREA
@application.route('/')
def indeks():
    return render_template('before login/beranda.html')


# LOGIN AREA
@application.route('/masuk')
def masuk():
    return render_template('before login/login.html')


@application.route('/autentifikasi', methods=['POST'])
def autentifikasi():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT role_id, nama FROM tb_user WHERE username=%s AND password=%s", (username, password))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            session['role_id'] = user_data[0]
            session['nama'] = user_data[1]
            if user_data[0] == 1:
                session['role'] = 'admin'
                flash('SELAMAT DATANG ADMIN!', 'success')
                return redirect(url_for('home_admin'))
            elif user_data[0] == 2:
                session['role'] = 'mahasiswa'
                flash('SELAMAT DATANG MAHASISWA!', 'success')
                return redirect(url_for('home_mahasiswa'))
        else:
            session.clear()
            flash('Nim atau password anda salah!', 'danger')
            return redirect(url_for('masuk'))
    return redirect(url_for('masuk'))


@application.route('/keluar')
def keluar():
    session.clear()
    return redirect(url_for('masuk'))


@application.route('/lupa-password')
def lupa_password():
    return render_template('before login/lupa_password.html')


# RESTRICTION PAGE AREA
def login_required(role_id):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'role_id' not in session:
                return redirect(url_for('masuk'))
            elif session['role_id'] != role_id:
                return abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@application.errorhandler(403)
def forbidden_page(error):
    return render_template('403.html'), 403


@application.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@application.route('/kembali')
def kembali():
    if 'role_id' in session:
        if session['role_id'] == '1':
            return redirect(url_for('home_admin'))
        elif session['role_id'] == '2':
            return redirect(url_for('home_mahasiswa'))
    return redirect(url_for('masuk'))


# ADMIN AREA
# DASHBOARD ADMIN
@application.route('/admin')
@login_required(1)
def home_admin():
    return render_template('after login/dashboard/home_admin.html')


# DATA MASTER
# DATA LOGIN USER
# @application.route('/data-login-user')
# @login_required(1)
# def read_user():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT nama, username, password, CASE role_id WHEN 1 THEN 'admin' WHEN 2 THEN 'mahasiswa' END AS role FROM tb_user")
#     data_user = cur.fetchall()
#     cur.close()
#     return render_template('after login/data_master/data_user.html', data_user=data_user)


@application.route('/data-mahasiswa')
@login_required(1)
def read_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, password, nama, CONCAT(tempat_lahir, ',', ' ',tanggal_lahir), jenis_kelamin, agama, alamat, no_telepon, email FROM tb_datamahasiswa")
    data_mahasiswa = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_mahasiswa.html', data_mahasiswa=data_mahasiswa)


@application.route('/data-admin')
@login_required(1)
def read_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, password, nama, CONCAT(tempat_lahir, ',', ' ',tanggal_lahir), jenis_kelamin, agama, alamat, no_telepon, email FROM tb_dataadmin")
    data_admin = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_admin.html', data_admin=data_admin)


# TAMBAH DATA ADMIN & MAHASISWA
@application.route('/tambah-data', methods=['GET', 'POST'])
@login_required(1)
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        agama = request.form['agama']
        alamat = request.form['alamat']
        no_telepon = request.form['no_telepon']
        email = request.form['email']
        # foto = request.form['foto']
        role_id = request.form['role_id']
        data_user = (username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, email, role_id)
        cur = mysql.connection.cursor()
        if role_id == 'admin':
            role_id = 1
            cur.execute("INSERT INTO tb_dataadmin (username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data_user)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('read_admin'))
        else:
            role_id = 2
            cur.execute("INSERT INTO tb_datamahasiswa (username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data_user)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('read_mahasiswa'))
    else:
        return render_template('after login/data_master/create_data.html')


# EDIT DATA ADMIN & MAHASISWA
@application.route('/edit-data/<int:id>', methods=['GET', 'POST'])
@login_required(1)
def update_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_user WHERE id=%s", [id])
    data = cur.fetchone()
    cur.close()
    return render_template('after login/data_master/update_datauser.html', data=data)


@application.route('/update_process', methods=['POST'])
@login_required(1)
def update_process():
    id = request.form['id']
    nama = request.form['nama']
    username = request.form['username']
    password = request.form['password']
    role_id = request.form['role_id']
    data_user = (id, nama, username, password, role_id)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tb_user SET nama=%s, password=%s, role_id=%s WHERE id=%s", data_user)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('data_user'))


# HAPUS DATA ADMIN & MAHASISWA
def delete_user():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_user WHERE id=%s")
    cur.close()


# MAHASISWA AREA
@application.route('/mahasiswa')
@login_required(2)
def home_mahasiswa():
    return render_template('after login/dashboard/home_mahasiswa.html')


if __name__ == '__main__':
    application.run(debug=True)
