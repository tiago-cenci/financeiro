from flask import Flask, request, jsonify
from config import Config
from models import db, Usuario, Receita, Despesa, DespesaDetalhe
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Rota de teste
@app.route('/')
def index():
    return 'API Controle Financeiro OK ✅'


# ==== USUÁRIOS ====

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    usuario = Usuario(nome=data['nome'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'id': usuario.id, 'nome': usuario.nome})


@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nome': u.nome} for u in usuarios])


# ==== RECEITAS ====

@app.route('/receitas', methods=['POST'])
def criar_receita():
    data = request.json
    receita = Receita(
        usuario_id=data['usuario_id'],
        valor=data['valor'],
        descricao=data.get('descricao'),
        data=datetime.strptime(data['data'], "%Y-%m-%d").date(),
        status=data.get('status', 'Não recebido')
    )
    db.session.add(receita)
    db.session.commit()
    return jsonify({'id': receita.id})


@app.route('/receitas', methods=['GET'])
def listar_receitas():
    receitas = Receita.query.all()
    return jsonify([
        {
            'id': r.id,
            'usuario_id': r.usuario_id,
            'valor': r.valor,
            'descricao': r.descricao,
            'data': r.data.isoformat(),
            'status': r.status
        } for r in receitas
    ])


# ==== DESPESAS ====

@app.route('/despesas', methods=['POST'])
def criar_despesa():
    data = request.json
    despesa = Despesa(
        usuario_id=data.get('usuario_id'),
        descricao=data['descricao'],
        valor_estimado=data.get('valor_estimado'),
        valor_real=data.get('valor_real'),
        status=data.get('status', 'Pendente'),
        data_vencimento=datetime.strptime(data['data_vencimento'], "%Y-%m-%d").date(),
        data_pagamento=datetime.strptime(data['data_pagamento'], "%Y-%m-%d").date() if data.get('data_pagamento') else None
    )
    db.session.add(despesa)
    db.session.commit()
    return jsonify({'id': despesa.id})


@app.route('/despesas', methods=['GET'])
def listar_despesas():
    despesas = Despesa.query.all()
    return jsonify([
        {
            'id': d.id,
            'usuario_id': d.usuario_id,
            'descricao': d.descricao,
            'valor_estimado': d.valor_estimado,
            'valor_real': d.valor_real,
            'status': d.status,
            'data_vencimento': d.data_vencimento.isoformat(),
            'data_pagamento': d.data_pagamento.isoformat() if d.data_pagamento else None
        } for d in despesas
    ])


# ==== DETALHES DAS DESPESAS ====

@app.route('/despesas/<int:despesa_id>/detalhes', methods=['POST'])
def adicionar_detalhe(despesa_id):
    data = request.json
    detalhe = DespesaDetalhe(
        despesa_id=despesa_id,
        descricao=data['descricao'],
        valor=data['valor']
    )
    db.session.add(detalhe)
    db.session.commit()
    return jsonify({'id': detalhe.id})


@app.route('/despesas/<int:despesa_id>/detalhes', methods=['GET'])
def listar_detalhes(despesa_id):
    detalhes = DespesaDetalhe.query.filter_by(despesa_id=despesa_id).all()
    return jsonify([
        {
            'id': d.id,
            'descricao': d.descricao,
            'valor': d.valor
        } for d in detalhes
    ])


# No final:
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
