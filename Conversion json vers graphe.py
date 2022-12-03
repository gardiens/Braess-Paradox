import json as json
import matplotlib.pyplot as plt
from numpy import inf

# x est en h^-1
gamma = 0.41
alpha = 2.6
latence = lambda x: L*m*(1+gamma*(x/kappa)**alpha)
latenceintegree= lambda x: L*m*(x + gamma*kappa*(x/kappa)**(alpha+1)/(1+alpha))
l = 3 #Longueur d'une voiture

reseauTest = {'A':{1:lambda x:x+50, 2: lambda x:2*x+30, 3: lambda x:3*x+10}, 1:{'B': lambda x:0}, 2:{'B': lambda x:0}, 3:{'B': lambda x:0}, 'B':{}}

def JSONversGraphe(fichier):
    return nx.adjacency_graph(json.load(open(fichier,'r')),directed=True, multigraph=False)

def ConversionJSONversDictionnaire(fichier):
    fichier = json.load(open(fichier,'r'))
    noeuds = []
    adjacence = []
    graphe = {}
    for point in fichier["nodes"]:
        noeuds.append(point["id"]) #On récupère les nœuds
    for liste in fichier["adjacency"]:
        adjacence.append(liste) #On récupère les données des routes où la n-ième liste récupérée contient les routes partant du n-ième nœud (avec longueur, type de route, vitesse maximale, et le nœud d'arrivée)
    for k in range(len(noeuds)):
        graphe[noeuds[k]] = {}
        for j in range(len(adjacence[k])):
            # Définition des constantes
            L = adjacence[k][j]["length"]
            mv =  1/adjacence[k][j]["max_v"]
            kappa = (1000/60)*(adjacence[k][j]["max_v"])/l #Facteur multiplicatif à ajuster #voiture/minute
            #Pour un autoroute : chaque route peut avoir au maximum 666 individus/min
            if adjacence[k][j]["highway"]=="motorway":
                #Autoroutes : 3 voies
                graphe[noeuds[k]][adjacence[k][j]["id"]] = [lambda x: L*mv* (1+gamma*(x/(3*kappa)**alpha)),+inf]
            elif adjacence[k][j]["highway"]=="trunk":
                #Routes principales : 2 voies
                graphe[noeuds[k]][adjacence[k][j]["id"]] = [lambda x: L*mv* (1+gamma*(x/(2*kappa)**alpha)),+inf]
            else:
                #Autres routes secondaires : 1 voie
                graphe[noeuds[k]][adjacence[k][j]["id"]] = [lambda x: L*mv* (1+gamma*(x/kappa)**alpha),+inf]
    return graphe
# Adjacence[k][j]  concerne la longueur de la route
# mv correspond à
#Gamma correspond à  temps saturation/ Temps libre,  on a t* = mv*V0/Vsat
# Kappa correspond à la capacité de la route


def DictionnaireAvecFonctionsLisibles(fichier):
    fichier = json.load(open(fichier,'r'))
    noeuds = []
    adjacence = []
    graphe = {}
    for point in fichier["nodes"]:
        noeuds.append(point["id"]) #On récupère les nœuds
    for liste in fichier["adjacency"]:
        adjacence.append(liste) #On récupère les données des routes où chaque liste récupérée est de la forme [nœud_depart, nœud_destination,]
    for k in range(len(noeuds)):
        graphe[noeuds[k]] = {}
        for j in range(len(adjacence[k])):
            graphe[noeuds[k]][adjacence[k][j]["id"]] = 'lambda x: '+str(adjacence[k][j]["length"]*60/adjacence[k][j]["max_v"])+'*(1+'+str(gamma)+'*(x/'+str(adjacence[k][j]["max_v"]/l)+')**'+str(alpha)
    return graphe


def ConversionJSONversDictionnairePotentiel(fichier):
    fichier = json.load(open(fichier,'r'))
    noeuds = []
    adjacence = []
    graphe = {}
    for point in fichier["nodes"]:
        noeuds.append(point["id"]) #On récupère les nœuds
    for liste in fichier["adjacency"]:
        adjacence.append(liste) #On récupère les données des routes où chaque liste récupérée est de la forme [nœud_depart, nœud_destination,]
    for k in range(len(noeuds)):
        graphe[noeuds[k]] = {}
        for j in range(len(adjacence[k])):
            # Définition des constantes
            La= adjacence[k][j]["length"]
            mv=  1/adjacence[k][j]["max_v"]
            kappa = (adjacence[k][j]["max_v"])/l

            graphe[noeuds[k]][adjacence[k][j]["id"]] = lambda x: (La*mv)*(x + gamma/((alpha+1)*kappa**alpha)* x**(alpha+1))
    return graphe


Eructest=ConversionJSONversDictionnaire("Eruc.json")