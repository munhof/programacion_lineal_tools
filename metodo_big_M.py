import numpy as np


def simplex_bigM(sistema_estandar, rhs, nuevas_vars, coste_modificado, M=10 ** 6):
    """
    Método Simplex con Big-M para maximización a partir del sistema estandarizado.
    Incluye impresión del valor de los vectores y del vértice en cada iteración.

    sistema_estandar: matriz de coeficientes del sistema estandarizado (A).
    rhs: vector b del lado derecho de las restricciones (rhs).
    nuevas_vars: lista con las variables de holgura y artificiales añadidas.
    coste_modificado: vector con el coste de la función objetivo, incluyendo penalizaciones para Big-M.
    M: valor grande para la penalización en la función objetivo.
    """
    A_extendido = np.array(sistema_estandar, dtype=float)  # Convertir sistema estandarizado en un array
    b = np.array(rhs, dtype=float)  # Vector b (lado derecho)
    c_extendido = np.array(coste_modificado, dtype=float)  # Coste modificado de la función objetivo

    num_filas, num_columnas = A_extendido.shape
    print("Tabla inicial:")
    imprimir_tabla_bigM(A_extendido, b, c_extendido, nuevas_vars)

    iteracion = 0
    while np.any(c_extendido > 0):  # Mientras haya coeficientes positivos en la función objetivo
        iteracion += 1
        print(f"\nIteración {iteracion}:")

        # Columna pivote (entra a la base)
        pivot_col = np.argmax(c_extendido) # Me quedo con el nuevo maximo
        print(f"Columna pivote: {pivot_col} (Variable que entra: {nuevas_vars[pivot_col]})")

        # Calcular ratios
        ratios = b / A_extendido[:, pivot_col]
        positivos = ratios[ratios > 0]

        if len(positivos) == 0:
            print("El problema es no acotado (no hay filas pivote válidas).")
            return None

        # Fila pivote (sale de la base)
        pivot_row = np.where(ratios == np.min(positivos))[0][0]
        print(f"Fila pivote: {pivot_row} (Variable que sale: {nuevas_vars[pivot_row]})")

        # Realizar el pivoteo
        A_extendido[pivot_row] /= A_extendido[pivot_row, pivot_col]
        b[pivot_row] /= A_extendido[pivot_row, pivot_col]
        for i in range(num_filas):
            if i != pivot_row:
                factor = A_extendido[i, pivot_col]
                A_extendido[i] -= factor * A_extendido[pivot_row]
                b[i] -= factor * b[pivot_row]

        # Actualizar la función objetivo
        factor_obj = c_extendido[pivot_col]
        c_extendido -= factor_obj * A_extendido[pivot_row]

        # Imprimir los valores de los vectores en esta iteración
        print("Estado de los vectores:")
        print(f"Vector b: {b}")
        print(f"Función objetivo: {c_extendido}")

        # Imprimir el vértice actual
        imprimir_vertice(A_extendido, b, c_extendido, nuevas_vars)

        print("\nTabla actualizada:")
        imprimir_tabla_bigM(A_extendido, b, c_extendido, nuevas_vars)

    print("\nSolución óptima encontrada:")
    imprimir_tabla_bigM(A_extendido, b, c_extendido, nuevas_vars)
    return b, c_extendido


def imprimir_vertice(A_extendido, b, c_extendido, nuevas_vars):
    """
    Imprime el vértice actual en la forma:
    x1 = ... x2 = ... para las variables básicas y no básicas.
    """
    print("Vértice actual (variables básicas y no básicas):")
    num_filas, num_columnas = A_extendido.shape
    for i in range(num_filas):
        ecuacion = f"w{i + 1} = {b[i]:.2f}"
        for j in range(num_columnas):
            if A_extendido[i, j] != 0:
                signo = "-" if A_extendido[i, j] < 0 else "+"
                ecuacion += f" {signo} {abs(A_extendido[i, j]):.2f}{nuevas_vars[j]}"
        print(ecuacion)
    print(f"z = {' + '.join(f'{c_extendido[j]:.2f}{nuevas_vars[j]}' for j in range(num_columnas))}")


def imprimir_tabla_bigM(A_extendido, b, c_extendido, nuevas_vars):
    """
    A_extendido: matriz extendida con coeficientes del sistema estandarizado.
    b: vector rhs (lado derecho).
    c_extendido: vector de la función objetivo.
    nuevas_vars: lista de nombres de variables en el sistema estandarizado.
    """
    print(f"{'Variables':<12}{'Coeficientes':<50}{'RHS'}")
    for i in range(A_extendido.shape[0]):
        coef = " ".join(f"{A_extendido[i, j]:.2f}" for j in range(A_extendido.shape[1]))
        print(f"{nuevas_vars[i]:<12} {coef:<50} {b[i]:.2f}")
    print(f"{'Costes reducidos.':<12} {' '.join(f'{v:.2f}' for v in c_extendido)}")


# Ejemplo de uso:
sistema_estandar = [
    [2, 1, 1, 0],  # Coeficientes del sistema estandarizado
    [1, 2, 0, 1]
]
rhs = [6, 8]  # Vector b (rhs)
nuevas_vars = ['x1', 'x2', 's1', 's2']  # Variables con holguras
coste_modificado = [3, 2, 1000000, 1000000]  # Función objetivo modificada para Big-M

# Llamar al método Big-M
simplex_bigM(sistema_estandar, rhs, nuevas_vars, coste_modificado)
