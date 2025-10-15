from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_personas = Blueprint("rutas_personas", __name__)
API_URL = "http://localhost:5000/api/v1/persona"

@rutas_personas.route("/personas")
def personas():
    try:
        resp = requests.get(API_URL)
        print("Respuesta personas API:", resp.text)
        personas = resp.json().get("datos", [])
    except Exception as e:
        personas = []
        print("Error al conectar con la API (personas):", e)
    return render_template("personas.html", personas=personas, persona=None, modo="crear")

@rutas_personas.route("/personas/buscar", methods=["POST"])
def buscar_persona():
    codigo = request.form.get("codigo_buscar")
    if codigo:
        try:
            resp = requests.get(f"{API_URL}/codigo/{codigo}")
            if resp.status_code == 200:
                datos = resp.json().get("datos", [])
                if datos:
                    persona = datos[0]
                    personas = requests.get(API_URL).json().get("datos", [])
                    return render_template("personas.html", personas=personas, persona=persona, modo="actualizar")
        except Exception as e:
            return f"Error en la búsqueda (persona): {e}"
    personas = requests.get(API_URL).json().get("datos", [])
    return render_template("personas.html", personas=personas, persona=None, mensaje="Persona no encontrada", modo="crear")

@rutas_personas.route("/personas/crear", methods=["POST"])
def crear_persona():
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "email": request.form.get("email"),
        "telefono": request.form.get("telefono")
    }
    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear persona: {e}"
    return redirect(url_for("rutas_personas.personas"))

@rutas_personas.route("/personas/actualizar", methods=["POST"])
def actualizar_persona():
    codigo = request.form.get("codigo")
    datos = {
        "nombre": request.form.get("nombre"),
        "email": request.form.get("email"),
        "telefono": request.form.get("telefono")
    }
    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar persona: {e}"
    return redirect(url_for("rutas_personas.personas"))

@rutas_personas.route("/personas/eliminar/<string:codigo>", methods=["POST"])
def eliminar_persona(codigo):
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar persona: {e}"
    return redirect(url_for("rutas_personas.personas"))
