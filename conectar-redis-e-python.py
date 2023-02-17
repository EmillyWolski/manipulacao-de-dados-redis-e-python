# PARA ABRIR O REDIS NO UBUNTU:
# wsl (dá pra abrir pelo VsCode direto)

# INICIALIZAR O REDIS:
# sudo service redis-server start
# redis-cli
#########################################################################

import time
start_time = time.time()

# IMPORTANDO O REDIS
import redis

# Função para conectar o Redis
def conectar_redis():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return r 
    #r é a variável que guarda a conexão

# Carregando os dados do arquivo CSV:
import pandas as pd

tabela = pd.read_csv("caminhoDaBaseDeDados", encoding="latin1")

# Conectando ao Redis
r = conectar_redis()

# for i, row in enumerate(tabela.iterrows()):
#     r.hmset("tabela:" + str(i), {str(k).encode(): str(v).encode() for k, v in row[1].to_dict().items()}) 

# Estamos percorrendo cada linha (representada por "row") em uma tabela Pandas e armazenando cada linha como um hash no Redis.
# Para cada linha, o hash é criado com a chave "tabela:i", onde "i" é o número da linha atual. 
# O valor do hash é um dicionário que contém as colunas da linha atual como pares de chave/valor.
# A chave do dicionário é a coluna em si, convertida em string, e o valor é o valor da coluna na linha atual, também convertido em string.

# Importante: a função "hmset" do Redis é usada para salvar o hash no Redis. 
              # encode() converte um objeto de string em uma representação de bytes
              # to_dict() converte uma estrutura de dados em Python, como um objeto pandas em um dicionário.

print("\n")
print("TEMPO DE EXECUCAO DA IMPORTACAO: {:.3f} segundos".format(time.time() - start_time))
print("\n")

########################################################################


# CONSULTAS
# CÁLCULO DA MÉDIA DE IDADE DOS CLIENTES

# Recuperar todas as chaves que começam com "tabela:"
# Usar decode() para decodificar dados codificados como bytes em uma string legível

import time
start_time = time.time()

keys = [k.decode() for k in r.keys("tabela:*")] 

# Inicializa a soma total das idades e o número de entradas
total_soma = 0
total_contador = 0

# Para cada chave, recuperamos o valor da idade e adicionamos à soma total
for key in keys:
    idade = int(r.hget(key, "Idade").decode())
    total_soma += idade
    total_contador += 1

# Calcula a média geral das idades
media = total_soma / total_contador

print("Média geral das idades:", media)

print("Tempo de execução: {:.3f} segundos".format(time.time() - start_time))
print("\n")

########################################################################


# QUANTIDADE DE CLIENTES POR CATEGORIA DE CARTÃO 

import time
start_time = time.time()

# Recuperar todas as chaves que começam com "tabela:"
keys = [k.decode() for k in r.keys("tabela:*")]

# Inicializa o dicionário que irá armazenar as contagens de cada categoria de cartão
quantidade_de_cada_categoria_de_cartao = {}

# Para cada chave, recupera o valor da categoria de cartão e adiciona à contagem
for key in keys:
    categoria_cartao = r.hget(key, "Categoria Cartão").decode()

    if categoria_cartao in quantidade_de_cada_categoria_de_cartao:
        quantidade_de_cada_categoria_de_cartao[categoria_cartao] += 1
    else:
        quantidade_de_cada_categoria_de_cartao[categoria_cartao] = 1

# Imprime a contagem de cada categoria de cartão
for categoria_cartao, contador in quantidade_de_cada_categoria_de_cartao.items():

    print("\nCategoria de Cartão: ", categoria_cartao, " | Quantidade:", contador)

print("Tempo de execução: {:.3f} segundos".format(time.time() - start_time))


#########################################################################


# QUANTIDADE DE CLIENTES E CANCELADOS

import time
start_time = time.time()

keys = [k.decode() for k in r.keys("tabela:*")]

count_cliente = 0
count_cancelado = 0

for key in keys:
    categoria = r.hget(key, "Categoria").decode()

    if categoria == "Cliente":
        count_cliente += 1
    elif categoria == "Cancelado":
        count_cancelado += 1

