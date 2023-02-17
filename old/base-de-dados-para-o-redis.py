# Códigos abaixo, originalmente escritos em um arquivo IPython Notebook transformados em arquivos python

# # Importando a base
# import pandas as pd

# tabela = pd.read_csv("C:/Users/emill/OneDrive/Área de Trabalho/TADS-2022-P4/banco-de-dados-3/big-data/teste-com-redis/ClientesBanco.csv", encoding="latin1")

# display(tabela)


# # Agora vamos tratar valores vazios e exibir um resumo das colunas da base de dados
# tabela = tabela.dropna()
# display(tabela.info())

# display(tabela.describe().round(1))


# # Vamos avaliar como está a divisão entre Clientes x Cancelados
# qtde_categoria = tabela["Categoria"].value_counts()
# display(qtde_categoria)

# qtde_categoria_perc = tabela["Categoria"].value_counts(normalize=True)
# display(qtde_categoria_perc)



# import pandas as pd

# tabela = pd.read_csv("C:/Users/emill/OneDrive/Área de Trabalho/TADS-2022-P4/banco-de-dados-3/big-data/teste-com-redis/ClientesBanco.csv", encoding="latin1")

# tabela = tabela.dropna()

# qtde_categoria = tabela["Categoria"].value_counts()

# qtde_categoria_perc = tabela["Categoria"].value_counts(normalize=True)











