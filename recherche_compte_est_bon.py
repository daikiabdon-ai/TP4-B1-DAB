#! /usr/bin/env python3

""" Implémentation des parcours de l’arbre de calculs à la volée :
- parcours en profondeur d’abord itératif
- parcours en profondeur d’abord récursif
- parcours en largeur d’abord itératif """

from TAD.piles_listes_python import Pile
from TAD.files_listes_python import File
# from TAD.piles_listes_simplement_chainees import *
# from TAD.files_listes_doublement_chainees import *
from notation_polonaise_inverse import *

OPERATEURS = ["+", "-", "*", "/"]

def parcours_DFS_v0(cartons, cible) : 
    # cartons : une liste
    # cible : entier 
    nb_noeuds = 0
    meilleur_valeur_atteinte  = 0
    meilleure_expression = []
    p  = Pile() #je creer la pile   
    for i in range(len(cartons)): # on initialise pour chaque debut d'arbre possible
        p.empiler( ([cartons[i]], cartons[:i]+ cartons[i+1:])) # ne pas oublier de retirer le carton noeud de la liste de carton
        while not p.vide() : 
            nb_noeuds += 1 
            ( exp_partielle, cartons_rest) = p.depiler()
            ( ValideOuNon, ValeurOuNone) = eval_NPI_liste( exp_partielle)
            if ValideOuNon == True:
                if ValideOuNone != None:
                    if distance(cible, ValeurOuNone) < distance( cible, meilleur_valeur_atteinte):
                        meilleur_valeur_atteinte = ValeurOuNone
                        meilleure_expression = exp_partielle
        #on ajoute un enfant
        for j in range( len(cartons_rest)):
            p.empiler( (exp_partielle + cartons_rest[j], cartons_rest[:j] + cartons_rest[j+1:] ))
        #ajouter un opérateur si il ya au moins 2 nombres disponibles
        nb_nombres = len( [x for x in exp_partielle if x not in OPERATEURS ])
        nb_ops = len( exp_partielle) - nb_nombres
        if nb_nombres - nb_ops >= 2:
            for op in OPERATEURS:
                p.empiler ( (exp_partielle + [op], cartons_rest ))

def parcours_DFS(cartons, cible):
    nb_noeuds = 0
    meilleure_valeur = None
    meilleure_expression = []

    p = Pile()
    # un noeud = (expression NPI, cartons restants)
    # la racine : expression vide, aucun carton utilisé
    p.empiler(([], cartons))

    while not p.est_vide():
        expression, restants = p.depiler()
        nb_noeuds += 1

        # 1) on évalue l'expression du noeud
        valide, valeur = eval_NPI_liste(expression)

        # 2) expression invalide : on ne regarde pas ses fils (élagage)
        if not valide:
            continue

        # 3) expression qui donne un résultat : est-il meilleur que le précédent ?
        if valeur is not None:
            if meilleure_valeur is None or abs(cible - valeur) < abs(cible - meilleure_valeur):
                meilleure_valeur = valeur
                meilleure_expression = expression
                print("Plus proche :", valeur, "avec", expression)
            # 4) cible atteinte : on s'arrête
            if valeur == cible:
                break

        # 5) fils "carton" : on ajoute un des cartons restants
        for i in range(len(restants)):
            nouvelle_expression = expression + [restants[i]]
            nouveaux_restants = restants[:i] + restants[i+1:]   # on retire le carton utilisé
            p.empiler((nouvelle_expression, nouveaux_restants))

        # 6) fils "opérateur" : possible seulement s'il y a au moins 2 nombres à combiner
        nb_nombres = 0
        nb_operateurs = 0
        for x in expression:
            if x in OPERATEURS:
                nb_operateurs += 1
            else:
                nb_nombres += 1
        if nb_nombres - nb_operateurs >= 2:
            for op in OPERATEURS:
                p.empiler((expression + [op], restants))

    return meilleure_expression, nb_noeuds
            

                        

    
    return meilleure_expression, nb_noeuds

