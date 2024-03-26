#fichier gérant les interactions entre l'interface et les fichiers fonctionnels
import fileOpening as fileop
import fileManagemt as flmngt
import codeGen 
from typing import *

def newPrjctRqst(name : str) -> None: 
    """newPrjctRequest 
    Fonction de transition entre le programme de l'interface et le programme de gestions des fichiers,
    envoie une requête de création d'un dossier pour un nouveau projet

    Parameters
    ----------
    name : str
        Nom du dossier à créer
    """
    fileop.dirCreation(name)


def rmproject(name : str) -> None:
    """rmproject 
    Envoie une requête de suppression d'un dossier

    Parameters
    ----------
    name : str
        Nom du fichier
    """
    fileop.rmDirectory(name)


def modidyPrjctRqst(name : str, dico : dict) -> None:
    """modidyPrjctRqst 
    Envoie une requête de modification des paramètres d'un projet

    Parameters
    ----------
    name : str
        Nom du projet
    dico : dict
        Dictionnaire des paramètres du projet
    """
    path = fileop.createPath(name)
    old_data = fileop.loadInfo(path)
    path = fileop.createPath(name + "\\" + "code.py")
    code = codeGen.mWinCode(old_data, dico, path)
    fileop.wCode(name, code)
    flmngt.modifyPrjtInfo(name, dico)


def renameDirReq(oldname : str, newname : str) -> bool:
    return fileop.renameDir(oldname, newname)


def getPrjtSetRqst(name : str) -> dict:
    """getPrjtSetRqst 
    Envoie une requête d'obtention des paramètres d'un projet

    Parameters
    ----------
    name : str
        Nom du projet

    Returns
    -------
    dict
        Paramètres du projet ciblé
    """
    path = fileop.createPath(name)
    return fileop.loadInfo(path = path)


def getMainWidSetsRqst() -> dict:
    """getMainWidSetsRqst 
    Envoie une requête d'obtention des données par défaut d'un widget

    Returns
    -------
    dict
        Paramètres du widget ciblé
    """
    return fileop.loadInfo(data = "widsets")


def getSetsInfoRqst() -> dict:
    """getSetsInfoRqst 
    Envoie une requête d'obtention des données des paramètres présent dans tkinter

    Returns
    -------
    dict
        Dictionnaire des données de chaque paramètre dans tkinter
    """
    return fileop.loadInfo(data = 'setsinfo')


def getWidNameListReq(project : str) -> list:
    """getWidNameListReq 
    Envoie une requête d'obtention de la liste des widgets d'un projet

    Parameters
    ----------
    project : str
        Nom du projet ciblé

    Returns
    -------
    list
        Liste contenant le nom de chaque widget du projet
    """
    path = fileop.createPath(project)
    print(path)
    return fileop.loadInfo(path, data = "widNameList")


def getWidSetReq(widname : str, project : str) -> dict:
    """getWidSetReq 
    Envoie une requête d'obtention des paramètres d'un widget créé par l'utilisateur

    Parameters
    ----------
    widname : str
        Nom du widget
    project : str
        Nom du projet parent du widget

    Returns
    -------
    dict
        Dictionnaire composé des paramètres du widget
    """
    path = fileop.createPath(project + "\\" + widname + ".json")
    return fileop.loadInfo(path, "actualwidSet")


def createWidSetFileReq(newwidget : str, project : str) -> str:
    """createWidSetFileReq 
    Envoie une requête de création d'un fichier pour un widget

    Parameters
    ----------
    newwidget : str
        Nom du nouveau widget
    project : str
        Nom du projet parent du widget

    Returns
    -------
    str
        Retourne le nouveau nom du widget
    """
    return flmngt.cNWSF(newwidget, project)


def modifyWidSetReq(widget : str, widname : str, dico : list, project : str) -> None:
    """modifyWidSetReq 
    Envoie une requête de modification des paramètres d'un widget créé par l'utilisateur

    Parameters
    ----------
    widget : str
        Identifiant du widget ( label, button etc)
    widname : str
        Nom du widget ( donné par l'utilisateur/ par le programme)
    dico : list
        Dictionnaire des paramètres du widget
    project : str
        Nom du projet parent du widget
    """
    path = fileop.createPath(project+ "\\" + widname + ".json")
    old_data = fileop.loadInfo(path, data = "actualwidSet")
    path = fileop.createPath(project + "\\" + "code.py")
    code = codeGen.mWidCode( old_data, dico, path)
    fileop.wCode(project, code)
    flmngt.uWS(widget,widname, dico, project)


def delWidReq(widget : str, wid_id : str, project : str) -> None:
    """delWidReq 
    Envoie une requête de suppression des données d'un widget

    Parameters
    ----------
    widget : str
        Nom du widget
    project : str
        Nom du projet parent du widget
    """
    path = fileop.createPath(project + "\\" + "code.py")
    code = codeGen.delWidCode( widget, wid_id, path)
    fileop.wCode(project, code)
    fileop.rmWid(widget, project)


def getCodeReq(project):
    path = fileop.createPath(project + "\\" + "code.py")
    return fileop.loadInfo(path, data = "prjtCode")


def tryWN(name : str) -> bool:
    """tryWN 
    Fonction de vérification de la validité d'un nom de widget entré,
    étant donné que ce nom est aussi utilisé comme nom de variable il doit :
    - ne pas contenir de caractères interdits
    - ne par commencer par une majuscule
    Parameters
    ----------
    name : str
        Nom de widget à tester

    Returns
    -------
    bool
        Renvoie True si le nom est valide, False sinon
    """
    allowedchar = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'
    ]
    for letters in name :
        if letters not in allowedchar :
            return False
    if name[0] in allowedchar[26:-2]:
        return False
    return True


def tryFont(family :str, family_list : str ) -> str :
    """tryFont 
    Vérifie si la police d'écriture entrée dans les paramètres de font est supportée par tkinter

    Parameters
    ----------
    family : str
        Police d'écriture entrée
    family_list : str
        Liste des polices d'écritures supportées par tkinter

    Returns
    -------
    str
        Retourne True si elle est valide, False sinon
    """
    #on récupère le
    family = family.capitalize().strip()
    if family + '\n' in family_list :
        return family
    else :
        return False


def getRssPath(rss : str ) -> str :
    """getRssPath 
    Retourne le chemin d'accès d'une ressource dans le fichier ressources

    Parameters
    ----------
    rss : str
        Nom de la ressource demandée

    Returns
    -------
    str
        Retourne le chemin d'accès de la ressource demandée
    """
    return fileop.createPath("rssDir" + "\\" + rss)


def getProjectPath(project : str) -> str:
    """getProjectPath 
    Retourne le chemin d'accès du projet

    Parameters
    ----------
    project : str
        Nom du projet

    Returns
    -------
    str
        Chemin d'accès du projet
    """
    return fileop.createPath(project)


#possibilité de lancer le programme seul, à des fins de débogage
if __name__ == "__main__" :
    name = input("nom : ")
    print(tryWN(name))