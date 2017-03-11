#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
###
###     Programme : Liaison série RS232 avec code correcteur d'erreur
###
###     Description : Implémentation d'un code correcteur d'erreur pour une
###                   liaison série capable de corriger deux erreurs par octets
###
###     Notes : ///////
###
###     Auteurs : Toladar
###               gregdub
###
###     Date : 23/02/17
###
################################################################################
"""



# Découpage du code :
def decoupage(str_code):
    """ Fonction de découpage en groupe de deux bits du code reçu"""
    listtest = [0, 2, 4, 6, 8, 10]
    for i in listtest:
        Liste_Code.append(str_code[i:i+2])
    print Liste_Code

def distance_hamming(str_code_a, str_code_b):
    """ Fonction qui calcul la distance de Hamming entre deux codes """

    # Création des listes pour le stockage des codes
    list_a = []
    list_b = []

    # On stock chaque caractère dans une liste
    for i in str_code_a:
        list_a.append(i)

    for i in str_code_b:
        list_b.append(i)

    # On compte le nombre de différences entre chaque case
    cpt = 0

    for i in range(2):
        if list_a[i] != list_b[i]:
            cpt = cpt + 1

    # On retourne le résultat
    return cpt

class Noeud(object):
    """ Objet noeud qui compose le treillis pour le décodage"""
    def __init__(self, str_type_noeud):
        self.type_noeud = str_type_noeud
        self.haut = None
        self.bas = None
        self.distance = 0
        self.code = ""

    def get_type_noeud(self):
        """ Fonction qui retourne le type du noeud """
        return self.type_noeud

    def get_haut(self):
        """ Fonction qui retourne l'adresse du noeud enfant en haut """
        return self.haut

    def get_bas(self):
        """ Fonction qui retourne l'adresse du noeud enfant du bas """
        return self.bas

    def get_distance(self):
        """ Fonction qui retourne la distance de hamming du noeud """
        return self.distance

    def get_code(self):
        """ Fonction qui retourne le code du noeud """
        return self.code

    def get_info(self):
        """ Fonction qui écrit dans la console les informations du noeud """
        print "Type de noeud     : " + self.type_noeud
        print "Noeud enfant haut : " + str(self.haut)
        print "Noeud enfant bas  : " + str(self.bas)
        print "Distance du noeud : " + str(self.distance)
        print "Code du noeud     : " + self.code
        print

    def set_type_noeud(self, str_type_noeud):
        """ Fonction qui modifie le type du noeud """
        self.type_noeud = str_type_noeud

    def set_haut(self, add_haut):
        """ Fonction qui modifie l'adresse de l'enfant du haut du noeud """
        self.haut = add_haut

    def set_bas(self, add_bas):
        """ Fonction qui modifie l'adresse de l'enfant du bas du noeud """
        self.bas = add_bas

    def set_distance(self, int_distance):
        """ Fonction qui modifie la distance de hamming qui noeud """
        self.distance = int_distance

    def set_code(self, str_code):
        """ Fonction qui modifie le code du noeud """
        self.code = str_code

