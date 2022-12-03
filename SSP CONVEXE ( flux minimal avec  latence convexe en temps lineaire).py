## Calcul  du problème du cout de Flux minimal
"""FICHIER POUR LE CALCUL DE COUT DE FLUX MINIMAL POUR DES FONCIONS CONVEXES AVEC UN GRAPHE RESIDUEL QUI ASSOCIE  A UN DEPLACEMENT DINDIVIDU UN PAR UN """
"""Fortement inspiré de http://cs.yazd.ac.ir/hasheminezhad/STSCS4R1.pdf page 570"""
""" La solution est apporté pour des unités de flux entière """
"""  LA CAPACITE SERA NEGLIGEE"""
from math import *
import numpy as np

## Dijkstra
def lePlusProche(liste, distance):
    """Cherche parmi les sommets pas encore étudiés celui dont la distance depuis le départ est la plus petite"""
    leplusproche = 0
    distance_min = +inf
    for sommet in liste:
        if distance_min >= distance[sommet]:
            distance_min = distance[sommet]
            leplusproche = sommet
    return leplusproche

def nouvelleDistance(s1,s2, graphe, distance, predecesseur):
    """Compare la distance déjà établie pour aller du départ à s2 avec la distance départ-s1-s2"""
    if distance[s2] > distance[s1]+graphe[s1][s2]:
        distance[s2] = distance[s1]+graphe[s1][s2]
        predecesseur[s2] = s1 #On note via quel sommet la distance est la plus courte pour aller à s2


def Dijkstra(graphe, depart,destination):
    """Renvoie le graphe des distances par rapport au départ et de l'autre part du tuple le chemin le plus rapide   """
    # Complexité O(nombre arête + nombre sommet)
    listeAttente = [sommet for sommet in graphe] #On met tous les sommets dans la liste d'attente
    distance = {}
    predecesseur = {}
    for sommet in graphe:
        """Initialisation : on affecte à tout les sommets une distance infinie, sauf au point de départ (qui est à distance 0 de lui-même)"""
        distance[sommet] = +inf
    distance[depart] = 0
    while listeAttente != []:
        """On prend dans la liste d'attente le sommet le plus proche du départ, et on l'enlève de la liste d'attente."""
        s = lePlusProche(listeAttente, distance)
        listeAttente.remove(s)
        """On regarde si, par hasard, ce serait pas plus rapide d'atteindre ce sommet par un de ses voisins, plutôt que par le chemin déjà connu"""
        for voisin in graphe[s]:
            nouvelleDistance(s, voisin, graphe, distance, predecesseur)
    chemin = [destination]
    if destination in predecesseur:
        while chemin[0] != depart:
            chemin = [predecesseur[chemin[0]]]+chemin
        return (distance,chemin)

## Recuperation Dijkstra fin

import numpy as np


def recuperergrapheentrantsortant(graphecout):
    """" Renvoi un graphe qui conteint des tuples avec (listedessommets qui va vers i , listedessommets qui sorts de i)"""
    graphe={}
    # Complexité en O(nombre arete + nombre sommet)
    #Initialisation
    for i in graphecout:
        graphe[i]=[[],[]]


    # On balaye toutes les arêtes pour obtenir le resultat
    for i in graphecout:
        for j in graphecout[i]:
            graphe[j][0].append(i) # On rajoute l'entrée qui est i
            graphe[i][1].append(j) # La sortie
    return graphe





def imbalance(flux,m,depart, arrivee ):
    """" Renvoi le graphe qui contient l'imbalance  du graphe"""
    # L'imbalance vaut  somme du flux qui rentre- somme  du flux qui sort pour ceux qui sont qui ne sont ni l'entrée ni la sortée
    #  Sinon il vaut +- m + somme entrée - somme sortie  si c'est le depart ou l'arrivee
    # C'est le déséquilibre du graphe
    # Complexité O( nombre arête + nombre sommet)
    graphe={}

    # Initialisation du graphe
    for i in flux:
        if i ==arrivee:
            graphe[i]=-m
        elif i== depart:
            graphe[i]= m
        else:
            graphe[i]=0


    grapheentrantsortant= recuperergrapheentrantsortant(flux)
    for i in flux: # On regarde chaque somet du graphe
        [entranti,sortanti]=grapheentrantsortant[i] # On récupère les sommets entrant et sortant
        sommeentranti=0
        sommesortanti=0 # On calcule séparément les sommes
        for k in entranti:
            sommeentranti+=flux[k][i]

        for j in sortanti:
            sommesortanti+=flux[i][j]

        graphe[i]= graphe[i] + sommeentranti-sommesortanti
    return graphe





def sommetexcesdeficit(flux,m,depart,arrivee):
    """renvoie ([sommetenexces],[sommetendeficit])"""
    # Un exces est défini comme un sommet qui a un imbalance >0 et réciproquement pour le deficit
    # Complexité O( nombre sommet + nombre arête)
    grapheimbalance= imbalance(flux,m,depart,arrivee)

    sommetexces=[]
    sommetdeficit=[]
    for i in grapheimbalance:
        if grapheimbalance[i]>0:
            sommetexces.append(i)
        elif grapheimbalance[i]<0:
            sommetdeficit.append(i)

    return (sommetexces,sommetdeficit)



## Fin paquet commun à tous


