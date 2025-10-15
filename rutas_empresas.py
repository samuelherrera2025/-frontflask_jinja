from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_empresas = Blueprint("rutas_empresas", __name__)
API_URL = "http://localhost:5000/api/empresa"

@rutas_empresas.route("/empresas")
def empresas():
    try:
        resp = requests.get(API_URL)
        print("Respuesta empresas API:", resp.text)
        empresas = resp.json().get("datos", [])
    except Exception as e:
        empresas = []
        print("Error al conectar con la API (empresas):", e)
    return render_template("empresas.html", empresas=empresas, empresa=None, modo="crear")

@rutas_empresas.route("/empresas/buscar", methods=["POST"])
def buscar_empresa():
    codigo = request.form.get("codigo_buscar")
    if codigo:
        try:
            resp = requests.get(f"{API_URL}/codigo/{codigo}")
            if resp.status_code == 200:
                datos = resp.json().get("datos", [])
                if datos:
                    empresa = datos[0]
                    empresas = requests.get(API_URL).json().get("datos", [])
                    return render_template("empresas.html", empresas=empresas, empresa=empresa, modo="actualizar")
        except Exception as e:
            return f"Error en la búsqueda (empresa): {e}"
    empresas = requests.get(API_URL).json().get("datos", [])
    return render_template("empresas.html", empresas=empresas, empresa=None, mensaje="Empresa no encontrada", modo="crear")

@rutas_empresas.route("/empresas/crear", methods=["POST"])
def crear_empresa():
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre")
    }
    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear empresa: {e}"
    return redirect(url_for("rutas_empresas.empresas"))

@rutas_empresas.route("/empresas/actualizar", methods=["POST"])
def actualizar_empresa():
    codigo = request.form.get("codigo")
    datos = {
        "nombre": request.form.get("nombre")
    }
    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar empresa: {e}"
    return redirect(url_for("rutas_empresas.empresas"))

@rutas_empresas.route("/empresas/eliminar/<string:codigo>", methods=["POST"])
def eliminar_empresa(codigo):
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar empresa: {e}"
    return redirect(url_for("rutas_empresas.empresas"))