def noeud_suivant(add_noeud, i, j):
    """ Fonction de création des noeuds en fonction de leur type (a, b, c, d)"""
    if add_noeud.get_type_noeud() == "a":
        #=======================================================================
        # Création du Noeud a
        branche_haut = Noeud(str_type_noeud="a")

        # Distance par rapport au code reçu
        distance_temp_haut = distance_hamming(Liste_Code[i], "00")

        # Ajout de la distance du noeud précédent
        distance_temp_haut = distance_temp_haut + add_noeud.get_distance()
        branche_haut.set_distance(distance_temp_haut)

        # Ajout du code précédent au code actuelle
        code_temp_haut = add_noeud.get_code()
        code_temp_haut = code_temp_haut + "0"
        branche_haut.set_code(code_temp_haut)

        #=======================================================================
        # Création du Noeud c
        branche_bas = Noeud(str_type_noeud="c")

        # Distance par rapport au code reçu
        distance_temp_bas = distance_hamming(Liste_Code[i], "11")

        # Ajout de la distance du noeud précédent
        distance_temp_bas = distance_temp_bas + add_noeud.get_distance()
        branche_bas.set_distance(distance_temp_bas)

        # Ajout du code précédent au code actuelle
        code_temp_bas = add_noeud.get_code()
        code_temp_bas = code_temp_bas + "1"
        branche_bas.set_code(code_temp_bas)

        #=======================================================================
        # Ajout au Noeud précédent :
        add_noeud.set_haut(branche_haut)
        add_noeud.set_bas(branche_bas)

        # Ajout à la liste :
        ListNoeud.append(branche_haut)
        ListNoeud.append(branche_bas)

    elif add_noeud.get_type_noeud() == "b":
        #=======================================================================
        # Adresse de la branche A précédament crée
        branche_haut = ListNoeud[j+2]

        # Distance par rapport au code reçu
        distance_temp_haut = distance_hamming(Liste_Code[i], "11")

        # Ajout de la distance du noeud précédent
        distance_temp_haut = distance_temp_haut + add_noeud.get_distance()
        # Comparaison de la distance calculée et la distance actuelle
        # Récupération de la distance actuelle de a
        distance_a = branche_haut.get_distance()

        if distance_a > distance_temp_haut:
            # On modifie la distance
            branche_haut.set_distance(distance_temp_haut)
            # On modifie le code
            code_temp_haut = add_noeud.get_code()
            code_temp_haut = code_temp_haut + "0"
            branche_haut.set_code(code_temp_haut)

        # Dans le cas contraire on ne fait rien

        #=======================================================================
        # Adresse de la branche C précédament crée
        branche_bas = ListNoeud[j+3]

        # Distance par rapport au code reçu
        distance_temp_bas = distance_hamming(Liste_Code[i], "00")

        # Ajout de la distance du noeud précédent
        distance_temp_bas = distance_temp_bas + add_noeud.get_distance()
        # Comparaison de la distance calculée et la distance actuelle
        # Récupération de la distance actuelle de a
        distance_a = branche_bas.get_distance()

        if distance_a > distance_temp_bas:
            # On modifie la distance
            branche_bas.set_distance(distance_temp_bas)
            # On modifie le code
            code_temp_bas = add_noeud.get_code()
            code_temp_bas = code_temp_bas + "1"
            branche_bas.set_code(code_temp_bas)

        # Dans le cas contraire on ne fait rien

        #=======================================================================
        # Ajout au Noeud précédent :
        add_noeud.set_haut(branche_haut)
        add_noeud.set_bas(branche_bas)

    elif add_noeud.get_type_noeud() == "c":
        #=======================================================================
        # Création du Noeud b
        branche_haut = Noeud(str_type_noeud="b")

        # Distance par rapport au code reçu
        distance_temp_haut = distance_hamming(Liste_Code[i], "10")

        # Ajout de la distance du noeud précédent
        distance_temp_haut = distance_temp_haut + add_noeud.get_distance()
        branche_haut.set_distance(distance_temp_haut)

        # Ajout du code précédent au code actuelle
        code_temp_haut = add_noeud.get_code()
        code_temp_haut = code_temp_haut + "0"
        branche_haut.set_code(code_temp_haut)

        #=======================================================================
        # Création du Noeud d
        branche_bas = Noeud(str_type_noeud="d")

        # Distance par rapport au code reçu
        distance_temp_bas = distance_hamming(Liste_Code[i], "01")

        # Ajout de la distance du noeud précédent
        distance_temp_bas = distance_temp_bas + add_noeud.get_distance()
        branche_bas.set_distance(distance_temp_bas)

        # Ajout du code précédent au code actuelle
        code_temp_bas = add_noeud.get_code()
        code_temp_bas = code_temp_bas + "1"
        branche_bas.set_code(code_temp_bas)

        #=======================================================================
        # Ajout au Noeud précédent :
        add_noeud.set_haut(branche_haut)
        add_noeud.set_bas(branche_bas)

        # Ajout à la liste :
        ListNoeud.append(branche_haut)
        ListNoeud.append(branche_bas)

    elif add_noeud.get_type_noeud() == "d":
        #=======================================================================
        # Adresse de la branche B précédament crée
        branche_haut = ListNoeud[j+3]

        # Distance par rapport au code reçu
        distance_temp_haut = distance_hamming(Liste_Code[i], "01")

        # Ajout de la distance du noeud précédent
        distance_temp_haut = distance_temp_haut + add_noeud.get_distance()
        # Comparaison de la distance calculée et la distance actuelle
        # Récupération de la distance actuelle de a
        distance_a = branche_haut.get_distance()

        if distance_a > distance_temp_haut:
            # On modifie la distance
            branche_haut.set_distance(distance_temp_haut)
            # On modifie le code
            code_temp_haut = add_noeud.get_code()
            code_temp_haut = code_temp_haut + "0"
            branche_haut.set_code(code_temp_haut)

        # Dans le cas contraire on ne fait rien

        #=======================================================================
        # Adresse de la branche D précédament crée
        branche_bas = ListNoeud[j+4]

        # Distance par rapport au code reçu
        distance_temp_bas = distance_hamming(Liste_Code[i], "10")

        # Ajout de la distance du noeud précédent
        distance_temp_bas = distance_temp_bas + add_noeud.get_distance()
        # Comparaison de la distance calculée et la distance actuelle
        # Récupération de la distance actuelle de a
        distance_a = branche_bas.get_distance()

        if distance_a > distance_temp_bas:
            # On modifie la distance
            branche_bas.set_distance(distance_temp_bas)
            # On modifie le code
            code_temp_bas = add_noeud.get_code()
            code_temp_bas = code_temp_bas + "1"
            branche_bas.set_code(code_temp_bas)

        # Dans le cas contraire on ne fait rien

        #=======================================================================
        # Ajout au Noeud précédent :
        add_noeud.set_haut(branche_haut)
        add_noeud.set_bas(branche_bas)

