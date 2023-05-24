from flask import Flask, render_template, request, redirect, url_for, session, abort
import os
from flask import flash
from flask_mysqldb import MySQL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

application = Flask(__name__)
application.secret_key = 'portalakademik'

UPLOAD_FOLDER = 'static/img/foto'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'db_pordik'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        cur.execute("SELECT role_id, password, nama, id FROM tb_dataadmin WHERE username=%s UNION SELECT role_id, password, nama, id FROM tb_datamahasiswa WHERE username=%s", (username, username))
        user_data = cur.fetchone()
        cur.close()
        if user_data and check_password_hash(user_data[1], password):
            session['role_id'] = user_data[0]
            session['nama'] = user_data[2]
            session['id'] = user_data[3]
            if user_data[0] == 1:
                session['role'] = 'admin'
                flash(f'Anda masuk sesi sebagai admin!', 'success')
                return redirect(url_for('home_admin'))
            elif user_data[0] == 2:
                session['role'] = 'mahasiswa'
                flash(f'Anda masuk sesi sebagai mahasiswa!', 'success')
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


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    return render_template('after login admin/dashboard/home_admin.html')


# DATA MASTER
# DATA MAHASISWA
@application.route('/data-mahasiswa')
@login_required(1)
def read_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, nama, CONCAT(tempat_lahir, ',', ' ',tanggal_lahir), jenis_kelamin, agama, alamat, no_telepon, email, foto FROM tb_datamahasiswa")
    data_mahasiswa = cur.fetchall()
    cur.close()
    return render_template('after login admin/data_master/data_mahasiswa.html', data_mahasiswa=data_mahasiswa)


# TAMBAH DATA MAHASISWA
@application.route('/data-mahasiswa/tambah-data-mahasiswa', methods=['GET', 'POST'])
@login_required(1)
def create_mahasiswa():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(
            request.form['password'], method='pbkdf2:sha256', salt_length=16)
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        agama = request.form['agama']
        alamat = request.form['alamat']
        no_telepon = request.form['no_telepon']
        email = request.form['email']
        role_id = request.form['role_id']
        # Mengubah role_id string menjadi integer
        if role_id == 'mahasiswa':
            role_id = 2
        foto = request.files['foto']
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(
                application.config['UPLOAD_FOLDER'], filename.replace('\\', '/')))
        else:
            filename = ''  # Set filename menjadi string kosong jika tidak ada file foto yang diunggah
        data_user = (username, password, nama, tempat_lahir, tanggal_lahir,
                     jenis_kelamin, agama, alamat, no_telepon, email, filename, role_id)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_datamahasiswa (username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, email, foto, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data_user)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('read_mahasiswa'))
    else:
        return render_template('after login admin/data_master/create_datamahasiswa.html')


