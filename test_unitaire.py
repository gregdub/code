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

import unittest
import random
import codage
import decodage
import constant

class TestClassCodage(unittest.TestCase):
    """ a faire """

    def test_codage(self):
        """ Fonction de test du codage """
        for i in range(8):
            lecodage = codage.CodeConvolutif().codage(constant.LIST_CODE[i])
            self.assertEqual(lecodage, constant.LIST_DECODE[i])

class TestClassDeCodage(unittest.TestCase):
    """ a faire """
    def test_decodage_manuel(self):
        """ Fonction de décodage manuel """
        code = "01000010110110111101"
        ledecodage = decodage.DecodeConvolutif().decodage(code)
        self.assertEqual(ledecodage, "001")

    def test_decodage(self):
        """ Fonction de test du décodage """
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
        """ Fonction de test du décodage avec deux erreurs par octet """
        # Génération des erreurs
        erreur = []

        liste = range(8)

        for i in range(2):
            alea = random.choice(liste)
            while alea in erreur:
                alea = random.choice(liste)
            erreur.append(alea)

        liste = range(8, 12)
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
            print "code sans erreur"
            print constant.LIST_DECODE[i]
            print "code avec erreur"
            print liste_erreur[i]
            ledecodage = decodage.DecodeConvolutif().decodage(liste_erreur[i])
            print ledecodage
            print "STOP"
            self.assertEqual(ledecodage, constant.LIST_CODE[i])


# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()
