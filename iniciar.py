from flask import Flask
from flask import render_template

app= Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def principal():
    return render_template("index.html")

@app.route('/administrador')
def administrador():
    return render_template("administrador.html")

if __name__=='__main__':
    app.run(debug=True, port=5000)
