from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ubicación de la base de datos
DATABASE = os.path.join(app.root_path, "database.db")


# --------------------------------------------------
# CONEXIÓN A LA BASE DE DATOS
# --------------------------------------------------
def conectar_bd():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


# --------------------------------------------------
# CREAR ESTRUCTURA DE LA BASE DE DATOS
# --------------------------------------------------
def crear_bd():
    conexion = sqlite3.connect(DATABASE)

    ruta_schema = os.path.join(app.root_path, "schema.sql")

    with open(ruta_schema, "r", encoding="utf-8") as archivo:
        conexion.executescript(archivo.read())

    conexion.close()


# --------------------------------------------------
# RUTA PRINCIPAL
# --------------------------------------------------
@app.route("/")
def inicio():

    conexion = conectar_bd()

    contactos = conexion.execute(
        "SELECT * FROM contactos ORDER BY id DESC"
    ).fetchall()

    conexion.close()

    return render_template(
        "index.html",
        contactos=contactos
    )


# --------------------------------------------------
# RUTA DEL FORMULARIO
# --------------------------------------------------
@app.route("/formulario", methods=["GET", "POST"])
def formulario():

    if request.method == "POST":

        # Recibir información del formulario
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        # Guardar información en la base de datos
        conexion = conectar_bd()

        conexion.execute(
            """
            INSERT INTO contactos (nombre, correo, mensaje)
            VALUES (?, ?, ?)
            """,
            (nombre, correo, mensaje)
        )

        conexion.commit()
        conexion.close()

        # Regresar a la página principal
        return redirect(url_for("inicio"))

    return render_template("formulario.html")


# --------------------------------------------------
# INICIAR SERVIDOR
# --------------------------------------------------
if __name__ == "__main__":
    crear_bd()
    app.run(debug=True)