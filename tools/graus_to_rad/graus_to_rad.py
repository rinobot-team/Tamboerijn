import math

# Função para converter graus para radianos
def graus_para_radianos(graus):
    return graus * (math.pi / 180)

# Ler o arquivo de entrada
entrada = "tools\graus_to_rad\getupFrontOld.pos"
saida = "getupFrontNew.pos"

with open(entrada, 'r') as arquivo_entrada, open(saida, 'w') as arquivo_saida:
    for linha in arquivo_entrada:
        # Escrever comentários e linhas em branco diretamente no arquivo de saída
        if linha.startswith('#') or not linha.strip():
            arquivo_saida.write(linha)
        else:
            # Converter valores de graus para radianos e escrever no arquivo de saída
            valores = linha.split()
            #valores_em_radianos = [round(graus_para_radianos(float(valor)), 3) for valor in valores]
            #arquivo_saida.write(' '.join(map(str, valores_em_radianos)) + '\n')
            for valor in valores:
                arquivo_saida.write(' ')
                arquivo_saida.write(str(round(graus_para_radianos(float(valor)), 3)))
                arquivo_saida.write(' ')
            arquivo_saida.write('\n')

print("Valores convertidos de graus para radianos e salvos em", saida)
