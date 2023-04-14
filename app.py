from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask import flash
from flask_mysqldb import MySQL
from functools import wraps

application = Flask(__name__)
application.secret_key = 'proyekspp'

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'db_pordik'

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


# LOGIN AREA
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
            if user_data[0] == 'Admin':
                flash('Anda berhasil masuk sebagai admin', 'success')
                return redirect(url_for('home_admin'))
            elif user_data[0] == 'Mahasiswa':
                flash('Anda berhasil masuk sebagai mahasiswa', 'success')
                return redirect(url_for('home_mahasiswa'))
        else:
            flash('Nim atau password anda salah!', 'danger')
            return redirect(url_for('masuk'))


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
    if 'role' in session:
        if session['role'] == 'Admin':
            return redirect(url_for('home_admin'))
        elif session['role'] == 'Mahasiswa':
            return redirect(url_for('home_mahasiswa'))
    return redirect(url_for('masuk'))


# ADMIN AREA
    # DASHBOARD ADMIN
    # DATA MASTER
        # DATA LOGIN USER
            # TAMBAH DATA LOGIN USER
            # EDIT DATA LOGIN USER
            # HAPUS
        # DATA ADMIN
            # TAMBAH DATA ADMIN
            # EDIT DATA ADMIN
            # HAPUS
        # DATA MAHASISWA
            # TAMBAH DATA MAHASISWA
            # EDIT DATA MAHASISWA
            # HAPUS
    # DATA TRANSAKSI
        # TAGIHAN MAHASISWA
            # TAMBAH
            # EDIT
            # HAPUS
        # UNGGAH BUKTI BAYAR
            # TAMBAH
            # EDIT
            # HAPUS
        # RIWAYAT PEMBAYARAN
            # TAMBAH
            # EDIT
            # HAPUS
    # DATA RESUME
        # MAHASISWA LUNAS
            # TAMBAH
            # EDIT
            # HAPUS
        # MAHASISWA NUNGGAK
            # TAMBAH
            # EDIT
            # HAPUS
        # PIUTANG
            # TAMBAH
            # EDIT
            # HAPUS


# DASHBOARD ADMIN
@application.route('/admin')
@login_required('Admin')
def home_admin():
    return render_template('after login/dashboard/home_admin.html')


# DATA MASTER
# DATA LOGIN USER
@application.route('/data-login-user')
def read_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nama, nim, password, role FROM tb_user")
    data_user = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_user.html', data_user=data_user)


# TAMBAH DATA LOGIN USER
@application.route('/tambah-login-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        nama = request.form['nama']
        password = request.form['password']
        role = request.form['role']
        data_user = (nama, password, role)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_user (nama, password, role) VALUES (%s, %s, %s)", data_user)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('data_user'))
    else:
        return render_template('after login/data_master/create_datauser.html')


# EDIT DATA LOGIN USER
@application.route('/edit-login-user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_user WHERE id=%s", [id])
    data = cur.fetchone()
    cur.close()
    return render_template('after login/data_master/update_datauser.html', data=data)


@application.route('/update_process', methods=['POST'])
def update_process():
    id = request.form['id']
    nama = request.form['nama']
    password = request.form['password']
    role = request.form['role']
    data_user = (nama, password, role, id)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tb_user SET nama=%s, password=%s, role=%s WHERE id=%s", data_user)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('data_user'))


# HAPUS DATA LOGIN USER
def delete_user():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_user WHERE id=%s")
    cur.close()


@application.route('/data-mahasiswa')
@login_required('Admin')
def data_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nim, nama, CONCAT(tempat_lahir, ',', ' ',tanggal_lahir), jenis_kelamin, alamat, no_telepon, email FROM tb_mahasiswa")
    data_mahasiswa = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_mahasiswa.html', data_mahasiswa=data_mahasiswa)


@application.route('/data-admin')
@login_required('Admin')
def data_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nim, nama, CONCAT(tempat_lahir, ',', ' ',tanggal_lahir), jenis_kelamin, alamat, no_telepon, email FROM tb_admin")
    data_admin = cur.fetchall()
    cur.close()
    return render_template('after login/data_master/data_admin.html', data_admin=data_admin)


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


if __name__ == '__main__':
    application.run(debug=True)
