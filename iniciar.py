import conexion
from flask import Flask
from flask import render_template
from flask import session,request,redirect,url_for
app= Flask(__name__)
app.secret_key="arsirtsawrkls"
conectar=conexion.conexion
#Interfaz de usuario------------------------------------
@app.route('/', methods=['POST', 'GET'])
def principal():
    return render_template("index.html")
@app.route('/<publicaciones>')
def principal_param(publicaciones):
    conectar.execute("SELECT * FROM publicaciones WHERE categoria=(%s)",[publicaciones])
    publicaciones=conectar.fetchall()
    if len(publicaciones)>=1:
        return render_template("publicaciones.html",publicacion=publicaciones)
    else:
        return "Error"

@app.route('/publicacion')
def publicacion():
    idpublicacion = request.args.get('id')
    conectar.execute("SELECT * FROM publicaciones WHERE idpublicacion=(%s)",[idpublicacion])
    publicacion=conectar.fetchall()
    return render_template("publicacion.html",publicacion=publicacion)
#-------------------------------------------------------------

@app.route('/administrador')
def administrador():
    if 'usuario' in session:
        return redirect("panel")
    else:
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


@app.route('/modificar')
def modificar():
    if 'usuario' in session:
        categoria = request.args.get('cat')
        conectar.execute("SELECT * FROM publicaciones WHERE categoria=(%s)",[categoria])
        categoria=conectar.fetchall()
        return render_template("Modificar-publicaciones.html",categoria=categoria)
    else:
        return redirect("/administrador")
@app.route('/modifi-read', methods=['POST'])
def buscar():
    tema=request.form['tema']
    return redirect("/modificar?cat=%s" %tema)

@app.route('/Edit')
def editar():
    if 'usuario' in session:
        id=request.args.get('publicacion')
        conectar.execute("SELECT * FROM publicaciones WHERE idpublicacion=(%s)",[id])
        publicacion=conectar.fetchall()
        for a in publicacion:
            titulo=a[2]
            cuerpo=a[3]
            return render_template("editar.html",id=id,titulo=titulo,cuerpo=cuerpo)
    else:
        return redirect("/administrador")
@app.route('/update', methods=['POST'])
def actualizar():
    if 'usuario' in session:
        id=request.args.get('id')
        titulo=request.form['titulo']
        categoria=request.form['tema']
        publicacion=request.form['publicacion']
        conectar.execute("UPDATE publicaciones SET categoria=%s,titulo=%s,publicacion=%s WHERE idpublicacion=%s ",[categoria,titulo,publicacion,id])
        conexion.datos.commit()
        return redirect("/panel")
    else:
        return redirect("/administrador")


if __name__=='__main__':
    app.run(debug=True, port=5000)
