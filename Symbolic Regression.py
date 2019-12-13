import numpy as np
import nltk
import matplotlib.pyplot as plt
from AlgoritmoGenetico import AlgoritmoGenetico
import arboles
import ast
'''
# Búsqueda de una funcion para un numero.
genes_disponibles = {0: 'a',
                     1: 'b',
                     2: 'c',
                     3: 'd',
                     4: 'e',
                     5: 'f',
                     6: 'g',
                     7: 'h',
                     8: 'i',
                     9: 'j',
                     10: 'k',
                     11: 'l',
                     12: 'm',
                     13: 'n',
                     14: 'ñ',
                     15: 'o',
                     16: 'p',
                     17: 'q',
                     18: 'r',
                     19: 's',
                     20: 't',
                     21: 'u',
                     22: 'v',
                     23: 'w',
                     24: 'x',
                     25: 'y',
                     26: 'z',
                     }

# La generación de genes es una letra del abecedario al azar.
def generagen_(genes_disponibles_):
    gen = genes_disponibles_[np.floor(len(genes_disponibles_) * np.random.random())]
    return gen


# La generación de individios a partir del largo, genera un individuo con letras al azar del tamaño correspondiente-
def generaind_(tamano_, generagen__):
    individuo = ''
    for _ in range(tamano_):
        aux = generagen__()
        individuo += aux
    return individuo





'''
# la base de los arboles de este problema son dos:
# las funciones:
allowed_f = [arboles.AddNode, arboles.SubNode, arboles.MultNode]
# los terminales:
allowed_t = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8,9, 10,'x','x','x','x','x','x']

rango_prueba=range(-100, 101)

nuevo_generador = ast.AST(allowed_f, allowed_t, 0.3)

# Seteo de parámetros para el GA.
objetivo = lambda x: x*x+x-6

np.random.seed(42)
poblacion = 20



def unico(arbol):
    aux = []
    termis = [x for x in arbol.serialize() if isinstance(x, arboles.TerminalNode)]
    for i in termis:
        if i.eval() not in aux:
           aux.append(i.eval())
    return len(termis)-len(aux)


def puntajesymbolic(x,rango_prueba,objetivo):
    diccionario ={}
    suma = 0
    for i in rango_prueba:
        diccionario['x']=i
        suma+=(objetivo(i)-x.eval(diccionario))**2
    return  suma

def paraplotear(x,rango_prueba,objetivo):
    diccionario ={}
    suma = 0
    original = []
    copia = []
    for i in rango_prueba:
        diccionario['x']=i
        original.append(objetivo(i))
        copia.append(x.eval(diccionario))
    return original, copia


puntaje =lambda x: puntajesymbolic(x,rango_prueba,objetivo)

generaind = (lambda x: nuevo_generador(x))

# Construcción del algoritmo para este caso.
GA = AlgoritmoGenetico(poblacion, puntaje, generaind, tasa_mutacion=0.1, cond_ter=50, prop=0.05, met_sel=True, maximo=False)
# (poblacion, puntaje, generagen, generaind, tasa_mutacion=0.2, cond_ter=500, met_sel=True, maximo=True, cov=False,
# prop= 0.02)

mi, pmi, historia = GA.evoluciona()

n = 0
prom_puntajes = []
for i in historia:
    n += 1
    lista_puntajes = list(i.values())
    prom_puntajes.append(np.mean(lista_puntajes))
    print('Puntaje promedio: {}, Máximo: {}, Mínimo: {}. En iteración {}'.format(np.mean(lista_puntajes),
                                                                                 max(lista_puntajes),
                                                                                 min(lista_puntajes), n))

plt.plot(prom_puntajes[5:])
plt.ylabel('Distancia al numero')
plt.xlabel('Generación')
plt.savefig('Distancia_Generacion.png')
plt.show()


print('mejor individuo:\n',mi)

print('puntaje:\t',pmi)


original,copia= paraplotear(mi,rango_prueba,objetivo)
plt.plot(rango_prueba,original,'r--',rango_prueba,copia,'b--')
plt.ylabel('Comparacion original(rojo), copia (azul)')
plt.xlabel('rango')
plt.savefig('Distancia_GeneracionX1.png')
plt.show()

