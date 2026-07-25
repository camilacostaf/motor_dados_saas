# 📊 Motor de dados e análise executiva de churn em um SaaS

Este projeto consiste em uma pipeline completa de dados para monitoramento de saúde de clientes (*Health Score*), cálculo de **MRR em Risco** (*Monthly Recurring Revenue*) e prevenção de **Churn** para empresas SaaS.

---

## 🎯 Objetivos de negócio

1. **Identificar inatividade:** Mapear clientes sem uso da plataforma nos últimos 30 e 60 dias.
2. **Quantificar impacto financeiro:** Classificar o MRR ameaçado conforme os planos (*Basic*, *Pro*, *Enterprise*).
3. **Priorizar atendimento:** Gerar uma lista de ação ordenada por valor financeiro para o time de atendimento.
4. **Visão executiva:** Entregar um painel gráfico e relatórios em planilha multi-abas para a diretoria de modo a facilitar a tomada de decisão.

---

## 🛠️ Tecnologias utilizadas

* **Python 3.x**
* **SQLAlchemy (ORM) / SQLite:** Estruturação do banco de dados relacional.
* **Faker:** Geração sintética de uma rede de clientes e logs de uso.
* **Pandas e NumPy:** Ingestão SQL, tratamento de datas, agrupamentos e vetorização de regras de negócio.
* **Matplotlib e Seaborn:** Criação do painel visual de métricas.
* **OpenPyXL:** Exportação do relatório executivo em formato Excel (`.xlsx`).

---

## 📂 Estrutura do projeto

* `src/db_setup.py`: Criação do banco de dados relacional e esquemas.
* `src/seed_data.py`: Povoamento sintético da base com dados realistas.
* `src/churn_analysis.py`: Lógica de negócio, classificação de risco via NumPy e exportação para Excel.
* `src/visualizations.py`: Geração do painel gráfico em imagem de alta resolução.

---

## 📊 Resultados e entregáveis

* 🖼️ **`painel_saas_analytics.png`**: Painel visual de engajamento e risco em alta resolução.
* 📄 **`relatorio_executivo_churn.xlsx`**: Relatório em duas abas (*Resumo Diretoria* e *Lista de Ação CS*).

---

## 🚀 Como executar o projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/motor_dados_saas.git](https://github.com/SEU_USUARIO/motor_dados_saas.git)
   cd motor_dados_saas