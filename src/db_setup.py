from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# 1. Base para criar os modelos
Base = declarative_base()

# 2. Tabela 'clientes'
class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    plano = Column(String(20), nullable=False)

    logs = relationship("LogUso", back_populates="cliente", cascade="all, delete-orphan")


# 3. Tabela 'logs_uso'
class LogUso(Base):
    __tablename__ = 'logs_uso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data_acesso = Column(DateTime, default=datetime.utcnow)
    funcionalidade_usada = Column(String(50), nullable=False)

    cliente = relationship("Cliente", back_populates="logs")


# 4. Criar o banco e as tabelas
if __name__ == '__main__':
    engine = create_engine('sqlite:///saas_database.db', echo=True)
    
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")