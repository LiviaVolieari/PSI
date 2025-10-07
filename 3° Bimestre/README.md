# 🧩 O que é Flask-SQLAlchemy?

**Flask-SQLAlchemy** é uma extensão do Flask que facilita o uso do **SQLAlchemy** dentro de aplicações web.

👉 Ele permite criar e gerenciar bancos de dados (como SQLite, MySQL, etc.) usando classes Python, sem precisar escrever SQL manualmente.

---

## ⚙️ Instalação

```bash
pip install flask flask_sqlalchemy
```

---

## 🚀 Configuração básica

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco (aqui usamos SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco
db = SQLAlchemy(app)
```

### 🧠 Explicando:

| Linha | Função |
|-------|--------|
| `SQLALCHEMY_DATABASE_URI` | Caminho do banco de dados |
| `'sqlite:///app.db'` | Cria um arquivo `app.db` (SQLite) |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | Desliga recurso desnecessário |
| `db = SQLAlchemy(app)` | Conecta o ORM (SQLAlchemy) ao Flask |

---

## 🧱 Criando modelos (tabelas)

Um **modelo** é uma classe Python que representa uma tabela no banco.

```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
```

| Elemento | Explicação |
|-----------|------------|
| `db.Model` | Classe base de todos os modelos |
| `db.Column()` | Cria uma coluna |
| `db.Integer` | Tipo da coluna (inteiro) |
| `db.String(100)` | Texto com até 100 caracteres |
| `primary_key=True` | Define a chave primária |
| `nullable=False` | Campo obrigatório |

---

## 🧰 Criando o banco e as tabelas

```python
with app.app_context():
    db.create_all()
```

📘 Isso cria o arquivo `app.db` e as tabelas definidas nos modelos.

---

## 💾 Inserindo dados

```python
with app.app_context():
    usuario = Usuario(nome="Lívia")
    db.session.add(usuario)
    db.session.commit()
```

🧠 `session` é a “ponte” entre o Python e o banco:

- `add()` → adiciona o registro  
- `commit()` → grava no banco  

---

## 🔍 Consultando dados

```python
usuarios = Usuario.query.all()     # todos os registros
usuario = Usuario.query.first()    # primeiro registro
um_usuario = Usuario.query.get(1)  # busca pelo id
```

---

## ✏️ Atualizando dados

```python
usuario = Usuario.query.get(1)
usuario.nome = "Lívia Tainá"
db.session.commit()
```

---

## 🗑️ Deletando dados

```python
usuario = Usuario.query.get(1)
db.session.delete(usuario)
db.session.commit()
```

---

## 🤝 Relacionamentos

### 🔹 1:N (Um para Muitos)

Exemplo: um time tem vários jogadores.

```python
class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    jogadores = db.relationship('Jogador', backref='time', lazy=True)

class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'))
```

| Termo | Explicação |
|--------|-------------|
| `ForeignKey('time.id')` | Cria o vínculo com a tabela `time` |
| `relationship('Jogador')` | Cria a ligação entre as classes |
| `backref='time'` | Permite acessar o time a partir do jogador |
| `lazy=True` | Carrega os dados quando forem acessados |

➡️ **Uso:**

```python
jogador = Jogador.query.first()
print(jogador.time.nome)  # mostra o nome do time do jogador
```

---

### 🔹 N:N (Muitos para Muitos)

Exemplo: um usuário participa de vários times e um time tem vários usuários.

```python
usuarios_times = db.Table(
    'usuarios_times',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('time_id', db.Integer, db.ForeignKey('time.id'), primary_key=True)
)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    times = db.relationship('Time', secondary=usuarios_times, back_populates='usuarios')

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    usuarios = db.relationship('Usuario', secondary=usuarios_times, back_populates='times')
```

➡️ **Uso:**

```python
usuario = Usuario.query.first()
print(usuario.times)  # lista de times do usuário
```

---

### 🔹 Auto-relacionamento (opcional)

Exemplo: usuário que é gerente de outros usuários.

```python
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    gerente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    gerenciados = db.relationship('Usuario', backref=db.backref('gerente', remote_side=[id]))
```

---

## ⚙️ Estrutura típica de app Flask com banco

```
📁 projeto/
 ├── app.py
 ├── templates/
 │   ├── index.html
 │   ├── usuarios.html
 │   └── times.html
 └── app.db
```

---

## 🔁 Comandos importantes

| Comando | Função |
|----------|--------|
| `db.create_all()` | Cria tabelas |
| `db.drop_all()` | Apaga tabelas |
| `db.session.add()` | Adiciona objeto |
| `db.session.commit()` | Salva no banco |
| `Model.query.all()` | Lista todos |
| `Model.query.get(id)` | Busca por ID |
| `db.ForeignKey()` | Cria chave estrangeira |
| `db.relationship()` | Cria ligação entre tabelas |

---

## 🧠 Resumo final

| Conceito | Significado |
|-----------|-------------|
| ORM | Mapeamento Objeto-Relacional |
| Modelo | Classe Python que representa uma tabela |
| Atributo | Coluna do banco |
| Registro | Objeto da classe |
| ForeignKey | Cria ligação entre tabelas |
| relationship | Cria relação entre objetos |
| 1:N | Um registro tem vários relacionados |
| N:N | Vários registros se relacionam com vários outros |
