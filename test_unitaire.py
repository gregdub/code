#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
################################################################################
###
###     Programme : test_unitaire.py
###
###     Description : Programme de test du codeur ainsi que du décodeur avec
###     focntion d'ajout d'erreur
###
###     Auteurs : Toladar
###               gregdub
###
###     Date : 23/02/17
###
################################################################################
"""

import unittest
import random
import codage
import decodage
import constant

class TestClassCodage(unittest.TestCase):
    """ Classe de test du codeur """

    def test_codage(self):
        """ Fonction de test du codeur avec tous les états possible """
        for i in range(8):
            lecodage = codage.CodeConvolutif().codage(constant.LIST_CODE[i])
            self.assertEqual(lecodage, constant.LIST_DECODE[i])

class TestClassDeCodage(unittest.TestCase):
    """ Classe de test du décodeur """

    def test_decodage_manuel(self):
        """ Fonction de test du décodage manuel """
        code = "01000010110110111101"
        ledecodage = decodage.DecodeConvolutif().decodage(code)
        self.assertEqual(ledecodage, "001")

    def test_decodage(self):
        """ Fonction de test du décodage avec tous les états possible """
        for i in range(8):
            ledecodage = decodage.DecodeConvolutif().decodage(constant.LIST_DECODE[i])
            self.assertEqual(ledecodage, constant.LIST_CODE[i])

    def test_decodage_une_erreur(self):
        """ Fonction de test du décodage avec une erreur par octet """
        # Génération des erreurs
        erreur = []

        liste = range(8)
        erreur.append(random.choice(liste))

        liste = range(8, 12)
        erreur.append(random.choice(liste))

        liste_erreur = ["", "", "", "", "", "", "", ""]
        # Ajout des erreurs dans le code
        for i in range(8):
            liste_erreur[i] = constant.LIST_DECODE[i]

        for i in range(8):
            erreur_temp = list(liste_erreur[i])

            for j in erreur:
                if erreur_temp[j] == "0":
                    erreur_temp[j] = "1"
                else:
                    erreur_temp[j] = "0"

            liste_erreur[i] = ''.join(erreur_temp)

        # Decodage
        for i in range(8):
            ledecodage = decodage.DecodeConvolutif().decodage(liste_erreur[i])
            self.assertEqual(ledecodage, constant.LIST_CODE[i])

    def test_decodage_deux_erreurs(self):
        """ Fonction de test du décodage avec deux erreurs dans les deux premiers octets """
        # Génération des erreurs
        erreur = []

        liste = range(8)

        for i in range(2):
            alea = random.choice(liste)
            while alea in erreur:
                alea = random.choice(liste)
            erreur.append(alea)

        liste = range(8, 16)
        for i in range(2):
            alea = random.choice(liste)
            while alea in erreur:
                alea = random.choice(liste)
            erreur.append(alea)

        liste_erreur = ["", "", "", "", "", "", "", ""]
        # Ajout des erreurs dans le code
        for i in range(8):
            liste_erreur[i] = constant.LIST_DECODE[i]

        for i in range(8):
            erreur_temp = list(liste_erreur[i])
            for j in erreur:
                if erreur_temp[j] == "0":
                    erreur_temp[j] = "1"
                else:
                    erreur_temp[j] = "0"

            liste_erreur[i] = ''.join(erreur_temp)

        # Decodage
        for i in range(8):
            ledecodage = decodage.DecodeConvolutif().decodage(liste_erreur[i])
            self.assertEqual(ledecodage, constant.LIST_CODE[i])

# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()
