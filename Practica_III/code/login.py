from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
import pandas as pd 
import numpy as np
from pandastable import Table, TableModel 
from bson.objectid import ObjectId
import pymongo
from pymongo import GEOSPHERE
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta
# es importante mapear al puerto usando -p 27017:27017 al construir el contenedor o en el docker-compose.yml
conn_str = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn_str, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
db = client['BDBicis']
#Alternativa:
# client = MongoClient('localhost', 27017)

# Probando conexión
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

# Carga de las estaciones
estaciones = pd.read_csv('data/estaciones.csv')
dict_id_estacion = dict(zip(estaciones.id, estaciones.name))
dict_estacion_id = dict(zip(estaciones.name, estaciones.id))

#Usuario logueado en cache
supertemporalUser=None

#Ventanas de interfaz grafica
class Login_window(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=300, y=170, width= 340, height=400)

        img1 = Image.open("img/img_logo.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(img1)
        lblimg1=Label(frame, image=self.photoImage1, bg="black", borderwidth=0)
        lblimg1.place(x=120, y=20, width=100, height=100)

        get_str = Label(frame, text="Login", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=130, y=100)
        
        #Label 
        username=Label(frame, text="Username", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        username.place(x=70, y=155)

        self.txtuser = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=240)

        #Icon Image
        img2 = Image.open("img/img_user.png")
        img2 = img2.resize((25,25), Image.ANTIALIAS)
        self.photoImage2= ImageTk.PhotoImage(img2)
        lblimg1=Label(frame, image=self.photoImage2, bg="black", borderwidth=0)
        lblimg1.place(x=40, y=155, width=25, height=25)

        #Login Button
        loginbtn=Button(frame,command=self.login, text="Login",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        loginbtn.place(x=110, y=230, width=120, height=35)

        #Register Button
        registerbtn=Button(frame,command=self.register_window, text="Registrate",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=110, y=280, width=120, height=35)

    def register_window(self): 
        self.root.switch_frame(Register)

    def login(self): 
        if self.txtuser.get()=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        else: 
            usernameVal = self.txtuser.get()
            from base_queries import existe_usuario
            existe_user = existe_usuario(usernameVal)
            if existe_user:
                global supertemporalUser 
                supertemporalUser=usernameVal
                messagebox.showinfo("Success", f"Bienvenido {supertemporalUser}")
                self.root.switch_frame(User_options)
            else: 
                self.txtuser.delete(0,END)
                messagebox.showerror("Error", "Usuario no existe,debe registrarse")

class Register(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1550x800+0+0")

        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=300, y=100, width= 340, height=600)

        img1 = Image.open("img/img_logo.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(img1)
        lblimg=Label(frame, image=self.photoImage1, bg="black", borderwidth=0)
        lblimg.place(x=130, y=20, width=100, height=100)

        get_str = Label(frame, text="Registrate", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=120, y=100)

        #Label 
        username=Label(frame, text="Username", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        username.place(x=70, y=155)

        self.txtuser = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=240)

        firstplace= Label(frame, text="Lugar favorito", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        firstplace.place(x=70, y=215)

        self.txtfirstplace = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtfirstplace.place(x=40, y=240, width=240)

        longitude=Label(frame, text="Longitud", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        longitude.place(x=70, y=275)

        self.txtlongitude = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtlongitude.place(x=40, y=300, width=240)

        latitude=Label(frame, text="Latitud", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        latitude.place(x=70, y=335)

        self.txtlatitude = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtlatitude.place(x=40, y=370, width=240)

        #Icon Image
        img2 = Image.open("img/img_user.png")
        img2 = img2.resize((25,25), Image.ANTIALIAS)
        self.photoImage2= ImageTk.PhotoImage(img2)
        lblimg1=Label(frame, image=self.photoImage2, bg="black", borderwidth=0)
        lblimg1.place(x=40, y=155, width=25, height=25)

        #Login Button
        registerbtn=Button(frame,command=self.register, text="Registrar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=40, y=420, width=120, height=35)

        loginnowbtn=Button(frame,command=self.login_window, text="Ir a Login",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        loginnowbtn.place(x=170, y=420, width=120, height=35)

    def login_window(self): 
        self.root.switch_frame(Login_window)

    def register(self):         
        usernameVal= self.txtuser.get() 
        firstplaceVal= self.txtfirstplace.get() 
        longitudeVal= self.txtlongitude.get()
        latitudeVal      = self.txtlatitude.get()
        if usernameVal=="" or longitudeVal=="" or latitudeVal=="" or firstplaceVal=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else:
            longitudeVal = float(longitudeVal)
            latitudeVal = float(latitudeVal)
            from base_queries import existe_usuario
            existe_user = existe_usuario(usernameVal)
            if existe_user:
                messagebox.showerror("Error", "El usuario ya existe, favor de hacer login")
                self.root.switch_frame(Login_window)
            else: 
                global supertemporalUser
                supertemporalUser=usernameVal
                from base_queries import crear_usuario
                crear_usuario(usernameVal, firstplaceVal, float(longitudeVal), float(latitudeVal))
                messagebox.showinfo("Success", f"Registro Exitoso, bienvenido {supertemporalUser}")
                self.root.switch_frame(User_options)

class User_options(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Perfil Usuario")
        self.root.geometry("1550x800+0+0")
        
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=50, y=150, width= 750, height=400)

        get_str = Label(frame, text="Panel Usuario", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=30, y=30)

        viewPlacesbtn=Button(frame,command = self.my_places, text="Ver Mis lugares",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        viewPlacesbtn.place(x=70, y=120, width=180, height=50)

        viewTripsbtn=Button(frame,command = self.my_trips, text="Ver Mis Viajes",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        viewTripsbtn.place(x=270, y=120, width=180, height=50)

        viewTripsbtn=Button(frame,command = self.my_est, text="Ver Estaciones Cercanas",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        viewTripsbtn.place(x=470, y=120, width=210, height=50)

        registerPlacesbtn=Button(frame,command = self.make_place, text="Registrar lugar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerPlacesbtn.place(x=170, y=220, width=180, height=50)

        registerTripsbtn=Button(frame,command = self.make_trip, text="Hacer Nuevo Viaje",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerTripsbtn.place(x=400, y=220, width=180, height=50)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=320, y=310, width=120, height=35)

    def login_window(self): 
        self.root.switch_frame(Login_window)

    def my_est(self): 
        self.root.switch_frame(Search_estations)
    def my_places(self): 
        global supertemporalUser
        if supertemporalUser==None:
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)

        from base_queries import lugares_guardados
        resultado = lugares_guardados(supertemporalUser)
        
        res = pd.DataFrame(resultado, columns= ['Nombre Lugar', 'Coordenadas'])
        pt = Table(f, dataframe=res,
                                showtoolbar=True, showstatusbar=True)
        pt.show()

    def my_trips(self): 
        global supertemporalUser
        if supertemporalUser==None:
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)

        from base_queries import historial_viajes
        resultado = historial_viajes(supertemporalUser)
        resultado['origen_name'] = resultado['id_origen']
        resultado['destino_name']= resultado['id_destino']
        def aux_funct(row):
            row.origen_name = dict_id_estacion[row.origen_name]
            row.destino_name = dict_id_estacion[row.destino_name]
            return row

        resultado = resultado.apply(aux_funct, axis=1)
        resultado = resultado[['origen_name', 'destino_name', 'hora_salida', 'hora_llegada']]
        #resultado['id_origen'] = resultado['id_origen'].apply(lambda x: dict_estacion_id(x))
        #resultado = resultado.drop(['_id', 'id_origen', 'id_destino' , 'usuario'], axis=1)
        pt = Table(f, dataframe=resultado,showtoolbar=True, showstatusbar=True)
        pt.show()
            
    def make_place(self): 
        self.root.switch_frame(Register_Place)
    
    def make_trip(self): 
        self.root.switch_frame(Register_Trip)
        messagebox.showinfo('Instrucciones', 'Las opciones se actualizan a tiempo real')
        
class Register_Place(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Register Place")
        self.root.geometry("1550x800+0+0")

        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=300, y=100, width= 340, height=400)

        get_str = Label(frame, text="Registrar/Actualizar Lugar", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=30, y=30)

        firstplace= Label(frame, text="Lugar favorito", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        firstplace.place(x=70, y=80)

        self.txtfirstplace = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtfirstplace.place(x=40, y=110, width=240)

        longitude=Label(frame, text="Longitud", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        longitude.place(x=70, y=150)

        self.txtlongitude = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtlongitude.place(x=40, y=180, width=240)

        latitude=Label(frame, text="Latitud", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        latitude.place(x=70, y=210)

        self.txtlatitude = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtlatitude.place(x=40, y=240, width=240)

        #Login Button
        registerbtn=Button(frame,command=self.register_new_place, text="Registrar Lugar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=30, y=320, width=140, height=35)

        exitbtn=Button(frame,command=self.user_control, text="Ir a Panel",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=180, y=320, width=140, height=35)

    def user_control(self): 
        self.root.switch_frame(User_options)

    def register_new_place(self):         
        firstplaceVal= self.txtfirstplace.get() 
        longitudeVal= self.txtlongitude.get()
        latitudeVal      =  self.txtlatitude.get()
        if longitudeVal=="" or latitudeVal=="" or firstplaceVal=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else:
            longitudeVal = float(longitudeVal)
            latitudeVal = float(latitudeVal)
            global supertemporalUser
            if supertemporalUser: 
                from base_queries import nuevo_lugar
                from base_queries import existe_lugar 
                existplace = existe_lugar(supertemporalUser, firstplaceVal)
                if existplace: 
                    self.txtfirstplace.delete(0, END)
                    self.txtlongitude.delete(0,END)  
                    self.txtlatitude.delete(0,END) 
                    messagebox.showerror("Error", "El lugar ya existe, cambie el nombre")
                else: 
                    nuevo_lugar(supertemporalUser, firstplaceVal, longitudeVal, latitudeVal)
                    messagebox.showinfo("Info", "Lugar creado con exito")
                    self.root.switch_frame(User_options)
            else: 
                self.root.switch_frame(Login_window)
                messagebox.showerror("Error", "No hay usuario registrado")
class Register_Trip(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=80, y=100, width= 700, height=600)

        get_str = Label(frame, text="Hacer Nuevo Viaje", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=30, y=30)

        hiper_text = """Instrucciones de uso:
1. Elige uno de tus lugares guardados para el cual deseas buscar estaciones cercanas.La opción “Elegir estación” te permite elegir cualquier estación como origen.

2. Introduce la duración deseada de tu viaje.

3. Selecciona una estación de origen, solo se muestran las estaciones cercanas a tu lugar guardado, o todas en caso de haber elegido Elegir estación.

4. En estación final se muestran las estaciones de destino sugeridas por el sistema. Selecciona una.

Nota: Si no hay viajes posibles dentro con tiempo cercano a tu tiempo deseado y el origen elegido,no se mostrará ninguna opción."""
        instructions = Label(frame, wraplength=270, justify='left', text=hiper_text,  font = ("calibri", 10), fg="white", bg="black")
        instructions.place(x=400, y=50, width=270)

        #Label 
        lugar=Label(frame, text="Lugar de origen", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        lugar.place(x=40, y=70)

        self.txtlugar = ttk.Combobox(frame, state="readonly",values=['Elegir estacion'])
        self.txtlugar.place(x=40, y=100, width=240)
        self.txtlugar.bind('<Enter>', self.update_place)
        self.txtlugar.bind('<<ComboboxSelected>>', self.update_estacion_origen)

        duracion=Label(frame, text="Duración:", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        duracion.place(x=40, y=120)
    
        self.hour_sb = ttk.Spinbox(frame,from_=0,to=9,width=40, wrap=True, state="readonly",font=('Times', 20),justify=CENTER)
        self.min_sb = ttk.Spinbox(frame,from_=0,to=59,width=40, wrap=True, state="readonly", font=('Times', 20),justify=CENTER)
        self.hour_sb.place(x=40,y= 150, width=50, height=25)
        self.min_sb.place(x=100,y= 150, width=50, height=25)

        msg = Label(frame, text="Horas    Minutos",font=("Times", 12),fg="lightseagreen", bg = "black")
        msg.place(x=40, y=170)


        est_origen=Label(frame, text="Estación de origen", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        est_origen.place(x=40, y=190)

        self.txtest_origen = ttk.Combobox(frame, state="readonly",values=[])
        self.txtest_origen.place(x=40, y=220, width=240)
        self.txtest_origen.bind('<<ComboboxSelected>>', self.update_estacion_final)        


        est_final=Label(frame, text="Estación final", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        est_final.place(x=40, y=240)

        self.txtest_final = ttk.Combobox(frame, state="readonly",values=[])
        self.txtest_final.place(x=40, y=270, width=240)

        #Login Button
        registerbtn=Button(frame,command=self.register_new_trip, text="Registrar Viaje",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=30, y=520, width=140, height=35)

        exitbtn=Button(frame,command=self.user_control, text="Ir a Panel",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=180, y=520, width=140, height=35)


    def update_place(self, event):
        if supertemporalUser: 
            from base_queries import  lugares_guardados_nombres
            listplaces= lugares_guardados_nombres(supertemporalUser)
            listplaces.append('Elegir estacion')
            self.txtlugar['state']= 'normal'
            self.txtlugar['values']= listplaces
            self.txtlugar['state']= 'readonly'
        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def update_estacion_origen(self, event): 
        if self.txtlugar.get()=="": 
            self.txtest_origen['state']= 'normal'
            self.txtest_origen['values']= []
            self.txtest_origen['state']= 'readonly' 
            return
        if supertemporalUser: 
            lugar_valor = self.txtlugar.get() 
            if lugar_valor == 'Elegir estacion': 
                self.txtest_origen['state']= 'normal'
                self.txtest_origen['values']= estaciones['name'].tolist()
                self.txtest_origen['state']= 'readonly'
                return
            else: 
                from base_queries import estaciones_mas_cercanas   
                df_est= estaciones_mas_cercanas(supertemporalUser, lugar_valor)  
                listplaces = df_est['nombre_estacion'].tolist()
                self.txtest_origen['state']= 'normal'
                self.txtest_origen['values']= listplaces
                self.txtest_origen['state']= 'readonly'
                return

        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    
    def update_estacion_final(self, event): 
        self.txtest_final['state']= 'normal'
        self.txtest_final['values']= []
        self.txtest_final['state']= 'readonly' 
        if self.hour_sb.get() =="" or self.hour_sb.get()=="":
            messagebox.showerror("Error", "Primero seleccione hora y minutos")
            return
        if self.txtlugar.get()=="": 
            self.txtest_final['state']= 'normal'
            self.txtest_final['values']= []
            self.txtest_final['state']= 'readonly' 
            return 
        if supertemporalUser: 
            self.roundTrip = messagebox.askyesno(title='Tipo de viaje',message='¿El viaje es redondo?') 
            est_origen_val = self.txtest_origen.get() 
            int_hour       = int(self.hour_sb.get())
            int_minutes    = int(self.min_sb.get())
            if self.roundTrip:
                from base_queries import viaje_redondo
                df_fin = viaje_redondo(dict_estacion_id[est_origen_val], 3600*(int_hour) + 60*int_minutes)
                list_id_fin = df_fin['punto_medio'].tolist()
                if not list_id_fin: 
                    self.txtest_final['state']= 'normal'
                    self.txtest_final['values']= []
                    self.txtest_final['state']= 'readonly'
                    messagebox.showinfo('Info', 'No se encontraron rutas que cumplan origen y tiempo deseado')
                    return
                list_est_fin = [ dict_id_estacion[name_est_fin] for name_est_fin in list_id_fin]
                self.txtest_final['state']= 'normal'
                self.txtest_final['values']= list_est_fin
                self.txtest_final['state']= 'readonly'
            else: 
                from base_queries import ruta_desde_estacion
                df_fin = ruta_desde_estacion(dict_estacion_id[est_origen_val], 3600*(int_hour) + 60*int_minutes)
                list_id_fin = df_fin['id_destino'].tolist()
                if not list_id_fin: 
                    self.txtest_final['state']= 'normal'
                    self.txtest_final['values']= []
                    self.txtest_final['state']= 'readonly'
                    messagebox.showinfo('Info', 'No se encontraron rutas que cumplan origen y tiempo deseado')
                    return
                list_est_fin = [ dict_id_estacion[name_est_fin] for name_est_fin in list_id_fin]
                self.txtest_final['state']= 'normal'
                self.txtest_final['values']= list_est_fin
                self.txtest_final['state']= 'readonly'
        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def user_control(self): 
        self.root.switch_frame(User_options)

    def register_new_trip(self):         
        global supertemporalUser
        lugar_valor    = str(self.txtlugar.get())
        est_origen_val = str(self.txtest_origen.get()) 
        est_fin_val    = str(self.txtest_final.get())
        int_hour       = int(self.hour_sb.get())
        int_minutes    = int(self.min_sb.get())
        if lugar_valor=="" or est_origen_val=="" or est_fin_val=="" or int_hour=="" or int_minutes=="": 
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else: 
            if not supertemporalUser: 
                messagebox.showerror("Error", "El usuario debería estar logueado")
                self.root.switch_frame(Login_window)
                return 
            else: 

                actual_time = datetime.now()
                tot_recorrido = 3600*int_hour +60*int_minutes
                final_time  = actual_time + timedelta(seconds=tot_recorrido)
                from base_queries import carga_viaje
                carga_viaje(dict_estacion_id[est_origen_val], dict_estacion_id[est_fin_val], 
                              actual_time, final_time, supertemporalUser)
                from base_queries import actualizar_tiempo
                if self.roundTrip: 
                    actualizar_tiempo(dict_estacion_id[est_origen_val], dict_estacion_id[est_fin_val], (3600*int_hour +60*int_minutes)/2)
                    actualizar_tiempo(dict_estacion_id[est_origen_val], dict_estacion_id[est_fin_val], (3600*int_hour +60*int_minutes)/2)
                else:
                    actualizar_tiempo(dict_estacion_id[est_origen_val], dict_estacion_id[est_fin_val], 3600*int_hour +60*int_minutes)   
        messagebox.showinfo("Info", "Viaje Registrado")
        self.root.switch_frame(User_options)


class Search_estations(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=250, y=100, width= 300, height=350)

        get_str = Label(frame, text="Estaciones cercanas", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=30, y=30)

        #Label 
        lugar=Label(frame, text="Elegir Lugar de origen", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        lugar.place(x=40, y=70)

        self.txtlugar = ttk.Combobox(frame, state="readonly",values=[])
        self.txtlugar.place(x=40, y=100, width=240)
        self.txtlugar.bind('<Enter>', self.update_place)

        #Login Button
        registerbtn=Button(frame,command=self.get_estations, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=80, y=150, width=140, height=35)

        exitbtn=Button(frame,command=self.user_control, text="Ir a Panel",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=80, y=200, width=140, height=35)


    def update_place(self, event):
        if supertemporalUser: 
            from base_queries import  lugares_guardados_nombres
            listplaces= lugares_guardados_nombres(supertemporalUser)
            self.txtlugar['state']= 'normal'
            self.txtlugar['values']= listplaces
            self.txtlugar['state']= 'readonly'
        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def get_estations(self): 
        if self.txtlugar.get()=="": 
            messagebox.showerror("Error", "Debes llenar todos los campos")
            return
        if supertemporalUser: 
            newWindow = Toplevel(self.root)
            Frame.__init__(self)
            newWindow.geometry('600x400+200+100')
            newWindow.title('Tabla')
            f = Frame(newWindow)
            f.pack(fill=BOTH,expand=1)
            lugar_valor = self.txtlugar.get() 
            from base_queries import estaciones_mas_cercanas   
            df_est= estaciones_mas_cercanas(supertemporalUser, lugar_valor)  
            df_est.drop('_id', axis=1, inplace=True)
            pt = Table(f, dataframe=df_est,showtoolbar=True, showstatusbar=True)
            pt.show()

        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def user_control(self): 
        self.root.switch_frame(User_options)

      

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(Login_window)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()