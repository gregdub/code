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
import codage
import decodage

class TestClassCodage(unittest.TestCase):

    def test_codage(self):
        code = "1001"
        lecodage = codage.CodeConvolutif().codage(code)
        self.assertEqual(lecodage, "111011111011")

class TestClassDeCodage(unittest.TestCase):

    def test_decodage(self):
        code = "111011111011"
        ledecodage = decodage.DecodeConvolutif().decodage(code)
        self.assertEqual(ledecodage, "1001")

# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()
