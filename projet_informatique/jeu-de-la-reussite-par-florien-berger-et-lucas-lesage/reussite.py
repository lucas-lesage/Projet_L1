import random
import matplotlib.pyplot as plt
import numpy as np
from math import *
from tkinter import *




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Affichage de la Reussite Et Création de Cartes"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def cree_carte(couleur, valeur):
#fonction créant le dictionnaire pour chaque carte
    carte = {'valeur':valeur, 'couleur':couleur}
    return carte


def carte_to_chaine(carte, char_special=True):
#crée l'affichage d'une carte au format "valeur symbole"
    if char_special:
        if carte['couleur'] == "P":
            couleur = chr(9824)    
        elif carte['couleur'] == "C":
            couleur = chr(9825)
        elif carte['couleur'] == "K":
            couleur = chr(9826)
        elif carte['couleur'] == "T":
            couleur = chr(9827)
            
        if (carte['valeur'] != 10):
            cartes = ' ' + str(carte['valeur']) + couleur
        else:
            cartes = str(carte['valeur']) + couleur
    else:
        couleur = carte['couleur']
        cartes = str(carte['valeur'])+ "-" + couleur
    
    return cartes  



def afficher_reussite(liste_carte):
#affiche une liste de cartes au format "valeur symbole"
    for i in liste_carte:
        print(carte_to_chaine(i), end=' ')
    print("\n")
    

def cree_paquet_cartes(nb_cartes):
#fonction creant le paquet de cartes   /// affichage 'val-coul'
    paquet = []
    liste_valeur = ["A","R","D","V","10","9","8","7","6","5","4","3","2"]
    liste_couleur = ["P", "C", "K", "T"]
    for couleur in liste_couleur:
        if nb_cartes == 32 :
            for valeur in range(len(liste_valeur)-5):
                carte = cree_carte(couleur, liste_valeur[valeur])
                affiche_carte= str(carte['valeur'] + '-' + carte['couleur'])
                paquet.append(affiche_carte)
        else :
            for valeur in liste_valeur:
                carte = cree_carte(couleur, valeur)
                affiche_carte= str(carte['valeur'] + '-' + carte['couleur'])
                paquet.append(affiche_carte)
    return paquet
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Entrées / Sorties avec des fichiers"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def chaine_to_dico(carte):
#change une carte d'une chaine 'val-coul' en dictionnaire {'valeur':..., 'couleur':...}
    liste_carte=carte.split('-')
    if (liste_carte[0] in ["A", "R", "D", "V"]):
        dico_carte={'valeur':liste_carte[0], 'couleur':liste_carte[1]}
    else:
        dico_carte={'valeur':int(liste_carte[0]), 'couleur':liste_carte[1]}
    return dico_carte

def init_pioche_fichier(nom_fichier):
#création d'une liste de carte à partir d'un paquet de carte neuf
    with open(nom_fichier, "r") as f:
        paquet = f.read()
        liste_paquet=paquet.split(" ")
        f.close()
    liste_dico = []
    for i in range(len(liste_paquet)):
        carte = chaine_to_dico(liste_paquet[i])
        liste_dico.append(carte)
    return liste_dico

def ecrire_fichier_reussite(nom_fichier_sauvegarde, pioche):
#ecriture d'une sauvegarde d'un fichier
    sauvegarde = open(nom_fichier_sauvegarde, 'w')
    for i in range(len(pioche)) :
        carte = carte_to_chaine(pioche[i], False)
        sauvegarde.write(carte + ' ')
    sauvegarde.close()
    
def init_pioche_alea(nb_carte=32):
    paquet = cree_paquet_cartes(nb_carte)
    random.shuffle(paquet)
    return paquet

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Programmer les règles de la réussite des alliances"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def alliance(carte1, carte2):
#vérifie si deux cartes ont la même valeur ou la même couleur
    return carte1['valeur']==carte2['valeur'] or carte1['couleur']==carte2['couleur']

def saut_si_possible (liste_tas, num_tas):
#vérifie si une alliance est possible à l'indice donné, et l'applique si oui
    if num_tas>=1 and len(liste_tas)>2 and alliance(liste_tas[num_tas-1], liste_tas[num_tas+1]):
        liste_tas.pop(num_tas-1)
        return True
    else:
        return False



