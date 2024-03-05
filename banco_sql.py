
"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM.

"""
import sqlalchemy
from sqlalchemy.orm import declarative_base 
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select 




# Utilizado para criar dados(entidades) que irão ser utilizadas na criação de tabelas.
Base = declarative_base()

class Cliente(Base):
    __tablename__ = "usuario_cliente"

    # Atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    # Definindo relacionamento de entidades
    conta = relationship(
        "Conta", back_populates="cliente"
        # Se não tiver o relacionamento pela foreignkey é deletado em cascata  
    )

    # Representation
    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"

class Conta(Base):
    __tablename__ = "conta_cliente"

    # Atributos
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("usuario_cliente.id"), nullable=False)
    saldo = Column(Integer)
    
    # Nullable não permite que seja null
    # ForeignKey direciona a chave estrangeira

    #definindo relacionamento de entidades
    cliente = relationship("Cliente", back_populates="conta")
    
    # Representation
    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, id_cliente={self.id_cliente}, saldo={self.saldo})"
    
# Conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas pro banco de dados
Base.metadata.create_all(engine)

# Utilizado para recuperar informações das tabelas, investiga o banco de dados
inspetor_engine = inspect(engine)

# Verifica se tem a tabela indicada
print(inspetor_engine.has_table("usuario_cliente"))

# Retorna o nome das tabelas
print(inspetor_engine.get_table_names())

# Retorna o nome do schema
print(inspetor_engine.default_schema_name)

# Criando sessão para persistir os dados 
with Session(engine) as session:
    # Variavel do tipo usuário 
    juliana = Cliente(
        nome = 'Juliana Mascarenhas',
        cpf = '01',
        endereco = 'Rua A'
    )
    # Variavel do tipo Conta
    # Adicionando instância de Conta para Juliana
    juliana.conta=[Conta(tipo="conta poupança", agencia='11', num='1', saldo=50)]

    diego = Cliente(
        nome = 'Diego Rodrigues',
        cpf = '02',
        endereco = 'Rua B'   
    )
    # Variavel do tipo Conta
    # Adicionando instância de Conta para Diego
    diego.conta=[Conta(tipo="conta poupança", agencia='22', num='3', saldo=150)]

    # Enviando para o banco de dados (persistencia de dados)
    session.add_all([juliana,diego])
    session.commit()

# Query com where para users
stmt = select(Cliente).where(Cliente.nome.in_(['juliana', 'diego']))
print('\nRecuperando usuários a partir de uma condição de filtragem')
for cliente in session.scalars(stmt):
    print(cliente)
# Print(stmt) - demonstra a query que foi utilizada

# Query com where para Conta
stmt_diego = select(Conta).where(Conta.id_cliente.in_([2]))
print('\nRecuperando a diego de Diego')
for diego in session.scalars(stmt_diego):
    print(diego)
print(stmt_diego)

print('\nRecuperando os nome em ordem decrescente')
stmt_order = select(Cliente).order_by(Cliente.nome.desc())
for nomes in session.scalars(stmt_order):
    print(nomes)
# Por padrão ordena em ascendente
    
# Retorna um join de chave estrangeira    
stmt_join = select(Cliente.nome, Conta.tipo).join_from(Conta, Cliente)
print("\n")
for joins in session.scalars(stmt_join):
    print(joins)
# Print(stmt_join)

# Recupera todos os dados de uma conexão 
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da conexão")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("\nnúmero total de instâncias")
for results in session.scalars(stmt_count):
    print(results)


