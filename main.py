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

class MainFrame(wx.Frame):
    """Class de la fenêtre principal"""

    def __init__(self):
        """Initialisation de la class"""
        # Configuration de la fenêtre (taille, nom, ...)
        wx.Frame.__init__(self, None, -1, title='Liaison série RS232'
                          , style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, size = (800, 400))

        # Evenement lors de la fermeture de la fenêtre :
        # self.Bind(wx.EVT_CLOSE, self.OnFerme)

        self.panel = wx.Panel(self)

        wx.StaticBox(self.panel,1," Configuration : ",(10,10),size=(400,200))

        # Modification du port :
        wx.StaticText(self.panel,-1,"Port :",(20,30))
        ListPort = ['COM1','COM2','COM3']
        wx.ComboBox(self.panel,-1,choices=ListPort,size=(80,26),pos=(150,30))

        # Vitesse de transmission
        wx.StaticText(self.panel,-1,"Vitesse :",(20,50))
        ListVitesse = ['2400','4800','9600','19200','38400','56000']
        wx.ComboBox(self.panel,-1,choices=ListVitesse,size=(80,26),pos=(150,50))


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
