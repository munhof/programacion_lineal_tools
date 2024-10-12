import numpy as np



def convertir_forma_estandar(restricciones, tipo_restriccion, rhs, tipo_variables, funcion_coste):
    num_restricciones, num_variables = restricciones.shape
    rango = np.linalg.matrix_rank(restricciones)

    # Inicializar las matrices de holgura y variables artificiales
    holgura = np.zeros((num_restricciones, num_restricciones))
    nuevas_vars = []  # Para las variables introducidas (no negativas)
    coste_modificado = []  # Para la función de coste modificada

    # Ajustar las desigualdades a igualdades y manejar rhs negativo
    for i in range(num_restricciones):
        if rhs[i] < 0:
            restricciones[i] = -restricciones[i]
            rhs[i] = -rhs[i]
            if tipo_restriccion[i] == '<=':
                tipo_restriccion[i] = '>='
            elif tipo_restriccion[i] == '>=':
                tipo_restriccion[i] = '<='

        # Ajustar las desigualdades a igualdades
        if tipo_restriccion[i] == '<=':
            holgura[i][i] = 1  # Agregar variable de holgura positiva
        elif tipo_restriccion[i] == '>=':
            holgura[i][i] = -1  # Agregar variable artificial

    # Manejar las variables según su tipo y transformar la función de coste
    nuevas_restricciones = []
    for j in range(num_variables):  # Cambiar rango a num_variables
        col = restricciones[:, j]

        if tipo_variables[j] == 'no_neg':
            nuevas_restricciones.append(col)
            coste_modificado.append(funcion_coste[j])

        elif tipo_variables[j] == 'negativa':
            nuevas_restricciones.append(-col)  # Cambiar el signo de la columna
            nuevas_vars.append(f"x_neg_{j}")
            coste_modificado.append(-funcion_coste[j])

        elif tipo_variables[j] == 'libre':
            nuevas_restricciones.append(col)  # Para x_j^+
            nuevas_restricciones.append(-col)  # Para x_j^-
            nuevas_vars.extend([f"x_pos_{j}", f"x_neg_{j}"])
            coste_modificado.append(funcion_coste[j])  # Para x_j^+
            coste_modificado.append(-funcion_coste[j])  # Para x_j^-

    # Ahora agregar los coeficientes de las variables de holgura a la función de coste (ceros)
    coste_modificado.extend([0] * num_restricciones)  # Cambiar a num_restricciones

    # Convertir nuevas restricciones en una matriz y combinar con holgura
    nuevas_restricciones = np.array(nuevas_restricciones).T
    sistema_estandar = np.hstack((nuevas_restricciones, holgura))

    return sistema_estandar, rhs, nuevas_vars, coste_modificado

def mostrar_formato_estandar(sistema_estandar, rhs, funcion_coste):
    print("b      | sistema_estandar")
    print("---    |-----------------")
    for i in range(len(rhs)):
        fila = " ".join(f"{x:7.2f}" for x in sistema_estandar[i][:-1])
        print(f"{rhs[i]:<6.2f}| {fila}")

    print("---    |-----------------")
    fila_coste = " ".join(f"{x:7.2f}" for x in funcion_coste[:-1])
    print(f"-      | {fila_coste}")