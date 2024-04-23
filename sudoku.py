import sys

def encontrar_espacio_vacio(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None


def movimiento_valido(tablero, fila, col, num):
    # Verificar fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False
    
    # Verificar columna
    for x in range(9):
        if tablero[x][col] == num:
            return False
    
    # Verificar subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[i + fila_inicial][j + col_inicial] == num:
                return False
    return True


def impresion(tablero):
    j = 0
    print("-------------------------")
    for fila in tablero:
        i = 0
        print("|", end=" ")
        for element in fila:
            i += 1
            print(element, end=" ")
            if i % 3 == 0:
                print("|", end=" ")
        j += 1
        print()
        if j % 3 == 0:
            print("-------------------------")


def solucion1_FB(tablero):
    vacio = encontrar_espacio_vacio(tablero)

    if vacio[0] == None:
        return True
    
    i, j = vacio

    for num in range(1, 10):
        if movimiento_valido(tablero, i, j, num):
            tablero[i][j] = num

            if solucion1_FB(tablero):
                return True

            tablero[i][j] = 0

    return False




def solucion2_BT(tablero):
    pass


def solucion3_BT_FC(tablero):
    pass


#Inicio del programa


tablero = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]]

print("Tablero inicial:")
impresion(tablero)

solucion1_FB(tablero)
print("\nSolución usando fuerza bruta:")
impresion(tablero)

tablero = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]]

# tablero_2 = [
#     [7, 1, 6, 4, 2, 3, 5, 8, 9],
#     [8, 5, 4, 9, 1, 7, 6, 2, 3],
#     [9, 2, 3, 8, 5, 6, 1, 4, 7],
#     [5, 9, 8, 3, 6, 1, 4, 7, 2],
#     [1, 6, 7, 2, 4, 8, 3, 9, 5],
#     [3, 4, 2, 5, 7, 9, 8, 1, 6],
#     [2, 8, 5, 6, 9, 4, 7, 3, 1],
#     [6, 3, 1, 7, 8, 2, 9, 5, 4],
#     [4, 7, 9, 1, 3, 5, 2, 6, 8]]

# print("\nSolución:")
# impresion(tablero_2)

# print("Es valido:")
# print(tablero_resuelto(tablero_2))
