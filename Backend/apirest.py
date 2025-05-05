from flask import Flask, request, jsonify
from flask_supabase import Supabase
from dotenv import load_dotenv
from flask_cors import CORS 
import os

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')

supabase = Supabase(app)

# Listar usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    resp = supabase.client.from_('usuarios').select('*').execute()
    if resp.data is not None:
        return jsonify(resp.data), 200
    else:
        return jsonify({'error': 'Erro ao buscar usuários', 'details': resp}), 500

# Criar usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    resp = supabase.client.from_('usuarios').insert([data]).execute()
    if resp.data is not None and len(resp.data) > 0:
        return jsonify(resp.data), 201
    else:
        return jsonify({'error': 'Erro ao criar usuário', 'details': resp}), 500

# Editar usuário
@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    data = request.json
    resp = supabase.client.from_('usuarios').update(data).eq('id', id).execute()
    if resp.data is not None and len(resp.data) > 0:
        return jsonify(resp.data), 200
    elif resp.count > 0: # Caso a resposta não retorne os dados atualizados
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    else:
        return jsonify({'error': 'Erro ao editar usuário', 'details': resp}), 500

# Excluir usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    resp = supabase.client.from_('usuarios').delete().eq('id', id).execute()
    if resp.count > 0:
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    else:
        return jsonify({'error': 'Erro ao excluir usuário', 'details': resp}), 500

# Health check da conexão com o Supabase
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Tenta fazer uma consulta simples para verificar a conexão
        resp = supabase.client.from_('usuarios').select('id').limit(1).execute()
        if resp.data is not None:
            return jsonify({'status': 'Conectado ao Supabase!'}), 200
        else:
            return jsonify({'status': 'Erro ao conectar ao Supabase', 'error': resp.error}), 500
    except Exception as e:
        return jsonify({'status': 'Erro inesperado ao conectar ao Supabase', 'error': str(e)}), 500

@app.route("/")
def home():
    return "API System Users está no ar!", 200

if __name__ == '__main__':
    app.run(debug=True)
