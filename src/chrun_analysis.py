import pandas as pd
from sqlalchemy import create_engine

# Conexão com o banco de dados SQLite
engine = create_engine('sqlite:///saas_database.db')

sql_query = """
SELECT 
    c.id AS cliente_id,
    c.nome,
    c.email,
    c.plano,
    c.data_cadastro,
    l.data_acesso
FROM clientes c
LEFT JOIN logs_uso l ON c.id = l.cliente_id
"""
df = pd.read_sql_query(sql_query, con=engine)

print(df.head())

df['data_acesso'] = pd.to_datetime(df['data_acesso'])

# Agrupar por cliente para calcular o último acesso e o total de acessos
df_cliente = df.groupby(['cliente_id', 'nome', 'email', 'plano']).agg(
    ultimo_acesso=('data_acesso', 'max'),
    total_acessos=('data_acesso', 'count')
).reset_index()

# Calcular quantos dias se passaram do último acesso até hoje
hoje = pd.to_datetime('now')
df_cliente['dias_sem_acesso'] = (hoje - df_cliente['ultimo_acesso']).dt.days.fillna(999).astype(int)

print("\n--- ÚLTIMO ACESSO POR CLIENTE ---")
print(df_cliente[['nome', 'plano', 'ultimo_acesso', 'dias_sem_acesso']].head())

# Dicionário com os preços dos planos
precos_planos = {
    'Basic': 49.00,
    'Pro': 149.00,
    'Enterprise': 499.00
}

# Criar coluna 'mrr' para associar o plano ao valor em dinheiro
df_cliente['mrr'] = df_cliente['plano'].map(precos_planos)

print("\n--- CLIENTES COM VALORES DE MENSALIDADE (MRR) ---")
print(df_cliente[['nome', 'plano', 'mrr', 'dias_sem_acesso']].head())

import numpy as np

# Dfeinir as condições de CHURN
condicoes = [
    (df_cliente['dias_sem_acesso'] <= 30),
    (df_cliente['dias_sem_acesso'] > 30) & (df_cliente['dias_sem_acesso'] <= 60),
    (df_cliente['dias_sem_acesso'] > 60)
]

# Definir rótulo de cada condição

status_rotulos = [
    '1. Ativo', 
    '2. Em Risco (30-60 dias)', 
    '3. Churned (60+ dias)'
]

df_cliente['status_churn'] = np.select(condicoes, status_rotulos, default='3. Churned (60+ dias)')

print("\n--- CLASSIFICAÇÃO DE RISCO DE CHURN ---")
print(df_cliente[['nome', 'plano', 'dias_sem_acesso', 'status_churn']].head(10))

# Agrupar por startus e somar MRR para contar clientes
resumo_mrr = df_cliente.groupby('status_churn').agg(
    qtd_clientes=('cliente_id', 'count'),
    mrr_total=('mrr', 'sum'),
    media_dias_inativo=('dias_sem_acesso', 'mean')
).reset_index()

# Cálculo de % do MRR total que cada categoria representa
total_mrr_empresa = resumo_mrr['mrr_total'].sum()
resumo_mrr['pct_mrr'] = (resumo_mrr['mrr_total'] / total_mrr_empresa) * 100

resumo_mrr['mrr_total'] = resumo_mrr['mrr_total'].round(2)
resumo_mrr['pct_mrr'] = resumo_mrr['pct_mrr'].round(1)
resumo_mrr['media_dias_inativo'] = resumo_mrr['media_dias_inativo'].round(0)

# Tabela final
print("\n--- RESUMO EXECUTIVO DE MRR E CHURN ---")
print(resumo_mrr.to_string(index=False))

# Filtrar apenas quem NÃO é 'Ativo'
df_cs_acao = df_cliente[df_cliente['status_churn'] != '1. Ativo'].copy()

# Ordenar por MRR maior (decrescente) e depois por dias inativos (decrescente)
df_cs_acao = df_cs_acao.sort_values(
    by=['mrr', 'dias_sem_acesso'], 
    ascending=[False, False]
)

print("\n--- TOP 5 CLIENTES PRIORITÁRIOS PARA O TIME DE ATENDIMENTO ---")
print(df_cs_acao[['nome', 'plano', 'mrr', 'dias_sem_acesso', 'status_churn']].head())

# Passo final: exportação para o Excel

nome_arquivo = 'relatorio_executivo_churn.xlsx'

# Usando o ExcelWriter para criar o arquivo e gravar as abas
with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
    resumo_mrr.to_excel(writer, sheet_name='Resumo Diretoria', index=False)
    df_cs_acao.to_excel(writer, sheet_name='Lista de Acao CS', index=False)

print(f"\n Relatório executivo gerado com sucesso: '{nome_arquivo}'!")