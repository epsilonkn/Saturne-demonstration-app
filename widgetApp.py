#fichier contenant les widgets à créer
#modifier la manière dont est construite l'interface
from typing import Optional, Tuple, Union
import customtkinter as ct
import json


class WidgetApp(ct.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.getWidget()
        self.title("Widgets")
        self.choice = None

        self.main_frame = ct.CTkScrollableFrame(self, width=360, height = 150)
        self.main_frame.grid()

        r_ind = 0
        c_ind = 0
        for elements in self.widgets_list :
            self.bt = ct.CTkButton(self.main_frame, text = elements["name"], font=ct.CTkFont(size=15, weight="bold"), width=160,height = 40, command = lambda x=elements["id"] : self.choiceDone(x))
            self.bt.grid(row = r_ind, column = c_ind, padx = 10, pady = 10)
            
            c_ind = c_ind + 1 if c_ind == 0 else 0
            r_ind +=1 if c_ind == 0 else 0


    def getWidget(self):
        """getWidget 
        Récupère les widgets existants
        """
        with open("rssDir\\widgetRss.json", "r", encoding= 'utf8') as file :
            self.widgets_list = json.load(file)
        file.close()


    def choiceDone(self, choice : str):
        """choiceDone 
        Enregistre l'ID du widget choisi

        Parameters
        ----------
        choice : str
            ID du widget choisi
        """
        self.choice = choice
        self.destroy()


    def get(self):
        """get 
        Retourne l'ID du widget choisi une fois la fenêtre fermée
        """
        self.master.wait_window(self)
        return self.choice