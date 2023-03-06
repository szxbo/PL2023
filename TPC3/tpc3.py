import json
import re
from collections import defaultdict


# Construa agora um ou vários programas Python para processar o texto 'processos.txt' (procurar o ficheiro no Bb) com o
# intuito de calcular frequências de alguns elementos (a ideia é utilizar arrays associativos, dicionários em Python,
# para o efeito) conforme solicitado a seguir:


def processos():
    procs = []
    with open('processos.txt', 'r') as bd:
        linhas = bd.readlines()
        er = re.compile(r'(?P<proc>[0-9]+)::(?P<data>.*?)::(?P<nomes>.*)::')
        for linha in linhas:
            num, data, nomes = er.match(linha).groups()
            proc = {
                'num': num,
                'data': data,
                'nomes': nomes.strip('::').split('::')
            }
            procs.append(proc)
        return procs


# a) Calcula a frequência de processos por ano (primeiro elemento da data);
def freq_proc_ano():
    processos_por_ano = defaultdict(int)
    with open('processos.txt', 'r') as bd:
        linhas = bd.readlines()
        er = re.compile(r'(?P<proc>[0-9]+)::(?P<data>.*?)::(?P<nomes>.*)::')
        for linha in linhas:
            num, data, nomes = er.match(linha).groups()
            ano = data.split('-')[0]
            processos_por_ano[ano] += 1
        return processos_por_ano


# b) Calcula a frequência de nomes próprios (o primeiro em cada nome) e apelidos (o ultimo em cada nome) por séculos e
# apresenta os 5 mais usados;
def freq_nomes():
    # Dicionários para armazenar as frequências de nomes próprios e apelidos
    primeiros_nomes = {}
    ultimos_nomes = {}

    # Expressões regulares para encontrar o primeiro e último nome em cada registro
    primeiro_nome_regex = re.compile(r'^\d+::\d{4}-\d{2}-\d{2}::([^\s]+)')
    ultimo_nome_regex = re.compile(r'::(\w+)$')

    # Loop através de cada linha no arquivo
    with open('processos.txt', 'r') as f:
        for linha in f:
            # Extrai o primeiro e último nome usando expressões regulares
            primeiro_nome = primeiro_nome_regex.search(linha).group(1)
            ultimo_nome = ultimo_nome_regex.search(linha).group(1)
            match = ultimo_nome_regex.search(linha)
            if match:
                ultimo_nome = match.group(1)
            else:
                ultimo_nome = None  # ou outro valor padrão que faça sentido para o seu código

            # Separa o primeiro nome em caso de existir mais de um nome
            primeiro_nome = primeiro_nome.split()[0]

            # Verifica o século da pessoa e atualiza o dicionário de frequências
            ano = int(linha.split('::')[1][:4])
            seculo = (ano - 1) // 100 + 1

            if seculo not in primeiros_nomes:
                primeiros_nomes[seculo] = {}

            if primeiro_nome not in primeiros_nomes[seculo]:
                primeiros_nomes[seculo][primeiro_nome] = 0

            primeiros_nomes[seculo][primeiro_nome] += 1

            # Atualiza o dicionário de frequências de apelidos
            if seculo not in ultimos_nomes:
                ultimos_nomes[seculo] = {}

            if ultimo_nome not in ultimos_nomes[seculo]:
                ultimos_nomes[seculo][ultimo_nome] = 0

            ultimos_nomes[seculo][ultimo_nome] += 1

    # Imprime as 5 primeiros nomes e apelidos mais frequentes em cada século
    for seculo in primeiros_nomes:
        print(f'Século {seculo}')
        for i, nome in enumerate(sorted(primeiros_nomes[seculo], key=primeiros_nomes[seculo].get, reverse=True)[:5]):
            print(f'{i + 1}. {nome}: {primeiros_nomes[seculo][nome]}')

        for i, nome in enumerate(sorted(ultimos_nomes[seculo], key=ultimos_nomes[seculo].get, reverse=True)[:5]):
            print(f'{i + 1}. {nome}: {ultimos_nomes[seculo][nome]}')


# c) Calcula a frequência dos vários tipos de relação: irmão, sobrinho, etc.;
def freq_relacoes():
    relacao_regex = re.compile(r'::([\w\s,]+)\.?\s?(?:Proc\.\d+)?::?$')

    # abrir o ficheiro
    with open('processos.txt', 'r') as f:
        procs = f.readlines()

    # inicializar dicionário de relações
    relacoes = {}

    # percorrer todas as linhas do ficheiro
    for linha in procs:
        # procurar por relações na linha
        relacao_match = relacao_regex.search(linha)
        if relacao_match:
            # extrair as relações
            relacoes_str = relacao_match.group(1)
            relacoes_list = [relacao.strip() for relacao in relacoes_str.split(',')]
            # adicionar as relações ao dicionário
            for relacao in relacoes_list:
                if relacao in relacoes:
                    relacoes[relacao] += 1
                else:
                    relacoes[relacao] = 1

    # imprimir resultados
    print("Frequência de relações:")
    for relacao, frequencia in relacoes.items():
        print(f"{relacao}: {frequencia}")


# d) Converta os 20 primeiros registos num novo ficheiro de output mas em formato Json.
def convert_json():
    with open('processos.txt', 'r') as f:
        linhas = f.readlines()

    registos = []
    for linha in linhas[:20]:
        processo, data, nome, pai, mae, parentesco = linha.strip().split('::')
        registos.append({
            'processo': processo,
            'data': data,
            'nome': nome,
            'pai': pai,
            'mae': mae,
            'parentesco': parentesco
        })

    with open('primeiros_registos.json', 'w') as f:
        json.dump(registos, f, indent=4)


def main():
    processos_por_ano = freq_proc_ano()
    lista_processos = processos()
    freq_nomes()
    freq_relacoes()
    convert_json()


if __name__ == '__main__':
    main()
