#fichier créant le code en python
import fileOpening as fileop


def mWinCode(old_data, data, project_path):
        code_dico = fileop.loadInfo(project_path, data = "prjtCodeList")
        try :
            if data["WinName"] != "":
                if f"window.title('{old_data["WinName"]}')\n" in code_dico :
                    del code_dico[code_dico.index(f"window.title('{old_data["WinName"]}')\n")]
                code_dico.insert(5, f"window.title('{data["WinName"]}')\n")
            else :
                del code_dico[code_dico.index(f"window.title('{old_data["WinName"]}')\n")] 
            print("okgen")
        except :
            pass
        
        try :
            if data["height"] == "" or data["width"] == "" :
                if f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" :
                    del code_dico[code_dico.index(f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n")]
            elif data["height"] > 50 and data["width"] > 50 and f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" not in code_dico :
                code_dico.insert(6, f"window.geometry('{data["height"]}x{data["width"]}')\n")
            elif f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" in code_dico :
                del code_dico[code_dico.index(f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n")]
                code_dico.insert(6, f"window.geometry('{data["height"]}x{data["width"]}')\n")
        except :
            pass
        code_dico.insert(7, "\n")
        return code_dico
    
def createWidCode(data : dict):
        str_sets = ["bg_color", "fg_color", "border_color", "text_color", "text_color_disabled",
             "compound", "anchor", "hover_color", "checkmark_color", "state"
            "button_color", "button_hover_color", "dropdown_fg_color", "dropdown_hover_color"
            "dropdown_text_color", "placeholder_text_color", "background_corner_colors"]
        
        widsets =  fileop.loadInfo(data = "setsinfo")
        widinfo = fileop.loadInfo(data = "widsets")
        init_seq = data[0]["name"] + " = " + widinfo[data[0]["ID"]]["tkid"]+ "(" + data[0]["master"]
        for keys, values in data[0].items() :
            if keys in ["name", "ID", "layout", "master"]:
                pass
            elif keys == "text" :
                init_seq += f", {keys} = \"{values}\""
            elif values != widsets[keys][0] and keys != "text": 
                if keys == "font" and values != "0":
                    font = "customtkinter.CTkFont("
                    for sets, val in data[1].items():
                        if sets in ["family", "weight", "slant"] :
                            font += f"{sets} = '{val}' ,"
                        else :
                            font += f"{sets} = {val} ,"
                    font = font[0:-1] + ")"
                    init_seq += f", {keys} = {font}"
                
                elif keys != "font" :
                    if keys in str_sets:
                        init_seq += f", {keys} = '{values}'"
                    elif keys == "values" :
                        sub_seq = "["
                        for element in values :
                            sub_seq += f"\"{element}\","
                        sub_seq = sub_seq[:-1] + "]"
                        init_seq += f", {keys} = {sub_seq}"
                    else :
                        init_seq += f", {keys} = {values}"
        init_seq += ')\n'
        layout_seq = f"{data[0]["name"]}.{data[0]["layout"]}("
        for sets, val in data[2].items():
            if sets in ["sticky", "side", "fill", "anchor"]:
                layout_seq += f"{sets} = '{val}' ,"
            else : 
                layout_seq += f"{sets} = {val} ,"
        layout_seq = layout_seq[0:-1] + ")\n" if len(data[2].keys()) > 0 else layout_seq + ")\n"
        return [init_seq, layout_seq, "\n"]
    

def mWidCode(old_data : list, new_data : list, project_path):
        code = fileop.loadInfo(project_path, data = "prjtCodeList")
        old_widcode = createWidCode(data = old_data)
        new_widcode = createWidCode(data = new_data)
        print(old_data, "\n", new_widcode)
        if old_widcode[0] != new_widcode[0] :
            if old_widcode[0] in code :
                code.insert(code.index(old_widcode[0]), new_widcode[0])
                del code[code.index(old_widcode[0])]
            else :
                code.append(new_widcode[0])
        
        if old_widcode[1] != new_widcode[1] :
            if old_widcode[1] in code :
                code.insert(code.index(old_widcode[1]), new_widcode[1])
                del code[code.index(old_widcode[1])]
            else :
                code.append(new_widcode[1])
        code.append(new_widcode[2])
        return code


def delWidCode(widget, wid_id, project_path):
        widinfo = fileop.loadInfo(data = "widsets")
        code = fileop.loadInfo(project_path, data = "prjtCodeList")
        for lines in code :
            print(lines)
            if f"{widget} = {widinfo[wid_id]["tkid"]}" in lines :
                del code[code.index(lines):code.index(lines)+3]
                #del code[code.index(lines)]
            
        return code