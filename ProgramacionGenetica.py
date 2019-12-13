import arboles
import ast
import random


def arbol_crossover(arbol1, arbol2, verb=False):
    arb1 = arbol1.copy()
    p1 = random.choice(arb1.serialize())
    arb2 = random.choice(arbol2.serialize()).copy()
    p1.replace(arb2)
    if verb:
        print("___________________________________________")
        print('arbol1copia:\n', arb1)
        print('punto1:\n ', p1)
        print('\n\n')
        print('arbol2:\n ', arbol2)
        print('sub arbol2:\n ', arb2)
        print('\n\n')
        print('arbol out:\n ',arb1)
        print("___________________________________________")
    return arb1


def arbol_mutacion(arbol1, generador, deepi=1, deepf=5, verb=False):
    arb1 = arbol1.copy()
    p1 = random.choice(arb1.serialize())
    arb2 = generador(random.randint(deepi, deepf))
    p1.replace(arb2)
    if verb:
        print("___________________________________________")
        print('arbol1copia:\n', arb1)
        print('punto1:\n ', p1)
        print('\n\n')
        print('mutacion:\n ', arb2)
        print('\n\n')
        print('arbol out:\n ', arb1)
        print("___________________________________________")
    return arb1

'''
allowed_f = [arboles.AddNode, arboles.SubNode, arboles.MaxNode, arboles.MultNode]
allowed_t = [1,   2,   3,   4,   5,'x']

nuevo_generador = ast.AST(allowed_f, allowed_t, 0.3)


arbol1 = nuevo_generador(2)
#arbol2 = nuevo_generador(2)
#arbol_crossover(arbol1, arbol2,verb=True)
#arbol_mutacion(arbol1, nuevo_generador,verb=True)
print(arbol1)
diccionario={'x': 2}
print('x=',diccionario['x'],'  \t',arbol1.eval(diccionario))

diccionario={'x': 3}
print('x=',diccionario['x'],'  \t',arbol1.eval(diccionario))

diccionario={'x': 4}
print('x=',diccionario['x'],'  \t',arbol1.eval(diccionario))

diccionario={'x': 5}
print('x=',diccionario['x'],'  \t',arbol1.eval(diccionario))




'''