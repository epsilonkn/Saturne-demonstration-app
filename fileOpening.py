#programme d'ouvertures des dossiers
from typing import *
import os
import json


#-------------------------- Fonctions de gestion des fichiers --------------------------

def dirCreation(name : str) -> None:
    """dirCreation 
    fonction de création du dossier associé à un projet, et des fichiers enfants

    Parameters
    ----------
    name : str
        nom du projet, servant de nom au dossier
    """
    path = os.getcwd() +"\\"+ name
    try :
        os.mkdir(path)
        with open(path +"\\"+ 'prjtset.json', "w") as file :
            pass
        with open(path +"\\"+ 'code.py', "w") as file :
            file.write("import customtkinter\n\nwindow = customtkinter.CTk()\n\n")
        with open(path +"\\"+ 'widNmeList.txt', "w") as file :
            pass
    except OSError as error :
        print("error raised : ", error)


def renameDir(oldname : str, newname : str ) -> bool :
    """renameDir 
    change le nom d'un dossier de projet

    Parameters
    ----------
    oldname : str
        ancien nom du projet
    newname : str
        nouveau nom du projet

    Returns
    -------
    bool
        renvoie True si le renommage est réussi, false sinon
    """
    try :
        os.rename(os.path.join(os.getcwd(), oldname), os.path.join(os.getcwd(), newname))
        return True
    except any as error :
        print(error)
        return False


def rmDirectory(name : str) -> None:
    """rmDirectory 
    fonction de suppression d'un dossier
    supprime d'abord tous les fichiers enfants

    Parameters
    ----------
    name : str
        nom du dossier à supprimer
    """
    path =  os.getcwd() +"\\"+ name
    rmFiles(path)
    os.rmdir(path)


def emptyDir(path : str) -> bool:
    """emptyDir 
    vérifie si un dossier est vide

    Parameters
    ----------
    path : str
        chement d'accès du dossier ciblé

    Returns
    -------
    bool
        renvoie True si le dossier est vide, False sinon
    """
    if os.path.exists(path) :
        return True if os.listdir(path) == [] else False


def verifyDir(path : str) -> bool:
    """verifyDir 
    vérifie que les fichiers enfants inhérents au dossier ciblé sont présent

    Parameters
    ----------
    path : str
        Chemin d'accès du dossier à vérifier

    Returns
    -------
    bool
        return True si tous les fichiers sont présent, sinon, appele la fonction "addFiletoDir" puis renvoie True
    """
    if os.path.exists(path) :
        files = os.listdir(path)
        if "code.py" in files and "prjtset.json" in files and "widNmeList.txt" in files :
            return True
        else :
            addFiletoDir(path)
            return True


def addFiletoDir(path : str) -> None:
    """addFiletoDir 
    Fonction d'ajout des fichiers de base à un dossier si ils sont manquant

    Parameters
    ----------
    path : str
        Chemin d'accès au dossier
    """
    files = os.listdir(path)
    if "code.py" not in files :
        with open(path +"\\"+  'code.py', "w") as file :
            pass
    if "prjtset.json" not in files :
        with open(path +"\\"+ 'prjtset.json', "w") as file :
            pass
    if "widNmeList.txt" not in files :
        with open(path +"\\"+ 'widNmeList.txt', "w") as file :
            pass


def rmFiles(path : str) -> None:
    """rmFiles 
    Fonction de suppression des fichiers présent dans le dossier pointé

    Parameters
    ----------
    path : str
        Chemin d'accès à un dossier
    """
    files_list = os.listdir(path)
    for files in files_list :
        try: 
            os.remove(path + "\\" + files)
        except : 
            os.rmdir()


def rmFile(path : str) -> None:
    """rmFile 
    Fonction de suppression d'un fichier

    Parameters
    ----------
    path : str
        Chemin d'accès du fichier à supprimer
    """
    os.remove(path)


def createPath(target : str) -> str:
    """createPath 
    Crée un chemin d'accès à partir du chemin absolu du programme et du nom du fichier ou du dossier cible

    Parameters
    ----------
    target : str
        Fichier ou dossier ciblé

    Returns
    -------
    str
        Retourne le chemin d'accès de la cible
    """
    return os.path.join(os.getcwd(), target)


#-------------------------- Fonctions de gestion des fichiers des projets --------------------------


def mPS(path : str, info : dict) -> None:
    """mPS : modify Project Settings 
    Ecrase les précédents paramètres du projet ciblé par les nouveaux

    Parameters
    ----------
    path : str
        Fichier ciblé
    info : dict
        Dictionnaire des paramètres
    """
    with open(path, "w", encoding= 'utf8') as file :
        json.dump(info, file)


#-------------------------- Fonctions de gestion des fichiers des widgets --------------------------


def rmWid(widget : str, project : str) -> None : 
    """rmWid : remove Widget
    Fonction de suppression d'un widget

    Parameters
    ----------
    widget : str
        Widget à supprimer
    project : str
        Projet parent du widget
    """
    path = createPath(project)
    os.remove(path + "\\" + widget + ".json")
    with open(path + "\\widNmeList.txt", 'r', encoding= 'utf8') as file :
        data = file.read().split(",")
        del data[data.index(widget)]
        data = ",".join(data)
    with open(path + "\\widNmeList.txt", 'w', encoding= 'utf8') as file :
        file.write(data)     


