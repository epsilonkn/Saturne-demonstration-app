#fichier gérant les interactions avec les fichiers de sauvegarde
import fileOpening as fileop


def modifyPrjtInfo(name : str, newinfo : dict):
    """modifyPrjtInfo 
    Modifie les paramètres d'un projet dans son fichier

    Parameters
    ----------
    name : str
        Nom du projet
    newinfo : dict
        Nouvelles données
    """
    get_path = fileop.createPath(name) +"\\"+ 'prjtset.json'
    fileop.mPS(get_path, newinfo)


def cNWSF(widget : str, project : str) -> str:
    """cNWSF : Create New Widget Settings File
    Crée les données par défaut d'un widget lors de son ajout dans l'application

    Parameters
    ----------
    widget : str
        ID du widget
    project : str
        Nom du projet

    Returns
    -------
    str
        Retourne le nouveau nom du widget ( constitué de son ID et d'un chiffre non utilisé )
    """
    sets = fileop.loadInfo(data = "widsets")
    sets = sets[widget]
    setvalues = fileop.loadInfo(data = "setsinfo")

    path = fileop.createPath(project)
    widnameused = fileop.loadInfo(path = path,data = "widNameList")
    flag = False
    incr = 1
    while flag == False :
        if widget + str(incr) not in widnameused :
            flag = True
            newname = widget + str(incr)
        else : incr += 1
    dico = {}
    dico["name"] = newname
    dico["ID"] = widget
    dico["layout"] = None
    for values in sets["parameters"]:
        dico [values] = setvalues[values][0]
    fileop.cWSF(path, newname, [dico, {}, {}])
    return newname 


def uWS(widid : str, widname : str, dico : dict, project : str) -> None:
    """uWS  : Update Widget Settings
    modifie les paramètres d'un widget

    Parameters
    ----------
    widid : str
        ID du widget
    widname : str
        Nom du wdiget
    dico : dict
        Dictionnaire contenant les nouveaux paramètres
    project : str
        Nom du projet
    """
    datasets = {}
    datasets["name"] = dico[0]["name"]
    datasets["ID"] = dico[0]["ID"]
    datasets["layout"] = dico[0]["layout"]
    sets = fileop.loadInfo(data = "widsets")
    sets = sets[widid]
    setvalues = fileop.loadInfo(data = "setsinfo")
    for settings in sets["parameters"] :
        if settings in dico[0] :
            datasets[settings] = dico[0][settings]
        else :
            datasets[settings] = setvalues[settings][0]
    print(datasets, dico[1], dico[2])
    path = fileop.createPath(project)
    fileop.rmFile(path + "\\" + widname + '.json')
    fileop.mWS(path, dico[0]["name"], widname, [datasets, dico[1], dico[2]])
