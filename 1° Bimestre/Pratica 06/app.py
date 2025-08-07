from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RANCA TAMPA E MANDA BOI'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# usuários no formato {username: senha}
usuarios = {}

# produtos disponíveis
produtos_ = {
    'gibao': 500,
    'bota': 1500,
    'espora': 200,
    'carralo': 15000,
    'bezerro': 3000,
    'chape': 500,
    'oculos': 1500,
    'capacete': 300
}

# Carrinhos por usuário (em memória)
carrinhos = {}

# Classe de usuário para flask_login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return User(user_id)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome in usuarios and usuarios[nome] == senha:
            user = User(nome)
            login_user(user)
            carrinhos.setdefault(nome, [])
            return redirect(url_for('produtos'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome not in usuarios:
            usuarios[nome] = senha
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/produtos')
@login_required
def produtos():
    return render_template('produtos.html', produtos=produtos_)



@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    prod = request.form['prod']
    carrinhos[current_user.id].append(prod)
    return redirect(url_for('carrinho'))

@app.route('/remover', methods=['POST'])
@login_required
def remover():
    prod = request.form['prod']
    carrinho = carrinhos[current_user.id]
    if prod in carrinho:
        carrinho.remove(prod)
    return redirect(url_for('carrinho'))


@app.route('/carrinho')
@login_required
def carrinho():
    carrinho_ = carrinhos.get(current_user.id, [])
    soma = sum(produtos_[p] for p in carrinho_)
    return render_template('carrinho.html', carrinho=carrinho_, valor=soma, produtos=produtos_)