print("\n")
print("\nQuantidade de 'Clientes':", count_cliente)
print("Quantidade de 'Cancelados':", count_cancelado)

print("Tempo de execução: {:.3f} segundos".format(time.time() - start_time))
print("\n")


#########################################################################


# CONSULTA PARA SABER A CATEGORIA DE CARTÃO DOS CLIENTES CANCELADOS

import time
start_time = time.time()

# Recupera todas as chaves que começam com "tabela:"
keys = [k.decode() for k in r.keys("tabela:*")]

cont = 0; cancelados_contador = 0; categoria_de_cartao_dos_cancelados =  {}

for key in keys:
    categoria = r.hget(key, "Categoria").decode()

    if categoria == "Cancelado":
        cancelados_contador += 1
        categoria_cartao = r.hget(key, "Categoria Cartão").decode()

        if categoria_cartao not in categoria_de_cartao_dos_cancelados:
            categoria_de_cartao_dos_cancelados[categoria_cartao] = 0
        
        categoria_de_cartao_dos_cancelados[categoria_cartao] += 1

print("\nQuantidade de clientes cancelados:", cancelados_contador)
print("\nQuantidade de clientes cancelados por categoria de cartão:")


for categoria_cartao, cont in categoria_de_cartao_dos_cancelados.items():
    print(f"\t{categoria_cartao}: {cont}")

print("Tempo de execução: {:.3f} segundos".format(time.time() - start_time))
print("\n")
print("\n")


########################################################################


# CONSULTA DA QUANTIDADE DE CONTATOS FEITOS 
import time
start_time = time.time()

# Recuperar todas as chaves que começam com "tabela:"
keys = [k.decode() for k in r.keys("tabela:*")]

contato_12m_por_cliente = {}

for key in keys:
    categoria = r.hget(key, "Categoria").decode()

    if categoria == "Cancelado":
        clientnum = r.hget(key, "CLIENTNUM").decode()

        contato_12m = r.hget(key, "Contatos 12m").decode()

        if clientnum not in contato_12m_por_cliente:
            contato_12m_por_cliente[clientnum] = 0
        
        contato_12m_por_cliente[clientnum] += int(contato_12m)

# print("Quantidade de 'Contato 12 m' por cliente:")

# for clientnum, contato_12m in contato_12m_por_cliente.items():
#     print(f"\tCliente {clientnum}: {contato_12m}")

# print("\n")


# Dicionário para armazenar a quantidade de clientes que realizaram uma quantidade específica de contatos
quantidade_por_contato = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    'mais': 0,
}

# Iterar sobre cada cliente e verificar quantos contatos ele realizou
for clientnum, contato in contato_12m_por_cliente.items():
    if contato == 1:
        quantidade_por_contato[1] += 1
    elif contato == 2:
        quantidade_por_contato[2] += 1
    elif contato == 3:
        quantidade_por_contato[3] += 1
    elif contato == 4:
        quantidade_por_contato[4] += 1
    elif contato == 5:
        quantidade_por_contato[5] += 1
    else:
        quantidade_por_contato['mais'] += 1


print("Quantidade contatos realizados pelos clientes que realizam o cancelamento:")

# Iterar sobre cada chave e valor no dicionário
for contato, quantidade in quantidade_por_contato.items():
    if contato == 'mais':
        print(f"\tMais de 5 contatos: {quantidade}")
    else:
        print(f"\t{contato} contato(s): {quantidade}")

print("Tempo de execução: {:.3f} segundos".format(time.time() - start_time))
print("\n")


###############################################################################


# GRÁFICO DE QTDE DE CONTATOS
# Importando a biblioteca Matplotlib: pip install matplotlib

# import matplotlib.pyplot as plt

# contatos = list(contato_12m_por_cliente.values())

# plt.hist(contatos, bins=range(min(contatos), max(contatos) + 2, 1), edgecolor='black', alpha=0.7)

# plt.xlabel("Contatos 12m")
# plt.ylabel("Número de clientes")
# plt.title("Histograma de Contatos 12m por Cliente")

# plt.show()


#########################################################################




