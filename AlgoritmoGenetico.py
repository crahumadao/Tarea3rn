import numpy as np
from ProgramacionGenetica import arbol_mutacion, arbol_crossover

class AlgoritmoGenetico:

    #  Constructor del algoritmo genético, setea las funciones de puntajes generacion de genes e individuos.
    def __init__(self, poblacion, puntaje,
                  generaind, tasa_mutacion=0.2,
                 cond_ter=500, met_sel=True, maximo=True, cov=False, prop=0.02):
        self.poblacion = poblacion
        self.puntaje = puntaje
        self.generaind = generaind
        self.tasa_mutacion = tasa_mutacion
        self.cond_ter = cond_ter
        self.met_sel = met_sel
        self.lista_individuos = []
        self.maximo = maximo
        self.cov = cov
        self.prop = prop
        for i in range(poblacion):
            nuevo_ind = self.generaind(10)
            self.lista_individuos.append(nuevo_ind)

    # Evaluación Retorna el x% de la población con mejor puntaje y los puntajes de todos.
    def evaluacion(self, prop):
        aux_dic = dict()
        for individuo in self.lista_individuos:
            aux_dic[individuo] = self.puntaje(individuo)

        mejores = [k for k in sorted(aux_dic, key=aux_dic.get, reverse=False)]
        return mejores[:int(np.floor(prop * self.poblacion))], aux_dic

    # Selección retorna el x% de los indiviuos a competir ya sea en ruleta o en torneo.
    def seleccion(self):
        if self.met_sel:
            sum_tot = 0
            if self.maximo:
                for individuo in self.lista_individuos:
                    sum_tot += self.puntaje(individuo)
                prob = sum_tot * np.random.random()
                sum_par = 0
                for individuo in self.lista_individuos:
                    sum_par += self.puntaje(individuo)
                    if sum_par >= prob:
                        return individuo
            else:
                for individuo in self.lista_individuos:
                    try:
                        sum_tot += 1 / (self.puntaje(individuo))
                    except:
                        sum_tot+=0
                prob = sum_tot * np.random.random()
                sum_par = 0
                for individuo in self.lista_individuos:
                    try:
                        sum_par += 1 / (self.puntaje(individuo))
                    except:
                        sum_par+=0
                    if sum_par >= prob:
                        return individuo

        else:

            nindividuos = int(np.floor(self.poblacion * self.prop))
            indices = [int(self.poblacion * np.random.random()) for _ in range(nindividuos)]

            if self.maximo:
                punt_comparacion = -1000000000000000
            else:  # if minimo
                punt_comparacion = +1000000000000000

            individuo = None
            for indice in indices:
                if self.maximo:
                    if self.puntaje(self.lista_individuos[indice]) > punt_comparacion:
                        punt_comparacion = self.puntaje(self.lista_individuos[indice])
                        individuo = self.lista_individuos[indice]
                else:
                    if self.puntaje(self.lista_individuos[indice]) < punt_comparacion:
                        punt_comparacion = self.puntaje(self.lista_individuos[indice])
                        individuo = self.lista_individuos[indice]
            return individuo

    # Reproducción retorna el o los individuos que resultan de un crossOver o de una mutación.
    def reproduccion(self, individuo1, individuo2=None):

        hijo1 = arbol_crossover(individuo1, individuo2)

        if not self.cov:
            return hijo1
        else:
            lista_nuevos_individuos = [hijo1, ]
            hijo2 = arbol_crossover(individuo2, individuo1)
            lista_nuevos_individuos.append(hijo2)
        return lista_nuevos_individuos

    def mutacion(self, individuo):
        if np.random.random() < self.tasa_mutacion:
            individuo2 = arbol_mutacion(individuo,generador=self.generaind)
            return individuo2
        else:
            return individuo.copy()

    def evoluciona(self):
        # Datos por generación (tendrá individuos y sus respectivos fitness).
        datos_por_generacion = []
        for n_iteracion in range(self.cond_ter):
            mejores, evaluacion_general = self.evaluacion(0.5)
            datos_por_generacion.append(evaluacion_general)
            if n_iteracion % 5 == 0:
                print('Iteración número {}, hay {}/{} individuos'.format(
                    n_iteracion,
                    len(self.lista_individuos),
                    len(evaluacion_general)))

                # CrossOver (1 solo hijo)
            nueva_lista_individuos = []
            if not self.cov:
                iters_para_repoblar = self.poblacion
            else:
                iters_para_repoblar = np.round(self.poblacion / 2)
                # La Ruleta


            while True:
                if len(nueva_lista_individuos)==self.poblacion:
                    break
                elif len(nueva_lista_individuos)> self.poblacion:
                    nueva_lista_individuos=nueva_lista_individuos[:-1]

                else:
                    individuo1 = self.seleccion()
                    individuo2 = self.seleccion()
                    nuevo = self.reproduccion(individuo1, individuo2)
                    if np.random.random()<self.tasa_mutacion:
                        arbol_mutacion(nuevo, self.generaind)
                    #    if nuevo not in nueva_lista_individuos:
                    nueva_lista_individuos.append(nuevo)




            self.lista_individuos = nueva_lista_individuos
            # Mutaciones.
            #for indice in range(iters_para_repoblar):
            #    aux = self.mutacion(self.lista_individuos[int(indice)])
            #    self.lista_individuos[indice] = aux

        mejores, evaluacion_general = self.evaluacion(1)
        mejor_iteracion = mejores[0]
        return mejor_iteracion, self.puntaje(mejor_iteracion), datos_por_generacion
