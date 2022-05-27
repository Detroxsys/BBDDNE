from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
import requests
import urllib.parse
from tkinter import messagebox
import pandas as pd 
import numpy as np
from pandastable import Table, TableModel 
from bson.objectid import ObjectId
from neomodel import db, clear_neo4j_database
from datetime import datetime, timedelta
import base_queries

# es importante mapear al puerto usando -p 27017:27017 al construir el contenedor o en el docker-compose.yml

# Probando conexión

# Carga de las estaciones
"""
estaciones = pd.read_csv('data/estaciones.csv')
dict_id_estacion = dict(zip(estaciones.id, estaciones.name))
dict_estacion_id = dict(zip(estaciones.name, estaciones.id))
"""
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
        frame.place(x=600, y=20, width= 340, height=400)

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
            #from base_queries import existe_usuario
            existe_user = base_queries.CheckUser(usernameVal)
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
        self.root.title("Registrar")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=600, y=20, width= 340, height=400)

        img1 = Image.open("img/img_logo.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(img1)
        lblimg1=Label(frame, image=self.photoImage1, bg="black", borderwidth=0)
        lblimg1.place(x=120, y=20, width=100, height=100)

        get_str = Label(frame, text="Registrate", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
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
        registerbtn=Button(frame,command=self.register, text="Registrar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=110, y=230, width=120, height=35)

        loginnowbtn=Button(frame,command=self.login_window, text="Ir a Login",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        loginnowbtn.place(x=110, y=280, width=120, height=35)

    def login_window(self): 
        self.root.switch_frame(Login_window)

    def register(self):         
        usernameVal  = self.txtuser.get() 
        if usernameVal=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else:
            #from base_queries import existe_usuario
            existe_user = base_queries.CheckUser(usernameVal)
            if existe_user:
                messagebox.showerror("Error", "El usuario ya existe, favor de hacer login")
                self.root.switch_frame(Login_window)
            else: 
                global supertemporalUser
                supertemporalUser=usernameVal
                base_queries.AltaUsuario(usernameVal)
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
        frame.place(x=125, y=20, width= 1300, height=700)

        get_str = Label(frame, text="Panel Usuario", font =("calibri", 20, "bold"), fg="lightseagreen", bg="black")
        get_str.place(x=20, y=20)


        #Dada un estado y una producto obtener tienda que lo tenga 
        chooseStoreQ1=Label(frame, text="Buscar Tienda", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStoreQ1.place(x=40, y=70)

        chooseStateQ1=Label(frame, text="Elegir Estado", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStateQ1.place(x=40, y=100)

        self.txtchooseStateQ1 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_estados())
        self.txtchooseStateQ1.place(x=40, y=140, width=200)

        chooseProductQ1=Label(frame, text="Elegir Producto", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProductQ1.place(x=40, y=180)

        self.txtchooseProductQ1 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_productos())
        self.txtchooseProductQ1.place(x=40, y=220, width=200)

        q1btn=Button(frame,command= self.q1Consulta, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        q1btn.place(x=40, y=270, width=180, height=50)

        #Dada un estado y tienda verificar si tiene algun incumplimiento de un producto
        chooseProductQ2=Label(frame, text="Verificar Tienda", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProductQ2.place(x=260, y=70)

        chooseStateQ2=Label(frame, text="Elegir Estado", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStateQ2.place(x=260, y=100)

        self.txtchooseStateQ2 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_estados())
        self.txtchooseStateQ2.place(x=260, y=140, width=200)
        self.txtchooseStateQ2.bind('<<ComboboxSelected>>', self.update_storeQ2)

        chooseStoreQ2=Label(frame, text="Elegir Tienda", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStoreQ2.place(x=260, y=180)

        self.txtchooseStoreQ2 = ttk.Combobox(frame, state="readonly",values=[])
        self.txtchooseStoreQ2.place(x=260, y=220, width=200)

        q2btn=Button(frame,command= self.q2Consulta, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        q2btn.place(x=260, y=270, width=180, height=50)

        #Dada un estado y un producto alternativa sin incumplimiento
        chooseStoreQ3=Label(frame, text="Tienda Sin incumplimientos", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStoreQ3.place(x=480, y=70)

        chooseStateQ3=Label(frame, text="Elegir Estado", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStateQ3.place(x=480, y=100)

        self.txtchooseStateQ3 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_estados())
        self.txtchooseStateQ3.place(x=480, y=140, width=200)

        chooseProductQ3=Label(frame, text="Elegir Producto", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProductQ3.place(x=480, y=180)

        self.txtchooseProductQ3 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_productos())
        self.txtchooseProductQ3.place(x=480, y=220, width=200)

        q3btn=Button(frame,command= self.q3Consulta, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        q3btn.place(x=480, y=270, width=180, height=50)
        
        #Recomendar un producto a un usuario segun lo que otros han comprado
        chooseProductQ7=Label(frame, text="Recomendar similares", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProductQ7.place(x=720, y=70)

        chooseProdQ7=Label(frame, text="Elegir Producto", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProdQ7.place(x=720, y=100)

        self.txtchooseProductQ7 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_productos())
        self.txtchooseProductQ7.place(x=720, y=140, width=200)

        q7btn=Button(frame,command= self.q7Consulta, text="Recomendar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        q7btn.place(x=720, y=180, width=180, height=50)
        

        #Dada un estado y tienda verificar si tiene algun incumplimiento de un producto
        chooseProductQ4=Label(frame, text="Comprar Producto", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProductQ4.place(x=960, y=70)

        chooseStateQ4=Label(frame, text="Elegir Estado", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStateQ4.place(x=960, y=100)

        self.txtchooseStateQ4 = ttk.Combobox(frame, state="readonly",values=base_queries.todos_estados())
        self.txtchooseStateQ4.place(x=960, y=140, width=200)
        self.txtchooseStateQ4.bind('<<ComboboxSelected>>', self.update_storeQ4)

        chooseStoreQ4=Label(frame, text="Elegir Tienda", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseStoreQ4.place(x=960, y=180)

        self.txtchooseStoreQ4 = ttk.Combobox(frame, state="readonly",values=[])
        self.txtchooseStoreQ4.place(x=960, y=220, width=200)
        self.txtchooseStoreQ4.bind('<<ComboboxSelected>>', self.update_productQ4)

        chooseProductQ4=Label(frame, text="Elegir Producto", font =("calibri", 15, "bold"), fg="lightseagreen", bg="black")
        chooseProductQ4.place(x=960, y=260)

        self.txtchooseProductQ4 = ttk.Combobox(frame, state="readonly",values=[])
        self.txtchooseProductQ4.place(x=960, y=300, width=200)

        q4btn=Button(frame,command= self.q4Consulta, text="Comprar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        q4btn.place(x=960, y=340, width=180, height=50)


        #Botones de Consultas
        viewProducts=Button(frame,command= self.q5Consulta, text="Ver Mis Productos",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        viewProducts.place(x=40, y=420, width=210, height=50)

        #viewStoresbtn=Button(frame,command="", text="Ver Mis Tiendas",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        #viewStoresbtn.place(x=260, y=360, width=180, height=50)

        viewBestStoresbtn=Button(frame,command = self.q8Consulta, text="Tasa de Incumplimiento por Estado",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        viewBestStoresbtn.place(x=480, y=420, width=500, height=50)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=550, y=600, width=120, height=50)

    def login_window(self): 
        global supertemporalUser
        supertemporalUser = None
        self.root.switch_frame(Login_window)

    def update_storeQ2(self, event): 
        if self.txtchooseStateQ2.get()=="": 
            self.txtchooseStoreQ2['state']= 'normal'
            self.txtchooseStoreQ2['values']= []
            self.txtchooseStoreQ2.set("")
            self.txtchooseStoreQ2['state']= 'readonly' 
            return
        if supertemporalUser: 
            estado = str(self.txtchooseStateQ2.get())
            list_est = base_queries.tiendas_en_estado(estado) 
            self.txtchooseStoreQ2['state']= 'normal'
            self.txtchooseStoreQ2['values']= list_est
            self.txtchooseStoreQ2['state']= 'readonly'
            return

        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def update_productQ4(self, event): 
        if self.txtchooseStoreQ4.get()=="": 
            self.txtchooseProductQ4['state']= 'normal'
            self.txtchooseProductQ4['values']= []
            self.txtchooseProductQ4.set("")
            self.txtchooseProductQ4['state']= 'readonly' 
            return
        if supertemporalUser: 
            self.txtchooseProductQ4.set("")
            tienda = str(self.txtchooseStoreQ4.get())
            list_est = base_queries.productos_en_tienda(tienda) 
            self.txtchooseProductQ4['state']= 'normal'
            self.txtchooseProductQ4['values']= list_est
            self.txtchooseProductQ4['state']= 'readonly'
            return

        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def update_storeQ4(self, event): 
        if self.txtchooseStateQ4.get()=="": 
            self.txtchooseStoreQ4['state']= 'normal'
            self.txtchooseStoreQ4['values']= []
            self.txtchooseStoreQ4.set("")
            self.txtchooseStoreQ4['state']= 'readonly' 
            return
        if supertemporalUser: 
            self.txtchooseStoreQ4.set("")
            estado = str(self.txtchooseStateQ4.get())
            list_est = base_queries.tiendas_en_estado(estado) 
            self.txtchooseStoreQ4['state']= 'normal'
            self.txtchooseStoreQ4['values']= list_est
            self.txtchooseStoreQ4['state']= 'readonly'
            return

        else: 
            messagebox.showerror("Error", "El usuario no esta logueado")
            self.root.switch_frame(Login_window)

    def q1Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return
        estado = self.txtchooseStateQ1.get()
        producto = self.txtchooseProductQ1.get()
        if estado=="" or producto == "":
            messagebox.showerror("Error", "No se eligieron producto o estado")
            return 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        res = base_queries.q1_hallar_tienda(estado, producto)
        res = pd.DataFrame(res, columns=['Tiendas con el producto'])
        pt = Table(f, dataframe=res,showtoolbar=True, showstatusbar=True)
        pt.show()

    def q2Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return
        estado = self.txtchooseStateQ2.get()
        tienda = self.txtchooseStoreQ2.get()
        if estado=="" or tienda == "":
            messagebox.showerror("Error", "No se eligieron tienda o estado")
            return 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        res = base_queries.q2_incumplimientos(estado, tienda)
        res = pd.DataFrame(res, columns=['Productos con Incumplimiento'])
        pt = Table(f, dataframe=res,showtoolbar=True, showstatusbar=True)
        pt.show()

    def q3Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return
        estado = self.txtchooseStateQ3.get()
        producto = self.txtchooseProductQ3.get()
        if estado=="" or producto == "":
            messagebox.showerror("Error", "No se eligieron producto o estado")
            return 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        res = base_queries.q3_alternativas(estado, producto)
        res = pd.DataFrame(res, columns=['Tiendas con el producto'])
        pt = Table(f, dataframe=res,showtoolbar=True, showstatusbar=True)
        pt.show()

    def q4Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return
        estado = self.txtchooseStateQ4.get()
        tienda = self.txtchooseStateQ4.get()
        producto = self.txtchooseProductQ4.get()
        if estado=="" or tienda == "" or producto == "":
            messagebox.showerror("Error", "No se eligieron producto, tienda o estado")
            return 
        base_queries.q4_comprar(supertemporalUser, producto, tienda)
        return 

    def q5Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return

        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        res = base_queries.q5_registros(supertemporalUser)
        pt = Table(f, dataframe=res,showtoolbar=True, showstatusbar=True)
        pt.show()

    def q7Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return
        producto = self.txtchooseProductQ7.get()
        if producto=="" : 
            messagebox.showerror("Error", "No se eligio producto")
            return 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        res = base_queries.q7_recomendar(producto)
        print(res)
        res = pd.DataFrame(res)
        pt = Table(f, dataframe=res,showtoolbar=True, showstatusbar=True)
        pt.show()


    def q8Consulta(self): 
        global supertemporalUser
        if supertemporalUser==None: 
            self.root.switch_frame(Login_window)
            messagebox.showerror("Error", "No hay usuario registrado")
            return
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        res = base_queries.q8_incumpliminetos()
        pt = Table(f, dataframe=res,showtoolbar=True, showstatusbar=True)
        pt.show()

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