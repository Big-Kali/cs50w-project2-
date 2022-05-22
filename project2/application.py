

from distutils.log import error
import os


from flask import Flask, jsonify, redirect, render_template, request, make_response
from flask_socketio import SocketIO, send, emit, join_room
from sqlalchemy import false, true


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


session = []


def validarCanal(nombre, lista):
    existente = False
    for canales in lista:
        if canales["name"] == nombre:
            existente = True
            break
    return existente


list_canales = [{
    'name': 'pan',
    'mensaje': [
        {
            'name': 'Usuario',
            'text': 'Este mensaje fue enviado'
        }
    ]
}]

"""
canales = {
    "id":{
        "canales":[]
    }
}
"""

diccionario = {
    "nickname": {



        "nombre": []




    }
}


@ app.route("/")
def index():
    get_nombre = request.cookies.get("session")
    return render_template('index.html', get_nombre=get_nombre)


@ socketio.on("usuario")
def verificar_user():
    join_room("private_user")
    emit("private_user", session, room="private_user")


@ socketio.on("register")
def registrar(nombre):
    existente = False
    if nombre in diccionario:
        existente = True

    else:
        session.append(nombre)
        diccionario[nombre] = {
            "name": nombre
        }

    join_room("register_ok")
    emit("register_ok", existente, nombre, room="register_ok")


@app.route('/register', methods=["POST"])
def register():
    name = request.form.get("nickname")
    nombre_existente = False
    if name in diccionario or name is None:
        nombre_existente = True
        return jsonify({"existente": nombre_existente}), 403

    repuesta = make_response(jsonify({"existente": nombre_existente}))
    repuesta.set_cookie("session", name)

    session.append(name)
    diccionario[name] = {
        "name": name

    }

    return repuesta


@app.route("/canal_unico", methods=["POST"])
def canal():
    nombre = request.form.get("canal")
    if nombre != None and not validarCanal(nombre, list_canales):
        list_canales.append({"name": nombre, "mensaje": []})
        return jsonify({"completado": True})

    return jsonify({"completado": False})


@socketio.on('listar_canales')
def permiso():

    join_room("send_canal")
    emit("send_canal", list_canales, room="send_canal")


@app.route('/canal/<nombre>', methods=['POST', 'GET'])
def canales(nombre):
    index_canal = None
    for canaleta in list_canales:
        print(canaleta)
        if canaleta['name'] == nombre:
            index_canal = canaleta
            break
    if index_canal is None:
        return redirect('/')
    return render_template("canales.html", canaleta=index_canal)


@app.route("/menssage", methods=["POST"])
def mensajes():
    mensajes_canal = None
    for mensajes_canales in list_canales:
        print(mensajes_canales)

        if mensajes_canales['name'] == request.form.get("nombre"):
            mensajes_canales["mensaje"].append({"name":request.cookies.get("session"),"text": request.form.get("canal")})
            mensajes_canal = mensajes_canales["mensaje"]
            
    if mensajes_canal is None:
        return jsonify({"error": True})
    
    return jsonify({"mensajes": mensajes_canal})

@socketio.on('cargar')
def cargares(nombre):
    
    mensajes_canal = None
    print(nombre,"estes es el nombre buscado")
    for mensajes_canales in list_canales:
        print(mensajes_canales)

        if mensajes_canales['name'] == nombre:
            
            mensajes_canal = mensajes_canales["mensaje"]
    join_room(nombre)
    emit(nombre, mensajes_canal, room=nombre)


if __name__ == '__main__':
    socketio.run(app, debug=True)
