#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
################################################################################
###
###     Programme : codage.py
###
###     Description : Programme de codage pour code convolutif
###     Rendement                   1/4
###     Longueur de contrainte      3
###     Distance libre              9
###     Pouvoir correcteur          4
###
###     Notes : Méthode d'intégration au Programme
###     import codage
###     code = codage.CodeConvolutif().codage(le_code_en_str)
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
        polynome_0 = self.registre[1] ^ self.registre[2]
        polynome_1 = self.registre[0] ^ self.registre[2]
        polynome_2 = self.registre[0] ^ self.registre[1]
        polynome_3 = self.registre[0] ^ self.registre[1] ^ self.registre[2]

        # Envoi de la chaine codé
        return str(polynome_0) + str(polynome_1) + str(polynome_2) + str(polynome_3)

    def decalage(self, code):
        """ Fonction de décalage du registre """
        self.registre[2] = self.registre[1]
        self.registre[1] = self.registre[0]
        self.registre[0] = code

        return self.registre

    def codage(self, code):
        """ Fonction de codage """

        code = code + "00"

        retour = ""

        for bit in code:
            self.decalage(int(bit))
            retour = retour + self.combinaison()
        return retour
