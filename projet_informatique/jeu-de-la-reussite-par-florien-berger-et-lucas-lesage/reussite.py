import random
import matplotlib.pyplot as plt
import numpy as np
from math import *
from tkinter import *
from tkinter.ttk import *




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

def paquet_to_liste_dico(paquet):
# change une liste au format['val-coul',...] au format [{'valeur':..., 'couleur':...},...]
    liste_dico = []
    for elem in paquet:
        carte = chaine_to_dico(elem)
        liste_dico.append(carte)
    return(liste_dico)

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
###ecriture d'une sauvegarde d'un fichier
    sauvegarde = open(nom_fichier_sauvegarde, 'w')
    for i in range(len(pioche)-1) :
        carte = carte_to_chaine(pioche[i], False)
        sauvegarde.write(carte + ' ')
    carte = carte_to_chaine(pioche[len(pioche)-1], False)
    sauvegarde.write(carte)
    sauvegarde.close()
    
def init_pioche_alea(nb_carte=32):
    paquet = cree_paquet_cartes(nb_carte)
    random.shuffle(paquet)
    return paquet_to_liste_dico(paquet)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Programmer les règles de la réussite des alliances"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def alliance(carte1, carte2):
#vérifie si deux cartes ont la même valeur ou la même couleur
    return carte1['valeur']==carte2['valeur'] or carte1['couleur']==carte2['couleur']

def saut_si_possible (liste_tas, num_tas):
#vérifie si une alliance est possible à l'indice donné, et l'applique si oui
    if (num_tas>=1 and num_tas<len(liste_tas)-1 and len(liste_tas)>2) and alliance(liste_tas[num_tas-1], liste_tas[num_tas+1]):
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
        while i+1 < len(liste_tas):
            reussite2 = saut_si_possible(liste_tas, i)
            if affiche and reussite2:
                    afficher_reussite(liste_tas)
            while reussite2 :
                i=1
                reussite2 = saut_si_possible(liste_tas, i)
                if reussite2 and affiche :
                    afficher_reussite(liste_tas)
            i += 1
            

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Faire une partie"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




