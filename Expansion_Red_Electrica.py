# Proyecto de red eléctrica: Primer mapeado con nodos conectados a la central eléctrica


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

    leyendas = {
        'colonia': 'Colonia con luz',
        'vacio': 'Colonia sin luz',
        'central': 'Central eléctrica'
    }

    for tipo, color in colores.items():
        plt.scatter([], [], c=color, label=leyendas[tipo], edgecolors='black')
    
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Leyenda")
    plt.title(titulo)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

visualizar_mapa_red(G)


#Aqui empieza el codigo para el segundo mapeo de los nodos que se conecten con el metodo prim

def obtener_subgrafo_luz(G):
    # Filtra nodos centrales y colonias (los que tienen luz)
    nodos_con_luz = [n for n, attr in G.nodes(data=True) if attr['tipo'] in ['central', 'colonia']]
    return G.subgraph(nodos_con_luz).copy()

def mst_prim(G_sub):
    # Usamos networkx para obtener el MST usando algoritmo de Prim
    mst = nx.minimum_spanning_tree(G_sub, algorithm='prim')
    return mst

def visualizar_red_con_mst(G, mst, titulo="Red eléctrica conectada con prim"):
    pos = nx.get_node_attributes(G, 'pos')
    
    # Colores nodos: verde/amarillo para nodos con luz, gris para los demás
    colores = []
    for n in G.nodes:
        tipo = G.nodes[n]['tipo']
        if tipo == 'central':
            colores.append('yellow')
        elif tipo == 'colonia':
            colores.append('green')
        else:
            colores.append('lightgray')
    
    plt.figure(figsize=(12, 9))
    
    # Dibujar grafo completo con nodos y aristas normales
    nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=700, edgecolors='black')
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    # Dibujar pesos en todas las aristas
    pesos = {(u, v): G[u][v]['peso'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=6)
    
    # Sobreponer MST con estilo más resaltado (aristas en azul grueso)
    nx.draw_networkx_edges(mst, pos, edge_color='blue', width=3)
    
    # Nodos en MST con borde negro y tamaño mayor para destacar
    nx.draw_networkx_nodes(mst, pos, node_color=[colores[n] for n in mst.nodes], node_size=900, edgecolors='black')
    
    # Leyenda
    leyendas = {
        'colonia': 'Colonia con luz',
        'central': 'Central eléctrica',
        'vacio': 'Colonia sin luz',
        'mst': 'Conexion por defecto'
    }
    for tipo, color in {'colonia': 'green', 'central': 'yellow', 'vacio': 'lightgray', 'mst': 'blue'}.items():
        plt.scatter([], [], c=color, label=leyendas[tipo], edgecolors='black' if tipo != 'mst' else 'none')
    
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Leyenda")
    plt.title(titulo)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

#Mandamos a llamar las funciones de expansion
G_luz = obtener_subgrafo_luz(G)
mst_luz = mst_prim(G_luz)

# Ya que tenemos la ruta con el prim solo la resaltamos
visualizar_red_con_mst(G, mst_luz)
