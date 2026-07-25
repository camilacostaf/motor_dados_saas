import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# COnectar com BD
engine = create_engine('sqlite:///saas_database.db')

sns.set_theme(style="whitegrid")

sql_query = """
SELECT 
    c.id AS cliente_id,
    c.nome,
    c.plano,
    l.data_acesso
FROM clientes c
LEFT JOIN logs_uso l ON c.id = l.cliente_id
"""

df = pd.read_sql_query(sql_query, con=engine)
df['data_acesso'] = pd.to_datetime(df['data_acesso'])

df_cliente = df.groupby(['cliente_id', 'nome', 'plano']).agg(
    ultimo_acesso=('data_acesso', 'max'),
    total_acessos=('data_acesso', 'count')
).reset_index()

hoje = pd.to_datetime('now')
df_cliente['dias_sem_acesso'] = (hoje - df_cliente['ultimo_acesso']).dt.days.fillna(999).astype(int)

print("✅ Dados carregados com sucesso! Total de clientes:", len(df_cliente))

# Figura contendo 3 subplots em 1 linha (1 linha, 3 colunas)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Painel de análise de engajamento e risco SaaS', fontsize=16, fontweight='bold')

# -------------------------------------------------------------
# GRÁFICO 1: Quantidade de Clientes por Plano
# -------------------------------------------------------------
sns.countplot(
    data=df_cliente, 
    x='plano', 
    ax=axes[0], 
    palette='Blues_d'
)
axes[0].set_title('Distribuição de Clientes por Plano')
axes[0].set_xlabel('Plano')
axes[0].set_ylabel('Quantidade de Clientes')

# -------------------------------------------------------------
# GRÁFICO 2: Média de Acessos por Plano
# -------------------------------------------------------------
sns.barplot(
    data=df_cliente, 
    x='plano', 
    y='total_acessos', 
    ax=axes[1], 
    palette='Greens_d',
    errorbar=None
)
axes[1].set_title('Média de Acessos Totais por Plano')
axes[1].set_xlabel('Plano')
axes[1].set_ylabel('Média de Logs de Uso')

# -------------------------------------------------------------
# GRÁFICO 3: Distribuição dos dias sem acesso (Risco de Churn)
# -------------------------------------------------------------
sns.histplot(
    data=df_cliente, 
    x='dias_sem_acesso', 
    bins=15, 
    kde=True, 
    ax=axes[2], 
    color='crimson'
)
# Linha de alerta vermelha nos 30 dias (limite de risco)
axes[2].axvline(30, color='black', linestyle='--', label='Alerta de Churn (30 dias)')
axes[2].set_title('Distribuição de Dias sem Acesso')
axes[2].set_xlabel('Dias de Inatividade')
axes[2].set_ylabel('Nº de Clientes')
axes[2].legend()

plt.tight_layout()
nome_imagem = 'painel_saas_analytics.png'
plt.savefig(nome_imagem, dpi=300)

print(f" Painel visual gerado e salvo como '{nome_imagem}'!")