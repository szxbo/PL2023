def somador():
    somar = True
    soma = 0
    i = 0
    numero = '0'
    linha = input('Insere a string para processar: ')
    linha.lower()

    for c in linha:
        i += 1
        if c.isnumeric():
            if somar:
                numero += c
                if not(linha[i].isdigit()):
                    soma += int(numero)
                    numero = '0'
        elif c == '=':
            print('A soma é ' + str(soma))
        elif c == 'o':
            if linha[i] == 'n':
                somar = True
            elif linha[i] == 'f' and linha[i+1] == 'f':
                somar = False


def main():
    somador()


main()
