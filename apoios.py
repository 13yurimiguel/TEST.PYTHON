 import numpy as np


def calculaCasoZero(n, L, q, IN):
    """
    De acordo com fórmula, apresenta
    o valor do caso zero de cada apoio
    """

    return -(1/3) * (L * (n-1)) * (
        (q * (L * (n-1)) ** 2) / 8
    ) * (
        (1 - (IN/(n-1))) * IN * L
    ) * (
        1 + ((1 - (IN/(n-1))) * (IN/(n-1)))
    )


def calculaDiagonal(n, L, IN):
    """
    De acordo com fórmula, calcula o valor dos elementos
    diagonais da matriz quadrática
    """
    return (-1 / 3) * L * (n - 1) * ((
        (1 - (IN / (n - 1))) * IN * L
    ) ** 2)


def calculaInferior(n, L, linha, coluna):
    """
    De acordo com fórmula, calcula o valor dos elementos
    inferiores (abaixo dos elementos diagonais) da matriz
    quadrática
    """
    s1 = coluna * L
    s2 = (linha - coluna) * L
    B1 = (1 - (coluna / (n - 1)))
    B2 = (1 - (linha / (n - 1)))
    i1 = B1 * s1
    i2 = (B1 * (s1 + s2) - s2)
    k1 = B2 * s1
    k2 = ((1 - (linha / (n - 1))) * (s1 + s2))
    s3 = (((n - 1) * L) - (s1 + s2))
    # return -(1/3) * 5 * 3.75 * 2.5 + (1/6) * 5 * (-2 * 3.75 * 2.5 - 3.75 * 5 - 2.5 * 2.5 -2 * 2.5 * 5) - (1/3) * 10 * 2.5 * 5
    return -(1/3) * s1 * i1 * k1 + (1/6) * s2 * (
        -2 * i1 * k1 - i1 * k2 - i2 * k1 - 2 * i2 * k2
    ) - (1/3) * s3 * i2 * k2


print("")
print("##################################################")
print("#                                                #")
print("#   Centro Universitário de Brasília - UNICeuB   #")
print("#   Teoria das estruturas                        #")
print("#   Yuri Miguel de Oliveira     - RA 21456352    #")
print("#   Diego Soares Bonifácio      - RA 21451480    #")
print("#   Isaac Ramon Borges da Silva - RA 21442250    #")
print("#                                                #")
print("##################################################")
print("")

n = input("Digite o numero de apoios (n): ")
n = int(n)


if n < 2:
    print("A viga eh hipostatica.")
    quit(0)

q = input("Digite a carga distribuida em Kn (q): ")
q = int(q)
L = input("Digite o tamanho do vão entre os apoios em metros (L): ")
L = int(L)


print("")
print("")
print("")

# Quando só temos dois apoios, dividimos L por dois para
# corrigir o cálculo de R1 e R2.
if n == 2:
    R1 = q*L/2.
    R2 = q*L/2.
    print('\nR1 = ', R1, 'kN')
    print('R2 = ', R2, 'kN')
    quit(0)

# Declara todas as matrizes
matrizCasoZero = []
matrizQuadratica = []


################################################################
# Matriz caso zero
for i in range(n-2):
    linha = i + 1
    matrizCasoZero.append(calculaCasoZero(n, L, q, linha))
################################################################

################################################################
# Criação das posições das vigas (matriz quadrática)
for i in range(n-2):
    linha = i + 1

    # Coloca dentro da matriz quadrática outra matriz
    matrizQuadratica.append([])


    # Criação dos casos (Coluna das matrizes)
    for j in range(n-2):
        coluna = j + 1
        itemArray = 0
        if i == j:
            itemArray = calculaDiagonal(n, L, coluna)
        elif i > j:
            itemArray = calculaInferior(n, L, linha, coluna)

        matrizQuadratica[i].append(itemArray)

# Copia valores inferiores para superiores
for i in range(n-2):
    for j in range(n-2):
        if i == j:
            continue
        elif i > j:
            continue
        matrizQuadratica[i][j] = matrizQuadratica[j][i]
################################################################

# Calcula determinante total
determinanteTotal = None
if len(matrizQuadratica):
    determinanteTotal = np.linalg.det(matrizQuadratica)


# Imprime matrizes e determinante
print("Matriz caso zero:")
print(np.array(matrizCasoZero))
print("")
print("Matriz quadrática:")
print(np.array(matrizQuadratica))
print("")
print("Determinante total: ", determinanteTotal)
print("")

reacoes = []
cont = 0
f = 0
# Calcula e imprime cada determinante
for i in range(n-2):
    matrizQuadraticaClone = np.copy(matrizQuadratica)
    for j in range(len(matrizCasoZero)):
        matrizQuadraticaClone[j][i] = matrizCasoZero[j]

    reacoes.append(np.linalg.det(matrizQuadraticaClone))

    print("Determinante R" + str(i+2), ":", reacoes[i])
    print("Matriz para cálculo de determinante para posição", i+2, ":")
    print(np.array(matrizQuadraticaClone))
    print("Reação R" + str(i+2) + ":", reacoes[i] / determinanteTotal)
    print("")

print("")
print("")
print("Relatório final:")
print("")

reacaoExtremidades = ((n-1)*L*q - (sum(reacoes))/determinanteTotal)/2

print("Reação R1:", reacaoExtremidades, "kN")
for i in range(len(reacoes)):
    print("Reação R" + str(i+2) + ":", reacoes[i] / determinanteTotal, "kN")

# Printa a última reação
print("Reação R" + str(n) + ":", reacaoExtremidades, "kN")

print("")
