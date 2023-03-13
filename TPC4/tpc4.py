import re
import json


def parse_cabecalho(file_name):
    with open(file_name, 'r') as file:
        formato = file.readline().strip()
        # separar todos os atributos do formato
        atributos = re.findall(r'(?:[^,{]|{[^}]*})*', formato)
        atributos = list(filter(lambda x: not re.match(r'^\s*$', x), atributos))
        atr_counter = list()
        for atr in atributos:

            # Verificar se há listas de atributos
            if intervalo := re.match(r'\w+\{(?P<min>\d+)\,(?P<max>\d+)\}', atr):
                atr_counter.append(range(int(intervalo.group('min')), int(intervalo.group('max'))))
            elif repete := re.search(r'\{(?P<valor>\d+)\}', atr):
                atr_counter.append(int(repete.group('valor')))
            else:
                atr_counter.append(1)
        atributos = [re.sub(r'\{[^}]*\}', '', atr) for atr in atributos]
        return atributos, atr_counter


def parse_csv(file, atributos, atr_count):
    tabela = []
    with open(file, 'r') as file:
        # Ignorar a linha do cabeçalho
        next(file)

        for linha in file:
            valores = re.split(r',', linha.strip())
            d = {}
            i = 0
            for atr, count in zip(atributos, atr_count):
                if isinstance(count, int):
                    if count == 1:
                        d[atr] = valores.pop(0)
                    else:
                        d[atr] = [valores.pop(0) for i in range(count)]
                else:
                    match = re.search(r'(?P<atr>\w+)(::(?P<op>[a-zA-Z]+))', atr)
                    vals = [int(v) for v in list(filter(None, valores))]
                    if match:
                        op = match.group('op')
                        d[match.group('atr') + '_' + match.group('op')] = op_result(vals, op)
                    else:
                        d[atr] = [int(v) for v in list(filter(None, valores[0:count.stop]))]
                        valores = valores[count.stop:]
                i += 1

            tabela.append(d)

    return tabela


def op_result(valores, op):
    result = 0
    if op == 'sum':
        return sum(valores)
    elif op == 'media':
        return sum(valores)/len(valores)

    return result


def write_json(json_output, tabela):
    with open(json_output, 'w') as outfile:
        json_list = [json.dumps(linha, indent=4, ensure_ascii=False) for linha in tabela]
        outfile.write('[\n')
        outfile.write(',\n'.join(json_list))
        outfile.write('\n]')


def main():
    file = 'alunos2'
    file_csv = file + '.csv'
    file_json = file + '.json'

    atributos, atr_counter = parse_cabecalho(file_csv)
    tabela = parse_csv(file_csv, atributos, atr_counter)
    write_json(file_json, tabela)


if __name__ == '__main__':
    main()
