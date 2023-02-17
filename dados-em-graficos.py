#Importando a base
import pandas as pd

tabela = pd.read_csv("caminhoDaBaseDeDados", encoding="latin1")

print(tabela)


# Tratando valores vazios:
tabela = tabela.dropna()
print(tabela.info())
print(tabela.describe().round(1))


# Avaliando a divisão de Clientes vs Cancelados
qtde_categoria = tabela["Categoria"].value_counts()
print(qtde_categoria)

qtde_categoria_perc = tabela["Categoria"].value_counts(normalize=True)
print(qtde_categoria_perc)


# IMPORTANTE:
# Instalar o plotly via terminal antes de executar essa célula
# pip install plotly

# Instalar as bibliotecas nbformat e IPython para exibir os gráficos:
# pip install nbformat ipython

import plotly.express as px

for coluna in tabela:
  grafico = px.histogram(tabela, x=coluna, color="Categoria")
  
  grafico.show()