# EDIT DATA MAHASISWA
@application.route('/data-mahasiswa/edit-data-mahasiswa/<int:id>')
@login_required(1)
def update_mahasiswa(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, email, foto, role_id FROM tb_datamahasiswa WHERE id='%s'" % id)
    data_user = cur.fetchone()
    return render_template('after login admin/data_master/update_datamahasiswa.html', data_user=data_user)


@application.route('/data-mahasiswa/update-process-mahasiswa', methods=['GET', 'POST'])
@login_required(1)
def update_process_mahasiswa():
    id = request.form['id']
    username = request.form['username']
    password = generate_password_hash(
        request.form['password'], method='pbkdf2:sha256', salt_length=16)
    nama = request.form['nama']
    tempat_lahir = request.form['tempat_lahir']
    tanggal_lahir = request.form['tanggal_lahir']
    jenis_kelamin = request.form['jenis_kelamin']
    agama = request.form['agama']
    alamat = request.form['alamat']
    no_telepon = request.form['no_telepon']
    email = request.form['email']
    role_id = request.form['role_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, email, foto, role_id FROM tb_datamahasiswa WHERE id='%s'" % id)
    data_user = cur.fetchone()
    # Mengubah role_id string menjadi integer
    if role_id == 'mahasiswa':
        role_id = 2
    else:
        None
    foto = request.files['foto']
    # Periksa apakah permintaan POST memiliki value input foto
    if foto and foto.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(
            application.config['UPLOAD_FOLDER'], filename.replace('\\', '/')))
    else:
        # Ambil nama file foto dari data user yang ada di database
        filename = data_user[11]
    data_user = (username, password, nama, tempat_lahir, tanggal_lahir,
                 jenis_kelamin, agama, alamat, no_telepon, email, filename, role_id, id)
    # Periksa apakah ekstensi file tidak sesuai
    if foto and '.' in foto.filename and foto.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        flash('Anda mengunggah jenis file yang salah!', 'danger')
        return redirect(url_for('update_mahasiswa', id=id))
    cur.execute("UPDATE tb_datamahasiswa SET username=%s, password=%s, nama=%s, tempat_lahir=%s, tanggal_lahir=%s, jenis_kelamin=%s, agama=%s, alamat=%s, no_telepon=%s, email=%s, foto=%s, role_id=%s WHERE id=%s", data_user)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('read_mahasiswa'))


# HAPUS DATA MAHASISWA
@application.route('/data-mahasiswa/hapus-data-mahasiswa/<int:id>')
@login_required(1)
def delete_mahasiswa(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_datamahasiswa WHERE id=%s" % id)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('read_mahasiswa'))


# DATA ADMIN
@application.route('/data-admin')
@login_required(1)
def read_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, nama, CONCAT(tempat_lahir, ',', ' ',tanggal_lahir), jenis_kelamin, agama, alamat, no_telepon, email FROM tb_dataadmin")
    data_admin = cur.fetchall()
    cur.close()
    return render_template('after login admin/data_master/data_admin.html', data_admin=data_admin)


# TAMBAH DATA ADMIN
@application.route('/data-admin/tambah-data-admin', methods=['GET', 'POST'])
@login_required(1)
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(
            request.form['password'], method='pbkdf2:sha256', salt_length=16)
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
        if role_id == 'admin':
            role_id = 1
        data_user = (username, password, nama, tempat_lahir, tanggal_lahir,
                     jenis_kelamin, agama, alamat, no_telepon, email, role_id)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_dataadmin (username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, email, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data_user)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('read_admin'))
    else:
        return render_template('after login admin/data_master/create_dataadmin.html')


