from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

class Receita(db.Model):
    __tablename__ = 'receitas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String)
    data = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, default='Não recebido')

    usuario = db.relationship('Usuario')

class Despesa(db.Model):
    __tablename__ = 'despesas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    descricao = db.Column(db.String, nullable=False)
    valor_estimado = db.Column(db.Float)
    valor_real = db.Column(db.Float)
    status = db.Column(db.String, default='Pendente')
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date)

    usuario = db.relationship('Usuario')

class DespesaDetalhe(db.Model):
    __tablename__ = 'despesas_detalhes'
    id = db.Column(db.Integer, primary_key=True)
    despesa_id = db.Column(db.Integer, db.ForeignKey('despesas.id'), nullable=False)
    descricao = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)

    despesa = db.relationship('Despesa', backref='detalhes')