def reussite_mode_auto(pioche, affiche=False):
# prend une pioche en argument et joue une réussite des alliances avec ladite pioche
    liste = []
    pioche2=list(pioche)
    if affiche :
        afficher_reussite(pioche2)
    liste.append(pioche2[0])
    pioche2.pop(0)
    if affiche :
        afficher_reussite(liste)
    liste.append(pioche2[0])
    pioche2.pop(0)
    if affiche :
        afficher_reussite(liste)    
    compteur = len(pioche2)
    while compteur > 0:
        une_etape_reussite(liste, pioche2, affiche)
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
    pioche_dico = list(pioche)
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
### Affiche un menu proposant plusieurs options : joueur une partie (auto, sauvegardée, manuelle...), effectuer des simulations, quitter le jeu.
    choix = int(input("-------------MENU-------------\n| 1- Jouer une partie         |\n| 2- Effectuer une simulation |\n| 3- Quitter                  |\n------------------------------\n"))

    while choix not in [1, 2, 3] :
        choix = int(input("-------------MENU-------------\n| 1- Jouer une partie         |\n| 2- Effectuer une simulation |\n| 3- Quitter                  |\n------------------------------\n"))

    while choix != 3 :

        if choix == 1 :
            mode = int(input("----MODE DE JEU----\n| 1- Automatique   |\n| 2- Manuel        |\n-------------------\n"))

            while mode not in [1, 2] :
                mode = int(input("----MODE DE JEU----\n| 1- Automatique   |\n| 2- Manuel        |\n-------------------\n"))

            if mode == 1 :
                jeu_fichier = input("Voulez vous jouer une partie enregistrée ? oui / non :")

                if jeu_fichier.lower()== "oui" :
                    # vérifie si le fichier que l'on veut charger existe, et demande de saisir un nom de fichier tant qu'on n'en trouve pas
                    erreur = True
                    while erreur : 
                        nom_fichier = input("Fichier: ")
                        try :
                            with open(nom_fichier+".txt") as file :
                                print("Chargement...")
                                erreur = False
                            pioche = init_pioche_fichier(nom_fichier+".txt")
                        except FileNotFoundError:
                            confirm = input("Fichier non trouvé. Saisissez 'q' pour abandonner, ou tout autre caractère pour saisir un nouveau nom : ")
                            if confirm.lower() == 'q' :
                                erreur = False
                                jeu_fichier = "non"
                        
                    
                                    
                if jeu_fichier.lower() != "oui" :       
                    nb_carte = int(input("Combien de cartes?\n 1- 32 cartes\n 2- 52 cartes\n"))
                    while nb_carte not in [1, 2] :
                        nb_carte = int(input("Combien de cartes?\n 1- 32 cartes\n 2- 52 cartes\n"))
                    pioche = init_pioche_alea(nb_carte)
                

                afficher = input("Voulez vous afficher les étapes ? oui / non : ")
                affichage = (afficher.lower() == "oui")
                reussite_mode_auto(pioche, affichage)

                if jeu_fichier.lower() != "oui" :
                    enreg = input("Voulez vous sauvegarder cette pioche ? oui / non : ")
                    if enreg.lower() == "oui" :
                        erreur_sauv = True
                        while erreur_sauv :
                            nom_fichier_sauv = input("Nom de la sauvegarde : ")
                            try :
                                with open(nom_fichier_sauv + ".txt") as file :
                                    confirm = input("Ce nom est déjà utilisé. Saisissez 'q' pour abandonner, ou tout autre caractère pour saisir un nouveau nom : ")
                                    if confirm.lower() == 'q' :
                                        erreur_sauv = False
                            except FileNotFoundError :
                                ecrire_fichier_reussite(nom_fichier_sauv + ".txt", pioche)
                                erreur_sauv = False

            if mode == 2 :
                nb_carte = int(input("Combien de cartes?\n 1- 32 cartes\n 2- 52 cartes\n"))
                while nb_carte not in [1, 2] :
                    nb_carte = int(input("Combien de cartes?\n 1- 32 cartes\n 2- 52 cartes\n"))
                pioche = init_pioche_alea(nb_carte)
                nb_tas_max = int(input("Combien de tas maximum pour gagner ? (entre 2 et le nombre de cartes choisi)"))
                reussite_mode_manuel(pioche, nb_tas_max)

        elif choix == 2 :
            nb_sim = int(input("Combien de Simulation voulez effectuer?: "))
            nb_carte = int(input("Combien de cartes?\n 1- 32 cartes\n 2- 52 cartes\n"))
            while nb_carte not in [1, 2] :
                nb_carte = int(input("Combien de cartes?\n 1- 32 cartes\n 2- 52 cartes\n"))
            simul = input("Quelle type de simulation Proba/Stats: ")
            if (simul.lower() == "proba"):
                graph_proba(nb_sim, nb_carte)
                
            else:
                graphique_stats(nb_sim, nb_carte)

        choix = int(input("-------------MENU-------------\n| 1- Jouer une partie         |\n| 2- Effectuer une simulation |\n| 3- Quitter                  |\n------------------------------\n"))

    print("Au revoir")

            

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Partie Extensions: Verification de la pioche"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def verifier_pioche(pioche, nb_cartes=32): 
#permet de verifier si un paquet est complet

    paquet_32 = [{'valeur': 'A', 'couleur': 'P'}, {'valeur': 'R', 'couleur': 'P'}, {'valeur': 'D', 'couleur': 'P'}, {'valeur': 'V', 'couleur': 'P'}, {'valeur': 10, 'couleur': 'P'}, {'valeur': 9, 'couleur': 'P'}, {'valeur': 8, 'couleur': 'P'}, {'valeur': 7, 'couleur': 'P'}, {'valeur': 'A', 'couleur': 'C'}, {'valeur': 'R', 'couleur': 'C'}, {'valeur': 'D', 'couleur': 'C'}, {'valeur': 'V', 'couleur': 'C'}, {'valeur': 10, 'couleur': 'C'}, {'valeur': 9, 'couleur': 'C'}, {'valeur': 8, 'couleur': 'C'}, {'valeur': 7, 'couleur': 'C'}, {'valeur': 'A', 'couleur': 'K'}, {'valeur': 'R', 'couleur': 'K'}, {'valeur': 'D', 'couleur': 'K'}, {'valeur': 'V', 'couleur': 'K'}, {'valeur': 10, 'couleur': 'K'}, {'valeur': 9, 'couleur': 'K'}, {'valeur': 8, 'couleur': 'K'}, {'valeur': 7, 'couleur': 'K'}, {'valeur': 'A', 'couleur': 'T'}, {'valeur': 'R', 'couleur': 'T'}, {'valeur': 'D', 'couleur': 'T'}, {'valeur': 'V', 'couleur': 'T'}, {'valeur': 10, 'couleur': 'T'}, {'valeur': 9, 'couleur': 'T'}, {'valeur': 8, 'couleur': 'T'}, {'valeur': 7, 'couleur': 'T'}]
    paquet_52 = [{'valeur': 'A', 'couleur': 'P'}, {'valeur': 'R', 'couleur': 'P'}, {'valeur': 'D', 'couleur': 'P'}, {'valeur': 'V', 'couleur': 'P'}, {'valeur': 10, 'couleur': 'P'}, {'valeur': 9, 'couleur': 'P'}, {'valeur': 8, 'couleur': 'P'}, {'valeur': 7, 'couleur': 'P'}, {'valeur': 6, 'couleur': 'P'}, {'valeur': 5, 'couleur': 'P'}, {'valeur': 4, 'couleur': 'P'}, {'valeur': 3, 'couleur': 'P'}, {'valeur': 2, 'couleur': 'P'}, {'valeur': 'A', 'couleur': 'C'}, {'valeur': 'R', 'couleur': 'C'}, {'valeur': 'D', 'couleur': 'C'}, {'valeur': 'V', 'couleur': 'C'}, {'valeur': 10, 'couleur': 'C'}, {'valeur': 9, 'couleur': 'C'}, {'valeur': 8, 'couleur': 'C'}, {'valeur': 7, 'couleur': 'C'}, {'valeur': 6, 'couleur': 'C'}, {'valeur': 5, 'couleur': 'C'}, {'valeur': 4, 'couleur': 'C'}, {'valeur': 3, 'couleur': 'C'}, {'valeur': 2, 'couleur': 'C'}, {'valeur': 'A', 'couleur': 'K'}, {'valeur': 'R', 'couleur': 'K'}, {'valeur': 'D', 'couleur': 'K'}, {'valeur': 'V', 'couleur': 'K'}, {'valeur': 10, 'couleur': 'K'}, {'valeur': 9, 'couleur': 'K'}, {'valeur': 8, 'couleur': 'K'}, {'valeur': 7, 'couleur': 'K'}, {'valeur': 6, 'couleur': 'K'}, {'valeur': 5, 'couleur': 'K'}, {'valeur': 4, 'couleur': 'K'}, {'valeur': 3, 'couleur': 'K'}, {'valeur': 2, 'couleur': 'K'}, {'valeur': 'A', 'couleur': 'T'}, {'valeur': 'R', 'couleur': 'T'}, {'valeur': 'D', 'couleur': 'T'}, {'valeur': 'V', 'couleur': 'T'}, {'valeur': 10, 'couleur': 'T'}, {'valeur': 9, 'couleur': 'T'}, {'valeur': 8, 'couleur': 'T'}, {'valeur': 7, 'couleur': 'T'}, {'valeur': 6, 'couleur': 'T'}, {'valeur': 5, 'couleur': 'T'}, {'valeur': 4, 'couleur': 'T'}, {'valeur': 3, 'couleur': 'T'}, {'valeur': 2, 'couleur': 'T'}]
    verif = 0
    
    if len(pioche) == 32 :
        for i in range(32):
            if  paquet_32[i] in pioche:
                verif += 1
    elif len(pioche) == 52 :
        for i in range(52):
            if paquet_52[i] in pioche :
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
    
