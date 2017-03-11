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

        """ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)"""
        # Modification du port :
        wx.StaticText(self.panel,-1,"Port :",(20,30))
        ListPort = ['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10']
        wx.ComboBox(self.panel,-1,choices=ListPort,size=(80,26),pos=(100,30))

        # Vitesse de transmission
        wx.StaticText(self.panel,-1,"Vitesse :",(20,50))
        ListVitesse = ['2400','4800','9600','19200','38400','56000','64000']
        wx.ComboBox(self.panel,-1,choices=ListVitesse,size=(80,26),pos=(100,50))

        # Boutton de test de la communication serie
        BoutonTest=wx.Button(self.panel,label="Test COM",pos=(200,30),size=(80,30))
        BoutonTest.SetBackgroundColour(wx.RED)
        self.Bind(wx.EVT_BUTTON, self.TestCom, BoutonTest)

##        ser = serial.Serial()
##        ser.baudrate = 19200
##        ser.port = 'COM1'
##        ser
##        Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
##        ser.open()
##        ser.is_open

        

        # configure the serial connections (the parameters differs on the device you are connecting to)
        """        ser = serial.Serial(
        port='COM1',
        baudrate=9600,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
        ser.isOpen()"""
     
    # ***** PARTIE RECEPTION *****
          
        wx.StaticBox(self.panel,1," Configuration du port de reception: ",(360,10),size=(300,100))

        # Modification du port :
        wx.StaticText(self.panel,-1,"Port :",(370,30))
        ListPort2 = ['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10']
        wx.ComboBox(self.panel,-1,choices=ListPort2,size=(80,26),pos=(450,30))

        # Vitesse de transmission
        wx.StaticText(self.panel,-1,"Vitesse :",(370,50))
        ListVitesse2 = ['2400','4800','9600','19200','38400','56000','64000']
        wx.ComboBox(self.panel,-1,choices=ListVitesse2,size=(80,26),pos=(450,50))


    # ***** PARTIE SAISIE TEXTE *****

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        #vbox.Add((-10, 10))
        vbox.AddSpacer(120)
        
        """l1 = wx.StaticText(self.panel, -1, "Saisie de la phrase :") 
		
        hbox1.Add(l1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t1 = wx.TextCtrl(self.panel, size = (600,100), style=wx.TE_MULTILINE) 
		
        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t1.Bind(wx.EVT_TEXT_ENTER,self.SaisiePhrase) 
        vbox.Add(hbox1)"""

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

    def TestCom(self,event):
        self.Close(True)

    def SaisiePhrase(self,event): 
        #print "Enter pressed"
        # conversion de la phrase en binaire et envoi à codage (variable code) par morceaux de 4 bits
        #print(bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in self.saisie), 0)))
        #self.saisieModif.SetLabel(SaisieConvBin)
        #self.saisieModif.SetLabel(SaisieConvBin.GetValue())
        
        a = wx.App(redirect=False)
        my_str = wx.GetTextFromUser("Enter A Number!")
        base = {'x':16,'b':2,'o':8}.get(my_str[1].lower(),10)
        int_val = int(my_str,base)
        hex_str = hex(int_val)   
        bin_str = bin(int_val)

        msg = """
        User Entered:%s
        Int:%s
        Hex:%s
        Bin:%s"""%(my_str,int_val,hex_str,bin_str)
        wx.MessageBox(msg)

    # ***** Fonction ENVOI DU CODE *****
    # par appui sur Enter ou bouton
    def SaisieModification(self,event): 
        print "Enter pressed"

    def Transmit(self,event): 
        print "Enter pressed"

        
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
