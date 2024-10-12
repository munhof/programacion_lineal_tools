import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import Slider

def ordenar_vertices(vertices):
    """ Ordena los vértices en sentido antihorario respecto al centroide. """
    centroide = np.mean(vertices, axis=0)
    angulo = np.arctan2(vertices[:, 1] - centroide[1], vertices[:, 0] - centroide[0])
    orden = np.argsort(angulo)
    return vertices[orden]


def graficar_region_factible_2d(restricciones, tipo_restriccion, rhs, tipo_variables, funcion_coste):
    """
    Graficar la región factible para un problema lineal en 2D.
    :param restricciones: Coeficientes de las restricciones.
    :param tipo_restriccion: Tipos de restricciones (<= o =).
    :param rhs: Lados derechos de las restricciones.
    :param tipo_variables: Tipos de variables (no_neg, neg, libre).
    :param funcion_coste: Función de coste a minimizar/maximizar.
    """
    plt.plot()
    plt.figure(figsize=(10, 6))
    x = np.linspace(min(list(rhs) + [-max(rhs)]), max(list(rhs) + [-min(rhs)]), 400)

    # Graficar las líneas de las restricciones
    for i in range(len(tipo_restriccion)):
        y = (rhs[i] - restricciones[i][0] * x) / restricciones[i][1]
        plt.plot(x, y, label=f'{restricciones[i][0]}*x1 + {restricciones[i][1]}x2 {tipo_restriccion[i]} {rhs[i]}')

        # Sombrear la región factible para la restricción actual
        if restricciones[i][1] != 0:
            if restricciones[i][1] < 0:
                plt.fill_between(x, y, max(x), where=(y <= max(x)), alpha=0.5)
            else:
                plt.fill_between(x, y, min(x), where=(y >= min(x)), alpha=0.5)

    # Sombrear las regiones válidas para las variables (x1 y x2)
    if 'no_neg' in tipo_variables:
        plt.fill_between(x, 0, max(x), where=(x >= 0), alpha=0.5, color='lightgreen', label='x1 >= 0')
    elif 'neg' in tipo_variables:
        plt.fill_between(x, min(x), 0, where=(x <= 0), alpha=0.5, color='lightgreen', label='x1 <= 0')

    # Asumimos que 'x2' también es no negativa
    y_vals = np.linspace(min(x), max(x), 400)
    if 'no_neg' in tipo_variables:
        plt.fill_betweenx(y_vals, 0, max(x), where=(y_vals >= 0), alpha=0.5, color='lightcoral', label='x2 >= 0')
    elif 'neg' in tipo_variables:
        plt.fill_betweenx(y_vals, min(x), 0, where=(y_vals <= 0), alpha=0.5, color='lightcoral', label='x2 <= 0')

    # Encontrar los puntos de intersección (vértices de la región factible)
    vertices = []

    # Agregar los vértices de las restricciones con los ejes
    for i in range(len(restricciones)):
        # Intersección con el eje y (x1 = 0)
        if restricciones[i][0] != 0:  # Evitar división por cero
            y_intersect = rhs[i] / restricciones[i][1]  # Resolver para el eje y
            if 0 <= y_intersect <= max(rhs):
                vertices.append(np.array([0, y_intersect]))  # Agregar intersección al eje y

        if (tipo_variables[0] == "no_neg" or tipo_variables[0] == "neg") and (
                tipo_variables[1] == "no_neg" or tipo_variables[1] == "neg"):
            vertices.append(np.array([0, 0]))

        # Intersección con el eje x (x2 = 0)
        if restricciones[i][1] != 0:  # Evitar división por cero
            x_intersect = rhs[i] / restricciones[i][0]  # Resolver para el eje x
            if 0 <= x_intersect <= max(rhs):
                vertices.append(np.array([x_intersect, 0]))  # Agregar intersección al eje x

    # Verificar las intersecciones de las restricciones
    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            A = np.array([restricciones[i], restricciones[j]])
            b = np.array([rhs[i], rhs[j]])

            # Resolver el sistema de ecuaciones
            try:
                vertex = np.linalg.solve(A, b)  # Obtener el punto de intersección

                # Verificar que el vértice está en el rango del gráfico y cumple todas las restricciones
                if np.all(vertex >= 0) and np.all(vertex <= max(rhs)):
                    cumple_restricciones = False

                    # Verificar las restricciones del problema
                    for k in range(len(restricciones)):
                        if np.dot(restricciones[k], vertex) <= rhs[k]:
                            cumple_restricciones = True
                            break

                    # Verificar restricciones de las variables
                    if 'no_neg' in tipo_variables:
                        if np.any(vertex < 0):
                            cumple_restricciones = False
                    elif 'neg' in tipo_variables:
                        if np.any(vertex > 0):
                            cumple_restricciones = False

                    # Agregar el vértice si cumple todas las condiciones
                    if cumple_restricciones:
                        vertices.append(vertex)

            except np.linalg.LinAlgError:
                # Si no se puede resolver el sistema (por ejemplo, son paralelas), continuar
                continue

    if not vertices:
        return print("No se puede graficar")

    # Comprobar si se encontraron vértices válidos
    if len(vertices) > 0:
        vertices = np.array(vertices)
        filter_vertices = []
        for vertice in vertices:
            z = restricciones @ vertice
            cond = True
            for i in range(len(z)):
                if z[i] > rhs[i]:
                    cond = False
            if cond:
                filter_vertices.append(vertice)

        vertices = np.array(filter_vertices)
        print("Vértices encontrados:", vertices)
        # Ordenar los vértices para formar un polígono y sombrear la región de intersección
        vertices_ordenados = ordenar_vertices(vertices)
        polygon = Polygon(vertices_ordenados, closed=True, color='lightgreen', alpha=0.6)  # Aumentamos la opacidad
        plt.gca().add_patch(polygon)

        for vertice in vertices:
            plt.plot(vertice[0], vertice[1], ".", label = f'({vertice[0]:.2f}, {vertice[1]:.2f})')

    else:
        print("No se encontraron vértices válidos.")

    # Generar las líneas de nivel de la función de coste
    t_values = np.linspace(min(x), max(x), 20)  # Valores de t para las curvas de nivel
    for t in t_values:
        # Ecuación de la línea de nivel: funcion_coste[0]*x1 + funcion_coste[1]*x2 = t
        # Rearreglamos para obtener x2
        x1 = np.linspace(min(x), max(x), 400)
        x2 = (t - funcion_coste[0] * x1) / funcion_coste[1]

        # Asignar color basado en el valor de t
        color = plt.cm.viridis((t - min(t_values)) / (max(t_values) - min(t_values)))  # Gradiente de color
        plt.plot(x1, x2, linestyle='--', color=color, alpha=0.6)  # Dibujar la curva de nivel

    # Personalizar el gráfico

    plt.xlim(min(x) + 0.1 * min(x), max(x) + 0.1 * max(x))
    plt.ylim(min(x) + 0.1 * min(x), max(x) + 0.1 * max(x))
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Región Factible')
    plt.grid(True)

    # Leyenda fuera del gráfico
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend = plt.legend(by_label.values(), by_label.keys(), title='Referencias',
                        )

    # Agregar escala de curvas de nivel
    plt.colorbar(plt.cm.ScalarMappable(cmap='viridis'), label='Escala de Curvas de Nivel', orientation='horizontal')

    plt.show()


"""
# Ejemplo de uso
restricciones = np.array([[8., -6.], [8., 1]])
rhs = np.array([10., 20.])
tipo_restriccion = ['<=', '<=']
tipo_variables = ['no_neg', 'no_neg']
funcion_coste = np.array([-1., 1.])

graficar_region_factible_2d(restricciones, tipo_restriccion, rhs, tipo_variables, funcion_coste)
"""