import os
from sys import argv

from flask import Flask, redirect, render_template, request, session, redirect,url_for, flash
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    session.clear()
    return render_template("login.html")

@app.route("/ind")
def busqueda():
    return render_template("ind.html")

@app.route("/login")
def ingreso():
    return render_template("login.html")

@app.route("/reg", methods=["GET", "POST"])
def registro():
    session.clear()

    if request.method == "POST":
    
        # asegura se haya elegido un usuario
        if not request.form.get("username"):
            flash("Usuario requerido")
            print("falla users")
            return render_template("reg.html")

        # asegura que haya una contraseña
        elif not request.form.get("password"):
            flash("Contraseña requerida")
            print("falla password")
            return render_template("reg.html")

        # Asegura que las contraseñas coincidan
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Contraseñas no coinciden")
            print("falla confirm")
            return render_template("reg.html")

        elif not request.form.get("mail"):
            flash("Correo Requerido")
            print("falla correo")
            return render_template("reg.html")

        username = request.form.get("username")
        password = request.form.get("password")
        mail = request.form.get("mail")

        nicks = db.execute("""
            INSERT INTO usersf(username, password, mail)
            VALUES(:username, :password, :mail) RETURNING id, username
        """,{
            "username": username,
            "mail": mail,
            "password": generate_password_hash(password)
        }
        ).fetchone()

        db.commit()
        session["user_id"] = nicks[0]
        session["username"] = nicks[1]

        flash("Registrado con exito")

        # redirecciona a la home page
        return render_template("ind.html")
    else:
        return render_template("reg.html")    

@app.route("/log", methods=["POST"])
def login():
    session.clear()

    if request.method == "POST":

        mail = request.form.get('mail')
        password = request.form.get('password')

        result = db.execute("select * from usersf where mail=:mail", {"mail": mail}
        ).fetchone()

        if not result:
            print("valimos")
            return render_template("login.html")
        else:
            if check_password_hash(result[2], password):
                print("iniciando sesión...")
            
                session["user_id"] = result[0]
                session["username"] = result[1]
            else:
                print("contraseña incorrecta")
                return render_template("login.html")
        
        return render_template("ind.html")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/search", methods=["POST"])
def search():

    if request.method == "POST":

        if request.form.get("search"):
            search= request.form.get("search").lower()
            print("1")

        if request.args.get("search"):
            search= request.args.get("search").lower()
            print("2")

        search1 = "%" + search + "%"
        books = db.execute("select * from books where lower(title) like :search or lower(author) like :search or lower(isbn) like :search or lower(year) like :search",
                            {"search": search1}
                            ).fetchall()
        print("3")
        return render_template("search.html", datos=books)

    else:
        flash("Busqueda Incorrecta")

@app.route("/info")
def inf():
    return render_template("info.html")