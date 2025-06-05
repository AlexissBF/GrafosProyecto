# Proyecto de red eléctrica: Primer mapeado con nodos conectados a la central eléctrica
#aqui no hay ningun cambio

#Primero importamos las librerias necesarias para representar el grafo
#IMPORTANTE WACHOS primero descargar la libreria en la terminal -> !pip install networkx matplotlib

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from queue import PriorityQueue

G = nx.Graph()

n_filas = 5
n_columnas = 5

posiciones = {}
nodos_colonia = set()
central = None

# Crear nodos y seleccionar una central
for i in range(n_filas):
    for j in range(n_columnas):
        nodo_id = i * n_columnas + j
        x, y = j * 20, i * 20
        posiciones[nodo_id] = (x, y)
        G.add_node(nodo_id, tipo='vacio', pos=(x, y))

# Seleccionar una central eléctrica aleatoria (nodo amarillo)
central = random.choice(list(G.nodes))
G.nodes[central]['tipo'] = 'central'

# Esta funcion nos jala para hacer que las colonias aleatorias que esten conectadas con la red electrica'
def expandir_colonias(G, central, max_colonias=6):
    visitados = set()
    pq = PriorityQueue()
    visitados.add(central)
    contador_colonias = 0

    for vecino in obtener_vecinos(central):
        peso = random.randint(5, 15)
        pq.put((peso, central, vecino))

    while not pq.empty() and contador_colonias < max_colonias:
        peso, u, v = pq.get()
        if v not in visitados:
            G.add_edge(u, v, peso=peso)
            G.nodes[v]['tipo'] = 'colonia'
            nodos_colonia.add(v)
            visitados.add(v)
            contador_colonias += 1
            for vecino in obtener_vecinos(v):
                if vecino not in visitados:
                    peso = random.randint(5, 15)
                    pq.put((peso, v, vecino))

# Vecinos posibles en cuadrícula
def obtener_vecinos(nodo):
    i, j = divmod(nodo, n_columnas)
    vecinos = []
    if i > 0:
        vecinos.append((i - 1) * n_columnas + j)
    if i < n_filas - 1:
        vecinos.append((i + 1) * n_columnas + j)
    if j > 0:
        vecinos.append(i * n_columnas + (j - 1))
    if j < n_columnas - 1:
        vecinos.append(i * n_columnas + (j + 1))
    return vecinos

expandir_colonias(G, central)

# Asignamos valores a lazar en los aristas de 5 - 20

for i in range(n_filas):
    for j in range(n_columnas):
        nodo_actual = i * n_columnas + j
        for vecino in obtener_vecinos(nodo_actual):
            if not G.has_edge(nodo_actual, vecino):
                peso = random.randint(5, 20)
                G.add_edge(nodo_actual, vecino, peso=peso)

#Toda esta parte del codigo es para poder visualizar el mapeo del grafo sin conexiones aun con la biblioteca de import network

def visualizar_mapa_red(G, titulo="Red eléctrica - Mapeo inicial"):
    pos = nx.get_node_attributes(G, 'pos')
    colores = {'vacio': 'lightgray', 'colonia': 'green', 'central': 'yellow'}
    node_colors = [colores[G.nodes[n]['tipo']] for n in G.nodes]

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=8)

    pesos = {(u, v): G[u][v]['peso'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=6)

    for tipo, color in colores.items():
        plt.scatter([], [], c=color, label=tipo, edgecolors='black')
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Leyenda")
    plt.title(titulo)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

visualizar_mapa_red(G)

