from models import Pessoas

def insere_pessoas():
    pessoa = Pessoas(nome = 'Teste1', idade = 23)
    print(pessoa)
    pessoa.save()

def consulta():
    pessoa = Pessoas.query.all()
    print(pessoa[1].idade)

def alterar_pessoa():
    pessoa = Pessoas.query.filter_by(nome = 'Teste1').first()
    pessoa.nome = 'Fulano'
    pessoa.save()

def excluir_pessoa():
    pessoa = Pessoas.query.filter_by(nome = 'Teste1').first()
    pessoa.delete()




if __name__ == '__main__':
    #insere_pessoas()
    consulta()
    #alterar_pessoa()
    #excluir_pessoa()




