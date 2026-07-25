import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Cliente, LogUso

# 1. Configuração do Faker em Português
fake = Faker('pt_BR')

# 2. Conexão com o banco de dados
engine = create_engine('sqlite:///saas_database.db')

def gerar_massa_de_dados(qtd_clientes=200):
    print(f"🔄 Recriando o banco de dados do zero...")
    # Apaga as tabelas antigas e recria limpas
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"🚀 Gerando {qtd_clientes} clientes e seus logs de uso...")

    planos = ['Basic', 'Pro', 'Enterprise']
    funcionalidades = ['login', 'exportar_relatorio', 'criar_dashboard', 'configuracoes']
    
    agora = datetime.utcnow()
    clientes_criados = []

    # 3. Gerar os Clientes
    for _ in range(qtd_clientes):
        # Sorteia data de cadastro nos últimos 365 dias
        dias_cadastro = random.randint(1, 365)
        data_cadastro = agora - timedelta(days=dias_cadastro)

        cliente = Cliente(
            nome=fake.name(),
            email=fake.unique.email(), # Garante e-mail único sem duplicata
            plano=random.choice(planos),
            data_cadastro=data_cadastro
        )
        clientes_criados.append(cliente)

    session.add_all(clientes_criados)
    session.commit() # Grava os clientes para gerar os IDs físicos

    print("✅ Clientes salvos. Gerando histórico de logs de uso...")

    # 4. Gerar os Logs de Uso para cada cliente
    logs_criados = []
    for cliente in clientes_criados:
        # Sorteia quantos acessos esse cliente teve (de 0 a 12 acessos)
        qtd_logs = random.randint(0, 12)

        for _ in range(qtd_logs):
            # Acesso ocorre entre o dia do cadastro do cliente e hoje
            dias_desde_cadastro = (agora - cliente.data_cadastro).days
            if dias_desde_cadastro > 0:
                dias_acesso = random.randint(0, dias_desde_cadastro)
            else:
                dias_acesso = 0

            log = LogUso(
                cliente_id=cliente.id,
                funcionalidade_usada=random.choice(funcionalidades),
                data_acesso=cliente.data_cadastro + timedelta(days=dias_acesso)
            )
            logs_criados.append(log)

    session.add_all(logs_criados)
    session.commit()

    print(f"🎉 Sucesso! {len(clientes_criados)} clientes e {len(logs_criados)} logs inseridos no banco!")

if __name__ == '__main__':
    gerar_massa_de_dados(200)