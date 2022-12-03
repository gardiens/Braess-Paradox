import networkx as nx
import json as json
import matplotlib.pyplot as plt

def JSONversGraphe(fichier):
    return nx.adjacency_graph(json.load(open(fichier,'r')),directed=True, multigraph=False)

def afficherGrapheDepuisJSON(fichier):
    G = JSONversGraphe(fichier)
    adjacence = json.load(open(fichier,'r'))
    coordonnees = {}
    numeroSommet = 0
    for sommet in adjacence["nodes"]:
        coordonnees[numeroSommet]=(adjacence["nodes"][numeroSommet]["lon"],adjacence["nodes"][numeroSommet]["lat"])
        numeroSommet += 1
    plt.clf()
    nx.draw_networkx(G, pos=coordonnees, with_labels=True, node_size=10, font_size=1)
    plt.axis('equal')
    plt.show()