def Grapheresiduelfonctionconvexe(graphecout,flux):
    """ Renvoie le graphe residuel"""
    # :Graphe cout est le graphe ou on a stocké les fonctions de couts , à chaque entrée on associe un cout
    # Flux est un graphe ou on a insérer le nombre d'individu
    # Graphe résiduelle est un graphe temporaire associé au flux qui va être utile pour résoudre notre problème
    # Ce graphe résiduel est pour SSPconvexe, il a donc pas de capacité
    # Complexité en O( nombre arete + nombre sommet)
    grapheresiduel={}

    # Initialisation du graphe
    for i in graphecout:
        grapheresiduel[i]={}

    for i in graphecout:
        for j in graphecout[i]:
            #print(i,j)
            #print(flux[i])

            xij= flux[i][j] # C'est le nombre d'invidu sur l'arête (i,j)
            # ici on néglige la capacité, on a toujours une arete de i vers j
            grapheresiduel[i][j]=graphecout[i][j](xij+1)-graphecout[i][j](xij)
            if xij>0: # Cas ou il faut ajouter une arête dans l'autre sens parce qu'on a un flux non nul
                grapheresiduel[j][i]=graphecout[i][j](xij-1)-graphecout[i][j](xij)




    return grapheresiduel











def misajourpotentiel(sommetpotentiel,d):
    """ Mets a jour des potentiels in place"""
    # D est le graphe des plus petites distances par rapport à un point i donnée
    for i in sommetpotentiel:
        sommetpotentiel[i]= sommetpotentiel[i]-d[i]
    return



def obtenirgrapheResiduelAvecCoutPotentiel(graphecout,flux,sommetpotentiel):
    """ Renvoie le graphe résiduel mais auquel on a ajouter les potentiels associés aux sommets"""
    #  Renvoie le graphe  avec les fonctions de cout de potentiel réduit
    graphecoutpotentiel=Grapheresiduelfonctionconvexe(graphecout,flux) # On récupère le graphe
    for i in graphecoutpotentiel: # On va rajouter à chaque arête le cout engendré par le potentiel
        for j in graphecoutpotentiel[i]:
            graphecoutpotentiel[i][j]=graphecoutpotentiel[i][j]+ sommetpotentiel[j]-sommetpotentiel[i] # Le potentiel est défini comme cij pi = cij + pi(j)-pi(i)


    return graphecoutpotentiel



# Inspiré de la page 338 et 520
# Base sur le principe qu'un flux x est solution si
def SSPconvexe(graphecout,m,depart,arrivee):
    # Algorithme qui calcule un flux de cout minimal pour un flux entier en placant chaque individu un par un

    listesommet=[]
    sommetpotentiel={} # il va stocker graphe[sommet]= fonctionpotentielle associé
    pseudoflux={} # ICI C'est un PSEUDOFLUX

    #initialisation de l'algorithme

    # On initialise le pseudoflux au minimum de chaque arête
    for i in graphecout:
        pseudoflux[i]={}
        for j in graphecout[i]:
            xij=0
            while graphecout[i][j](xij)>graphecout[i][j](xij+1):
                xij+=1
            #  Si la boucle s'arrête on est "au creux" de la fonction convexe
            pseudoflux[i][j]=xij
    # les flux sont initialisés
    #Initialisation potentiel
    for  sommet in graphecout:
        listesommet.append(sommet) # on récupère les sommets
        sommetpotentiel[sommet]=0 # les fonctions de potentiels sont nuls
    # Corps du programme
    (E,D)=sommetexcesdeficit(pseudoflux,m,depart,arrivee) # ce sont les sommets en exces et en déficit qu'on va devoir réglé
    grapheresiduelcoutpotentiel= obtenirgrapheResiduelAvecCoutPotentiel(graphecout,pseudoflux,sommetpotentiel)
    while E!=[]:
         # Tant qu'il existe encore un sommet en exces
        k= E[0] # on en choisit un en excès
        i=D[0] # On choisit un element de E et de D
        (graphedistance,P)= Dijkstra( grapheresiduelcoutpotentiel, k,i) # Graphe des distances par rapport à  K et de l'autre  coté le chemin jusqu'à J. P correspond à un chemin de k vers i
        misajourpotentiel(sommetpotentiel,graphedistance) # On met à jour le potentiel
        # On va maintenant faire transiter une unité de pseudoflux de K vers I
        for i in range(len(P)-1):
            deb=P[i]
            sortie=P[i+1]
            if sortie in pseudoflux[deb]:
                pseudoflux[deb][sortie]=pseudoflux[deb][sortie]+1 # On rajoute un élément sur chaque arête du chemin
            else:
                pseudoflux[sortie][deb]=pseudoflux[sortie][deb]-1 # Ou on a l'arête inverse


        # On met ensuite à jour toutes les données , on met à jour le flux(déjà fait) , Le graphe résiduel, E et D

        (E,D)=sommetexcesdeficit(pseudoflux,m,depart,arrivee)

        grapheresiduelcoutpotentiel= obtenirgrapheResiduelAvecCoutPotentiel(graphecout,pseudoflux,sommetpotentiel)
        incrementeur +=1
    return pseudoflux





PigouPont = {"A":{"B":lambda x:1*x,"C":lambda x:1}, "B":{"C":lambda x:0, "D":lambda x:1}, "C":{"D":lambda x:1*x}, "D":{}}


