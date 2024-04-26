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
    # Encontrar una posición vacía en el tablero (si hay alguna)
    fila, col = encontrar_espacio_vacio(tablero)
    
    # Si no hay espacios vacíos, hemos resuelto el sudoku
    if fila is None:
        return True
    
    # Probar con números del 1 al 9 en la posición vacía encontrada
    for num in range(1, 10):
        if movimiento_valido(tablero, fila, col, num):
            tablero[fila][col] = num  # Aplicar el número al tablero
            
            # Continuar con backtracking recursivamente
            if solucion2_BT(tablero):
                return True
            
            # Si no se encuentra solución, hacer backtrack
            tablero[fila][col] = 0
    
    # Si ninguno de los números funciona, retorno falso
    return False


def eliminar_dominios(tablero, fila, col, num, dominios):
    # Eliminar num de los dominios de las celdas en la misma fila, columna y subcuadrícula
    for i in range(9):
        dominios[fila*9 + i].discard(num)  # Fila
        dominios[i*9 + col].discard(num)  # Columna
        
        # Subcuadrícula
        cuad_fila, cuad_col = 3 * (fila // 3), 3 * (col // 3)
        for r in range(cuad_fila, cuad_fila + 3):
            for c in range(cuad_col, cuad_col + 3):
                dominios[r*9 + c].discard(num)

def solucion3_BT_FC(tablero):
    # Inicializar dominios para todas las celdas vacías
    dominios = {i: set(range(1, 10)) for i in range(81) if tablero[i//9][i%9] == 0}
    
    # Función recursiva con forward checking
    def backtrack():
        # Si todos los dominios son vacíos, hemos asignado un valor a cada celda
        if all(tablero[i//9][i%9] != 0 for i in range(81)):
            return True
        
        # Encontrar la próxima celda vacía con menos opciones en su dominio
        celda_vacia, min_dominio = min(((i, dominios[i]) for i in dominios if tablero[i//9][i%9] == 0),
                                        key=lambda x: len(x[1]), default=(None, None))
        if celda_vacia is None:
            return False
        
        fila, col = divmod(celda_vacia, 9)
        
        # Copia de seguridad de los dominios antes de cualquier cambio
        backup_dominios = dominios.copy()
        
        # Probar cada opción en el dominio de la celda
        for num in min_dominio:
            if movimiento_valido(tablero, fila, col, num):
                tablero[fila][col] = num
                eliminar_dominios(tablero, fila, col, num, dominios)
                
                # Si después de la asignación, ningún dominio es vacío, continuar con backtracking
                if all(dominios[i] for i in dominios):
                    if backtrack():
                        return True
                
                # Si la asignación no condujo a una solución, restaurar dominios y hacer backtrack
                tablero[fila][col] = 0
                dominios = backup_dominios.copy()
        
        return False

    # Iniciar backtracking
    return backtrack()




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
solucion2_BT(tablero)
print("\nSolución usando backtracking:")
impresion(tablero)
print("\nSolución usando backtracking con forward checking:")
if solucion3_BT_FC(tablero):
    print("Tablero resuelto:")
    impresion(tablero)
else:
    print("No se encontró solución.")
    
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
