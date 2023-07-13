from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

app=Flask(__name__,template_folder='template')
app.secret_key="flash message"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='student'

mysql=MySQL(app)

@app.route('/')
def home():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM stmarks")
    stData=cur.fetchall()
    cur.close()
    return render_template("Home.html",students=stData)

@app.route('/insert',methods = ['post'])
def insert():
    if request.method == "POST":
        flash("Data Insert Successful")
        Name=request.form['stname']
        Maths = request.form['stmaths']
        Physics = request.form['stphysics']
        Chemistry = request.form['stChemistry']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO stmarks (Name,Maths,Physics,Chemistry) VALUES (%s,%s,%s,%s)",(Name,Maths,Physics,Chemistry))
        mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/update',methods=['post','get'])
def update():
    if request.method == "POST":
        id_data = request.form['id']
        name = request.form['stname']
        maths = request.form['stmaths']
        physics = request.form['stphysics']
        chemi = request.form['stChemistry']

        cur = mysql.connection.cursor()
        cur.execute("""

            UPDATE stmarks
            SET Name=%s, Maths=%s, Physics=%s, Chemistry=%s
            WHERE id=%s

            """, (name, maths, physics, chemi, id_data))
        flash("Data Update Successfully")
        mysql.connection.commit()

    return redirect(url_for('home'))

@app.route('/delete/<id>',methods=['post','get'])
def delete(id):
    if request.method=="POST":
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM stmarks WHERE id=%s", (id,))
        mysql.connection.commit()
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True)