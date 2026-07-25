from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importar classes/tabelas
from db_setup import Cliente, LogUso

# Conectar com banco existente
engine = create_engine('sqlite:///saas_database.db')
Session = sessionmaker(bind=engine)
session = Session()

def consultar_dados():
    print("--- LISTA DE TODOS OS CLIENTES ---")

    # Busca todos os clientes no banco
    clientes = session.query(Cliente).all()

    # Percorre a lista para exibir para cliente
    for cliente in clientes:
        print(f"ID: {cliente.id} | Nome: {cliente.nome}, | Plano: {cliente.plano} | E-mail: {cliente.email}")

if __name__ == '__main__':
    consultar_dados()

from datetime import datetime, timedelta

def consultar_clientes_pro_ou_enterprise():
    print("\n--- CLIENTES PREMIUM (Pro ou Enterprise) ---")
    clientes_premium = session.query(Cliente).filter(Cliente.plano.in_(["Pro", "Enterprise"])).all()

    for cliente in clientes_premium:
        print(f"Nome: {cliente.nome}  Plano: {cliente.plano}")

def identificar_clientes_em_risco_churn():
    print("\n--- CLIENTE EM RISCO DE CHURN ---")

    # Limite de 30 dias atrás
    limite_dias = datetime.utcnow() - timedelta(days=30)

    # Buscar logs com data anterior há 30 dias
    logs_antigos = session.query(LogUso).filter(LogUso.data_acesso < limite_dias).all()

    for log in logs_antigos:
        cliente = session.query(Cliente).get(log.cliente_id)
        print(f"Alerta! Cliente '{cliente.nome}' (ID: {cliente.id}) acessou pela última vez em: {log.data_acesso.strftime('%d/%m/%Y')}")

if __name__ == '__main__':
    consultar_dados()
    consultar_clientes_pro_ou_enterprise()
    identificar_clientes_em_risco_churn()