def parcours_BFS(cartons, cible) : 
    # exactement le même programme, mais avec une File à la place de la Pile
    nb_noeuds = 0
    meilleure_valeur = None
    meilleure_expression = []

    f = File()
    f.enfiler(([], cartons))

    while not f.est_vide():
        expression, restants = f.defiler()
        nb_noeuds += 1

        valide, valeur = eval_NPI_liste(expression)
        if not valide:
            continue

        if valeur is not None:
            if meilleure_valeur is None or abs(cible - valeur) < abs(cible - meilleure_valeur):
                meilleure_valeur = valeur
                meilleure_expression = expression
                print("Plus proche :", valeur, "avec", expression)
            if valeur == cible:
                break

        for i in range(len(restants)):
            nouvelle_expression = expression + [restants[i]]
            nouveaux_restants = restants[:i] + restants[i+1:]
            f.enfiler((nouvelle_expression, nouveaux_restants))

        nb_nombres = 0
        nb_operateurs = 0
        for x in expression:
            if x in OPERATEURS:
                nb_operateurs += 1
            else:
                nb_nombres += 1
        if nb_nombres - nb_operateurs >= 2:
            for op in OPERATEURS:
                f.enfiler((expression + [op], restants))

    return meilleure_expression, nb_noeuds

def parcours_DFS_recursif(cartons, cible):
    meilleure_expression = []
    meilleure_valeur = None
    nb_noeuds = 0
    trouve = False

    def parcours_DFSR_aux(choisis, restants):
        nonlocal meilleure_expression
        nonlocal meilleure_valeur
        nonlocal nb_noeuds
        nonlocal trouve

        nb_noeuds += 1
        valide, valeur = eval_NPI_liste(choisis)

        # cas de base 1 : expression invalide, on arrête cette branche
        if not valide:
            return

        if valeur is not None:
            if meilleure_valeur is None or abs(cible - valeur) < abs(cible - meilleure_valeur):
                meilleure_valeur = valeur
                meilleure_expression = choisis
                print("Plus proche :", valeur, "avec", choisis)
            # cas de base 2 : cible atteinte
            if valeur == cible:
                trouve = True
                return

        # cas général : un appel récursif par fils
        for i in range(len(restants)):
            parcours_DFSR_aux(choisis + [restants[i]], restants[:i] + restants[i+1:])
            if trouve:
                return

        nb_nombres = 0
        nb_operateurs = 0
        for x in choisis:
            if x in OPERATEURS:
                nb_operateurs += 1
            else:
                nb_nombres += 1
        if nb_nombres - nb_operateurs >= 2:
            for op in OPERATEURS:
                parcours_DFSR_aux(choisis + [op], restants)
                if trouve:
                    return

    parcours_DFSR_aux([], cartons)

    return meilleure_expression, nb_noeuds

import sys
import time
import io
from contextlib import redirect_stdout
from recherche_compte_est_bon import *

nombres = [int(x) for x in sys.argv[1:]]
cartons, cible = nombres[:-1], nombres[-1]
print("Cartons :", cartons, "| Cible :", cible)

for parcours in (parcours_DFS, parcours_DFS_recursif, parcours_BFS):
    debut = time.time()
    with redirect_stdout(io.StringIO()):      # masque les "Plus proche : ..."
        expr, nb_noeuds = parcours(cartons, cible)
    duree = time.time() - debut
    valide, valeur = eval_NPI_liste(expr)
    statut = "TROUVÉ" if valeur == cible else f"non trouvé (meilleur : {valeur})"
    print(f"{parcours.__name__:22} {statut:30} {nb_noeuds:>10} nœuds  {duree:.2f} s")


if __name__ == "__main__":
    parcours_DFS([3,5, 7, 9, 25, 50], 859)
    parcours_BFS([3,5, 7, 9, 25, 50], 859)
    parcours_DFS_recursif([3,5, 7, 9, 25, 50], 859)
 
