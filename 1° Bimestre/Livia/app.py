from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Armazenamento dos usuários (em memória)
usuarios = {}  # chave = matrícula, valor = dict com email e senha hash

@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('bem_vindo'))
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']

        if any(user['email'] == email for user in usuarios.values()):
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))

        if matricula in usuarios:
            flash('Matrícula já cadastrada!', 'danger')
            return redirect(url_for('cadastro'))

        usuarios[matricula] = {
            'email': email,
            'senha': generate_password_hash(senha)
        }

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        user = usuarios.get(matricula)
        if user and check_password_hash(user['senha'], senha):
            session['usuario'] = matricula
            return redirect(url_for('bem_vindo'))
        else:
            flash('Matrícula ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/bem-vindo')
def bem_vindo():
    if 'usuario' not in session:
        flash('Você precisa fazer login para acessar essa página.', 'warning')
        return redirect(url_for('login'))

    return render_template('bem_vindo.html', nome=session['usuario'])

@app.route('/logout')
def logout():
    session
