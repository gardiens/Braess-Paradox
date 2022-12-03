## Constante
PasequNashGrad= 0.5  # Lui c'est le pas de descente lors de la descente en gradient sans contrainte de Equ Nash
erreurmin= 10**-2 # erreur pour la descente en gradient sans contrainte par rapport au minimum voulu


pasderivee= 10**-4 # Pour l'approximation des dérivées
erreurestpositif=10**-5 # Sert uniquement pour estpositif


PasPNE =1 # Est utilisé dans l'algorithme de meilleur réponse

vaut0=10**-5 # On vérifie si le nombre est plus petit que ça ,alors ça vaut sinon sinon il est non nul


# Pour la distribution sur les arêtes, la complexité de mon programme est vraimment pas bonne, i lfaudrait enfaite pour chaque arête récupérer les indices des flux associés et ensuite additionner chacun des flux.
# C'est beaucoup plus efficace en terme de compléxité
##  Obtenir tous les chemins possibles

def estpresent(x,L):
    """Test si un élément est present dans la liste , il renvoie true ou false"""
    for k in L:
        if k==x:
            return True

    return False



def embranchement2 (graphe,chemin,listechemin,arrivee):
    # Fonction auxiliaire à la liste des chemins,
    #print("tour de boucle",chemin, listechemin)
    i=chemin[-1]
    if graphe[i]=={} or i==arrivee: # Cas d'arrivée d'un sommet ou il n'y a pas d'arête sortantes
        if i ==arrivee: # Est-il l'arrivée?
            listechemin.append(chemin[:])


    else:
        for sommetavisiter in graphe[i]:
            if not estpresent(sommetavisiter,chemin):
                chemin.append(sommetavisiter)
                embranchement2(graphe,chemin,listechemin,arrivee)
                chemin.pop()
    return

def listedeschemins(graphe,depart,arrivee):

    """renvoie la liste des chemins ,version récursive"""

    listechemin=[] # Stocke le résultat
    start= [depart] # C'est le chemin initial
    embranchement2(graphe,start,listechemin,arrivee)
    print(" La liste des chemins contient ", len(listechemin),"éléments") # Si il n'y a qu'une route , la terminaison de certains algorithme n'est pas assuré
    return listechemin


## Fin liste des chemins


## Fonction De Potentielle

def distributionSurlesAretes(graphe,Listechemin,ListecheminNpersonne):
    """ Renvoie un graphe ou sur chaque  arête on a le nombre d'individu empruntant cette arête """
    grapheresultat= {} # resultat
    # On initialise un dictionnaire identique à graphe mais auquel on associe la valeur 0
    for  depart in graphe :
        grapheresultat[depart]={} # initialise le resultat
        for arrivee in graphe[depart]:
            grapheresultat[depart][arrivee]=0

    # On énumère les chemins et on ajoute le nombre d'usager empruntant chaque chemin sur les arêtes concernés
    for indice in range (len(Listechemin)): # on se place dans un chemin
        for sommet in range (len(Listechemin[indice])-1): # on se place en un sommet du chemin
            grapheresultat[Listechemin[indice][sommet]][Listechemin[indice][sommet+1]] = grapheresultat[Listechemin[indice][sommet]][Listechemin[indice][sommet+1]] +  ListecheminNpersonne[indice]
    return grapheresultat





def fonctiondepotentielledegraphe(graphefonctionpotentielle,Listechemin,ListecheminNpersonne):
    """ Il renvoie la valeur de la fonction de potentielle avec le flux actuel"""
    grapheNombreDePersonne= distributionSurlesAretes(graphefonctionpotentielle,Listechemin,ListecheminNpersonne) # On distribue les individus sur les arêtes

    resultat = 0
    for debutArete in graphefonctionpotentielle:
        for finArete in graphefonctionpotentielle[debutArete]:
            resultat+= graphefonctionpotentielle[debutArete][finArete](grapheNombreDePersonne[debutArete][finArete]) # On ajoute juste à f la fonction de potentielle évalué au nombre de personne dans le chemin
    return resultat









## Fin Fonction De Potentielle



## Algorithme descente en gradient
#pour le calcul des fonctions à n variables, les n variables seront stockes  la fonction sera de la forme f(l)

from math import sqrt

def calculderiveepartielle (f,L,pasderive,x):
    # X est l'indice de la  variable , le pas est trivialement  le pas et f la fonction à n variable
    """Renvoie la valeur de la derivée partielle en x  """
    # Ici, pour diminuer la complexité, on calcule la derive partielle in place, pour cela on ajoute directement à la liste L
    a1= f(L)
    L[x]=L[x]+pasderive
    aapres=f(L)  # c'est le f(x+h)
    L[x]=L[x]-pasderive
    return (aapres-a1)/pasderive

