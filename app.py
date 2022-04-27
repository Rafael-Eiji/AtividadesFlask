from sqlalchemy import delete, false
from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Pessoas, Atividades, Usuarios

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
''' 
USUARIOS = {
    'rafael':'123',
    'teste': '456'
} '''

''' @auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return false
    return USUARIOS.get(login) == senha '''

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return false
    return Usuarios.query.filter_by(login = login, senha = senha)




class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome = nome).first()
        response = {
            'nome' : pessoa.nome,
            'idade' : pessoa.idade,
            'id' : pessoa.id
        }

        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome = nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }

        return response
    
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome = nome).first()
        mensagem = 'Pessoa {} deletada com sucesso'.format(pessoa.nome)
        pessoa.delete()
        return {'status':'sucesso', 'mensagem':mensagem}

    def post(self):
        dados = request.json
        pessoa = Pessoa(nome = dados['nome'], idade = dados['idade'])
        pessoa.save()
        return {'id': pessoa.id, 'idade':pessoa.idade, 'nome': pessoa.nome}


class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id,'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response
        
    
class AdicionaPessoa(Resource):
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome = dados['nome'], idade = dados['idade'])
        pessoa.save()
        response = {'id': pessoa.id, 'idade':pessoa.idade, 'nome': pessoa.nome}
        return response


class AdicionaAtividade(Resource):
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome = dados['pessoa']).first()
        atividade = Atividades(nome = dados['nome'], pessoa = pessoa)
        atividade.save()
        response = {
            'id': atividade.id,
            'nome': atividade.nome,
            'pessoa':atividade.pessoa.nome
            }
        return response

class ListarAtividades(Resource):
    def get(self):
        atividade = Atividades.query.all()
        response = [{'id': i.id, 'nome':i.nome,'pessoa' : i.pessoa.nome} for i in atividade]

        return response

class AdicionaUsuario(Resource):
    def post(self):
        dados = request.json
        user = Usuarios(login = dados['login'], senha = dados['senha'])
        user.save()
        response ={'id' : user.id, 'login' :user.login, 'senha': user.senha}
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoas, '/pessoa/lista')
api.add_resource(AdicionaPessoa, '/pessoa/')
api.add_resource(AdicionaAtividade, '/atividade/')
api.add_resource(ListarAtividades, '/atividade/lista')
api.add_resource(AdicionaUsuario, '/usuario')

if __name__ == '__main__':
    app.run(debug = True)


