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

# Module python :
import wx # Module pour l'affichage de la fenètre
#import codage # Module pour l'encodage des bits
#import time
import serial
import serial.tools.list_ports
from serial import SerialException



class MainFrame(wx.Frame):
    """Class de la fenêtre principal"""

    def __init__(self):
        """Initialisation de la class"""
        # Configuration de la fenêtre (taille, nom, ...)
        wx.Frame.__init__(self, None, -1, title='Liaison serie RS232'
                          , style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, size = (800, 600))
        self.Centre()
        # Evenement lors de la fermeture de la fenêtre :
        # self.Bind(wx.EVT_CLOSE, self.OnFerme)

        self.panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(10)
        
        wx.StaticBox(self.panel,1," Configuration du port d'emission: ",(10,10),size=(300,100))

        #ListPort = list(serial.tools.list_ports.comports())
        #for p in ListPort:
            #print(p)
            #ListPort = [p] ???
        # Modification du port :
        wx.StaticText(self.panel,-1,"Port :",(20,30))
        ListPort = ['COMx','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10']
        self.combo1=wx.ComboBox(self.panel,-1,value=ListPort[0],choices=ListPort,size=(80,26),pos=(100,30))
        
        
        # Vitesse de transmission
        wx.StaticText(self.panel,-1,"Vitesse :",(20,50))
        ListVitesse = ['2400','4800','9600','19200','38400','56000','64000']
        self.combo2=wx.ComboBox(self.panel,-1,value=ListVitesse[6],choices=ListVitesse,size=(80,26),pos=(100,50))

        # Boutton de test de la communication serie
        self.BoutonTest=wx.Button(self.panel,label="Test COM",pos=(200,30),size=(80,30))
        self.BoutonTest.SetBackgroundColour(wx.RED)
        self.Bind(wx.EVT_BUTTON, self.TestCom, self.BoutonTest)

        # configure the serial connections
        if self.combo1.GetValue() != 'COMx':
            ser = serial.Serial(
            port=self.combo1.GetValue(),
            baudrate=self.combo2.GetValue(),
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
            ser.isOpen()
     
    # ***** PARTIE RECEPTION *****
          
        wx.StaticBox(self.panel,1," Configuration du port de reception: ",(360,10),size=(300,100))

        # Modification du port :
        wx.StaticText(self.panel,-1,"Port :",(370,30))
        ListPort2 = ['COMx','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10']
        self.combo3=wx.ComboBox(self.panel,-1,value=ListPort2[0],choices=ListPort2,size=(80,26),pos=(450,30))

        # Vitesse de transmission
        wx.StaticText(self.panel,-1,"Vitesse :",(370,50))
        ListVitesse2 = ['2400','4800','9600','19200','38400','56000','64000']
        self.combo4=wx.ComboBox(self.panel,-1,value=ListVitesse2[6],choices=ListVitesse2,size=(80,26),pos=(450,50))

        """if self.combo3.GetValue() != 'COMx':
            ser = serial.Serial(
            port=self.combo3.GetValue(),
            baudrate=self.combo4.GetValue(),
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
            ser.isOpen()"""

    # ***** PARTIE SAISIE TEXTE *****

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        #vbox.Add((-10, 10))
        vbox.AddSpacer(120)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self.panel, label='Saisie de la phrase :')
        hbox1.Add(st1)
        vbox.Add(hbox1, flag=wx.LEFT | wx.TOP)

        #vbox.Add((-1, 10))

        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        self.saisie = wx.TextCtrl(self.panel, size = (600,100), style=wx.TE_MULTILINE)
        hbox10.Add(self.saisie,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        vbox.Add(hbox10) 
        self.saisie.Bind(wx.EVT_TEXT_ENTER,self.SaisiePhrase)


        
        
    # ***** PARTIE MODIFICATION DU TEXTE *****

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self.panel, label='Code a envoyer :')
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP)

        #vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.saisieModif = wx.TextCtrl(self.panel, size = (600,100), style=wx.TE_MULTILINE)
        hbox3.Add(self.saisieModif,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        vbox.Add(hbox3) 
        self.saisieModif.Bind(wx.EVT_TEXT_ENTER,self.SaisieModification)

        #vbox.Add((-1, 25))
    
    
    # ***** RECEPTION DU CODE *****

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self.panel, label='Code recu :')
        hbox4.Add(st3)
        vbox.Add(hbox4, flag=wx.LEFT | wx.TOP)

        #vbox.Add((-1, 10))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.t3 = wx.TextCtrl(self.panel, size = (600,100), style=wx.TE_MULTILINE)
        hbox5.Add(self.t3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        vbox.Add(hbox5) 

        # a mettre pour la répartition des zones de texte sur l'ecran
        self.panel.SetSizer(vbox)

        # Boutton pour la transmission
        BoutonTransmit=wx.Button(self.panel,label="Envoi",pos=(700,500),size=(80,30))
        self.Bind(wx.EVT_BUTTON, self.Transmit, BoutonTransmit)


    # ***** FONCTIONS *****
    
    def TestCom(self,event):
        #self.Close(True)
        #ser = serial.Serial(self.combo1.GetValue(), self.combo2.GetValue(), timeout=1)
        try:
            ser = serial.Serial(self.combo1.GetValue(), self.combo2.GetValue(), timeout=1)
        except SerialException:
            self.BoutonTest.SetBackgroundColour(wx.RED)
            msg = """ port COM inexistant """
            wx.MessageBox(msg)
            return None
        chaine="test"
        envoi=ser.write(chaine)     # Envoi de la chaine de caracteres
        lecture=ser.readline()      # Lecture du port jusqu'au \n (retour ligne)
        if (chaine==lecture):
            self.BoutonTest.SetBackgroundColour(wx.GREEN)
        else:
            self.BoutonTest.SetBackgroundColour(wx.RED)

    def SaisiePhrase(self,event): 
        
        # conversion de la phrase en binaire :

        #ListCar = list self.saisie
        #for EachCar in self.saisie.Get:
        #    print(EachCar)
            
        #et envoi à codage (variable code) par morceaux de 4 bits :
        
        #print(bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in self.saisie), 0)))
        #self.saisieModif.SetLabel(SaisieConvBin)
        #self.saisieModif.SetLabel(SaisieConvBin.GetValue())

        
        
        a = wx.App(redirect=False)
##        my_str = wx.GetTextFromUser("Enter A Number!")
##        base = {'x':16,'b':2,'o':8}.get(my_str[1].lower(),10)
##        int_val = int(my_str,base)
##        hex_str = hex(int_val)   
##        bin_str = bin(int_val)
##
##        msg = """
##        User Entered:%s
##        Int:%s
##        Hex:%s
##        Bin:%s"""%(my_str,int_val,hex_str,bin_str)
##        wx.MessageBox(msg)

    # ***** Fonction ENVOI DU CODE *****
    # par appui sur Enter ou bouton
    def SaisieModification(self,event): 
        print "Enter pressed"
        #ser.write(bytes(b'your_commands'))

    def Transmit(self,event): 
        print "Enter pressed"
        #ser.write(bytes(b'your_commands'))

        
"""
    def OnFerme(self, event):
        Lors de la fermeture de la fenêtre
        dialogue = wx.MessageDialog(self, "Souhaitez vous vraiment quitter cette application ?"
                                    ,"Quitter l'application", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dialogue.ShowModal()
        dialogue.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
"""
if __name__ == '__main__':
    APP = wx.App(redirect=True)
    FRAME = MainFrame()
    FRAME.Show()
    APP.MainLoop()