def une_etape_reussite(liste_tas, pioche, affiche=False):
#ajoute une carte de la pioche au tas actuel, et vérifie si une alliance est possible. Si oui, vérifie si alliance possible depuis la gauche
    liste_tas.append(pioche[0])
    pioche.pop(0)
    if affiche:
        afficher_reussite(liste_tas)
    reussite = saut_si_possible(liste_tas, len(liste_tas)-2)
    if affiche and reussite:
        afficher_reussite(liste_tas)
    if reussite :
        i = 1
        while len(pioche)>0 and i+1 < len(liste_tas):
            reussite2 = saut_si_possible(liste_tas, i)
            if reussite2 :
                i=1
                reussite2 = saut_si_possible(liste_tas, i)
                if affiche :
                    afficher_reussite(liste_tas)
            i += 1
            

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Faire une partie"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def paquet_to_liste_dico(paquet):
# change une liste au format['val-coul',...] au format [{'valeur':..., 'couleur':...},...]
    liste_dico = []
    for elem in paquet:
        carte = chaine_to_dico(elem)
        liste_dico.append(carte)
    return(liste_dico)

def reussite_mode_auto(pioche, affiche=False):
# prend une pioche en argument et joue une réussite des alliances avec ladite pioche
    pioche_dico = paquet_to_liste_dico(pioche)
    liste = []
    liste.append(pioche_dico[0])
    pioche_dico.pop(0)
    liste.append(pioche_dico[0])
    pioche_dico.pop(0)
    compteur = len(pioche_dico)
    while compteur > 0:
        une_etape_reussite(liste, pioche_dico, affiche)
        compteur = compteur - 1
    i = 1
    while i+1 < len(liste):
        a = saut_si_possible(liste, i)
        if a :
            i=1
            a = saut_si_possible(liste, i)
            if affiche :
                afficher_reussite(liste)
        i = i+1                                            
    return liste

def reussite_mode_manuel(pioche, nb_tas_max = 2):
# prend une pioche en argument et laisse le joueur choisir s'il veut réaliser les sauts
    pioche_dico = paquet_to_liste_dico(pioche)
    liste = []
    liste.append(pioche_dico[0])
    pioche_dico.pop(0)
    liste.append(pioche_dico[0])
    pioche_dico.pop(0)
    compteur = len(pioche_dico)
    reponse = 0

    while compteur > 0 :
        while reponse not in [1, 2, 3]:
            reponse = int(input("1-Piocher une carte \n2- Proposer un saut \n3- Quitter\n"))
        if reponse == 1 :
            liste.append(pioche_dico[0])
            pioche_dico.pop(0)
            compteur = compteur - 1
            afficher_reussite(liste)
            reponse = 0
        elif reponse == 2 :
            i=int(input("Sur quel indice faire le saut ? (0 = première carte) \n"))
            while i not in range(1, len(liste)-1):
                i=int(input("Saisie invalide ! \nSur quel indice faire le saut ? (0 = première carte) \n"))
            reussite = saut_si_possible(liste, i)
            if not reussite :
                print("Saut non réalisable.")
            afficher_reussite(liste)
            reponse = 0                
        elif reponse == 3 :
            while compteur > 0 :
                liste.append(pioche_dico[0])
                pioche_dico.pop(0)
                compteur = compteur - 1
                afficher_reussite(liste)

    if len(liste)<=nb_tas_max :
        print("Reussite !")
    else :
        print("Perdu...")
        
def lance_reussite(mode, nb_carte=32, affiche=False, nb_tas_max=2):
    pioche = init_pioche_alea(nb_carte)
    
    if (mode == "auto"):
        reussite_mode_auto(pioche, affiche)
    
    elif(mode == "manuel"):
        reussite_mode_manuel(pioche, nb_tas_max)
        
    else:
        while(mode != "auto" or mode != "manuel"):
            mode = intput("Quel mode: auto ou manuel")
            
