# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Facundo Munho)s
"""
import numpy as np
import re
from convertir_a_diccionario import convertir_forma_estandar
from convertir_a_diccionario import mostrar_formato_estandar
from graficar_region_factible import graficar_region_factible_2d
import sys


def procesar_problema(problema):
    # Inicializar listas
    funcion_coste = []
    restricciones = []
    rhs = []
    tipo_restriccion = []
    tipo_variables = []

    # Separar líneas del problema
    lineas = problema

    # Procesar la función de coste
    coef_coste = re.findall(r"([-+]?\d*\.?\d*)x\d+",lineas[0].replace("−", "-").replace(" ", ""))
    for coef in coef_coste:
        if coef == "-" or coef == "+" or coef == "":
            funcion_coste.append(float(coef + "1"))
        else:
            funcion_coste.append(float(coef))

    funcion_coste = np.array(funcion_coste)


    rango = len(funcion_coste)

    if lineas[0].startswith("min"):
        funcion_coste = -1 * funcion_coste

    # Procesar las restricciones
    for linea in lineas[1:len(lineas) - rango]:
        # Restricciones de desigualdades y igualdades
        if "≤" in linea or ">=" in linea or "=":
            linea = linea.replace("s.a:", "")
            linea = linea.replace(" ", "")
            linea = linea.replace("−", "-")
            restriccion = re.findall(r"([-+]?\d*\.?\d*)x\d+", linea)

            # Extraer el valor de rhs
            rhs_valor = float(re.findall(r"(?<=[≤≥=<>])\s*([-+]?\d+\.?\d*)", linea)[0])

            # Agregar la restricción a la lista
            coeficientes_restriccion = []
            for coef in restriccion:
                coef = coef.strip()
                if coef == "+" or coef == "":
                    coef = 1
                elif coef == "-":
                    coef = -1
                coeficientes_restriccion.append(float(coef))

            # Detectar tipo de restricción
            if "≤" in linea or "<=" in linea:
                tipo_restriccion.append("<=")
            elif "≥" in linea or ">=" in linea:
                tipo_restriccion.append(">=")
                # Invertir los coeficientes y rhs para mantener la restricción como <=
                coeficientes_restriccion = [-c for c in coeficientes_restriccion]
                rhs_valor = -rhs_valor  # Invertir el valor de rhs
            elif "=" in linea:
                tipo_restriccion.append("=")

            restricciones.append(coeficientes_restriccion)
            rhs.append(rhs_valor)

    # Procesar variables con restricciones sobre las variables
    for linea in lineas[len(lineas) - rango:]:
        for j in range(len(linea)):
            if f"x{j + 1}" in linea:
                if "≥" in linea or ">=" in linea:
                    tipo_variables.append("no_neg")
                if "≤" in linea or "<=" in linea:
                    tipo_variables.append("negativa")
                if "libre" in linea:
                    tipo_variables.append("libre")

    # Alinear las restricciones
    restricciones_extendidas = [
        restriccion + [0] * (rango - len(restriccion)) for restriccion in restricciones]

    # Formato de salida
    return {
        "restricciones": np.array(restricciones_extendidas),
        "rhs": np.array(rhs),
        "tipo_restriccion": tipo_restriccion,
        "tipo_variables": tipo_variables,
        "funcion_coste": funcion_coste
    }

#Algunos casos de test:
# 3 variables
"""
max x1−x2+x3
s.a: x1 + 2x2 − x3≤3
x1 − x2 − x3 ≤ −2
x1 − x2 = 10
x1 ≥ 0
x2 ≤ 0
x3 libre
"""
#2 variables infactibles
"""
max x1-x2
s.a: x1 + 2x2 ≤3
x1 − x2  ≤ −2
x1 + 3x2 >= 10
x1 ≥ 0
x2 >= 0
"""
#2 varibales factibles
"""
max 13x1 + 16x2 + 11x3
8x1 + 16x2 + 12x3 <= 240
4x1 + 8x2 + 10x3 >= 90
7x1 + 9x2 + 8x3 = 110
x1 >= 0
x2 >= 0
x3 >= 0
"""

print("Ingrese el problema e ingrese -1 cuando termine el problema: ")

problema = []
entrada = input()
while entrada != "-1":
    problema.append(entrada)
    entrada = input()

print("Problema original:")
print(problema)

resultado = procesar_problema(problema)

print("-----------------------------------------------------------------------")
print("Problema en matriz")
# Construir la expresión con los coeficientes y variables (x1, x2, etc.)
expresion = " + ".join(f"({coef})x{i+1}" for i,
                       coef in enumerate(resultado["funcion_coste"]))
# Imprimir el resultado con 'problema[0:3]'
print(problema[0:3], " ", expresion)
# Imprimir las restricciones con el formato que deseas
print("s.a")
for i, fila in enumerate(resultado["restricciones"]):
    fila_str = " ".join(f"{coef}" for j, coef in enumerate(fila))
    print(f"[{fila_str}] {'[x'+str(i+1)+']' if i <= len(resultado['tipo_variables']) else ''}  {resultado['tipo_restriccion'][i]} [{resultado['rhs'][i]}]")

for _, key in enumerate(resultado):
    print(f"{key}")
    print(f"{resultado[key]}")


if len(resultado['tipo_variables']) == 2:
    orden = input("Deseas graficar [Yes]/No")
    if orden in ["Y","y","Yes","yes"] or orden == "":
        graficar_region_factible_2d(resultado["restricciones"], resultado["tipo_restriccion"], resultado["rhs"], resultado["tipo_variables"],resultado["funcion_coste"])


print("-----------------------------------------------------------------------")

sistema_estandar, rhs_estandar, nuevas_vars, coste_modificado = convertir_forma_estandar(
    resultado["restricciones"], resultado["tipo_restriccion"], resultado["rhs"], resultado["tipo_variables"],
    resultado["funcion_coste"])


mostrar_formato_estandar(sistema_estandar, rhs_estandar, coste_modificado)
