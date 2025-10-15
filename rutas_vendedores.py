from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_vendedores = Blueprint("rutas_vendedores", __name__)
API_URL = "http://localhost:5000/api/vendedor"

@rutas_vendedores.route("/vendedores")
def vendedores():
    try:
        resp = requests.get(API_URL)
        print("Respuesta vendedores API:", resp.text)
        vendedores = resp.json().get("datos", [])
    except Exception as e:
        vendedores = []
        print("Error al conectar con la API (vendedores):", e)
    return render_template("vendedores.html", vendedores=vendedores, vendedor=None, modo="crear")

@rutas_vendedores.route("/vendedores/buscar", methods=["POST"])
def buscar_vendedor():
    idbus = request.form.get("codigo_buscar")
    if idbus:
        try:
            resp = requests.get(f"{API_URL}/id/{idbus}")
            if resp.status_code == 200:
                datos = resp.json().get("datos", [])
                if datos:
                    vendedor = datos[0]
                    vendedores = requests.get(API_URL).json().get("datos", [])
                    return render_template("vendedores.html", vendedores=vendedores, vendedor=vendedor, modo="actualizar")
        except Exception as e:
            return f"Error en la búsqueda (vendedor): {e}"
    vendedores = requests.get(API_URL).json().get("datos", [])
    return render_template("vendedores.html", vendedores=vendedores, vendedor=None, mensaje="Vendedor no encontrado", modo="crear")

@rutas_vendedores.route("/vendedores/crear", methods=["POST"])
def crear_vendedor():
    datos = {
        "carnet": int(request.form.get("carnet", 0)),
        "direccion": request.form.get("direccion"),
        "fkcodpersona": request.form.get("fkcodpersona")
    }
    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear vendedor: {e}"
    return redirect(url_for("rutas_vendedores.vendedores"))

@rutas_vendedores.route("/vendedores/actualizar", methods=["POST"])
def actualizar_vendedor():
    idv = request.form.get("id")
    datos = {
        "carnet": int(request.form.get("carnet", 0)),
        "direccion": request.form.get("direccion"),
        "fkcodpersona": request.form.get("fkcodpersona")
    }
    try:
        requests.put(f"{API_URL}/id/{idv}", json=datos)
    except Exception as e:
        return f"Error al actualizar vendedor: {e}"
    return redirect(url_for("rutas_vendedores.vendedores"))

@rutas_vendedores.route("/vendedores/eliminar/<int:idv>", methods=["POST"])
def eliminar_vendedor(idv):
    try:
        requests.delete(f"{API_URL}/id/{idv}")
    except Exception as e:
        return f"Error al eliminar vendedor: {e}"
    return redirect(url_for("rutas_vendedores.vendedores"))
