#fichier contenant l'interface graphique du programme
from typing import Union
import tkinter as tk
from tkinter import messagebox
import customtkinter as ct
import json
import tool_tip as tl
import intermediateLayer as interl
from settingsApp import AppEditing
from widgetApp import WidgetApp
from projectApp import ProjectApp
from topLevelWin import *
import webbrowser


class interface(ct.CTk):


    def __init__(self) -> None:
        super().__init__()
        
        self.widgets_list = [] #liste des widgets existant dans le projet ouvert
        self.actual_sets = [] #liste des paramètres utilisés dans l'application
        self.layout_list = [] #liste contenant des paramètres de layout, comprenant pour chacun : leur nom, entrée associée, et valeur par défaut
        self.language_dict = {} #dictionnaire contenant les traductions
        self.settings = None # défini si la fenêtre de paramètre est ouverte ou non
        self.widgetapp = None # défini si la fenêtre de widgets est ouverte ou non
        self.project_app = None # défini si la fenêtre des projets est ouverte ou non
        self.actual_widget = None #défini le widget ouverte à un instant T
        self.actual_project = None # défini le projet ouverte
        self.widget_id = None # défini l'ID du widget de self.actual_widget
        self.app = None

        #on récupère la liste des polices d'écriture supportées par custom tkinter
        self.tk_family_path = interl.getRssPath("tk_family.txt")
        with open(self.tk_family_path, "r", encoding='utf8') as file :
            self.tk_family = file.readlines()
            for element in self.tk_family :
                element.replace("\n", "")
        file.close()

        #on récupère le dictionnaire de langue
        language_dict_path = interl.getRssPath("languageDict.json")
        with open(language_dict_path, 'r', encoding='utf8') as file :
            self.language_dict = json.load(file)
        file.close()

        self.setsinfo = self.fLoadFunct("getsetsinfo")
        self.widgetInfo = self.fLoadFunct("getWidInfo")


        self.getSettings()
        self.createInterface()
        if self.actual_widget != None :
            self.widgetParametersFrame(self.actual_widget)
        self.openProjectApp(reason = "new")

        #on initialise les raccourcis clavier
        self.bind("<Alt-p>", self.openParameters)
        self.bind("<Control-c>", self.copyCode)
        self.bind("<Control-p>", self.openPreview)
        self.bind("<Control-o>", self.openProjectApp)
        self.bind("<Control-a>", self.widgetAdding)
        self.bind("<Control-m>", self.modifyWid)
        self.bind("<Control-w>", self.delWid)


    #-------------------- fonctions de création de la fenêtres --------------------
        

    def createInterface(self) -> None:
        """createInterface
        Fonction de création du corps de l'interface
        """
        try :
            #-------------------- création des frames --------------------
            
            
            self.code_frame = ct.CTkFrame(self, width=self.width*(40/100), height=self.height, border_color = "#000000", border_width= 2)
            self.edit_frame = ct.CTkScrollableFrame(self, width=self.width*(40/100), height=self.height*(90/100))
            self.actionbtframe = ct.CTkFrame(self, height = self.height*(10/100), width = self.width*(60/100))
            self.main_item_frame = ct.CTkScrollableFrame(self, height = self.height*(85/100), width = self.width*(18/100), label_text = "widgets :")


            self.code_frame.grid(row =0, rowspan =2, column = 0, ipadx = 10, sticky = "N")
            self.edit_frame.grid(row = 0, column = 1, sticky = "e")
            
            self.main_item_frame.grid(row = 0, column = 2, sticky = "e")
            self.actionbtframe.grid(row = 1,column =1, columnspan = 2 )
            

            #-------------------- création du menu --------------------

            self.menubar = tk.Menu(self)
            self.config(menu=self.menubar)

            self.fichier = tk.Menu(self.menubar, tearoff = False)
            self.application = tk.Menu(self.menubar, tearoff = False)
            self.widget_menu = tk.Menu(self.menubar, tearoff = False)
            self.code_menu = tk.Menu(self.menubar, tearoff = False)
            
            self.fichier.add_command(label = self.language_dict["menufile1"][self.int_lang], command = lambda x = self.actual_project : self.openProjectApp(x))
            self.fichier.add_command(label = self.language_dict["menufile2"][self.int_lang], command = lambda x = "new" : self.openProjectApp(x))
            self.fichier.add_command(label = "Help", command = lambda : webbrowser.open("https://github.com/epsilonkn/Saturne-demonstration-app/wiki"))
            
            self.application.add_command(label= self.language_dict["menuapp1"][self.int_lang], command = lambda x = "all" : self.clear(x))
            self.application.add_command(label= self.language_dict["menuapp2"][self.int_lang], command = lambda : self.openParameters())
            self.application.add_command(label=self.language_dict["menuapp3"][self.int_lang], command = lambda : self.on_quit())

            self.widget_menu.add_command(label=self.language_dict["menuwid1"][self.int_lang], command = lambda : self.widgetAdding())
            self.widget_menu.add_command(label=self.language_dict["menuwid2"][self.int_lang], command = lambda : self.delWid())
            self.widget_menu.add_command(label=self.language_dict["menuwid3"][self.int_lang], command = lambda : self.modifyWid())
            

            self.code_menu.add_command(label=self.language_dict["menucode1"][self.int_lang], command = lambda : self.copyCode())
            self.code_menu.add_command(label=self.language_dict["menucode2"][self.int_lang], command = lambda : self.openPreview())


            self.menubar.add_cascade(label = self.language_dict["menufile"][self.int_lang], menu = self.fichier)
            self.menubar.add_cascade(label = self.language_dict["menuapp"][self.int_lang], menu = self.application)
            self.menubar.add_cascade(label = self.language_dict["menuwid"][self.int_lang], menu = self.widget_menu)
            self.menubar.add_cascade(label = self.language_dict["menucode"][self.int_lang], menu = self.code_menu)
            

            #-------------------- création des widgets et des boutons d'actions --------------------


            self.code_output = ct.CTkTextbox(self.code_frame, width=self.width*(35/100), height=self.height*(96/100)-20, activate_scrollbars=False)
            self.code_scrollbar = ct.CTkScrollbar(self.code_frame, command=self.code_output.yview, height=self.height*(96/100)-20)
            self.code_scrollbar.grid()
            self.code_output.configure(yscrollcommand=self.code_scrollbar.set)

            self.copy_bt = ct.CTkButton(self.code_frame, width= self.width*(10/100), height= self.height*(4/100),
                                        text = self.language_dict["menucode1"][self.int_lang], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, 
                                        command = lambda : self.copyCode())
            self.preview_bt = ct.CTkButton(self.code_frame, width= self.width*(10/100), height= self.height*(4/100),
                                        text = self.language_dict["menucode2"][self.int_lang], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, 
                                        command = lambda : self.openPreview())


            self.parameter_button = ct.CTkButton(self.actionbtframe, width= self.width*(10/100), height= self.height*(6/100),
                                                text = self.language_dict["menuapp2"][self.int_lang], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.openParameters())
            tl.CreateToolTip(self.parameter_button, text = "Bouton d'ouverture de la fenêtre de paramètres.") if self.showtooltip == "Oui" else None

            self.modify_button = ct.CTkButton(self.actionbtframe,  width= self.width*(10/100), height= self.height*(6/100),
                                                text = self.language_dict["menuwid3"][self.int_lang], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.modifyWid())
            tl.CreateToolTip(self.modify_button, text = "Bouton de modification des paramètres d'un widget.") if self.showtooltip == "Oui" else None
            self.modify_button.configure(state = "disabled") if self.actual_widget == None else None

            self.delete_button = ct.CTkButton(self.actionbtframe,  width= self.width*(10/100), height= self.height*(6/100),
                                                text = self.language_dict["menuwid2"][self.int_lang], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.delWid())
            tl.CreateToolTip(self.delete_button, text = "Bouton de suppression d'un widget.") if self.showtooltip == "Oui" else None
            self.delete_button.configure(state = "disabled") if self.actual_widget == None else None


            self.code_output.grid(column =0, row = 0, pady = 5, padx = 10, columnspan = 2)
            self.code_scrollbar.grid(column = 2, row = 0, padx = 10)

            self.copy_bt.grid(row = 1, column = 1, padx = 10, pady = 5)
            self.preview_bt.grid(row = 1, column = 0, padx = 10, pady = 5)
            
            self.delete_button.place(x = self.width*(5/200), y = self.height*(3/200))
            self.modify_button.place(x = self.width*(35/200), y = self.height*(3/200))
            self.parameter_button.place(x = self.width*(70/200), y = self.height*(3/200))

            self.sideWidgetsUptdating()   
            self.codeFrame() if self.actual_project != None else None
        except any as error :
            print(error)
            messagebox.showwarning("Une erreur est survenue", "Une erreur est survenue lors du chargement de la fenêtre principale")
            self.destroy()
            

    def configActionBt(self) -> None:
        """configActionBt 
        Fonction de modification de l'état des boutons de suppression et de sauvegarde des widgets 
        """
        self.modify_button.configure(state = "disabled") if self.actual_widget == None else self.modify_button.configure(state = "normal")
        self.delete_button.configure(state = "disabled") if self.actual_widget == None else self.delete_button.configure(state = "normal")


    def sideWidgetsUptdating(self) -> None:
        """sideWidgetsUptdating
        Fonction de création des boutons pour les widgets, sur le coté droit de la fenêtre
        """
        self.clear('itemFrame')
        
        self.add_button = ct.CTkButton(self.main_item_frame, width= self.width*(16/100), height= 40, text = self.language_dict["add_label"][self.int_lang],border_width= 2, border_color = "#FFFFFF",
                                       font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command= lambda : self.widgetAdding())
        tl.CreateToolTip(self.add_button, text = "Bouton d'ajout de widgets dans le projet.") if self.showtooltip == "Oui" else None
        self.add_button.configure(state = "disabled") if self.actual_project == None else None
        self.add_button.grid(padx = 5, pady = 5)
        for widgets in self.widgets_list :
            if widgets != "" :
                w_bt = ct.CTkButton(self.main_item_frame, text = widgets, width= self.width*(16/100), height= self.height*(6/100), 
                                    font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda w_id = widgets : self.widgetParametersFrame(w_id))
                w_bt.grid(padx = 5, pady = 5)
            else : pass


    def widgetParametersFrame(self, widget : str)  -> None:
        """widgetParametersFrame 
        Fonction de création de la frame de paramètres du widget

        Parameters
        ----------
        widget : str
            widget dont la fonction doit afficher les paramètres, et leurx valeurs respectives
        """
        if self.app != None :
            return
        self.clear("sets")
        self.actual_sets = []
        self.actual_widget = widget
        #on configue les boutons d'action pour les rendre actifs
        self.configActionBt()
        #on configure la disposition des paramètres selon la largeur de la fenêtre
        self.column_num = 1 if self.width*(30/100) < 490 else 3
        row = 2
        column = 0
        loading = True
        try :
            #on récupère les données du widget, les données associées à chaque paramètre, et les paramètre par défaut du widget
            self.actualwidset = self.fLoadFunct("getWidSet")
            self.widget_id = self.actualwidset[0]["ID"]
            widsets = self.widgetInfo[self.widget_id]
        except any as error :
            print(error)
            loading = False
            messagebox.showwarning("Fichier introuvable", "Une erreur est survenue lors du chargement des données.")

        if loading == True :
            try :
                #-------------------- création des entrées de modification des paramètres --------------------
                
                self.settings_frame = ct.CTkFrame(self.edit_frame)
                self.settings_frame.grid( row = 1, column = 0, sticky = 'w')

                #on crée le label titre, ainsi que l'entrée permettant de renseigner le nom du widget
                self.overal_lbl = ct.CTkLabel(self.edit_frame, text = self.actualwidset[0]["name"],font=ct.CTkFont(size=25, weight="bold"))

                self.widnamelbl = ct.CTkLabel(self.settings_frame, text = "Nom du widget :",font=ct.CTkFont(size=15, weight="bold"))
                self.widname = ct.CTkEntry(self.settings_frame, width= 150, height = 40,font=ct.CTkFont(weight="bold"))
                tl.CreateToolTip(self.widnamelbl, "Nom du widget, attention ce nom sera aussi utilisé comme nom de variable dans le code.") if self.showtooltip == "Oui" else None
                self.widname.insert(0, self.actualwidset[0]["name"])

                self.overal_lbl.grid(column = 0, row = 0 , pady = 15, sticky = 'w')
                self.widnamelbl.grid(row = 1, column = 0, columnspan = 2 if self.column_num == 3 else 1, 
                                     pady = 20, sticky = 'e')
                self.widname.grid(row = 1, column = 2 if self.column_num == 3 else 1, 
                                  columnspan = 2 if self.column_num == 3 else 1 , padx = 10, pady = 20)
                
                detail_dico = {"Simple" : (0,1), "Normal" : (1,2), "Complet" : (1,2,3)}
                
                #on crée le reste des paramètres, selon le type ( soit une entrée texte, un menu, un switch, ou un bouton)
                for parameter in widsets["parameters"]:
                    
                    if self.setsinfo[parameter][1] in detail_dico[self.detail_lvl] :
                        lbl = ct.CTkLabel(self.settings_frame, text = parameter + " :", font=ct.CTkFont(size=12, weight="bold"))
                        
                        if parameter in ["font", "hover", "image"]:
                            entry = ct.CTkSwitch(self.settings_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
                            entry.select() if self.actualwidset[0][parameter] == '1' else None
                            if parameter == "font" :
                                try : self.fontvar= ct.StringVar(value = self.actualwidset[0][parameter])
                                except : self.fontvar = ct.StringVar(value = "0")
                                entry.configure(command = lambda : self.showFontFrame(), variable = self.fontvar)

                        elif parameter in ("width", "height") :
                            entry = ct.CTkEntry(self.settings_frame, width = 100,font=ct.CTkFont(weight="bold"))
                            entry.insert(0, self.actualwidset[0][parameter] if self.actualwidset[0][parameter] != self.setsinfo[parameter][0] else "default")

                        elif parameter in ["state", "anchor", "compound", "justify"]:
                            entry = ct.CTkOptionMenu(self.settings_frame, values = self.setsinfo[parameter][3])  
                            entry.set(self.actualwidset[0][parameter])  

                        elif parameter == "text":
                            entry = ct.CTkButton(self.settings_frame, text = "Ajouter", command = lambda : self.openTextTopLevel(self.actualwidset[0]["text"]))
                            self.text = self.actualwidset[0]["text"]
                        
                        elif parameter == "values" :
                            entry = ct.CTkButton(self.settings_frame, text = "Ajouter", command = lambda : self.openValuesTopLevel(self.actualwidset[0]["values"]))
                            self.values = self.actualwidset[0]["values"]

                        elif parameter == "command" :
                            entry = ct.CTkButton(self.settings_frame, text = "Ajouter", command = lambda : self.openCommandTopLevel(self.actualwidset[0]["command"]), state = "disabled")
                            self.command = self.actualwidset[0]["command"]

                        elif parameter == "variable" :
                            entry = ct.CTkButton(self.settings_frame, text = "Ajouter", command = lambda : self.openVariableTopLevel(self.actualwidset[0]["varible"]), state = "disabled")
                            self.command = self.actualwidset[0]["variable"]
                        
                        else :
                            entry = ct.CTkEntry(self.settings_frame, width = 100,font=ct.CTkFont(weight="bold"))
                            entry.insert(0, self.actualwidset[0][parameter])
                        self.actual_sets.append((entry, parameter))
                        tl.CreateToolTip(lbl, self.setsinfo[parameter][2]) if self.showtooltip == "Oui" else None
                        
                        lbl.grid(row = row, column = column, padx = 5, pady = 10, sticky = 'n')
                        column = column + 1 if column < self.column_num else 0
                        row += 1 if column == 0 else 0
                        
                        entry.grid(row = row, column = column, padx = 5, pady = 10, sticky = 'n')
                        column = column + 1 if column < self.column_num else 0
                        row += 1 if column == 0 else 0

                self.layoutlbl = ct.CTkLabel(self.settings_frame, text = "affichage du widget : ", font=ct.CTkFont(size=15, weight="bold") )
                self.layout = ct.CTkSegmentedButton(self.settings_frame, font=ct.CTkFont(size=15, weight="bold"), values = ["pack", "grid"], 
                                                     command = self.showLayoutFrame)
                self.layout.set(self.actualwidset[0]["layout"]) if self.actualwidset[0]["layout"] != None else None
                self.layoutlbl.grid(row = row +1, column = 0)
                self.layout.grid(row = row+1, column = 1)

                try : self.showFontFrame() if self.fontvar.get() == "1" else None
                except : pass
                self.showLayoutFrame(self.layout.get()) if self.layout.get() != "" else None
            except any as error :
                print(error)
                messagebox.showwarning("Erreur de chargement", "Une erreur est survenue lors de l'affichage des données")


    def codeFrame(self):
        """codeFrame 
        Actualisation de la fenêtre de code
        """
        #on récupère le code
        self.txt_code = interl.getCodeReq(self.actual_project)
        #on renvoie un message d'erreur si le code n'a pas été récupéré
        if self.txt_code == None :
            messagebox.showerror("Erreur d'affichage", "Une erreur est survenue lors de l'affichage du code.")
            return
        self.code_output.delete("0.0", "end")
        self.code_output.insert("0.0", self.txt_code)


    def showFontFrame(self):
        """showFontFrame 
        Crée la boite "font" dans les paramètres du widget, 
        est appelée lorsque le paramètre font est activé
        """
        self.clear("fontframe")
        if self.fontvar.get() == "1" :

            self.font_frame = ct.CTkFrame(self.edit_frame, border_width = 3, border_color= '#FFFFFF')
            self.font_frame.grid(column = 0, row =2, pady = 30, sticky = "w", ipadx = self.width*(7/100))

            self.font_lbl = ct.CTkLabel(self.font_frame, text = "Font", font=ct.CTkFont(size=20, weight="bold"))
            self.font_lbl.grid(row = 0, column = 0, columnspan = 2, padx = 10)

            self.familylbl = ct.CTkLabel(self.font_frame , text = "Family : ", font=ct.CTkFont(size=15, weight="bold") )
            self.family = ct.CTkEntry(self.font_frame, width = 100,font=ct.CTkFont(weight="bold"))
            tl.CreateToolTip(self.familylbl,"Nom de la police") if self.showtooltip == "Oui" else None
            self.familylbl.grid(row = 1, column = 0, padx = 10, pady = 5)
            self.family.grid(row = 1, column = 1, padx = 10, pady = 5)

            self.fontsizelbl = ct.CTkLabel(self.font_frame , text = "Size : ", font=ct.CTkFont(size=15, weight="bold") )
            self.fontsize =ct.CTkEntry(self.font_frame, width = 100,font=ct.CTkFont(weight="bold"))
            tl.CreateToolTip(self.fontsizelbl,"Taille du texte") if self.showtooltip == "Oui" else None
            self.fontsizelbl.grid(row = 2, column = 0, padx = 10, pady = 5)
            self.fontsize.grid(row = 2, column = 1, padx = 10, pady = 5)

            self.fontweightlbl = ct.CTkLabel(self.font_frame , text = "Weight : ", font=ct.CTkFont(size=15, weight="bold") )
            self.fontweight = ct.CTkOptionMenu(self.font_frame, values = ["normal", "bold"])
            tl.CreateToolTip(self.fontweightlbl,"Mise en Gras du texte ( bold ), normal sinon") if self.showtooltip == "Oui" else None
            self.fontweightlbl.grid(row = 3, column = 0, padx = 10, pady = 5)
            self.fontweight.grid(row = 3, column = 1, padx = 10, pady = 5)

            self.slantlbl = ct.CTkLabel(self.font_frame , text = "Slant : ", font=ct.CTkFont(size=15, weight="bold") )
            self.slant = ct.CTkOptionMenu(self.font_frame, values = ["roman", "italic"])
            tl.CreateToolTip(self.slantlbl,"Mise en italique du texte ( italic), roman sinon") if self.showtooltip == "Oui" else None
            self.slantlbl.grid(row = 4, column = 0, padx = 10, pady = 5)
            self.slant.grid(row = 4, column = 1, padx = 10, pady = 5)

            self.underlinelbl = ct.CTkLabel(self.font_frame , text = "Underline : ", font=ct.CTkFont(size=15, weight="bold") )
            self.underline = ct.CTkSwitch(self.font_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
            tl.CreateToolTip(self.underlinelbl,"Soulignage du texte") if self.showtooltip == "Oui" else None
            self.underlinelbl.grid(row = 5, column = 0, padx = 10, pady = 5)
            self.underline.grid(row = 5, column = 1, padx = 10, pady = 5)
    
            self.overstrikelbl = ct.CTkLabel(self.font_frame , text = "Overstrike : ", font=ct.CTkFont(size=15, weight="bold") )
            self.overstrike = ct.CTkSwitch(self.font_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
            tl.CreateToolTip(self.overstrikelbl,"Raturage du texte") if self.showtooltip == "Oui" else None
            self.overstrikelbl.grid(row = 6, column = 0, padx = 10, pady = 5)
            self.overstrike.grid(row = 6, column = 1, padx = 10, pady = 5)

            for keys, values in self.actualwidset[1].items():
                match keys :
                    case "family" :
                        self.family.insert(0, values)
                    case "size" :
                        self.fontsize.insert(0, values)
                    case "weight" :
                        self.fontweight.set(values)
                    case "slant" :
                        self.slant.set(values)
                    case "underline" :
                        self.underline.toggle() if values == "1" else None
                    case "overstrike" :
                        self.overstrike.toggle() if values == "1" else None


    def showLayoutFrame(self, value : str) -> None:
        """showLayoutFrame 
        crée l'encadré pour les paramètre de layout

        Parameters
        ----------
        value : str
            prend pour valeur le type de layout choisit ( pack ou grid )
        """
        self.layout_list = []
        self.clear("layoutframe")
        self.layout_frame = ct.CTkFrame(self.edit_frame, border_width = 3, border_color= '#FFFFFF')
        self.layout_frame.grid(column = 0, row =3, pady = 30, sticky = "w", ipadx = self.width*(7/100))

        self.layoutlbl = ct.CTkLabel(self.layout_frame, text = value, font=ct.CTkFont(size=20, weight="bold"))
        self.layoutlbl.grid(row = 0, column = 0, columnspan = 2, padx = 10)
        
        self.ipadxlbl = ct.CTkLabel(self.layout_frame, text = "ipadx", font=ct.CTkFont(size=15, weight="bold"))
        self.ipadxlbl.grid(row = 1, column = 0, padx = 10, pady = 5)
        self.ipadx = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
        self.ipadx.grid(row = 1, column = 1, padx = 10, pady = 5)
        self.layout_list.append(["ipadx",self.ipadx, ""])

        self.ipadylbl = ct.CTkLabel(self.layout_frame, text = "ipady", font=ct.CTkFont(size=15, weight="bold"))
        self.ipadylbl.grid(row = 2, column = 0, padx = 10, pady = 5)
        self.ipady = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
        self.ipady.grid(row = 2, column = 1, padx = 10, pady = 5)
        self.layout_list.append(["ipady",self.ipady, ""])

        self.padxlbl = ct.CTkLabel(self.layout_frame, text = "padx", font=ct.CTkFont(size=15, weight="bold"))
        self.padxlbl.grid(row = 3, column = 0, padx = 10, pady = 5)
        self.padx = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
        self.padx.grid(row = 3, column = 1, padx = 10, pady = 5)
        self.layout_list.append(["padx",self.padx, ""])

        self.padylbl = ct.CTkLabel(self.layout_frame, text = "pady", font=ct.CTkFont(size=15, weight="bold"))
        self.padylbl.grid(row = 4, column = 0, padx = 10, pady = 5)
        self.pady = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
        self.pady.grid(row = 4, column = 1, padx = 10, pady = 5)
        self.layout_list.append(["pady", self.pady, ""])

        if value == "grid" :

            self.columnlbl = ct.CTkLabel(self.layout_frame, text = "column", font=ct.CTkFont(size=15, weight="bold"))
            self.columnlbl.grid(row = 5, column = 0, padx = 10, pady = 5)
            self.column = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.column.grid(row = 5, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["column", self.column, ""])

            self.columnspanlbl = ct.CTkLabel(self.layout_frame, text = "columnspan", font=ct.CTkFont(size=15, weight="bold"))
            self.columnspanlbl.grid(row = 6, column = 0, padx = 10, pady = 5)
            self.columnspan= ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.columnspan.grid(row = 6, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["columnspan", self.columnspan, ""])

            self.rowlbl = ct.CTkLabel(self.layout_frame, text = "row", font=ct.CTkFont(size=15, weight="bold"))
            self.rowlbl.grid(row = 7, column = 0, padx = 10, pady = 5)
            self.row = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.row.grid(row = 7, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["row", self.row, ""])

            self.rowspanlbl = ct.CTkLabel(self.layout_frame, text = "rowspan", font=ct.CTkFont(size=15, weight="bold"))
            self.rowspanlbl.grid(row = 8, column = 0, padx = 10, pady = 5)
            self.rowspan = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.rowspan.grid(row = 8, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["rowspan", self.rowspan, ""])

            self.stickylbl = ct.CTkLabel(self.layout_frame, text = "sticky", font=ct.CTkFont(size=15, weight="bold"))
            self.stickylbl.grid(row = 9, column = 0, padx = 10, pady = 5)
            self.sticky = ct.CTkOptionMenu(self.layout_frame, values = ['W', "N", 'S', 'E'])
            self.sticky.grid(row = 9, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["sticky", self.sticky, "E"])

        elif value == "pack" :
            
            self.afterlbl = ct.CTkLabel(self.layout_frame, text = "after", font=ct.CTkFont(size=15, weight="bold"))
            self.afterlbl.grid(row = 5, column = 0, padx = 10, pady = 5)
            self.afterentry = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.afterentry.grid(row = 5, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["after", self.afterentry, ""])

            self.anchorlbl = ct.CTkLabel(self.layout_frame, text = "anchor", font=ct.CTkFont(size=15, weight="bold"))
            self.anchorlbl.grid(row = 6, column = 0, padx = 10, pady = 5)
            self.anchorentry = ct.CTkOptionMenu(self.layout_frame, values = ['W', "N", 'S', 'E'])
            self.anchorentry.grid(row = 6, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["anchor", self.anchorentry, 'W'])

            self.beforelbl = ct.CTkLabel(self.layout_frame, text = "before", font=ct.CTkFont(size=15, weight="bold"))
            self.beforelbl.grid(row = 7, column = 0, padx = 10, pady = 5)
            self.before = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.before.grid(row = 7, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["before", self.before, ""])

            self.expandlbl = ct.CTkLabel(self.layout_frame, text = "expand", font=ct.CTkFont(size=15, weight="bold"))
            self.expandlbl.grid(row = 8, column = 0, padx = 10, pady = 5)
            self.expand = ct.CTkSwitch(self.layout_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
            self.expand.grid(row = 8, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["expand", self.expand, "0"])

            self.filllbl = ct.CTkLabel(self.layout_frame, text = "fill", font=ct.CTkFont(size=15, weight="bold"))
            self.filllbl.grid(row = 9, column = 0, padx = 10, pady = 5)
            self.fill= ct.CTkOptionMenu(self.layout_frame, values = ["None", 'X', 'Y', 'BOTH'])
            self.fill.grid(row = 9, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["fill", self.fill, "None"])

            self.sidelbl = ct.CTkLabel(self.layout_frame, text = "side", font=ct.CTkFont(size=15, weight="bold"))
            self.sidelbl.grid(row = 10, column = 0, padx = 10, pady = 5)
            self.side= ct.CTkOptionMenu(self.layout_frame, values = ["TOP", "BOTTOM", "LEFT", "RIGHT"])
            self.side.grid(row = 10, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["side", self.side, "TOP"])


        for element in self.layout_list :
            if element[0] in self.actualwidset[2].keys() :
                if element[0] == "expand" :
                    element[1].toggle() if self.actualwidset[2][element[0]] == "1" else None
                elif element[0] in ("side", "fill", "sticky", "anchor"):
                    element[1].set(self.actualwidset[2][element[0]])
                else :
                    element[1].insert(0, self.actualwidset[2][element[0]])


    #-------------------- fonctions de gestions des évènements --------------------
                 

    def clear(self, mod : str) -> None:
        """clear 
        Fonction de destruction de widgets

        Parameters
        ----------
        mod : str
            défini les widgets à détruire :
            -all : détruit tous les widgets de l'interface ( frames comprises )
            -itemFrame : détruit les boutons associés aux widgets
            -sets : détruit les labels et entrées de paramètres d'un widget
            -fontframe : détruit la frame des paramètres de font
            -layoutframe : détruit la frame contenant les paramètres de layout du widget
        """
        try :
            if mod == 'all' :
                liste = self.grid_slaves() + self.pack_slaves()
                for element in liste :
                    element.destroy()
                self.createInterface()
                if self.actual_widget != None :
                    self.widgetParametersFrame(self.actual_widget)
                self.sideWidgetsUptdating()
            if mod == 'itemFrame' :
                liste = self.main_item_frame.grid_slaves()
                for element in liste :
                    element.destroy()
            if mod == 'sets':
                liste = self.edit_frame.grid_slaves()
                for element in liste :
                    element.destroy()
            if mod == 'fontframe' :
                try : 
                    liste = self.font_frame.grid_slaves()
                    for element in liste :
                        element.destroy()
                    self.font_frame.destroy()
                except :
                    pass
            if mod == 'layoutframe' :
                try : 
                    liste = self.layout_frame.grid_slaves()
                    for element in liste :
                        element.destroy()
                    self.layout_frame.destroy()
                    self.layout_list = []
                except :
                    pass
        except any as error :
            print(error)
            loading = False
            messagebox.showwarning("Une erreur est survenue", "Une erreur est survenue lors de l'actualisation de la fenêtre")



    def fLoadFunct(self, event : str, *dico : dict) -> Union[None, dict]:
        """fLoadFunct 
        Fonction d'envoi de requêtes de chargement/envoi de données

        Parameters
        ----------
        event : str
            décrit l'action à réaliser :
            -widnamelist : récupère la liste des widgets du projet, et actualise la frame des widget
            -getWidSet : récupère les données d'un widget ciblé            ( fichier "[nom du projet]\\[nom du widget].json")
            -modifyWidSet : modifie les données d'un widget ciblé          ( fichier "[nom du projet]\\[nom du widget].json")
            -getsetsinfo : récupère les données des paramètres des widgets ( fichier "widParaInfo.json")
            -getWidInfo : récupères les données de base du widget ciblé    ( fichier "widgetInfo.json")
        Returns
        -------
        Union[None, dict]
            renvoie None dans la plupart des cas, 
            renvoie un dictionnaire si l'appel est lié à l'obtention des données d'un widget
        """
        if event == "widnamelist" :
            self.widgets_list = interl.getWidNameListReq(self.actual_project)
            self.sideWidgetsUptdating()
        if event == "getWidSet" :
            return interl.getWidSetReq(self.actual_widget, self.actual_project)
        if event == 'modifyWidSet' :
            interl.modifyWidSetReq(self.widget_id, self.actual_widget, dico[0], self.actual_project)
        if event == "getsetsinfo" :
            return interl.getSetsInfoRqst()
        if event == "getWidInfo" :
            return interl.getMainWidSetsRqst()


    def modifyWid(self, event = None) -> None:
        """modifyWid 
        Fonction de modification des paramètres d'un widget,
        appele la fonction de chargement/envoi de données (fLoadFunct)
        """
        if self.actual_widget != None :
            layout_dico = {}
            font_dico = {}
            dico = {}
            dico['ID'] = self.widget_id

            #vérification du layout et ajout dans le dictionnaire correspondant
            if self.layout.get() != "" :
                dico["layout"] = self.layout.get()
                for element in self.layout_list :
                    if element[1].get() != element[2] :
                        if element[0] in ("column", "columnspan", "row", "rowspan") or (element[0] in ("ipadx", "ipady", "padx", "pady") and element[1].get() != "0") :
                            try :
                                layout_dico[element[0]] = int(element[1].get())
                            except :
                                messagebox.showerror("Erreur d'entrée", "Un mauvais nombre a été entré comme paramètre dans le layout")
                        else : 
                            layout_dico[element[0]] = element[1].get()
            else :
                messagebox.showerror("Erreur d'entrée", "Aucune méthode de layout sélectionné")
                return 0
            #on vérifie que le nom de widget donné respecte les règles de typage pour une variable
            if interl.tryWN(self.widname.get()) == True :
                dico["name"] = self.widname.get() 
            else :
                messagebox.showerror("Erreur d'entrée", "Le nom du widget est invalide.")
                dico["name"] = self.actual_widget
                #on supprime le nom invalide dans l'entrée associée et le remplace par le précédent nom
                self.widname.delete()
                self.widname.insert(0, self.actual_widget)
            
            for element in self.actual_sets :
                
                if element[1] in ["width", "height"] :
                    if element[0].get() != "default" :
                        dico[element[1]] = int(element[0].get())
                
                #on s'occupe des paramètres de font
                elif element[1] == "font" :
                    dico[element[1]] = element[0].get()
                    if dico[element[1]] == "1" :
                        
                        if self.family.get() != "" :
                            family = interl.tryFont(self.family.get(), self.tk_family)
                            if family == False :
                                messagebox.showerror("Erreur d'entrée", "Mauvaise police d'écriture entrée,\nconsultez la console pour voir la liste des polices tolérées.")
                                print("mauvaise police d'écriture entrée, liste des police tolérées :\n", self.tk_family_path)
                                return 0
                            else :
                                font_dico["family"] = family
                        
                        if self.fontsize.get() != "" :
                            try :
                                font_dico["size"] = int(self.fontsize.get())
                            except :
                                messagebox.showerror("Erreur d'entrée", "Mauvaise taille de caractère entrée.")
                                return 0
                        
                        if self.fontweight.get() != "normal" :
                            font_dico["weight"] = self.fontweight.get()
                        
                        if self.slant.get() != "roman" :
                            font_dico["slant"] = self.slant.get()
                        
                        if self.underline.get() != '0' :
                            font_dico["underline"] = "True"
                        
                        if self.overstrike.get() != '0' :
                            font_dico["overstrike"] = "True"
                        #si aucun paramètre de font n'est utilisé, on met le paramètre font par défaut
                        if len(font_dico) == 0 :
                            dico[element[1]] = '0'
                
                elif element[1] == "hover" :
                    if element[0].get() == "0" : dico[element[1]] = "False"
                    else : dico[element[1]] = "True"

                elif element[1] == "text":
                    text = self.text.replace("\'", "\\\'").replace("\"", "\\\"")
                    dico[element[1]] = text

                elif element[1] == "values":
                    dico[element[1]] = self.values

                elif element[1] == "command" :
                    dico[element[1]] = self.command

                elif element[1] == "variable" :
                    dico[element[1]] = self.variable
                elif element[1] == "master" :
                    if element[0].get() != "window" :
                        if element in self.widgets_list :
                            dico[element[1]] = element[0].get()
                        else : 
                            messagebox.showerror("Erreur d'entrée", "Le widget parent sélectionné n'existe pas")
                            return
                    else : 
                        dico[element[1]] = "window"
                else : 
                    dico[element[1]] = element[0].get()
            
            self.fLoadFunct("modifyWidSet", [dico, font_dico, layout_dico])
            self.fLoadFunct("widnamelist")
            self.overal_lbl.configure(text = dico["name"])
            self.actual_widget = dico["name"]
            self.codeFrame()
        else : 
            messagebox.showinfo("Utilisation impossible", "Modification impossible, aucun widget n'est ouvert.")


    def getSettings(self) -> None:
        """getSettings 
        Fonction de récupération des paramètres de l'application,
        attribue les paramètres chargé aux variable de l'application
        """
        try :
            with open("rssDir\\wdSettings.json", "r") as file :
                self.parameters = json.load(file)
            file.close()
            if self.parameters["fullscreen"]: 
                self.width   = self.winfo_screenwidth() -10
                self.height  = self.winfo_screenheight() -10
                self.attributes('-fullscreen', True)
            else : 
                self.attributes('-fullscreen', False)
                self.width   = self.parameters["width"]
                self.height  = self.parameters["height"]
            self.showtooltip = self.parameters["tooltip"]
            self.detail_lvl  = self.parameters["detail"]
            self.int_lang    = self.parameters["int_language"]

            ct.set_default_color_theme(self.parameters["color"])
            ct.set_appearance_mode(self.parameters["theme"])
            
            self.title("Saturne")
            self.geometry("500x300")
            self.minsize(self.width, self.height)
        except any as error :
            print(error)
            messagebox.showwarning("Erreur de chargement", "Une erreur est survenue lors du chargement des paramètres,\nveuillez vérifier leur validité")
        

    def resetAttr(self) -> None:
        """resetAttr 
        Fonction de réinitialisation de certaines variables de l'application,
        utilisé lorsque l'application est lancé sans projet ouvert
        """
        if self.actual_project == None :
            self.widgets_list = []
            self.actual_widget = None


    def delWid(self, event = None) -> None:
        """delWid 
        Fonction de suppression d'un widget.
        """
        if self.app != None :
            return
        if self.actual_widget != None :
            interl.delWidReq(self.actual_widget,self.widget_id, self.actual_project)
            self.fLoadFunct('widnamelist')
            self.clear("sets")
            self.actual_sets = []
            self.actual_widget = None
            self.widget_id = None
            self.configActionBt()
            self.codeFrame()
        else :
            print("aucun widget selectionné")

    
    def on_quit(self) -> None:
        """on_quit 
        Détruit la fenêtre lorsque le bouton "Quitter" du menu est pressé
        """
        self.destroy()


    def copyCode(self, event = None):
        """copyCode 
        Fonction de copie du code créé

        Parameters
        ----------
        event : any
            paramètre présent si la fonction est appelée via le raccouri clavier
        """
        code = self.code_output.get("0.0", "end")
        code += "\n\nwindow.mainloop()"
        self.clipboard_clear()
        self.clipboard_append(code)


    def openPreview(self, event = None):
        """openPreview 
        Fonction d'ouverture de la fenêtre de preview

        Parameters
        ----------
        event : any
            paramètre présent si la fonction est appelée via le raccouri clavier
        """
        document = interl.getProjectPath(self.actual_project) + "\\code.py"
        with open(document,"r")as file:
            code = file.read()
            code = code + "\nwindow.mainloop()"
            exec(code)
        

    def openTextTopLevel(self, text):
        """openTextTopLevel 
        Fonction d'ouverture de la fenêtre d'ajout d'un texte pour les widget en comportant un

        Parameters
        ----------
        text : str
            texte actuellement entré dans le widget
        """
        if self.app != None :
            return
        self.app = TextTopLevelWin(text = text)
        self.app.grab_set()
        self.text = self.actualwidset[0]["text"] = self.app.contentGet()
        self.app = None


    def openValuesTopLevel(self, values):
        """openValuesTopLevel 
        Fonction d'ouverture de la fenêtre d'ajout de valeur pour les menus déroulant

        Parameters
        ----------
        values : list
            liste contenant les valeurs actuelles du manu déroulant
        """
        if self.app != None :
            return
        self.app = ValuesTopLevelWin(values = values) if type(values) == list else ValuesTopLevelWin()
        self.app.grab_set()
        self.values = self.actualwidset[0]["values"] = self.app.contentGet()
        self.app = None


    def openCommandTopLevel(self, command):
        """openCommandTopLevel 
        Fonction d'ouverture de la fenêtre d'ajout de commande

        Parameters
        ----------
        command : str
            commande actuellement ajoutée
        """
        if self.app != None :
            return
        self.app = CommandTopLevelWin(command = command)
        self.app.grab_set()
        self.command = self.actualwidset[0]["command"] = self.app.contentGet()
        self.app = None


    def openVariableTopLevel(self, variable):
        """openVariableTopLevel 
        Fonction d'ouverture de la fenêtre d'ajout d'une variable

        Parameters
        ----------
        variable : str
            variable actuellement ajoutée
        """
        if self.app != None :
            return
        self.app = VariableTopLevelWin(variable = variable)
        self.app.grab_set()
        self.variable = self.actualwidset[0]["variable"] = self.app.contentGet()
        self.app = None


#-------------------- fonctions de création de fenêtres enfant --------------------
    

    def openProjectApp(self, reason) -> None:
        """openProjectApp 
        Fonction d'ouverture de la fenêtre de projets,
        modifie le nom
        de l'application si un projet est ouvert
        """
        if self.project_app != None :
            return
        if reason != "new" :
            reason = self.actual_project
        self.project_app = ProjectApp(reason, self.int_lang, self.language_dict)
        self.project_app.grab_set()
        self.actual_project = self.project_app.closed()
        self.project_app = None
        if self.actual_project != None :
            self.title(f"Saturne : {self.actual_project}")
            self.fLoadFunct(event = "widnamelist")
        else :
            self.title("Saturne")
            self.resetAttr()
        self.clear('all')


    def openParameters(self, event = None) -> None:
        """openParameters 
        Fonction d'ouverture des paramètres, 
        appele la fonction "getSettings" à l'issue
        """
        if self.settings != None :
            return 
        self.settings = AppEditing(self.parameters, self.int_lang, self.language_dict)
        self.settings.grab_set()
        self.parameters = self.settings.get()
        self.settings = None
        self.getSettings()
        self.clear('all')


    def widgetAdding(self, event = None) -> None:
        """widgetAdding 
        Fonction d'ouverture de la fenêtre d'ajout de Widgets
        """
        if self.widgetapp == None :
            self.widgetapp = WidgetApp()
            self.widgetapp.grab_set()
            newwidget = self.widgetapp.get()
            if newwidget != None :
                newwidget = interl.createWidSetFileReq(newwidget, self.actual_project)
                self.widgets_list.append(newwidget)
            self.widgetapp = None
            self.sideWidgetsUptdating()
        else :
            print("fenêtre d'ajout d'un widget déjà ouverte")


if __name__ == "__main__":
    app = interface()
    app.mainloop()