def norme(L):
    """ Renvoie la norme euclidienne des n uplets (a,b,c,d): sqrt(a²+b²+c²+d² ...)
    """
    resultat = 0
    for k in L:
        resultat+= k**2
    return sqrt(resultat)

def gradient(f,L,pasderive):
    """On renvoie le gradient des dérivées partielles dans l'ordre usuelle"""
    # L désigne la liste qui contient les n variables de f, """
    resultat = [] # c'est le gradient
    for indicevariable in range(len(L)):
      resultat.append(calculderiveepartielle(f,L,pasderive,indicevariable))   # on ajouter df/dx
    return resultat






# NB : ATTENTION POUR LE CALCUL DE DERIVEE DANS NOTRE PARADOXE , ON CONNAIT EXACTEMENT LA VALEUR DE CETTE DERIVEE : CEST LA FONCTION DE LATENCE
def Algogradientavecderivee(f,L,pasequilibre):
  """ Renvoie la liste sensé être un minimum local de la fonction f"""
  # Algo Classique de descente en gradient qui calcule approximativement la dérivée. Il marche dans le cas d'une optimisation sans contrainte
  #erreurmin est l'erreur associé au minimum
  # Il utilise comme constante global: erreur min
  equilibretemporaire=L[:] # l represente la liste ou on va stocker nos n uplets
  grad= gradient(f,equilibretemporaire,pasderivee) #Il represente  notre gradient
  #print("equilibretemporaire",equilibretemporaire,"gradient",grad)
  nombreiteration= 0
  #print("résultat avant entrée dans le gradient", "Valeur f ", f(L),  " voilà la norme", norme(grad), "la liste", L, "gradient", grad, " erreur", erreur   )
  while norme(grad) >erreurmin :  #Tant qu'on est superieur à l'erreur  ( En effet au minimum on a une norme sensiblement egale à 0 car on est dans un minimum pour les n variable )
    for k in range(len(equilibretemporaire)):
        equilibretemporaire[k]= equilibretemporaire[k]-pasequilibre*grad[k]
        """" Parce que si la derivee est postive il faut aller de l'autre sens ( car le minimum est plus bas ) et on  modifie chaque terme de la liste"""
    grad=gradient(f,equilibretemporaire,pasderivee)
    nombreiteration+=1
    #print("Valeur f ", f(L),  " voilà la norme", norme(grad), "la liste", l, "gradient", grad ," nombre itération",nombreiteration,    " erreur", erreur   )
  #print("résultat après calcul dans le gradient ",  "Valeur f ", f(equilibretemporaire),  " voilà la norme", norme(grad), "la liste", equilibretemporaire, "gradient", grad ," nombre itération",nombreiteration,    " erreur", erreur   )
  return equilibretemporaire  #On renvoie le groupe de n-uplets qui representent notre  minimum













def indmin(L):
    """Renvoie l'indice du minimum"""
    i=0
    min=L[0]
    for k in range(1,len(L)):
        if L[k]<min:
            i=k
            min=L[i]

    return i



def Algogradientprojete(f,L,N,m):
  # Méthode de Descente en gradient dans le cas d'un ensemble convexe avec des contraintes de type simplexe.
  """ Renvoie l'équilibre trouvé après l'algorithme """
  # N est le nombre d'itération
  # m désigne la plus grande valeur possible dans une des variables possible
  mintemp=L[:] # l represente la liste ou on va stocker nos n uplets
  grad= gradient(f,mintemp,pasderivee) #Il represente  notre gradient
  #print("mintemp",mintemp,"gradient",grad)
  nombreiteration= 0
  #print("résultat avant entrée dans le gradient", "Valeur f ", f(mintemp),  " voilà la norme", norme(grad), "la liste", mintemp, "gradient", grad)
  #print("on rentre dans la boucle ")
  for k in range(N):
    #print("résultat avant entrée dans le gradient", "Valeur f ", f(mintemp),  " voilà la norme", norme(grad), "la liste", mintemp, "gradient", grad)

    grad=gradient(f,mintemp,pasderivee) # Calcul du gradient
    gamma=2/(2+nombreiteration)
    # détermination de la direction de descente  Ici la direction est donnée par le nombre avec la plus petite dérivée
    i= indmin(grad)
    # on construit la direction, la direction qui minimise est celle ou la dérivée est la plus faible
    xk=[0 for k in range(len(L))]
    xk[i]=m # à priori, m désigne  le nombre total d'individu
    for k in range(len(mintemp)):
        mintemp[k]= mintemp[k]+ gamma*(xk[k]-mintemp[k]) # On se déplace en crabe pour obtenir notre équilibre # ATTENTION AU MOINS

    nombreiteration+=1
  #print("résultat après calcul dans le gradient ",  "Valeur f ", f(mintemp),  " voilà la norme", norme(grad), "la liste", mintemp, "gradient", grad ," nombre itération",nombreiteration,    " erreur", erreur   )
  return mintemp  #On renvoie le groupe de n-uplets qui representent notre  minimum


