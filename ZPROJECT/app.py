from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projectx",
    password="")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = cnx.cursor()
    query = ("select * from user where username = %s and password = %s")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('admin'))
    else:
        return f"salah username atau password!!!"

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))
    



@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    nama_pasar = request.form["nama_pasar"]
    lokasi_pasar = request.form["lokasi_pasar"]
    rata_rata = request.form["rata_rata"]
    tahun_berdiri = request.form["tahun_berdiri"]
    cursor = cnx.cursor()
    query = ("insert into pasar values( %s, %s, %s, %s,%s)")
    data = ( "1", nama_pasar, lokasi_pasar, tahun_berdiri,rata_rata )
    cursor.execute( query, data )
   
    cursor.close()
    return render_template('tampil.html',data=data)

@app.route('/tampil')
def tampil():
    cursor = cnx.cursor()
    cursor.execute("select * from pasar")
    data = cursor.fetchall()
    cursor.close()
    return render_template('tampil.html',data=data) 

@app.route('/hapus/<id>')
def hapus(id):
    cursor = cnx.cursor()
    query = ("delete from pasar where id_pasar = %s")
    data = (id,)
    cursor.execute( query, data )
    cursor.close()
    return redirect('/tampil')

@app.route('/update/<id>')
def update(id):
    cursor = cnx.cursor()
    sql = ("select * from pasar where id_pasar = %s")
    data = (id,)
    cursor.execute( sql, data )
    value = cursor.fetchone()
    return render_template('update.html',value=value) 


@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    id = request.form["id_pasar"]
    nama_pasar = request.form["nama_pasar"]
    lokasi_pasar = request.form["lokasi_pasar"]
    tahun_berdiri = request.form["tahun_berdiri"]
    rata_rata = request.form["rata_rata"]
    cursor = cnx.cursor()
    # query = ("insert into pasar values( %s, %s, %s, %s,%s)")
    query = ("update pasar set nama_pasar = %s, lokasi_pasar = %s, tahun_berdiri = %s , rata_rata_pengunjung = %s  where id_pasar= %s")
    data = ( nama_pasar,lokasi_pasar,tahun_berdiri, rata_rata, id )
    cursor.execute( query, data )
    cursor.close()
    return redirect('/tampil')


if __name__ == "__main__":
    app.run(debug=True)
