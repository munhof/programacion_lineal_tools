import numpy as np
import matplotlib.pyplot as plt

def graficar_region_factible(restricciones, rhs, tipo_variables, tipo_restriccion, funcion_coste):
    # Número de variables (columnas de restricciones)
    rango = np.linalg.matrix_rank(restricciones)

    def plot_region_2d(restricciones, rhs, tipo_variables, tipo_restriccion):
        # Definir el rango de valores de las variables
        x1_vals = np.linspace(-10, 10, 400)
        x2_vals = np.linspace(-10, 10, 400)
        X1, X2 = np.meshgrid(x1_vals, x2_vals)

        # Crear una matriz de booleanos para identificar la región factible
        region_factible = np.ones(X1.shape, dtype=bool)

        # Verificar cada restricción y aplicar sobre la malla
        for i in range(rango):
            a, b = restricciones[i]
            c = rhs[i]

            if tipo_restriccion[i] == "<=":
                region_factible &= (a * X1 + b * X2 <= c)
            else:  # Asumimos que es de tipo "="
                region_factible &= (a * X1 + b * X2 == c)

        # Procesar el tipo de variables (positivas, negativas, libres)
        if tipo_variables[0] == 'no_neg':  # x1 >= 0
            region_factible &= (X1 >= 0)
        if tipo_variables[-1] == 'no_neg':  # x2 >= 0
            region_factible &= (X2 >= 0)

        # Graficar la región factible
        fig, ax = plt.subplots()
        ax.contourf(X1, X2, region_factible, levels=[0, 1], colors=['green'], alpha=0.3)

        # Graficar las líneas de las restricciones
        for i in range(rango):
            a, b = restricciones[i]
            c = rhs[i]

            if b != 0:
                # Resolver para x2
                x2_line = (c - a * x1_vals) / b
                ax.plot(x1_vals, x2_line, label=f'Restricción {i + 1}: {a}x1 + {b}x2 {tipo_restriccion[i]} {c}')
            else:
                ax.axvline(x=c / a, color='red', label=f'Restricción {i + 1}: {a}x1 {tipo_restriccion[i]} {c}')

        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.legend()
        ax.grid(True)
        plt.title('Región factible en 2D')
        plt.show()

    if rango == 2:
        plot_region_2d(restricciones, rhs, tipo_variables, tipo_restriccion)
        print("plot 2d")
    if rango == 3:
        print("no disponible aun")
        print("plot 3d")
