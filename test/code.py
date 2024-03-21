import customtkinter

window = customtkinter.CTk()

label1 = customtkinter.CTkLabel(window, text = "texte")
label1.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 0 ,sticky = 'W' )

entry1 = customtkinter.CTkEntry(window, width = 150)
entry1.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 1 ,sticky = 'W' )

