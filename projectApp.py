from typing import Optional, Tuple, Union
import customtkinter as ct
from tkinter import messagebox
import json
import intermediateLayer as interl
import tool_tip as tl

class ProjectApp(ct.CTkToplevel):

    def __init__(self, reason : str, language : int, language_dict : dict ):
        super().__init__()

        self.newprojectname = None
        settings = self.openWinSets()
        self.tooltip = settings["tooltip"]

        self.language = language
        self.language_dict = language_dict

        self.char_weight = 'normal' if self.language == 2 else "bold"

        self.main_frame = ct.CTkFrame(self)
        self.side_frame = ct.CTkScrollableFrame(self.main_frame, height = 300, width = 180)
        self.work_frame = ct.CTkFrame(self.main_frame, height = 300, width=600)

        self.main_frame.grid()
        self.side_frame.grid(row = 0, column =0)
        self.work_frame.grid(row =0, column = 1)
        self.actual_prjt = None
        if reason == "new" :
            self.sideFrameUpdating()
            self.workFrameCreation()
        else :
            self.sideFrameUpdating()
            self.modifyFrame(reason) if reason != None else self.workFrameCreation()
        
        self.bind("<Control-a>", self.workFrameCreation)


    def workFrameCreation(self, event = None):
        self.clear("workFrame")
        
        self.project_label = ct.CTkLabel(self.work_frame, text = self.language_dict["project_label"][self.language], width=600)
        self.entry = ct.CTkEntry(self.work_frame, width=200)
        self.content_valid_bt = ct.CTkButton(self.work_frame, text = self.language_dict["content_valid_bt"][self.language], height = 30, width=200, command = lambda : self.addProject())

        self.project_label.grid(row = 0, column = 0, pady = 15)
        self.entry.grid(row = 1, column = 0, pady = 15)
        self.content_valid_bt.grid(row =2, column = 0, pady = 15)


    def modifyFrame(self, project):
        self.clear("workFrame")

        self.actual_prjt = project 
        dico = self.loadPrjctInfo()


        #-------------------- création des frames -------------------- 


        self.upper_frame = ct.CTkFrame(self.work_frame, corner_radius=0)
        self.lower_frame = ct.CTkFrame(self.work_frame, corner_radius=0)

        self.upper_frame.grid(row = 0, column = 0)
        self.lower_frame.grid(row =1, column = 0)


        #-------------------- création des labels -------------------- 

        self.prjt_name_lbl = ct.CTkLabel(self.upper_frame, text = self.language_dict["prjt_name_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.prjt_name_lbl , "Nom du projet") if self.tooltip == "Oui" else None
        self.win_name_lbl = ct.CTkLabel(self.upper_frame, text = self.language_dict["win_name_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.win_name_lbl , "Nom de la fenêtre") if self.tooltip == "Oui" else None
        self.win_height_lbl = ct.CTkLabel(self.upper_frame, text = self.language_dict["win_height_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.win_height_lbl , "Hauteur de la fenêtre,\n200 par défaut") if self.tooltip == "Oui" else None
        self.win_width_lbl = ct.CTkLabel(self.upper_frame, text = self.language_dict["win_width_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.win_width_lbl , "Largeur de la fenêtre,\n200 par défaut.") if self.tooltip == "Oui" else None

        self.prjt_name_lbl.grid(row = 0, column =0, padx = 10, pady = 10)
        self.win_name_lbl.grid(row = 1, column =0, padx = 10, pady = 10)
        self.win_height_lbl.grid(row = 0, column =2, padx = 5, pady = 10)
        self.win_width_lbl.grid(row = 1, column =2, padx = 5, pady = 10)


        #-------------------- création des entrées -------------------- 


        self.prjt_name = ct.CTkEntry(self.upper_frame, width = 100)
        self.prjt_name.insert(0, self.actual_prjt)

        self.win_name = ct.CTkEntry(self.upper_frame, width = 100)
        self.win_name.insert(0, dico['WinName'] if dico != None else "")

        self.win_height = ct.CTkEntry(self.upper_frame, width=90)
        self.win_height.insert(0, dico["height"] if dico != None else "")

        self.win_width = ct.CTkEntry(self.upper_frame, width=90)
        self.win_width.insert(0, dico["width"] if dico != None else "")


        self.prjt_name.grid(row = 0, column = 1)
        self.win_name.grid(row = 1, column = 1)
        self.win_height.grid(row = 0, column =3, padx = 5)
        self.win_width.grid(row = 1, column =3, padx = 5, pady = 10)


        #-------------------- création des boutons -------------------- 


        self.del_bt = ct.CTkButton(self.lower_frame, text = self.language_dict["menuwid2"][self.language], height = 30, width=130, command = lambda : self.delProject(project))
        self.modify_bt = ct.CTkButton(self.lower_frame, text = self.language_dict["menuwid3"][self.language], height = 30, width=130, command = lambda :self.modifyInfo())
        self.open_bt = ct.CTkButton(self.lower_frame, text = self.language_dict["open_bt"][self.language], height = 30, width=130, command = lambda : self.destroy())

        self.del_bt.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.modify_bt.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.open_bt.grid(row = 0, column = 2, padx = 10, pady = 10)


        self.work_frame.configure(bg_color = self.upper_frame.cget("bg_color"))



    def loadPrjctInfo(self):
        dico =  interl.getPrjtSetRqst(self.actual_prjt)
        return dico
            

    def modifyInfo(self):
        modify = True
        try : 
            name = self.win_name.get()
        except :
            modify = False
            messagebox.showerror("Mauvais titre de fenêtre.", "Mauvais Titre de fenêtre entré.")
        try : 
            height = self.win_height.get()
            height.replace(" ", "")
            height = int(height) if height != "" else ""
        except :
            modify = False

            messagebox.showerror("Hauteur invalide.", "Hauteur entrée invalide.")
        try : 
            width = self.win_width.get()
            width.replace(" ", "")
            width = int(width) if width != "" else ""
        except :
            modify = False
            messagebox.showerror("Largeur invalide.", "Largeur entrée invalide.")
        try : 
            newname = self.prjt_name.get()
        except :
            modify = False
            messagebox.showerror("Nom de projet invalide.", "Nouveau nom de projet entré invalide.")

        if modify == True :
            dico = {}
            dico["PrjtName"]    = newname
            dico["WinName"]     = name
            dico["height"]      = height
            dico["width"]       = width
            if newname != self.actual_prjt :
                rename = interl.renameDirReq(self.actual_prjt, newname)
                if rename == False :
                    messagebox.showerror("Erreur de sauvergade.", "Une erreur est survenue lors du renommage du projet.")
                    return 0
                else :
                    self.project_info.insert(self.project_info.index(self.actual_prjt), newname)
                    del self.project_info[self.project_info.index(self.actual_prjt)]
                    converted_info = ",".join(self.project_info)
                    with open("rssDir\prjctNameSave.txt", "w", encoding= 'utf8') as file :
                        file.write(converted_info)
                    file.close()
                    self.actual_prjt = newname
                    self.clear("sideFrame")
                    self.sideFrameUpdating()
            interl.modidyPrjctRqst(self.actual_prjt, dico)


    
    def openProjectInfo(self):
        with open("rssDir\prjctNameSave.txt", "r", encoding= 'utf8') as file :
            self.project_info = file.read().split(",")
        file.close()


    def sideFrameUpdating(self):
        self.openProjectInfo()
        self.clear("sideFrame")
        self.add_button = ct.CTkButton(self.side_frame, text = self.language_dict["add_project_label"][self.language], width = 160, height = 30, command = lambda : self.workFrameCreation())
        self.add_button.grid(padx = 10, pady = 5)

        for projects in self.project_info:
            if projects != "":
                bt = ct.CTkButton(self.side_frame, text = projects, width = 160, height = 30, command = lambda projects = projects : self.modifyFrame(projects))
                bt.grid(padx = 10, pady = 5)


    def addProject(self, event = None):
        self.newprojectname = self.entry.get()
        self.project_info.append(self.newprojectname)
        converted_info = ",".join(self.project_info)

        
        with open("rssDir\prjctNameSave.txt", "w", encoding= 'utf8') as file :
            file.write(converted_info)
        file.close()
        
        if self.newprojectname != None and type(self.newprojectname) == str :
            interl.newPrjctRqst(self.newprojectname)
        
        self.clear("sideFrame")
        self.clear("workFrame")
        self.sideFrameUpdating()
        self.modifyFrame(self.newprojectname)


    def delProject(self, project):
        try : 
            if type(project) == str :
                interl.rmproject(project)
            del self.project_info[self.project_info.index(project)]
            converted_info = ",".join(self.project_info)
            with open("rssDir\prjctNameSave.txt", "w", encoding= 'utf8') as file :
                file.write(converted_info)
            file.close()
            
            self.clear("workFrame")
            self.clear("sideFrame")
            self.sideFrameUpdating()
        except :
            messagebox.showerror("Suppression impossible", "Une erreur est survenue lors de la suppresion du projet.")


    def openWinSets(self) :
        with open("rssDir\wdSettings.json", "r", encoding= 'utf8') as file :
            return json.load(file)

    def clear(self, choice):
        if choice == "sideFrame":
            liste = self.side_frame.grid_slaves()
        if choice =='workFrame':
            liste = self.work_frame.grid_slaves()
        for widgets in liste :
            widgets.destroy()
    

    def closed(self):
        self.master.wait_window(self)  
        return self.actual_prjt
