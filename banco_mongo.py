"""
    Primeiro programa de integração com banco de dados
    utilizando Pymongo.

"""
import pprint
import pymongo
import datetime

client = pymongo.MongoClient(
    "mongodb+srv://pymongo:pymongo@cluster0.pifcgtb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )

# Cria o schema test
db = client.mongodesafio

# Cria a coleção test_collection
collection = db.cliente

# Verifica a coleção
print(db.cliente)

# Criando um documento
post = {
    "nome": "Juliana Mascarenhas",
    "cpf" : '01',
    "endereco" : 'Rua A',
    "conta_bancaria": [{"tipo" : "conta poupança"}, {"agencia" : "11"}, {"num" : "1"}, {"saldo" : "50"}],
    "date": datetime.datetime.now(datetime.UTC)
}

# Criando uma coleção de posts
conta = db.conta

# Inserindo o documento na coleção
post_id = conta.insert_one(post).inserted_id
print(post_id)

# Verifica a coleção
print(db.conta)

# Lista nome das coleções
print(db.list_collection_names())

# Recuperando documentos da coleção
print(db.conta.find_one())
pprint.pprint(db.conta.find_one())

# Bulk inserts, inserindo mais de um documento de uma vez
new_conta = [{
    "nome": "Diego Mascarenhas",
    "cpf" : '02',
    "endereco" : 'Rua B',
    "conta_bancaria": [{"tipo" : "conta corrente"}, {"agencia" : "12"}, {"num" : "2"}, {"saldo" : "150"}],
    "date": datetime.datetime.now(datetime.UTC)},
    {
        "nome": "Carlos Mascarenhas",
        "cpf" : '03',
        "endereco" : 'Rua C',
        "conta_bancaria": [{"tipo" : "conta poupança"}, {"agencia" : "13"}, {"num" : "3"}, {"saldo" : "250"}],
    "date": datetime.datetime.now(datetime.UTC)}   
]

#inserindo no banco varios documentos ao mesmo tempo
result = conta.insert_many(new_conta)
print(result.inserted_ids)

print("\nRecuperando documento com o nome = Juliana Mascarenhas")
pprint.pprint(db.conta.find_one({"nome" : "Juliana Mascarenhas"}))

print("\nRecuperando todos os documentos na coleção conta")
for post in conta.find():
    pprint.pprint(post)