def menu_reussite():
    rep_part = input("Voulez-Vous Faire une Partie? Oui/Non : ")
    
    if (rep_part == "Oui"):
        nb_carte = int(input("Combien de cartes? 32/52 : "))
        pioche = init_pioche_alea(nb_carte)
        mode = input("Quel mode de jeu? auto/manuel/quitter/simulation: ")
        
        while (mode != "auto" and mode != "manuel" and mode != "quitter" and mode != "simulation"):
            mode = input("Quel mode de jeu? auto/manuel/quitter: ")
            
        if (mode == "auto"):
            affichage = input("Voulez-Vous afficher? Oui/Non: ")
            reussite_mode_auto(pioche, affichage)
        
        elif (mode == "manuel"):
            nb_tas_max = int(input("Combien de tas maximum: "))
            reussite_mode_manuel(pioche, nb_tas_max)
        
        elif (mode == "simulation"):
            nb_sim = int(input("Combien de Simulation voulez effectuer?: "))
            simul = input("Quelle type de simulation Proba/Stats: ")
            if (simul == "Proba"):
                graph_proba(nb_sim, nb_carte)
                
            else:
                graphique_stats(nb_sim)
                
        
        else:
            print("Au Revoir")
    
    else:
        print("Au Revoir")
            
            

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Partie Extensions: Verification de la pioche"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def verifier_pioche(pioche, nb_cartes=32): 
#permet de verifier si un paquet est complet

    paquet_32 = ['A-P', 'R-P', 'D-P', 'V-P', '10-P', '9-P', '8-P', '7-P', 'A-C', 'R-C', 'D-C', 'V-C', '10-C', '9-C', '8-C', '7-C', 'A-K', 'R-K', 'D-K', 'V-K', '10-K', '9-K', '8-K', '7-K', 'A-T', 'R-T', 'D-T', 'V-T', '10-T', '9-T', '8-T', '7-T']
    paquet_52 = ['A-P', 'R-P', 'D-P', 'V-P', '10-P', '9-P', '8-P', '7-P', '6-P', '5-P', '4-P', '3-P', '2-P', 'A-C', 'R-C', 'D-C', 'V-C', '10-C', '9-C', '8-C', '7-C', '6-C', '5-C', '4-C', '3-C', '2-C', 'A-K', 'R-K', 'D-K', 'V-K', '10-K', '9-K', '8-K', '7-K', '6-K', '5-K', '4-K', '3-K', '2-K', 'A-T', 'R-T', 'D-T', 'V-T', '10-T', '9-T', '8-T', '7-T', '6-T', '5-T', '4-T', '3-T', '2-T']
    verif = 0
    
    for i in range(0, nb_cartes):
        if (nb_cartes == 32 and pioche[i] in paquet_32):
            verif += 1
        elif (nb_cartes == 52 and pioche[i] in paquet_52):
            verif += 1
    
    return (nb_cartes == verif)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Partie Extensions: Statistique et graphique"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def res_multi_simulation(nb_sim, nb_cartes=32): 
#créer une liste des tas fais par rapport au nombre de simulations
    nb_total_tas = []
    partie = 0
    while partie < nb_sim:
        pioche = init_pioche_alea()
        nb_cartes_tas = len(reussite_mode_auto(pioche))
        nb_total_tas.append(nb_cartes_tas)
        partie += 1
    return nb_total_tas

def statistiques_nb_tas(nb_sim, nb_cartes=32): 
#donne le maximum, le minimum et la moyenne
    moyenne = 0
    somme_tas = 0
    compteur = 0
    
    resul_sim = res_multi_simulation(nb_sim, nb_cartes)
    
    for tas in resul_sim:
        somme_tas += tas
        compteur += 1
    moyenne = somme_tas // compteur
    
    maximum = max(resul_sim)
    minimum = min(resul_sim)
    
    print("La moyenne du nombre de tas sur ", nb_sim, "simulation est : ", moyenne, "avec pour minimum: ", minimum, "et pour maximum: ", maximum, ".\n")
        

def moyenne_tas(nb_tas):
#donne la moyenne
    moyenne = 0
    somme_tas = 0
    compteur = 0
    for tas in nb_tas:
        somme_tas += tas
        compteur += 1
    moyenne = somme_tas // compteur
    return moyenne
    
