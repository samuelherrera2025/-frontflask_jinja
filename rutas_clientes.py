from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_clientes = Blueprint("rutas_clientes", __name__)
API_URL = "http://localhost:5000/api/v1/cliente"

@rutas_clientes.route("/clientes")
def clientes():
    try:
        resp = requests.get(API_URL)
        print("Respuesta clientes API:", resp.text)
        clientes = resp.json().get("datos", [])
    except Exception as e:
        clientes = []
        print("Error al conectar con la API (clientes):", e)
    return render_template("clientes.html", clientes=clientes, cliente=None, modo="crear")

@rutas_clientes.route("/clientes/buscar", methods=["POST"])
def buscar_cliente():
    codigo = request.form.get("codigo_buscar")
    if codigo:
        try:
            resp = requests.get(f"{API_URL}/id/{codigo}")
            if resp.status_code == 200:
                datos = resp.json().get("datos", [])
                if datos:
                    cliente = datos[0]
                    clientes = requests.get(API_URL).json().get("datos", [])
                    return render_template("clientes.html", clientes=clientes, cliente=cliente, modo="actualizar")
        except Exception as e:
            return f"Error en la búsqueda (cliente): {e}"
    clientes = requests.get(API_URL).json().get("datos", [])
    return render_template("clientes.html", clientes=clientes, cliente=None, mensaje="Cliente no encontrado", modo="crear")

@rutas_clientes.route("/clientes/crear", methods=["POST"])
def crear_cliente():
    datos = {
        "credito": float(request.form.get("credito", 0)),
        "fkcodpersona": request.form.get("fkcodpersona"),
        "fkcodempresa": request.form.get("fkcodempresa")
    }
    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear cliente: {e}"
    return redirect(url_for("rutas_clientes.clientes"))

@rutas_clientes.route("/clientes/actualizar", methods=["POST"])
def actualizar_cliente():
    id_cliente = request.form.get("id")
    datos = {
        "credito": float(request.form.get("credito", 0)),
        "fkcodpersona": request.form.get("fkcodpersona"),
        "fkcodempresa": request.form.get("fkcodempresa")
    }
    try:
        requests.put(f"{API_URL}/id/{id_cliente}", json=datos)
    except Exception as e:
        return f"Error al actualizar cliente: {e}"
    return redirect(url_for("rutas_clientes.clientes"))

@rutas_clientes.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar_cliente(id_cliente):
    try:
        requests.delete(f"{API_URL}/id/{id_cliente}")
    except Exception as e:
        return f"Error al eliminar cliente: {e}"
    return redirect(url_for("rutas_clientes.clientes"))