def graphique_stats(nb_sim, nb_cartes=32): 
# affichage par un graphique du nombre de tas pour chaques simulations
    nb_tas = res_multi_simulation(nb_sim+1, nb_cartes)
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

master = Tk() 
  
master.geometry("500x500")
master['bg'] = '#00561b'

def stats_32():
    nb_sim = int(input("Combien de Simulations: "))
    graphique_stats(nb_sim, 32)
     
    
def probas_32():
    nb_sim = int(input("Combien de Simulations: "))
    graph_proba(nb_sim, 32)
    
    
def stats_52():
    nb_sim = int(input("Combien de Simulations: "))
    graphique_stats(nb_sim, 52)
 
    
def probas_52():
    nb_sim = int(input("Combien de Simulations: "))
    graph_proba(nb_sim, 52)
    

def open_fenetre_simulation_32(fenetre=master): 
      
    
    for widget in fenetre.winfo_children():
        widget.destroy()
  
    
    Label(fenetre, text ="Quel type de simulation voulez-vous réaliser?").pack()
    btn_stats =  Button(fenetre,  
             text ="Lancer Simulations de Statistique",  
             command = stats_32)
    btn_probas =  Button(fenetre,  
             text ="Lancer Simulations de Probalités",  
             command = probas_32)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_stats.pack(pady = 10)
    btn_probas.pack(pady = 15)
    btn_quitter.pack(pady = 20)
    