##  Fin  descente  en gradient





## Début calcul equilibre de Nash

    ## Calcul equilibre continu




def estpositif(L):
    # Verifie si tous les nombres sont positifs,
    #l'erreur permet d'éviter les approximations de python, elle est défini au début de ce programme

    resultat= True
    for element in L:
        resultat = resultat and (element>=-erreurestpositif)
    return resultat


import random as rd
def trouverNombresommeegalea(n,m):
    """Renvoie une liste de n nombre tel que leur somme est égal à m """
    # On trouve n nombre aléatoire tel que la somme vaut m, On prend n nombre entre  0 et 1 , puis oon les normalise avec m/somme
    L=[ rd.random() for k in range (n)]
    somme= sum(L,0)
    for k in range (len(L)):
        L[k]= m*L[k]/somme
    return L






def CalcEquNashAvecGradient(Listechemin,graphefonctionpotentielle,Nindividu):
    """ Renvoi une liste L  correspondant aux nombre d'inviidus sur chaque chemin à l'équilibre. Quel que soit le minimum trouvé, il le renvoie"""
    #Nindividu correspond au nombre total d'individu sur la route
    #Listechemin est la liste de TOUS les chemins pour partir du départ à l'arrivée
    # On note n le nombre de chemin, cette algorithme minimise sans contrainte la fonction de potentielle définit sur les n-1 variables et la dernière est déduite des autres

    def ajouterledernier(L,Nindividu):
        # Fonction qui a L renvoie  L auquel on ajoute comme dernier element  n - la somme des autre elemnts
        somme=0
        for k in L:
            somme+= k
        L.append(Nindividu-somme)
        return L
    def fonctionpotentielle (ListecheminNpersonne):
        """ renvoie la valeur de la fonction de potentielle pour une liste de chemin qui contient n-1 variables."""
        #Méthode in place
        somme=0
        for k in ListecheminNpersonne:
            somme+= k
        ListecheminNpersonne.append(Nindividu-somme) # Il faut ajouter la derniere composante qui est définit a partir du nombre de personne qui passe par les chemins C1,... Cn-1

        valeurfonction= fonctiondepotentielledegraphe(graphefonctionpotentielle,Listechemin,ListecheminNpersonne)
        ListecheminNpersonne.pop() # Il faut supprimer le dernier element
        return valeurfonction


    fauxminimum=[] # Stocke les minimums locaux
    n=0  # Pour éviter une boucle infini

    """ Ici je vais changer  comment on initialise C la liste initiale, enfaite pour le premier jet je vais partir avec une liste parfaitement équilibré """
    C=trouverNombresommeegalea(len(Listechemin),Nindividu)[:-1] # [:-1] assure un slicing, on récupère n-1 valeurs



    while True:
        print("liste initialisiée", C)
        #time1.sleep(2)
        L= Algogradientavecderivee(fonctionpotentielle,C,PasequNashGrad)
        print("On a passé  la descente en gradient ")
        ajouterledernier(L,Nindividu)

        if estpositif(L): # si tous les ai sont positifs
            return L #Il faut ne pas oublier de rajouter le dernier element qui depend des autres personnes sur le chemins
        print(" l'équilibre n'est pas physique, un des nombres est négatif ")
        return L






def EquContinuGrad(graphefonctionpotentielle,depart,arrivee,Nindividu):

    """il renvoie une liste L qui correspond à l'équilibre de nash, et un tuple avec la liste des chemins """
    #Fonction de synthèse, il calcule la liste des chemins  à partir d'un graphe avec une fonction de potentielle
    Listechemin=listedeschemins(graphefonctionpotentielle,depart,arrivee)
    #print("Listechemin",Listechemin," suite verificationnash")

    L=CalcEquNashAvecGradient(Listechemin,graphefonctionpotentielle,Nindividu)

    return (Listechemin, L)



    ## Calcul equilibre continu avec méthode du gradient projeté

