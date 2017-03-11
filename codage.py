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

class CodeConvolutif(object):
    """Classe rassemblant toutes les fonctions nécessaires au codage convolutif
    """
    def __init__(self):
        self.registre = [0, 0, 0]

    def combinaison(self):
        """ Fonction de combinaison """
        # Premier polynome générateur
        polynome_1 = self.registre[0] ^ self.registre[1] ^ self.registre[2]
        # Second polynome générateur
        polynome_2 = self.registre[0] ^ self.registre[2]

        # Envoi de la chaine codé
        return str(polynome_1) + str(polynome_2)

    def decalage(self, code):
        """ Fonction de décalage du registre """
        #Ajout de la nouvelle valeur
        self.registre.append(code)

        # Décalage du registre
        self.registre[0] = self.registre[1]
        self.registre[1] = self.registre[2]
        self.registre[2] = self.registre[3]

        # Suppresion de la valeur
        del self.registre[3]

        return self.registre

    def codage(self, code):
        """ Fonction de codage """
        #Ajout de la réinitialisation au code
        code = code + "00"

        #Variable codé avec le code code convolutif
        retour = ""

        for bit in code:
            self.decalage(int(bit))
            retour = retour + self.combinaison()

        return retour
