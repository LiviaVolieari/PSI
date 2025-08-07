from flask import Flask, render_template, request, make_response, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votar', methods = ['GET', 'POST'])
def votar():
    if request.method == 'GET':
        return render_template('votar.html')
    else:
        # 'nome' é o atributo name do input
        nome = request.form['nome']
        genero = request.form['genero']

    genero_escolhido = request.args.get('genero')
    response = make_response(redirect(url_for('resultado', genero_escolhi = genero_escolhido)))
    #foi não rapaz
    response.set_cookie(nome, genero, max_age=300)
    response = nome + "  -  " + genero
    return response

@app.route('/resultado')
def resultado():
    return "Não soube exibir aqui"

    