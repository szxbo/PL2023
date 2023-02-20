
# Extra: explore o módulo matplotlib e crie gráficos para as suas distribuições.
from math import log2


# Função que lê a informação do ficheiro para um modelo
def parse_bd():
    with open('myheart.csv', 'r') as base_de_dados:
        # Ler todas as linhas do ficheiro
        linhas = base_de_dados.readlines()

        # Separar a linha dos paramêtros das linhas de dados
        parametros = linhas[0]
        linhas = linhas[1:]

        # Modelo para guardar uma distribuição: Lista de dicionários
        dados = []
        for linha in linhas:
            linha = linha.strip().split(',')
            idade, sexo, tensao, colesterol, batimento, tem_doenca = linha
            linha = {
                'idade': int(idade),
                'sexo': sexo,
                'tensao': int(tensao),
                'colesterol': int(colesterol),
                'batimento': int(batimento),
                'tem_doenca': bool(int(tem_doenca))
            }
            dados.append(linha)
    return dados


# Função que calcula a distribuição da doença por sexo
def distribuicao_por_sexo(dados):
    n_mulheres = 0
    n_homens = 0
    total_doentes = 0
    for x in dados:
        if x.get('tem_doenca'):
            total_doentes += 1
            if x.get('sexo') == 'F':
                n_mulheres += 1
            else:
                n_homens += 1
    distr_mulheres = n_mulheres / total_doentes * 100
    distr_homens = n_homens / total_doentes * 100

    print(f'Porcentagem de mulheres: {distr_mulheres:.2f}%\nPorcentagem de homens: {distr_homens:.2f}%\n')


# Função que calcula a distribuição da doença por escalões etários
def distribuicao_por_idades(dados):
    idades = []
    for x in dados:
        idades.append(x.get('idade'))
    idade_min = min(idades)
    idade_max = max(idades)
    # Regra de Sturges
    k = 1 + log2(len(dados))
    intervalo = int((idade_max - idade_min) / k)
    intervalos = {}

    for i in range(idade_min, idade_max, intervalo):
        intervalo_min = i
        intervalo_max = i + intervalo
        intervalo_str = f'{intervalo_min}-{intervalo_max}'
        intervalos[intervalo_str] = 0
        for pessoa in dados:
            if pessoa.get('tem_doenca'):
                idade = pessoa.get('idade')
                if intervalo_min <= idade < intervalo_max:
                    intervalos[intervalo_str] += 1

    imprimir_distribuicao(intervalos, 'escalões etários')


# Função que calcula a distribuição da doença por níveis de colesterol.
def distribuicao_por_colesterol(dados):
    colesterois = []
    for x in dados:
        colesterois.append(x.get('colesterol'))
    colesterol_min = min(colesterois)
    colesterol_max = max(colesterois)
    intervalo = 10
    intervalos = {}

    for i in range(colesterol_min, colesterol_max, intervalo):
        intervalo_min = i
        intervalo_max = i + intervalo
        intervalo_str = f"{intervalo_min}-{intervalo_max}"
        intervalos[intervalo_str] = 0
        for pessoa in dados:
            if pessoa.get('tem_doenca'):
                colesterol = pessoa.get('colesterol')
                if intervalo_min <= colesterol < intervalo_max:
                    intervalos[intervalo_str] += 1

    imprimir_distribuicao(intervalos, 'níveis de colesterol')


# Função que imprime na forma de uma tabela uma distribuição
def imprimir_distribuicao(intervalos, tipo):
    print(f'[Distribuição da doença por {tipo}]')
    print('---------------------------------------------')
    print('Intervalo    |  Número de pessoas com doença')
    print('---------------------------------------------')

    for intervalo, num_pessoas in intervalos.items():
        coluna_intervalo = intervalo.ljust(12)
        coluna_num_pessoas = str(num_pessoas).ljust(30)
        print('{} |     {}'.format(coluna_intervalo, coluna_num_pessoas))

    print('--------------------------------------------\n')


# Apresenta as tabelas correspondentes às distribuições pedidas
def main():
    dados = parse_bd()
    distribuicao_por_sexo(dados)
    distribuicao_por_idades(dados)
    distribuicao_por_colesterol(dados)


if __name__ == '__main__':
    main()
