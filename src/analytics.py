import pandas as pd
from sqlalchemy import create_engine

# 1. Conexão com o banco de dados
engine = create_engine('sqlite:///saas_database.db')

def gerar_relatorio_churn():
    print("--- 📊 CARREGANDO DADOS NO PANDAS ---")

    # 2. Consulta SQL usando os apelidos 'c' (clientes) e 'l' (logs) de forma consistente
    sql_query = """
    SELECT 
        c.id AS cliente_id,
        c.nome,
        c.email,
        c.plano,
        c.data_cadastro,
        l.funcionalidade_usada,
        l.data_acesso
    FROM clientes c
    LEFT JOIN logs_uso l ON c.id = l.cliente_id
    """

    # 3. O Pandas lê a consulta
    df = pd.read_sql_query(sql_query, con=engine)

    # 4. Exibe o DataFrame no terminal
    print("\nVisão geral do DataFrame:")
    print(df.head())

    # 5. Contagem de clientes por plano
    print("\n--- 📈 DISTRIBUIÇÃO DE CLIENTES POR PLANO ---")
    resumo_planos = df['plano'].value_counts()
    print(resumo_planos)

    # 6. Exporta para o arquivo Excel
    df.to_excel("relatorio_churn_saas.xlsx", index=False)
    print("\n✅ Relatório 'relatorio_churn_saas.xlsx' gerado com sucesso na raiz do projeto!")

if __name__ == '__main__':
    gerar_relatorio_churn()