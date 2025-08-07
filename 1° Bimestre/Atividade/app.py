from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    #retorna reposta

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        # 'nome' é o atributo name do input
        nome = request.form['nome']
        genero = request.form['genero']



        # return "Em construção " + genero3
        # return "Em construção " + nome
        response = make_response(redirect(url_for('preferencia')))
        response.set_cookie(nome, genero, max_age=7*24*3600)
        return response
@app.route('/preferencia')
def preferencia():

    valor = request.cookies['nome']
    return valor

@app.route('/recomendar')
def recomendar():
    pass


