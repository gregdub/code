#!/usr/bin/python
# -*- coding:  mbcs -*-
"""
################################################################################
###
###     Programme : Liaison série RS232 avec code correcteur d'erreur
###
###     Description : Implémentation d'un code correcteur d'erreur pour une
###                   liaison série capable de corriger deux erreurs par octets
###
###     Auteurs : Toladar
###               gregdub
###
###     Date : 23/02/17
###
################################################################################
"""

# Module python :
import time
from math import *
import wx # Module pour l'affichage de la fenètre
import serial
import serial.tools.list_ports
from serial import SerialException
import binascii
import codage # Module pour l'encodage des bits
import decodage # Module pour le decodage des bits

class MainFrame(wx.Frame):
    """Classe de la fenêtre principal"""

    def __init__(self):
        """Initialisation de la class"""
        # Configuration de la fenêtre (taille, nom, ...)
        wx.Frame.__init__(self, None, -1, title="Liaison serie RS232"
                          , style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, size=(800, 600))
        self.Centre()

        self.panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)

        wx.StaticText(self.panel, -1,
                      "Transmission série avec correction de 2 erreurs/octet - Copyright Blochet Bastien et Dubois Grégoire",
                      (1, 550))

        wx.StaticBox(self.panel, 1, " Configuration du port d'emission: ",
                     (10, 10), size=(300, 100))

        # Modification du port :
        wx.StaticText(self.panel, -1, "Port :", (20, 30))
        list_port = ['COMx', 'COM1', 'COM2', 'COM3', 'COM4',
                     'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                     'COM10']
        self.combo1 = wx.ComboBox(self.panel, -1, value=list_port[3],
                                  choices=list_port, size=(80, 26), pos=(100, 30))

        # Vitesse de transmission
        wx.StaticText(self.panel, -1, "Vitesse :", (20, 50))
        list_vitesse = ['2400', '4800', '9600', '19200', '38400', '56000', '64000']
        self.combo2 = wx.ComboBox(self.panel, -1, value=list_vitesse[6],
                                  choices=list_vitesse, size=(80, 26), pos=(100, 50))

        # Bouton de test de la communication serie
        self.boutontest = wx.Button(self.panel, label="Test COM", pos=(200, 30), size=(80, 30))
        self.boutontest.SetBackgroundColour(wx.RED)
        self.Bind(wx.EVT_BUTTON, self.test_com, self.boutontest)

        # Configure la connexion de la liaison série
        if self.combo1.GetValue() != 'COMx':
            ser_trans = serial.Serial(port=self.combo1.GetValue(),
                                      baudrate=self.combo2.GetValue(),
                                      parity=serial.PARITY_EVEN,
                                      stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS)
            ser_trans.isOpen()

        #=======================================================================
        #                   ***** PARTIE RECEPTION *****
        #=======================================================================

        wx.StaticBox(self.panel, 1, " Configuration du port de reception: ",
                     (360, 10), size=(300, 100))

        # Modification du port :
        wx.StaticText(self.panel, -1, "Port :", (370, 30))
        list_port2 = ['COMx', 'COM1', 'COM2', 'COM3', 'COM4',
                      'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10']

        self.combo3 = wx.ComboBox(self.panel, -1, value=list_port2[0],
                                  choices=list_port2, size=(80, 26), pos=(450, 30))

        # Vitesse de reception
        wx.StaticText(self.panel, -1, "Vitesse :", (370, 50))
        list_vitesse2 = ['2400', '4800', '9600', '19200', '38400', '56000', '64000']
        self.combo4 = wx.ComboBox(self.panel, -1, value=list_vitesse2[6],
                                  choices=list_vitesse2, size=(80, 26), pos=(450, 50))

        #=======================================================================
        #                   ***** PARTIE SAISIE TEXTE *****
        #=======================================================================
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        vbox.AddSpacer(120)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label=' Saisie de la phrase :')
        hbox1.Add(st1)
        vbox.Add(hbox1, flag=wx.LEFT | wx.TOP)

        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        self.saisie = wx.TextCtrl(self.panel, size=(600, 50), style=wx.TE_MULTILINE)
        hbox10.Add(self.saisie, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
        vbox.Add(hbox10)
        self.saisie.Bind(wx.EVT_TEXT_ENTER, self.saisie_phrase)

        #=======================================================================
        #                   ***** PARTIE MODIFICATION DU TEXTE *****
        #=======================================================================

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self.panel, label=' Code a envoyer :')
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.saisie_modif = wx.TextCtrl(self.panel, size=(600, 50), style=wx.TE_MULTILINE)
        hbox3.Add(self.saisie_modif, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox3)
        self.saisie_modif.Bind(wx.EVT_TEXT_ENTER, self.saisie_modification)

        vbox.Add((-1, 50))

        #=======================================================================
        #                   ***** RECEPTION DU CODE *****
        #=======================================================================

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self.panel, label=' Code recu decode :')
        hbox4.Add(st3)
        vbox.Add(hbox4, flag=wx.LEFT | wx.TOP)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.coderecu = wx.TextCtrl(self.panel, size=(600, 50), style=wx.TE_MULTILINE)
        hbox5.Add(self.coderecu, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox5)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self.panel, label=' Retranscription de la phrase :')
        hbox6.Add(st4)
        vbox.Add(hbox6, flag=wx.LEFT | wx.TOP)

        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.phrasedecode = wx.TextCtrl(self.panel, size=(600, 50), style=wx.TE_MULTILINE)
        hbox7.Add(self.phrasedecode, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox7)

        # a mettre pour la répartition des zones de texte sur l'ecran
        self.panel.SetSizer(vbox)

        # Bouton pour la transmission
        bouton_transmit = wx.Button(self.panel, label="Envoi", pos=(650, 235), size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.transmit, bouton_transmit)

        # Bouton pour tout effacer
        bouton_clear = wx.Button(self.panel, label="Clear all", pos=(650, 400), size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.clear, bouton_clear)


    def test_com(self, event):
        """ Fonction de test la communication série """
        try:
            ser = serial.Serial(self.combo1.GetValue(), self.combo2.GetValue(), timeout=1)
        except SerialException:
            self.boutontest.SetBackgroundColour(wx.RED)
            msg = """ port COM inexistant """
            wx.MessageBox(msg)
            return None
        chaine = "test"
        ser.write(chaine)     # Envoi de la chaine de caracteres
        lecture = ser.readline()      # Lecture du port jusqu'au \n (retour ligne)
        if chaine == lecture:
            self.boutontest.SetBackgroundColour(wx.GREEN)
        else:
            self.boutontest.SetBackgroundColour(wx.RED)

    def saisie_phrase(self, event):
        """ TODO """
        self.saisie_modif.SetLabel('')
        # conversion de la phrase en binaire :
        codepage1252 = self.saisie.GetValue()
        
        liste=list(codepage1252)
        taille=len(liste)
        ajout = 3-(taille %3)        
        if ajout != 0:
            for i in range(0,ajout):
                liste.append(" ")
                
        codepage1252 = "".join(liste)
        
        codepage1252 = codepage1252.encode('cp1252')       
        

        #print(codepage1252)
        hexstring = codepage1252.encode('hex')
        #print(hexstring)
        binary = bin(int('1' + hexstring, 16))[3:]
        #print(binary)

        longueurenvoi=len(binary)
        code3=[]
            
        for i in range(0,longueurenvoi/3):
            code3.append(binary[i*3:(i*3)+3])
            
        for i in range(0,len(code3)):
            motcode = codage.CodeConvolutif().codage(code3[i])
            #print motcode
            #affichage de la phrase codee
            currentcode = self.saisie_modif.GetValue()
            self.saisie_modif.SetLabel(currentcode + motcode)

        var = self.saisie_modif.GetValue()
        nb_sep = 8
        b = " ".join([var[i:i+nb_sep] for i in range(0,len(var),nb_sep)])
        self.saisie_modif.SetLabel(b)

    def saisie_modification(self, event):
        """ Fonction d'envoi du code par appui sur le bouton ou la
        touche entrer """
        self.coderecu.SetLabel('')
        start_time = time.time()
        #envoi sur la liaison serie
        ser_trans = serial.Serial(self.combo1.GetValue(), self.combo2.GetValue(), timeout=1)
        ser_trans.write(bytes(self.saisie_modif.GetValue()))

        #reception sur la liaison serie
        if self.combo3.GetValue() != 'COMx':
            ser_recep = serial.Serial(self.combo3.GetValue(), self.combo4.GetValue(), timeout=1)
            lecturecode = ser_recep.readline()
        else:
            lecturecode = ser_trans.readline()

        #fonction decodage
        lecturecode=str(lecturecode)
        lecturecode = lecturecode.replace(' ','')
        longueur=len(lecturecode)
        listcode=[]
        
        for i in range(0,longueur/20):
            listcode.append(lecturecode[i*20:(i*20)+20])

        for i in range(0,len(listcode)):
            motdecode = decodage.DecodeConvolutif().decodage(listcode[i])
            current = self.coderecu.GetValue()
            self.coderecu.SetLabel(current + motdecode)

        mystring = binascii.unhexlify('%x' % int('0b' + self.coderecu.GetValue(), 2))
        self.phrasedecode.SetLabel(mystring)
                                      
        wx.StaticText(self.panel, -1,
                      " Executed in : %s second(s)" % (time.time() - start_time), (1, 530))


    def transmit(self, event):
        """ TODO """
        #execute la meme fonction que SaisieModification
        self.saisie_modification(event)

    def clear(self, event):
        """ Fonction qui efface les différentes boites de dialogue """
        self.saisie.SetLabel('')
        self.saisie_modif.SetLabel('')
        self.coderecu.SetLabel('')
        self.phrasedecode.SetLabel('')

if __name__ == '__main__':
    APP = wx.App(redirect=True)
    FRAME = MainFrame()
    FRAME.Show()
    APP.MainLoop()
