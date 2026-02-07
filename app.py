from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

# CONEXIÓN A MYSQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistema_api"
)
cursor = db.cursor(dictionary=True)

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        user = cursor.fetchone()

        if user:
            if check_password_hash(user["password"], password):
                session["user"] = usuario
                flash("Inicio de sesión exitoso ✅", "success")
                return redirect("/dashboard")
            else:
                flash("Contraseña incorrecta ❌", "danger")
        else:
            flash("Usuario no encontrado ❌", "danger")

    return render_template("login.html")


# ---------- REGISTRO ----------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        password_segura = generate_password_hash(password)

        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
                (usuario, password_segura)
            )
            db.commit()
            flash("Registro exitoso 🎉 Ahora puedes iniciar sesión", "success")
            return redirect("/")
        except:
            flash("El usuario ya existe ⚠️", "warning")

    return render_template("registro.html")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
