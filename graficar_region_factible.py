import numpy as np
import matplotlib.pyplot as plt

def graficar_region_factible_2d(restricciones, tipo_restriccion, rhs, tipo_variables, funcion_coste):
    """
    es importante notar que todas las restricciones son del tipo <= o =
    :param restricciones:
    :param tipo_restriccion:
    :param rhs:
    :param tipo_variables: no_neg, neg, libre
    :param funcion_coste:
    :return:
    """

    x1 = []
    x2 = []

    if tipo_variables[0] == "no_neg":
        x1 = np.linspace(0, 10,100)
    elif tipo_variables[0] == "neg":
        x1 = np.linspace(-10, 0,100)
    else:
        x1 = np.linspace(-10, 10,100)

    if tipo_variables[1] == "no_neg":
        x2 = np.linspace(0,10,100)
    elif tipo_variables[1] == "neg":
        x2 = np.linspace(-10,0,100)
    else:
        x2 = np.linspace(-10,10,100)

    region = np.zeros([len(x1),len(x2)])
    
    for i in range(len(tipo_restriccion)):
        x = np.linspace(-10,10,100)
        plt.plot(x, (rhs[i] - restricciones[i][0] * x) / restricciones[i][1])
        


    for x in x1:
        for y in x2:
            pinto = True
            for i in range(len(tipo_restriccion)):
                if tipo_restriccion[i] == "<=":
                    pinto &= (restricciones[i][0] * x + restricciones[i][1] * y <= rhs[i])
                elif tipo_restriccion[i] == "=":
                    pinto &= (restricciones[i][0] * x + restricciones[i][1] * y == rhs[i])
            if pinto:
                plt.plot(x,y,".b")


    plt.plot(2*x1,0*x1,"--k")
    plt.plot(0*x2,2*x2,"--k")

    
    plt.grid()
    plt.show()

"""
restricciones = np.array([[ 1.,  -5.], [ 8., 9.]])
rhs = np.array([ 10., 5.])
tipo_restriccion = ['<=', '<=']
tipo_variables = ['no_neg', 'no_neg']
funcion_coste = np.array([-1.,  1.])

graficar_region_factible_2d(restricciones, tipo_restriccion, rhs, tipo_variables, funcion_coste)"""