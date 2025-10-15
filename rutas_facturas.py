from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_facturas = Blueprint("rutas_facturas", __name__)
API_URL = "http://localhost:5000/api/factura"

@rutas_facturas.route("/facturas")
def facturas():
    try:
        resp = requests.get(API_URL)
        print("Respuesta facturas API:", resp.text)
        facturas = resp.json().get("datos", [])
    except Exception as e:
        facturas = []
        print("Error al conectar con la API (facturas):", e)
    return render_template("facturas.html", facturas=facturas, factura=None, modo="crear")

@rutas_facturas.route("/facturas/buscar", methods=["POST"])
def buscar_factura():
    numero = request.form.get("codigo_buscar")
    if numero:
        try:
            resp = requests.get(f"{API_URL}/numero/{numero}")
            if resp.status_code == 200:
                datos = resp.json().get("datos", [])
                if datos:
                    factura = datos[0]
                    facturas = requests.get(API_URL).json().get("datos", [])
                    return render_template("facturas.html", facturas=facturas, factura=factura, modo="actualizar")
        except Exception as e:
            return f"Error en la búsqueda (factura): {e}"
    facturas = requests.get(API_URL).json().get("datos", [])
    return render_template("facturas.html", facturas=facturas, factura=None, mensaje="Factura no encontrada", modo="crear")

@rutas_facturas.route("/facturas/crear", methods=["POST"])
def crear_factura():
    datos = {
        # 'numero' normalmente auto-generado por la DB; no lo solicitamos en formulario.
        "fecha": request.form.get("fecha"),
        "total": float(request.form.get("total", 0)),
        "fkidcliente": int(request.form.get("fkidcliente")),
        "fkidvendedor": int(request.form.get("fkidvendedor"))
    }
    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear factura: {e}"
    return redirect(url_for("rutas_facturas.facturas"))

@rutas_facturas.route("/facturas/actualizar", methods=["POST"])
def actualizar_factura():
    numero = request.form.get("numero")
    datos = {
        "fecha": request.form.get("fecha"),
        "total": float(request.form.get("total", 0)),
        "fkidcliente": int(request.form.get("fkidcliente")),
        "fkidvendedor": int(request.form.get("fkidvendedor"))
    }
    try:
        requests.put(f"{API_URL}/numero/{numero}", json=datos)
    except Exception as e:
        return f"Error al actualizar factura: {e}"
    return redirect(url_for("rutas_facturas.facturas"))

@rutas_facturas.route("/facturas/eliminar/<int:numero>", methods=["POST"])
def eliminar_factura(numero):
    try:
        requests.delete(f"{API_URL}/numero/{numero}")
    except Exception as e:
        return f"Error al eliminar factura: {e}"
    return redirect(url_for("rutas_facturas.facturas"))