def open_fenetre_simulation_52(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()
    
  
    
    Label(fenetre, text ="Quel type de simulation voulez-vous réaliser?").pack()
    btn_stats =  Button(fenetre,  
             text ="Lancer Simulations de Statistique",  
             command = stats_52)
    btn_probas =  Button(fenetre,  
             text ="Lancer Simulations de Probalités",  
             command = probas_52)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_stats.pack(pady = 10)
    btn_probas.pack(pady = 15)
    btn_quitter.pack(pady = 20)
    
 

def manuel_32():
    pioche = init_pioche_alea(32)
    nb_tas_max = int(input("Combien de Tas au Maximum: "))
    reussite_mode_manuel(pioche, nb_tas_max)
    

def manuel_52():
    pioche = init_pioche_alea(52)
    nb_tas_max = int(input("Combien de Tas au Maximum: "))
    reussite_mode_manuel(pioche, nb_tas_max)
       

def open_fenetre_manuel_32(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()
  
    
    Label(fenetre, text ="Lancer le Mode Manuel").pack()
    btn_lance =  Button(fenetre,  
             text ="Lancer Partie",  
             command = manuel_32)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_lance.pack(pady = 10)
    btn_quitter.pack(pady = 15)
    
def open_fenetre_manuel_52(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()

  
    
    Label(fenetre, text ="Lancer le Mode Manuel").pack()
    btn_lance =  Button(fenetre,  
             text ="Lancer Partie",  
             command = manuel_52)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy)    
    btn_lance.pack(pady = 10)
    btn_quitter.pack(pady = 15)


def auto_32(affiche):
    pioche = init_pioche_alea(32)
    reussite_mode_auto(pioche, affiche)

    
def auto_52(affiche):
    pioche = init_pioche_alea(32)
    reussite_mode_auto(pioche, affiche)


def open_fenetre_auto_32(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()
    

  
    
    Label(fenetre, text ="Voulez-Vous Afficher le déroulement de la partie (la partie se lancera toute seule)?").pack()
    
    btn_oui =  Button(fenetre,  
             text ="Oui",  
             command = lambda: auto_32(True))
    btn_non =  Button(fenetre,  
             text ="Non",  
             command = lambda : auto_32(False))
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_oui.pack(pady = 10) 
    btn_non.pack(pady = 15)
    btn_quitter.pack(pady = 20) 
    
def open_fenetre_auto_52(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()
 
  
    
    Label(fenetre, text ="Voulez-Vous Afficher le déroulement de la partie?").pack()
    
    btn_oui =  Button(fenetre,  
             text ="Oui",  
             command = lambda: auto_52(True))
    btn_non =  Button(fenetre,  
             text ="Non",  
             command = lambda : auto_52(False))
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_oui.pack(pady = 10) 
    btn_non.pack(pady = 15)
    btn_quitter.pack(pady = 20)
    
    
  
def open_fenetre_mode_jeu_32(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()
     
  
    
    Label(fenetre,  
          text ="Veuillez Choisir Votre Mode de Jeu").pack()
    
    btn_auto =  Button(fenetre,  
             text ="Automatique",  
             command = open_fenetre_auto_32)
    btn_manuel =  Button(fenetre,  
             text ="Manuel",  
             command = open_fenetre_manuel_32)
    btn_sim =  Button(fenetre,  
             text ="Simulation",  
             command = open_fenetre_simulation_32)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_auto.pack(pady = 10) 
    btn_manuel.pack(pady = 15) 
    btn_sim.pack(pady = 20) 
    btn_quitter.pack(pady = 25)
    
    
def open_fenetre_mode_jeu_52(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()

  
    
    Label(fenetre,  
          text ="Veuillez Choisir Votre Mode de Jeu").pack()
    
    btn_auto =  Button(fenetre,  
             text ="Automatique",  
             command = open_fenetre_auto_52)
    btn_manuel =  Button(fenetre,  
             text ="Manuel",  
             command = open_fenetre_manuel_52)
    btn_sim =  Button(fenetre,  
             text ="Simulation",  
             command = open_fenetre_simulation_52)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_auto.pack(pady = 10) 
    btn_manuel.pack(pady = 15) 
    btn_sim.pack(pady = 20)
    btn_quitter.pack(pady = 25)
         
    
     
def open_fenetre_cartes(fenetre=master): 
      
    for widget in fenetre.winfo_children():
        widget.destroy()
  
    
    Label(fenetre, text ="Avec Combien de Cartes voulez-vous jouer?").pack()
    
    btn_32 =  Button(fenetre,  
             text ="32",  
             command = open_fenetre_mode_jeu_32)
    btn_52 =  Button(fenetre,  
             text ="52",  
             command = open_fenetre_mode_jeu_52)
    btn_quitter = Button(fenetre,  
             text ="Quitter",  
             command = master.destroy) 
    btn_32.pack(pady = 10) 
    btn_52.pack(pady = 15) 
    btn_quitter.pack(pady = 20)
  
"""""""fenetre de depart"""
label = Label(master,  
              text ="Voulez-Vous Jouez?") 
  
label.pack(pady = 10) 
  
btn_oui = Button(master,  
             text ="Oui",  
             command = open_fenetre_cartes)
btn_non = Button(master,  
             text ="Non",  
             command = master.destroy) 
btn_oui.pack(pady = 10) 
btn_non.pack(pady = 15) 
"""""""""fin de fenetre de départ"""

mainloop()
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Partie Main"

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

if __name__=="__main__":

    paquet = [{'valeur':7, 'couleur':'P'}, {'valeur':10, 'couleur':'K'}, {'valeur':'A', 'couleur':'T'}]
    afficher_reussite(paquet)
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