def cWSF(path : str, name : str, settings : dict) -> None:
    """cWSF : create Widget Settings File
    Crée le fichier correspondant au widget créé par l'utilisateur,
    modifie la liste des widgets dans le fichier "widNmeList.txt"

    Parameters
    ----------
    path : str
        Chemin d'accès au fichier du widget
    name : str
        nom du widget
    settings : dict
        Dictionnaire des paramètres du widget
    """
    with open(path + "\\" + name + ".json", "w", encoding= 'utf8') as file :
        json.dump(settings, file)
    with open(path + "\\widNmeList.txt", 'a', encoding= 'utf8') as file :
        file.write("," + name)
    

def mWS(path : str, newname : str, oldname : str, settings : dict) -> None :
    """mWS : modify Widget Settings
    A la manière de la fonction "cWSF", crée un fichier contenant les nouvelles données du widget,
    si le nom du widget a été changé, la fonction modifie aussi le nom dans le fichier "widNmeList.txt"

    Parameters
    ----------
    path : str
        Chemin d'accès du dossier du projet parent
    newname : str
        Nouveau nom du widget
    oldname : str
        Ancien nom du widget 
    note : newname et oldname peut être identiques
    settings : dict
        Dictionnaires contenant les paramètres du widget
    """
    with open(path + "\\" + newname + ".json", "w", encoding= 'utf8') as file :
        json.dump(settings, file)
    if newname != oldname :
        with open(path + "\\widNmeList.txt", 'r', encoding= 'utf8') as file :
            data = file.read().split(',')
            print(data)
            data.insert(data.index(oldname), newname)
            del data[data.index(oldname)]
            print(data)
            data = ','.join(data)
        with open(path + "\\widNmeList.txt", 'w', encoding= 'utf8') as file :
            file.write(data)


#-------------------------- Fonctions annexes --------------------------


def loadInfo(path : str = None, data : str = 'prjctInfo') -> Union[dict, list, None]:
    """loadInfo _summary_
    Fonction de chargement des données des fichiers

    Parameters
    ----------
    path : str, optional
        Chemin d'accès au fichier, by default None
    data : str, optional
        Précise les données à charger :
        -widsets      : chargement des données relative à un widget précis (widgetInfo.json)
        -setsinfo     : chargement des données relatives aux paramètres des widgets 
        -prjctInfo    : chargement des paramètres du projet selectionné
        -widNameList  : chargement de la liste des widget du projet selectionné
        -actualwidSet : chargement des données d'un widget créé par l'utilisateur
        -prjtCode     : chargement du code du projet 
        -prjtCodeList : Chargement du code du projet sous forme d'une liste

    Returns
    -------
    Union[dict, list, None]
        Retourne :
        -widsets      : retourne un dictionnaire si le chargement a réussi, None sinon
        -setsinfo     : retourne un dictionnaire si le chargement a réussi, None sinon
        -prjctInfo    : retourne un dictionnaire si le chargement a réussi, None sinon
        -widNameList  : retourne la liste des widget si le chargement a réussi, une liste vide sinon
        -actualwidSet : retourne un dictionnaire si le chargement a réussi, False sinon
        -prjtCode     : retourne lu code du projet si le chargement du projet a réussi, None sinon
        -prjtCodeList : retourne lu code du projet sous forme d'une liste si le chargement du projet a réussi, None sinon
    """
    if data == "widsets" :
        try : 
            with open('rssDir\\widgetInfo.json', "r", encoding= 'utf8') as file:
                return json.load(file)
        except :
            return None
    if data == 'setsinfo' :
        try : 
            with open('rssDir\\widParaInfo.json', "r", encoding= 'utf8') as file:
                return json.load(file)
        except :
            return None
    if data == 'prjctInfo' : 
        if verifyDir(path = path) :
            try : 
                with open(path + '\\prjtset.json', "r", encoding= 'utf8' ) as file:
                    return json.load(file)
            except :
                return None
    if data == "widNameList" :
        try :
            with open(path + "\\widNmeList.txt", 'r', encoding= 'utf8') as file :
                widsaved = file.read().split(",")
            file.close()
            return widsaved
        except :
            return []
    if data == "actualwidSet" :
        try :
            with open(path, 'r', encoding= 'utf8') as file :
                return json.load(file)
        except :
            return None
    if data == "prjtCode" :
        try :
            with open(path, "r", encoding= 'utf8') as file :
                return file.read()
        except any as error :
            print(error)
            return None
    if data == "prjtCodeList" :
        try :
            with open(path, "r", encoding= 'utf8') as file :
                return file.readlines()
        except any as error :
            print(error)
            return None
        

def wCode(project : str, code : list):
    """wCode 
    Ecrase le code d'un projet par le nouveau

    Parameters
    ----------
    project : str
        Nom du projet
    code : list
        Code du projet sous forme d'une liste
    """
    path = createPath(project + "\\" + "code.py")
    with open(path, "w", encoding= 'utf8') as file :
        file.writelines(code)
    file.close()