def CalcEquNashAvecGradientproj(listechemin,graphefonctionpotentielle,Nindividu,Niteration):
    """ Renvoi une liste L  correspondant aux nombre d'inviidus sur chaque chemin à l'équilibre. Quel que soit le minimum trouvé, il le renvoie"""
    # Niteration correspond au nombre d'iteration de la descente en gradient projeté
    # Utilise comme constante global
    # On note n le nombre de chemin, cette algorithme minimise sans contrainte la fonction de potentielle définit sur les n-1 variables et la dernière est déduite des autres

    # 2 fonctions auxiliaires uniquement associé à cette fonction
    def fonctionpotentielle (ListecheminNpersonne):
        """ renvoie la valeur de la fonction de potentielle pour une liste de chemin qui contient n-1 variables."""
        #Méthode in place
        return fonctiondepotentielledegraphe(graphefonctionpotentielle,listechemin,ListecheminNpersonne)

    """ Ici je vais changer  comment on initialise C la liste initiale, enfaite pour le premier jet je vais partir avec une liste parfaitement équilibré """
    C=trouverNombresommeegalea(len(listechemin),Nindividu)[:] #Ici il faut tous prendre, car on minimise sur les n variables



    while True:

        #print("liste initialisiée", C)
        #time1.sleep(2)
        L= Algogradientprojete(fonctionpotentielle,C,Niteration,Nindividu)
        print("On a passé  la descente en gradient ")

        if estpositif(L): # si tous les ai sont positifs
            return L #Il faut ne pas oublier de rajouter le dernier element qui depend des autres personnes sur le chemins
        #print(" l'équilibre n'est pas physique, un des nombres est négatif ")
        return L





import time as time1
def EquContinuGradproj(graphefonctionpotentielle,depart,arrivee,Nindividu,Niteration):

    """il renvoie une liste L qui correspond à l'équilibre de nash, et un tuple avec la liste des chemins """
    #Fonction de synthèse, il calcule la liste des chemins  à partir d'un graphe avec une fonction de potentielle
    listechemin=listedeschemins(graphefonctionpotentielle,depart,arrivee)
    #print("listechemin",listechemin," suite verificationnash")

    L=CalcEquNashAvecGradientproj(listechemin,graphefonctionpotentielle,Nindividu,Niteration)

    return (listechemin, L)



    ## Calcul d'équilibre fini

def PNE(graphesimple,Listechemin,listeNInidividu): # ALGORITHME DE MEILLEUR REPONSE dans le cas fini
    """
    la portion modifié à chaque étape d'usager sur le réseau est définit au début du programme dans Pas PNE """
    """ Le principe: on prend à chaque fois les n uplets qui nous interessent, on regarde si on peut améliorer le trafic, si oui on l'améliore sinon on s'arretek"""
    def fonctionpotentiellePNE(ListecheminNpersonne): # Fonction de potentielle adapté à notre probllème
        return fonctiondepotentielledegraphe(graphesimple,Listechemin,ListecheminNpersonne)

    traqueur = True # c'est lui qui va pouvoir nous dire si on a modifié ou non  un des elements de la liste, si il n'y a pas de modification  il est faux
    stockage= listeNInidividu[:]
    while traqueur == True:  # Pour chaque route, tant qu'on peut ameliorer  le traqueur reste en true
        #print(stockage,"debutbou")
        traqueur=False #  Il faut faux dans chaque boucle, si on a une amelioration à un moment, alors le traqueur deviens true et continue la boucle
        for  indice in range(len(listeNInidividu)): # On s'interesse  à savoir si le changement d'un invidividu est profitable ou non sur la route numéro i
            if stockage[indice]>0: # On vérifie qu'aucun est nul
                liste=stockage[:]# c'est celle qui nous permettrai de comparer  apres changement si on a ou non ameliorer le reseau
                for  i in range (len(listeNInidividu)):# On va parcourir une à  une les  autres prive de l'indice qu'on regarde
                    if i!=indice:
                        liste[indice], liste [i] = liste[indice] - PasPNE, liste[i]+PasPNE  # On change les valeurs des indices à l'interieur
                        if fonctionpotentiellePNE(liste)< fonctionpotentiellePNE(stockage)and liste[indice]>=0:
                            stockage= liste[:]
                            traqueur=True # Au prochain tour de boucle, on aura stockage
                        else: # Si c'est pas mieux,
                            liste[indice], liste [i] = liste[indice] + PasPNE, liste[i]-PasPNE  # On reverse les changements
                #print("stockage",stockage)


    return stockage


def trouversommeentieregal(n,m):
    """Pareil que l'autre mais avec des entiers,
    N est la longueur de la liste, m la somme total entière souhaité """
    L=trouverNombresommeegalea(n,m)
    resultat=[0 for k in range(len(L))]
    for k in range (len(L)-1):
        resultat[k]= int(L[k])
    resultat[-1]= int(m-sum(resultat,0))
    return resultat


def EquFini(graphesimple,depart,arrivee,Nindividu):

    """il renvoie une liste L qui correspond à l'équilibre de nash, et un tuple avec la liste des chemins """
    #Fonction de synthèse, il calcule la liste des chemins  à partir d'un graphe avec une fonction de potentielle
    Listechemin=listedeschemins(graphesimple,depart,arrivee)
    listeNindividu=trouversommeentieregal(len(Listechemin),Nindividu)
    print(" suite verificationnash")

    L=PNE(graphesimple,Listechemin,listeNindividu)
    return (Listechemin,L)




## FONCTION DE SYNTHESE






























