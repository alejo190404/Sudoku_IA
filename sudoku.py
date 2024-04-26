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


def es_tablero_valido(tablero):
    # Verifica si hay espacios vacíos
    for fila in tablero:
        if 0 in fila:
            return False

    # Verifica filas
    for fila in tablero:
        if not es_valida(fila):
            return False

    # Verifica columnas
    for col in range(9):
        columna = [fila[col] for fila in tablero]
        if not es_valida(columna):
            return False

    # Verifica cajas
    for fila_caja in range(0, 9, 3):
        for col_caja in range(0, 9, 3):
            caja = [tablero[fila][col]
                    for fila in range(fila_caja, fila_caja + 3)
                    for col in range(col_caja, col_caja + 3)]
            if not es_valida(caja):
                return False

    return True

def es_valida(lista):
    # Verifica que todos los elementos sean únicos y estén en el rango correcto
    elementos = [elemento for elemento in lista if elemento != 0]
    return len(elementos) == len(set(elementos)) and set(elementos).issubset(set(range(1, 10)))

def unir_filas(matriz):
    # Une en una fila, todas las filas de una matriz
    filas_unidas = []
    for fila in matriz:
        filas_unidas.extend(fila)

    return filas_unidas

def lista_a_matriz(lista, n):
    # Transforma una lista y la separa en una matriz nxn
    matriz = []
    for i in range(n):
        fila = lista[i*n:(i+1)*n]
        matriz.append(fila)

    return matriz

def increment_number(digits, protected_indices):
    # Caso base: si la lista está vacía, devuelve [1]
    if not digits:
        return [1]

    # Toma el último dígito de la lista y su índice
    last_index = len(digits) - 1
    last_digit = digits[-1]

    # Si el último índice está en la lista de índices protegidos
    if last_index in protected_indices:
        # Llama recursivamente a la función con la lista restante
        # (excepto el último dígito)
        new_digits = increment_number(digits[:-1], protected_indices)

        # Concatena el último dígito al final de la nueva lista devuelta
        new_digits.append(last_digit)
        return new_digits

    # Si el último dígito es menor que 9, lo incrementa y devuelve la lista actualizada
    if last_digit < 9:
        digits[-1] = last_digit + 1
        return digits

    # Si el último dígito es 9, lo establece en 0 y llama recursivamente a la función
    # con la lista restante (excepto el último dígito)
    else:
        digits[-1] = 0
        new_digits = increment_number(digits[:-1], protected_indices)

        # Concatena el 0 al final de la nueva lista devuelta por la llamada recursiva
        new_digits.append(0)
        return new_digits

def encontrar_no_vacios(tablero):
    lista = []
    for i in range(9):
        for j in range(9):
            if tablero[i][j] != 0:
                lista.append(i + (j * 10))
    return lista

def solucion1_FB(tablero):
    lista = encontrar_no_vacios(tablero)
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                tablero[i][j] = 1
    impresion(tablero)
    while(not(es_tablero_valido(tablero))):
        filas = unir_filas(tablero)
        filasIncrement = increment_number(filas, lista)
        tablero = lista_a_matriz(filasIncrement, 9)



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


def solucion3_BT_FC(tablero):
    dominios = {i: set(range(1, 10)) if tablero[i // 9][i % 9] == 0 else {tablero[i // 9][i % 9]} for i in range(81)}

    def eliminar_dominios(fila, col, num):
        afectados = set()
        for i in range(9):
            indices = [
                (fila, i),  # Fila
                (i, col),  # Columna
                (3 * (fila // 3) + i // 3, 3 * (col // 3) + i % 3)  # Subcuadrícula
            ]
            for f, c in indices:
                idx = f * 9 + c
                if num in dominios[idx] and len(dominios[idx]) > 1:  # Solo modificar si hay más de una opción
                    dominios[idx].remove(num)
                    afectados.add((f, c))
                    if not dominios[idx]:  # Fallo si algún dominio está vacío
                        return False, set()
        return True, afectados

    def restaurar_dominios(afectados, num):
        for f, c in afectados:
            dominios[f * 9 + c].add(num)


    def backtrack():
        # Encuentra el índice de la celda vacía con el menor número de valores posibles en su dominio (MRV Heuristic).
        idx = min((i for i in range(81) if tablero[i // 9][i % 9] == 0), key=lambda x: len(dominios[x]), default=None)

        if idx is None:  # No hay más espacios vacíos, lo que significa que el Sudoku está resuelto
            return True

        fila, col = idx // 9, idx % 9  # Convertir índice lineal en coordenadas de fila y columna

        for num in list(dominios[fila * 9 + col]):  # Iterar sobre una copia porque el conjunto puede cambiar
            if movimiento_valido(tablero, fila, col, num):
                tablero[fila][col] = num
                success, afectados = eliminar_dominios(fila, col, num)
                if success:
                    if backtrack():
                        return True
                tablero[fila][col] = 0
                restaurar_dominios(afectados, num)

        return False


    return backtrack()

# Usar el código en el entorno de prueba y asegurarse de que el tablero inicial se establece correctamente





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

#No se ejecuta por fuerza bruta, pues demoraría 480901057067040820250070093540030076029564130130090045370080014014050760690407082 operaciones
#solucion1_FB(tablero)
#print("\nSolución usando fuerza bruta:")
#impresion(tablero)

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
print("\nTablero inicial:")
impresion(tablero)
solucion2_BT(tablero)
print("\nSolución usando backtracking:")
impresion(tablero)

print("\nTablero inicial:")
impresion(tablero)
print("\nSolución usando backtracking con forward checking:")

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
print("\nTablero inicial:")
impresion(tablero)
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
