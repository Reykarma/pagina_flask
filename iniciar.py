import conexion
from flask import Flask
from flask import render_template
from flask import session,request,redirect,url_for
app= Flask(__name__)
app.secret_key="arsirtsawrkls"
conectar=conexion.conexion

@app.route('/', methods=['POST', 'GET'])
def principal():
    return render_template("index.html")
@app.route('/<parametro>')
def principal_param(parametro):
    conectar.execute("SELECT * FROM publicaciones WHERE categoria=(%s)",[parametro])
    publicaciones=conectar.fetchall()
    if len(publicaciones)>=1:
        return render_template("publicaciones.html",publicacion=publicaciones)
    else:
        return "Error"


@app.route('/administrador')
def administrador():
    return render_template("administrador.html")

@app.route('/verifi', methods=['POST'])
def verificar():
    usuario=request.form['usuario']
    contraseña=request.form['contraseña']
    conectar.execute("SELECT * FROM Usuarios WHERE Usuario=(%s) AND contrasena=(%s)",[usuario, contraseña])
    respuesta=conectar.fetchone()
    if respuesta != None:
        session['usuario']=request.form['usuario']
        return redirect("/panel")
    else:
        return redirect(url_for("administrador"))

@app.route('/panel')
def panel():
    if 'usuario' in session:
        return render_template("inicio-panel.html",usuario=session['usuario'])
    else:
        return redirect("/administrador")

@app.route('/nueva')
def nueva_publicacion():
    if 'usuario' in session:
        return render_template("nueva-publicacion.html")
    else :
        return redirect("/administrador")

@app.route('/addnew', methods=['POST'])
def agregar_nueva():
    titulo=request.form['titulo']
    categoria=request.form['tema']
    publicacion=request.form['publicacion']
    conectar.execute("INSERT INTO publicaciones(categoria,titulo,publicacion) VALUES (%s,%s,%s)",[categoria,titulo,publicacion])
    conexion.datos.commit()
    if 'usuario' in session:
        return redirect("/panel")
    else:
        return redirect("/administrador")

if __name__=='__main__':
    app.run(debug=True, port=5000)