def graphique_stats(nb_sim): 
# affichage par un graphique du nombre de tas pour chaques simulations
    nb_tas = res_multi_simulation(nb_sim+1)
    y2 = moyenne_tas(nb_tas)
    for i in range(0, len(nb_tas)):
        x = i
        y1 = nb_tas[i]
        plt.plot(x,y1, "b:o")
    plt.plot([0, nb_sim], [y2,y2], color='#FF0000', linestyle='solid', label="Moyenne")
    plt.xlabel('Nombre de Simulations')
    plt.ylabel('Nombres de Tas')
    plt.xlim(1, len(nb_tas))
    plt.ylim(2, max(nb_tas))
    plt.legend()
    plt.show()
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Partie Extensions: Probabilité et graphique"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def proba(nb_sim, nb_carte=32): 
#créer un dictionnaire qui contient le nombre de fois sa clé est sortie lors des simulations

    tas_32 = {"2":0, "3":0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0,"29": 0, "30": 0, "31": 0, "32":0}
    tas_52 = {"2":0, "3":0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0,"29": 0, "30": 0, "31": 0, "32":0, "33":0, "34": 0, "35": 0, "36": 0, "37": 0, "38": 0, "39": 0, "40": 0, "41": 0, "42": 0, "43":0, "44":0, "45": 0, "46": 0, "47": 0, "48": 0, "49": 0, "50": 0, "51": 0, "52": 0}
    nb_total_tas = res_multi_simulation(nb_sim, nb_carte)
    
    if (nb_carte == 32):
        for i in range(0,len(nb_total_tas)):
            for tas in tas_32:
                if (tas == str(nb_total_tas[i])):
                    tas_32[tas] += 1
        return tas_32
    
    elif (nb_carte == 52):
        for i in range(0,len(nb_total_tas)):
            for tas in tas_52:
                if (tas == str(nb_total_tas[i])):
                    tas_52[tas] += 1
        return tas_52

def dico_to_liste(dico): 
#transforme un dictionnaire en liste
    liste = []
    for key in dico:
        liste.append(dico[key])
    return liste

def DensiteNormale(x,mu,sigma): 
#fonction représentaant la fonction de densité par rapport à la loi normale
    return (sigma * sqrt(2*pi))*exp(-0.5*((x-mu)/sigma)**2)

def graph_proba(nb_sim, nb_carte=32): 
#affichage distribution des tas, de la loi normal de la distribution par histogramme et fonction
    dico_proba = proba(nb_sim, nb_carte)   
    liste_proba = dico_proba.items()
    
    liste_probas = dico_to_liste(dico_proba)
    moyenne = np.mean(liste_probas)
    ecart_type = np.std(liste_probas)
    
    x, y = zip(*liste_proba)
    
    plt.plot(x, y, label='dsitibution des tas sur le nombre de simulations')
    plt.xlim(0, nb_carte)
    plt.ylim(0, nb_sim/6)
    
    
    normale=np.random.normal(ecart_type, moyenne,nb_sim)
    plt.hist(normale,bins=50,density=False, color='yellow', edgecolor='yellow', label='Histogramme représentant la loi normal de la distribution')
    
    lx=np.linspace(0,nb_sim, nb_sim)
    ly=[DensiteNormale(x, ecart_type ,moyenne) for x in lx]
    plt.plot(lx,ly,'r-', label = ' fonction de densité de la loi normale')
    plt.legend()
    plt.show()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Extension Tkinter"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Partie Main"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__=="__main__":

    paquet = [{'valeur':7, 'couleur':'P'}, {'valeur':10, 'couleur':'K'}, {'valeur':'A', 'couleur':'T'}]
    #afficher_reussite(paquet)
    #paquet2 = init_pioche_alea()
    #print(paquet2)
    #paquet_32 = cree_paquet_cartes(32)
    #paquet_52 = cree_paquet_cartes(52)
    #print(paquet_32)
    #print(paquet_52)
    #print(paquet_to_liste_dico(paquet2))
    #une_etape_reussite([{'valeur':8, 'couleur':'T'},{'valeur':3, 'couleur':'K'}], [{'valeur':8, 'couleur':'K'}], True)
    #a = reussite_mode_auto(paquet2, True)
    #print(a)

    #paquet = [{'valeur':7, 'couleur':'P'}, {'valeur':10, 'couleur':'K'}, {'valeur':'A', 'couleur':'T'}]
    #afficher_reussite(paquet)
    #paquet2 = init_pioche_alea()
    #print(paquet2)
    #print(paquet_to_liste_dico(paquet2))
    #une_etape_reussite([{'valeur':"A", 'couleur':'P'},{'valeur':"V", 'couleur':'P'}], [{'valeur':1, 'couleur':'P'}], True)
    #reussite_mode_auto(paquet2, True)
    #reussite_mode_manuel(paquet2, 25)

    #print(res_multi_simulation(3))

    #graphique_stats(300)
    #graphique_stats(10)
    #print(res_multi_simulation(3))
    #statistiques_nb_tas(3)
    #print(moyenne_tas(res_multi_simulation(300)))
    #tas = proba(300, 32)
    #print(tas)
    #graph_proba(3000, 32)
    #lance_reussite("manuel", nb_tas_max=10)
    #menu_reussite()
    print(carte_to_chaine({'valeur':7, 'couleur':'P'}, False))