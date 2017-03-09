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
###     Date : 09/03/17
###
################################################################################
"""

# Initialisation du registre
REGISTRE=[0,0,0]

# Code envoyé
CODE = "1001"

# Chaine de caractère de retour
RETOUR = ""

def codeConvolutif():
    """ Fonction de génération """
    # Premier polynome générateur
    c1 = REGISTRE[0] ^ REGISTRE[1] ^ REGISTRE[2]
    # Second polynome générateur
    c2 = REGISTRE[0] ^ REGISTRE[2]

    # Envoi de la chaine codé
    return str(c1) + str(c2)

def decalage(x):
    """ Fonction de décalage du registre """
    #Ajout de la nouvelle valeur
    REGISTRE.append(x)

    # Décalage du registre
    REGISTRE[0]=REGISTRE[1]
    REGISTRE[1]=REGISTRE[2]
    REGISTRE[2]=REGISTRE[3]

    # Suppresion de la valeur
    del REGISTRE[3]

# Rajout de deux bits à zéro pour le réinitialisation
CODE = CODE + "00"

# Parcours du Code
for bit in CODE:
    decalage(int(bit))
    RETOUR = RETOUR + str(codeConvolutif())

# Affichage du retour
print RETOUR