# EDIT DATA ADMIN
@application.route('/data-admin/edit-data-admin/<int:id>')
@login_required(1)
def update_admin(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, nama, tempat_lahir, tanggal_lahir, jenis_kelamin, agama, alamat, no_telepon, email, role_id FROM tb_dataadmin WHERE id='%s'" % id)
    data_user = cur.fetchone()
    return render_template('after login admin/data_master/update_dataadmin.html', data_user=data_user)


@application.route('/data-admin/update-process-admin', methods=['GET', 'POST'])
@login_required(1)
def update_process_admin():
    id = request.form['id']
    username = request.form['username']
    password = generate_password_hash(
        request.form['password'], method='pbkdf2:sha256', salt_length=16)
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
    if role_id == 'admin':
        role_id = 1
    data_user = (username, password, nama, tempat_lahir, tanggal_lahir,
                 jenis_kelamin, agama, alamat, no_telepon, email, role_id, id)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tb_dataadmin SET username='%s', password='%s', nama='%s', tempat_lahir='%s', tanggal_lahir='%s', jenis_kelamin='%s', agama='%s', alamat='%s', no_telepon='%s', email='%s', role_id='%s' WHERE id=%s" % data_user)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('read_admin'))


# HAPUS DATA ADMIN
@application.route('/data-admin/hapus-data-admin/<int:id>')
@login_required(1)
def delete_admin(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_dataadmin WHERE id=%s" % id)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('read_admin'))


# DATA PROFIL ADMIN
@application.route('/profil-admin')
@login_required(1)
def profil_admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_dataadmin WHERE id=%s", (session['id'],))
    profil_admin = cur.fetchone()
    cur.close()
    return render_template('after login admin/profil_admin/data_profiladmin.html', profil_admin=profil_admin)


# EDIT FOTO PROFIL ADMIN
@application.route('/edit-foto-profil-admin', methods=['GET', 'POST'])
@login_required(1)
def edit_foto_profil_admin():
    if request.method == 'POST':
        foto = request.file['foto']
        data_user = (foto, session['id'])
        cur = mysql.connection.cursor()


# EDIT DATA DIRI ADMIN
@application.route('/edit-data-diri-admin', methods=['GET', 'POST'])
@login_required(1)
def edit_data_diri_admin():
    if request.method == 'POST':
        agama = request.form['agama']
        no_telepon = request.form['no_telepon']
        email = request.form['email']
        alamat = request.form['alamat']
        data_diri = (agama, no_telepon, email, alamat, session['id'])
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE tb_dataadmin SET agama=%s, no_telepon=%s, email=%s, alamat=%s WHERE id=%s", (data_diri))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('profil_admin'))


# EDIT PASSWORD ADMIN
@application.route('/edit-password-admin', methods=['GET', 'POST'])
@login_required(1)
def edit_password_admin():
    if request.method == 'POST':
        password_lama = request.form['password_lama']
        password_baru = request.form['password_baru']
        ulangi_password_baru = request.form['ulangi_password_baru']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM tb_dataadmin WHERE id=%s",
                    (session['id'],))
        user_password = cur.fetchone()[0]
        cur.close()

        # Validasi password lama
        if not check_password_hash(user_password, password_lama):
            error = flash(f'Password lama tidak cocok', 'danger')
            return redirect(url_for('profil_admin', _anchor='password_tab', error=error))

        # Validasi password baru dan ulangi password
        if password_baru != ulangi_password_baru:
            error = flash(
                f'Password baru dan ulangi password tidak cocok!', 'danger')
            return redirect(url_for('profil_admin', _anchor='password_tab', error=error))

        # Validasi syarat password
        if not (any(c.isupper() for c in password_baru) and any(c.isdigit() for c in password_baru) and any(not c.isalnum() for c in password_baru)):
            error = flash(
                f'Password harus terdiri dari huruf kapital, angka, dan simbol!', 'warning')
            return redirect(url_for('profil_admin', _anchor='password_tab', error=error))

        # Jika semua validasi berhasil, lakukan perubahan password
        hashed_password_baru = generate_password_hash(
            password_baru, method='pbkdf2:sha256', salt_length=16)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tb_dataadmin SET password=%s WHERE id=%s",
                    (hashed_password_baru, session['id']))
        mysql.connection.commit()
        cur.close()
        flash(f'Password anda berhasil diganti!', 'success')
        return redirect(url_for('profil_admin'))

    else:
        return redirect(url_for('profil_admin'))


# MASIH PENGEMBANGAN AKSES TANPA AKUN
# DATA TAGIHAN DAN TRANSAKSI
@application.route('/tagihan-mahasiswa')
def tagihan_mahasiswa():
    return render_template('after login admin/data_transaksi/data_tagihanmahasiswa.html')


# TAMBAH TAGIHAN MAHASISWA
@application.route('/tambah-tagihan-mahasiswa')
def create_tagihanmahasiswa():
    return render_template('after login admin/data_transaksi/create_datatagihanmahasiswa.html')


# EDIT TAGIHAN MAHASISWA
@application.route('/edit-tagihan-mahasiswa')
def update_tagihanmahasiswa():
    return render_template('after login admin/data_transaksi/update_datatagihanmahasiswa.html')


# HAPUS TAGIHAN MAHASISWA
@application.route('/hapus-tagihan-mahasiswa')
def delete_tagihanmahasiswa():
    return redirect(url_for('tagihan_mahasiswa'))


