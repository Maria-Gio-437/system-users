from flask import Flask, request, jsonify
from flask_supabase import Supabase
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
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
    return jsonify(resp.data), resp.status_code

# Editar usuário
@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    data = request.json
    resp = supabase.client.from_('usuarios').update(data).eq('id', id).execute()
    return jsonify(resp.data), resp.status_code

# Excluir usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    resp = supabase.client.from_('usuarios').delete().eq('id', id).execute()
    return jsonify(resp.data), resp.status_code

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
