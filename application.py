import os

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
    return render_template("index.html")


@app.route("/reg", methods=["GET", "POST"])
def registro():
    """Register user"""

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

        nicks = db.execute("""
            INSERT INTO users(username, password)
            VALUES(:username, :password) RETURNING id, username
        """,{
            "username": username,
            "password": generate_password_hash(password)
        }
        ).fetchone()

        db.commit()
        session["user_id"] = nicks[0]
        session["username"] = nicks[1]

        flash("Registrado con exito")

        # redirecciona a la home page
        return render_template("index.html")

    else:
        return render_template("reg.html")    
