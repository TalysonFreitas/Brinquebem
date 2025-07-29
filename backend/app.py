# app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from flask_cors import CORS
from models import db, Usuario
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Rota para cadastrar usuário
@app.route('/cadastra', methods=['POST'])
def criar_usuario():
    dados = request.json

    if Usuario.query.filter_by(email=dados['email']).first():
        return jsonify({"erro": "Email já cadastrado"}), 409

    usuario = Usuario(
        nome=dados['nome'],
        email=dados['email'],
        cpf=dados['cpf'],
        endereco=dados['endereco'],
        cidade=dados['cidade']
    )
    usuario.set_senha(dados['senha'])

    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict()), 201

# Rota para realizar o login 
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario = Usuario.query.filter_by(email=dados['email']).first()

    if usuario and usuario.verificar_senha(dados['senha']):
        token = create_access_token(identity=usuario.id)
        return jsonify(access_token=token)
    return jsonify({"erro": "Credenciais inválidas"}), 401
