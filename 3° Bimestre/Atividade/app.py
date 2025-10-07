import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

# -------------------------
# CONFIG
# -------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///times.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------
# MODELOS (com __tablename__)
# -------------------------
usuario_time = db.Table(
    'usuario_time',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('time_id', db.Integer, db.ForeignKey('time.id'), primary_key=True)
)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    times = db.relationship('Time', secondary=usuario_time, back_populates='usuarios')

class Time(db.Model):
    __tablename__ = 'time'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuarios = db.relationship('Usuario', secondary=usuario_time, back_populates='times')
    jogadores = db.relationship('Jogador', backref='time', lazy=True)

class Jogador(db.Model):
    __tablename__ = 'jogador'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'))

# -------------------------
# CRIA AS TABELAS (IMPORT SAFE)
# -------------------------
# Colocado aqui (após os modelos) para funcionar tanto com "python app.py" quanto com "flask run"

with app.app_context():
    db.create_all()

# -------------------------
# ROTAS (exemplos)
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        nome = request.form['nome']
        db.session.add(Usuario(nome=nome))
        db.session.commit()
        return redirect(url_for('usuarios'))
    return render_template('usuarios.html', usuarios=Usuario.query.all())

@app.route('/times', methods=['GET', 'POST'])
def times():
    if request.method == 'POST':
        nome = request.form['nome']
        db.session.add(Time(nome=nome))
        db.session.commit()
        return redirect(url_for('times'))
    return render_template('times.html', times=Time.query.all())

@app.route('/vincular', methods=['GET', 'POST'])
def vincular():
    if request.method == 'POST':
        u_id = int(request.form['usuario_id'])
        t_id = int(request.form['time_id'])
        u = Usuario.query.get(u_id)
        t = Time.query.get(t_id)
        if t not in u.times:
            u.times.append(t)
            db.session.commit()
        return redirect(url_for('vincular'))
    return render_template('vincular.html', usuarios=Usuario.query.all(), times=Time.query.all())

@app.route('/jogadores', methods=['GET', 'POST'])
def jogadores():
    if request.method == 'POST':
        nome = request.form['nome']
        time_id = int(request.form['time_id'])
        db.session.add(Jogador(nome=nome, time_id=time_id))
        db.session.commit()
        return redirect(url_for('jogadores'))
    return render_template('jogadores.html', jogadores=Jogador.query.all(), times=Time.query.all())

# # -------------------------
# # ROTA DE DEBUG (veja pasta e tabelas)
# # -------------------------
# @app.route('/_tables')
# def _tables():
#     inspector = inspect(db.engine)
#     return jsonify({
#         "cwd": os.getcwd(),
#         "db_uri": app.config['SQLALCHEMY_DATABASE_URI'],
#         "tables": inspector.get_table_names()
#     })

# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
