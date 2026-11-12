#! /usr/bin/env python3

""" Implémentation des parcours de l’arbre de calculs à la volée :
- parcours en profondeur d’abord itératif
- parcours en profondeur d’abord récursif
- parcours en largeur d’abord itératif """

from TAD.piles_listes_python import Pile
from TAD.files_listes_python import File
from TAD.piles_listes_simplement_chainees import Pile
from TAD.files_listes_doublement_chainees import File
from notation_polonaise_inverse import *

def parcours_DFS(cartons, cible) : 
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
            

                        

    
    return meilleure_expression, nb_noeuds

def parcours_BFS(cartons, cible) : 
    # cartons : une liste
    # cible : entier 
    nb_noeuds = 0
    meilleure_expression = []

    return meilleure_expression, nb_noeuds 

def parcours_DFS_recursif(cartons, cible) :
    meilleure_expression = []
    nb_noeuds = 0

    def parcours_DFSR_aux(choisis, restants) :
        nonlocal meilleure_expression
        nonlocal nb_noeuds
        nonlocal cible
        pass
        
    # Appeler parcours_DFSR_aux ! 

    return meilleure_expression, nb_noeuds


if __name__ == "__main__":
    parcours_DFS([3,5, 7, 9, 25, 50], 859)
    parcours_BFS([3,5, 7, 9, 25, 50], 859)
    parcours_DFS_recursif([3,5, 7, 9, 25, 50], 859)
 
