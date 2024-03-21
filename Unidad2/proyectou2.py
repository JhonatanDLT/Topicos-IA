import customtkinter
import os
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import ttk
import pandas as pd


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Peliculas.py")
        
        self.geometry("1500x700")
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Reglas",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Calificadas",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        


                 #-------------------------------------------------------------------------------------------------------------------------------
        # Definir el universo de discurso

        #genero = ['Terror', 'Comedia', 'Drama', 'Animacion', 'Accion', 'suspenso'] #AGREGAR GENEROS
        genero = np.arange(0, 11, 1) #AGREGAR GENEROS

        # Definir las variables de entrada y salida
        calificacion_promedio = ctrl.Antecedent(np.arange(0, 100, 1), 'calificacion_promedio')
        genero = ctrl.Antecedent(np.arange(len(genero)), 'genero')
        ano_estreno = ctrl.Antecedent(np.arange(1888, 2025, 1), 'ano_estreno')
        recomendacion = ctrl.Consequent(np.arange(0, 101, 1), 'recomendacion', defuzzify_method='som')

        # Definir conjuntos difusos para la calidad de comida
        calificacion_promedio['mala'] = fuzz.trapmf(calificacion_promedio.universe, [0, 0, 30, 40])
        calificacion_promedio['regular'] = fuzz.trimf(calificacion_promedio.universe, [40, 60, 80])
        calificacion_promedio['buena'] = fuzz.trapmf(calificacion_promedio.universe, [ 70,85,100,100])

        # Funciones de membresía personalizadas para la calidad de genero // LISTA DE ETIQUETAS
        genero['Terror'] = fuzz.trimf(genero.universe, [0, 0, 1])
        genero['Comedia'] = fuzz.trimf(genero.universe, [1, 2, 3])
        genero['Drama'] = fuzz.trimf(genero.universe, [3, 4, 5])
        genero['Animacion'] = fuzz.trimf(genero.universe, [5, 6, 7])
        genero['Accion'] = fuzz.trimf(genero.universe, [7, 8, 9])
        genero['suspenso'] = fuzz.trimf(genero.universe, [9, 10, 10])

        # Definir conjuntos difusos para la ano_estreno
        ano_estreno['antiguo'] = fuzz.trapmf(ano_estreno.universe, [1888, 1888, 1999, 2003])
        ano_estreno['reciente'] = fuzz.trapmf(ano_estreno.universe, [2002,2008,2024,2024])

        # Definir conjuntos difusos para la satisfacción
        recomendacion['No recomendada'] = fuzz.trapmf(recomendacion.universe, [0, 0, 30, 40])
        recomendacion['Poco recomendada'] = fuzz.trimf(recomendacion.universe, [40, 50, 60])
        recomendacion['recomendada'] = fuzz.trapmf(recomendacion.universe, [60, 70, 80, 85])
        recomendacion['Altamente recomendada'] = fuzz.trapmf(recomendacion.universe, [85, 90, 100, 100])

        # Reglas difusas corregidas para la recomendacion
        rule1 = ctrl.Rule(genero['Terror'] & calificacion_promedio['mala'] & ano_estreno['reciente'], recomendacion['Poco recomendada'])
        rule2 = ctrl.Rule(genero['Terror'] & calificacion_promedio['regular'] & ano_estreno['reciente'], recomendacion['Poco recomendada'])
        rule3 = ctrl.Rule(genero['Terror'] & calificacion_promedio['buena'] & ano_estreno['reciente'], recomendacion['Altamente recomendada'])
        rule4 = ctrl.Rule(genero['Terror'] & calificacion_promedio['mala'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule5 = ctrl.Rule(genero['Terror'] & calificacion_promedio['regular'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule6 = ctrl.Rule(genero['Terror'] & calificacion_promedio['buena'] & ano_estreno['antiguo'], recomendacion['recomendada'])

        rule7 = ctrl.Rule(genero['Comedia'] & calificacion_promedio['mala'] & ano_estreno['reciente'], recomendacion['Poco recomendada'])
        rule8 = ctrl.Rule(genero['Comedia'] & calificacion_promedio['regular'] & ano_estreno['reciente'], recomendacion['recomendada'])
        rule9 = ctrl.Rule(genero['Comedia'] & calificacion_promedio['buena'] & ano_estreno['reciente'], recomendacion['Altamente recomendada'])
        rule10 = ctrl.Rule(genero['Comedia'] & calificacion_promedio['mala'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule11 = ctrl.Rule(genero['Comedia'] & calificacion_promedio['regular'] & ano_estreno['antiguo'], recomendacion['recomendada'])
        rule12 = ctrl.Rule(genero['Comedia'] & calificacion_promedio['buena'] & ano_estreno['antiguo'], recomendacion['recomendada'])

        rule13 = ctrl.Rule(genero['Drama'] & calificacion_promedio['mala'] & ano_estreno['reciente'], recomendacion['Poco recomendada'])
        rule14 = ctrl.Rule(genero['Drama'] & calificacion_promedio['regular'] & ano_estreno['reciente'], recomendacion['recomendada'])
        rule15 = ctrl.Rule(genero['Drama'] & calificacion_promedio['buena'] & ano_estreno['reciente'], recomendacion['Altamente recomendada'])
        rule16 = ctrl.Rule(genero['Drama'] & calificacion_promedio['mala'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule17 = ctrl.Rule(genero['Drama'] & calificacion_promedio['regular'] & ano_estreno['antiguo'], recomendacion['recomendada'])
        rule18 = ctrl.Rule(genero['Drama'] & calificacion_promedio['buena'] & ano_estreno['antiguo'], recomendacion['Altamente recomendada'])

        rule19 = ctrl.Rule(genero['Animacion'] & calificacion_promedio['mala'] & ano_estreno['reciente'], recomendacion['Poco recomendada'])
        rule20 = ctrl.Rule(genero['Animacion'] & calificacion_promedio['regular'] & ano_estreno['reciente'], recomendacion['recomendada'])
        rule21 = ctrl.Rule(genero['Animacion'] & calificacion_promedio['buena'] & ano_estreno['reciente'], recomendacion['Altamente recomendada'])
        rule22 = ctrl.Rule(genero['Animacion'] & calificacion_promedio['mala'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule23 = ctrl.Rule(genero['Animacion'] & calificacion_promedio['regular'] & ano_estreno['antiguo'], recomendacion['recomendada'])
        rule24 = ctrl.Rule(genero['Animacion'] & calificacion_promedio['buena'] & ano_estreno['antiguo'], recomendacion['Altamente recomendada'])

        rule25 = ctrl.Rule(genero['Accion'] & calificacion_promedio['mala'] & ano_estreno['reciente'], recomendacion['Poco recomendada'])
        rule26 = ctrl.Rule(genero['Accion'] & calificacion_promedio['regular'] & ano_estreno['reciente'], recomendacion['recomendada'])
        rule27 = ctrl.Rule(genero['Accion'] & calificacion_promedio['buena'] & ano_estreno['reciente'], recomendacion['recomendada'])
        rule28 = ctrl.Rule(genero['Accion'] & calificacion_promedio['mala'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule29 = ctrl.Rule(genero['Accion'] & calificacion_promedio['regular'] & ano_estreno['antiguo'], recomendacion['recomendada'])
        rule30 = ctrl.Rule(genero['Accion'] & calificacion_promedio['buena'] & ano_estreno['antiguo'], recomendacion['Altamente recomendada'])

        rule31 = ctrl.Rule(genero['suspenso'] & calificacion_promedio['mala'] & ano_estreno['reciente'], recomendacion['No recomendada'])
        rule32 = ctrl.Rule(genero['suspenso'] & calificacion_promedio['regular'] & ano_estreno['reciente'], recomendacion['recomendada'])
        rule33 = ctrl.Rule(genero['suspenso'] & calificacion_promedio['buena'] & ano_estreno['reciente'], recomendacion['Altamente recomendada'])
        rule34 = ctrl.Rule(genero['suspenso'] & calificacion_promedio['mala'] & ano_estreno['antiguo'], recomendacion['No recomendada'])
        rule35 = ctrl.Rule(genero['suspenso'] & calificacion_promedio['regular'] & ano_estreno['antiguo'], recomendacion['recomendada'])
        rule36 = ctrl.Rule(genero['suspenso'] & calificacion_promedio['buena'] & ano_estreno['antiguo'], recomendacion['recomendada'])

        # Creación del controlador difuso
        sistema_ctrl = ctrl.ControlSystem([
            rule1, rule2, rule3, rule4, rule5, rule6,
            rule7, rule8, rule9, rule10, rule11, rule12,
            rule13, rule14, rule15, rule16, rule17, rule18,
            rule19, rule20, rule21, rule22, rule23, rule24,
            rule25, rule26, rule27, rule28, rule29, rule30,
            rule31, rule32, rule33, rule34, rule35, rule36
        ])
        sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

        # Evaluación de una entrada específica
        sistema.input['calificacion_promedio'] = 100
        sistema.input['ano_estreno'] = 2020
        sistema.input['genero'] = 0

        sistema.compute()

        print(f"Nivel de recomendacion: {sistema.output['recomendacion']:.2f}")

#--------------------------------------------------------------------------------------------
        

        # create home frame CALCULAR
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        nombre_pelicula =""
        ano_pelicula = 0
        calificacion = 0
        generos = 0

        def button_click_nombre():
            dialog = customtkinter.CTkInputDialog(text="Nombre de la pelicula:", title="nombre")
            nombre_pelicula = dialog.get_input()
            print(nombre_pelicula)


        button_nombre = customtkinter.CTkButton( self.home_frame, text="Nombre", command=button_click_nombre)
        button_nombre.pack(padx=20, pady=20)

        def button_click_ano():
            dialog = customtkinter.CTkInputDialog(text="Año de lanzamiento:", title="año")
            sistema.input['ano_estreno'] = int(dialog.get_input())
            print(ano_pelicula)


        button_ano = customtkinter.CTkButton( self.home_frame, text="Año de lanzamiento", command=button_click_ano)
        button_ano.pack(padx=20, pady=20)

        def button_click_calificacion():
            dialog = customtkinter.CTkInputDialog(text="Calificacion:", title="Calificacion")
            sistema.input['calificacion_promedio'] = int(dialog.get_input())
            print(calificacion)


        button_calificacion = customtkinter.CTkButton( self.home_frame, text="Calificacion", command=button_click_calificacion)
        button_calificacion.pack(padx=20, pady=20)
        
        
        """
                Terror: 0,
                Comedia: 2,
                Drama: 4,
                Animacion: 6,
                Accion: 8,
                Suspenso: 10
        """

        def button_click_genero():
            dialog = customtkinter.CTkInputDialog(text=" terror:0, comedia:2, drama:4, animacion:6, accion:8, suspenso:10 ", title="genero")
            sistema.input['genero'] = int(dialog.get_input())
            print(generos)


        button_genero = customtkinter.CTkButton( self.home_frame, text="genero", command=button_click_genero)
        button_genero.pack(padx=20, pady=20)

            
        def obtener_valor_numerico():
            sistema.compute()
            label_r = customtkinter.CTkLabel(self.home_frame, justify=customtkinter.LEFT, text=sistema.output['recomendacion'])
            label_r.pack(padx=20, pady=20)
            print(sistema.output['recomendacion'])




        self.main_button_1 = customtkinter.CTkButton(self.home_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Calcular", command=obtener_valor_numerico)
        self.main_button_1.pack(padx=20, pady=20)
        

        def  mostrar_graficas():
            calificacion_promedio.view(sim=sistema)
            genero.view(sim=sistema)
            ano_estreno.view(sim=sistema)
            recomendacion.view(sim=sistema)
            plt.show

        self.main_button_2 = customtkinter.CTkButton(self.home_frame, text="Graficas",  command=mostrar_graficas)
        self.main_button_2.pack(padx=20, pady=20)
        


#____________________ create second frame REGLAS_____________________________________________________________________
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        text_1 = customtkinter.CTkTextbox(self.second_frame, width=700, height=500) 
        #text_1 = customtkinter.CTkTextbox(self.second_frame, wrap=customtkinter.WORD, state=customtkinter.DISABLED)
        text_1.pack(fill="both", expand=True)
        # Crea una instancia de ControlSystemSimulation
        sistema = ctrl.ControlSystemSimulation(sistema_ctrl)
        # Obtén las reglas
        lista_de_reglas = sistema_ctrl.rules
        # Imprime las reglas
        reglas_texto = "\n".join(str(regla) for regla in lista_de_reglas)
        text_1.insert(customtkinter.END, reglas_texto)
        text_1.configure(state="disabled")


#************************************* create third frame***********************************************************************     
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        # Leer el archivo CSV con Pandas
        df = pd.read_csv('peliculas.csv')  # Reemplaza 'tu_archivo.csv' con la ruta de tu archivo CSV

        tabla = ttk.Treeview(self.third_frame)
        tabla["columns"] = list(df.columns)
        tabla.pack(fill=tk.BOTH, expand=True)

        # Configurar las columnas de la tabla
        for columna in df.columns:
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=100)  # Ajusta el ancho de las columnas según tus necesidades

        # Mostrar los datos del DataFrame en la tabla
        for indice, fila in df.iterrows():
            tabla.insert("", tk.END, values=list(fila))
        

        # select default frame
        self.select_frame_by_name("home")
        
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
            

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
   

if __name__ == "__main__":
    app = App()
    app.mainloop()
    