@application.route('/validasi-bukti-bayar')
def validasi_tagihan():
    return render_template('after login admin/data_transaksi/validasi.html')


# MAHASISWA AREA
@application.route('/mahasiswa')
@login_required(2)
def home_mahasiswa():
    return render_template('after login mahasiswa/dashboard/home_mahasiswa.html')


# DATA PROFIL MAHASISWA
@application.route('/profil-mahasiswa')
@login_required(2)
def profil_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_datamahasiswa WHERE id=%s", (session['id'],))
    profil_mahasiswa = cur.fetchone()
    cur.close()
    return render_template('after login mahasiswa/profil_mahasiswa/data_profilmahasiswa.html', profil_mahasiswa=profil_mahasiswa)


# EDIT DATA DIRI MAHASISWA
@application.route('/edit-data-diri-mahasiswa', methods=['GET', 'POST'])
@login_required(2)
def edit_data_diri_mahasiswa():
    if request.method == 'POST':
        agama = request.form['agama']
        no_telepon = request.form['no_telepon']
        email = request.form['email']
        alamat = request.form['alamat']
        data_diri = (agama, no_telepon, email, alamat, session['id'])
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE tb_datamahasiswa SET agama=%s, no_telepon=%s, email=%s, alamat=%s WHERE id=%s", (data_diri))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('profil_mahasiswa'))


# EDIT PASSWORD MAHASISWA
@application.route('/edit-password-mahasiswa', methods=['GET', 'POST'])
@login_required(2)
def edit_password_mahasiswa():
    if request.method == 'POST':
        password_lama = request.form['password_lama']
        password_baru = request.form['password_baru']
        ulangi_password_baru = request.form['ulangi_password_baru']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM tb_datamahasiswa WHERE id=%s",
                    (session['id'],))
        user_password = cur.fetchone()[0]
        cur.close()

        # Validasi password lama
        if not check_password_hash(user_password, password_lama):
            error = flash(f'Password lama tidak cocok', 'danger')
            return redirect(url_for('profil_mahasiswa', _anchor='password_tab', error=error))

        # Validasi password baru dan ulangi password
        if password_baru != ulangi_password_baru:
            error = flash(
                f'Password baru dan ulangi password tidak cocok!', 'danger')
            return redirect(url_for('profil_mahasiswa', _anchor='password_tab', error=error))

        # Validasi syarat password
        if not (any(c.isupper() for c in password_baru) and any(c.isdigit() for c in password_baru) and any(not c.isalnum() for c in password_baru)):
            error = flash(
                f'Password harus terdiri dari huruf kapital, angka, dan simbol!', 'warning')
            return redirect(url_for('profil_mahasiswa', _anchor='password_tab', error=error))

        # Jika semua validasi berhasil, lakukan perubahan password
        hashed_password_baru = generate_password_hash(
            password_baru, method='pbkdf2:sha256', salt_length=16)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tb_datamahasiswa SET password=%s WHERE id=%s",
                    (hashed_password_baru, session['id']))
        mysql.connection.commit()
        cur.close()
        flash(f'Password anda berhasil diganti!', 'success')
        return redirect(url_for('profil_mahasiswa'))

    else:
        return redirect(url_for('profil_mahasiswa'))

# TAGIHAN SAYA
@application.route('/tagihan-saya')
def tagihan_saya():
    return render_template('after login mahasiswa/data_transaksi/data_tagihanmahasiswa.html')


# UPLOAD BUKTI BAYAR
@application.route('/unggah-bukti-bayar')
def unggah_bukti_bayar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_datamahasiswa WHERE id=%s", (session['id'],))
    data_mahasiswa = cur.fetchall()
    cur.close()
    return render_template('after login mahasiswa/data_transaksi/bukti_bayar.html', data_mahasiswa=data_mahasiswa)


if __name__ == '__main__':
    application.run(debug=True)