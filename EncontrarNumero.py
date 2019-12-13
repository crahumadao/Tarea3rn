import numpy as np
import nltk
import matplotlib.pyplot as plt
from AlgoritmoGenetico import AlgoritmoGenetico
import arboles
import ast




# la base de los arboles de este problema son dos:
# las funciones:
allowed_f = [arboles.AddNode, arboles.SubNode, arboles.MaxNode, arboles.MultNode]
# los terminales:
allowed_t = [25, 7, 8, 100, 4, 2]

nuevo_generador = ast.AST(allowed_f, allowed_t, 0.3)

# Seteo de parámetros para el GA.
numero = 65346
np.random.seed(42)
poblacion = 20


# puntaje mejorado ( con largo de arbol)



def unico(arbol):
    aux = []
    termis = [x for x in arbol.serialize() if isinstance(x, arboles.TerminalNode)]
    for i in termis:
        if i.eval() not in aux:
           aux.append(i.eval())
    return len(termis)-len(aux)


# puntaje agregando la no repeticion:
puntSel = 2
if puntSel==0:
    puntaje = (lambda x: abs(x.eval()-numero))
elif puntSel == 1:
    coef = 1
    puntaje = (lambda x: abs(x.eval()-numero)+coef*len(x.serialize()))
elif puntSel == 2:
    puntaje = (lambda x: abs(x.eval()-numero)+unico(x)*2000)



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
print('resultado:\t',mi.eval())
print('puntaje:\t',pmi)






