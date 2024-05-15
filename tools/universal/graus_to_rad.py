import csv
import math

# Função para converter graus em radianos
def graus_para_radianos(graus):
    if graus < 180 and graus > -180:
        return graus * (math.pi/180)
    else:
        return graus

# Caminhos dos arquivos
arquivo_entrada = 'tools\graus_to_rad\getupFrontOld.pos'
arquivo_saida = 'tools\graus_to_rad\getupFrontNew.csv'

# Leitura do arquivo .pos e conversão para radianos
linhas_convertidas = []
with open(arquivo_entrada, mode='r') as arquivo_entrada:
    leitor = csv.reader(arquivo_entrada)
    # Ler o cabeçalho
    cabecalho = next(leitor)
    cabecalho[0].split()
    linhas_convertidas.append(cabecalho)  # Adiciona o cabeçalho na lista de linhas convertidas

    # Processa o restante das linhas
    for linha in leitor:
        if linha and not linha[0].startswith('#'):  # Verifica se a linha não está vazia e não é um comentário
            # Remove espaços em branco e divide a linha em valores individuais
            valores = linha[0].split()
            # Converte cada valor para radianos
            linha_convertida = [graus_para_radianos(float(valor)) for valor in valores]
            linhas_convertidas.append(linha_convertida)

# Escrever a nova tabela em um arquivo CSV
with open(arquivo_saida, mode='w', newline='') as arquivo_saida:
    escritor = csv.writer(arquivo_saida)
    # Escrever as linhas convertidas
    escritor.writerows(linhas_convertidas)

print(f"Arquivo convertido salvo como {arquivo_saida}")