def debug():
    """ Fonction de visualisation de l'ensemble des noeuds """
    for itt in ListNoeud:
        print
        print itt
        print itt.get_info()


CODE = "100101010000"
# 11 10 11 11 10 11
Liste_Code = []

ListNoeud = []
decoupage(CODE)

#Création de la racine du treillis
racine = Noeud(str_type_noeud="a")
ListNoeud.append(racine)

#Création des deux premier noeuds de la racine : i = 0
noeud_suivant(ListNoeud[0], 0, 0)

# i = 1
noeud_suivant(ListNoeud[1], 1, 1)

noeud_suivant(ListNoeud[2], 1, 2)

# i = 2

noeud_suivant(ListNoeud[3], 2, 3)

noeud_suivant(ListNoeud[4], 2, 4)

noeud_suivant(ListNoeud[5], 2, 5)

noeud_suivant(ListNoeud[6], 2, 6)

# i = 3
noeud_suivant(ListNoeud[7], 3, 7)

noeud_suivant(ListNoeud[8], 3, 8)

noeud_suivant(ListNoeud[9], 3, 9)

noeud_suivant(ListNoeud[10], 3, 10)

# i = 4
noeud_suivant(ListNoeud[11], 4, 11)

noeud_suivant(ListNoeud[12], 4, 12)

noeud_suivant(ListNoeud[13], 4, 13)

noeud_suivant(ListNoeud[14], 4, 14)

# i = 5
noeud_suivant(ListNoeud[15], 5, 15)

noeud_suivant(ListNoeud[16], 5, 16)

noeud_suivant(ListNoeud[17], 5, 17)

noeud_suivant(ListNoeud[18], 5, 18)


# Liste des feuilles du treillis :
ListTemp = ListNoeud[-4:]
ListResultats = []
# Supprimer de toute la list les code qui ne finisent pas par "00"
for i in range(4):
    code = ListTemp[i].get_code()
    print code
    code = code[-2:]
    if code == "00":
        ListResultats.append(ListTemp[i])

del ListTemp

# Test de la longueur du tableau des résultats
if len(ListResultats) == 1:
    lecode = ListResultats[0].get_code()
    lecode = lecode[:-2]
    print "Le résultat est : " + lecode
else:
    pass
