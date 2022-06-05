#Interfaz Grafica 
from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
from tkinter import simpledialog

#Python Manipulations
import pandas as pd 
import numpy as np
from pandastable import Table, TableModel 
from datetime import datetime, timedelta

#Usuario logueado en cache
superUser=None
isAdmin = False

#INTERFAZ GRAFICA 

#Login de Usuario
class Login_window(Frame):
    def __init__(self, root):
        self.root=root
        #self.root.wm_attributes("-transparentcolor", 'black')
        self.root.title("EL VOLOVAN")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="white")
        frame.place(x=450, y=180, width= 600, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=20, y=20, width=200, height=200)



        get_str = Label(frame, text="Login", font =("sans-serif", 80, "bold"), fg="darkorange", bg="white")
        get_str.place(x=225, y=75)
        
        #Label 
        user=Label(frame, text="RFC", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        user.place(x=100, y=240)

        self.txtuser = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtuser.place(x=300, y=240, width=250)

        password=Label(frame, text="Contraseña", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        password.place(x=100, y=290)

        self.txtpassword = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtpassword.place(x=300, y=290, width=250)


        #Login Button
        loginbtn=Button(frame,command=self.login, text="Iniciar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        loginbtn.place(x=140, y=400, width=120, height=35)

        #Register Button
        registerbtn=Button(frame,command=self.register_window, text="Registrar",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=360, y=400, width=120, height=35)

    def register_window(self): 
        self.root.switch_frame(Register_window)

    def login(self): 
        if self.txtuser.get()=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        else: 
            usernameVal = self.txtuser.get()
            existe_user = True
            if existe_user:
                global supertemporalUser 
                supertemporalUser=usernameVal
                messagebox.showinfo("Success", f"Bienvenido {supertemporalUser}")
                self.root.switch_frame(RegisterBox_window)
            else: 
                self.txtuser.delete(0,END)
                self.txtpassword.delete(0, END)
                messagebox.showerror("Error", "Usuario no existe,debe registrarse")

#Registrar Nuevo Usuario
class Register_window(Frame):
    def __init__(self, root):
        self.root=root
        #self.root.wm_attributes("-transparentcolor", 'black')
        self.root.title("EL VOLOVAN")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="white")
        frame.place(x=250, y=180, width= 900, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=20, y=20, width=200, height=200)



        get_str = Label(frame, text="Registrarse", font =("sans-serif", 60, "bold"), fg="darkorange", bg="white")
        get_str.place(x=250, y=75)
        
        #Label 
        name=Label(frame, text="Nombre", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        name.place(x=20, y=240)

        self.txtname = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtname.place(x=170, y=240, width=250)

        lastname=Label(frame, text="Apellidos", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        lastname.place(x=450, y=240)

        self.txtlastname = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtlastname.place(x=620, y=240, width=250)

        user=Label(frame, text="RFC", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        user.place(x=20, y=320)

        self.txtuser = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtuser.place(x=170, y=320, width=250)

        password=Label(frame, text="Contraseña", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        password.place(x=450, y=320)

        self.txtpassword = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtpassword.place(x=620, y=320, width=250)


        #Login Button
        loginbtn=Button(frame,command=self.login, text="Ir a Login",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        loginbtn.place(x=240, y=400, width=120, height=35)

        #Register Button
        registerbtn=Button(frame,command=self.register_user, text="Registrar",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerbtn.place(x=560, y=400, width=120, height=35)

    def register_user(self): 
        self.root.switch_frame(Admin_window)
        pass

    def login(self): 
        self.root.switch_frame(Login_window)


#Registrar Nuevo Usuario
class Admin_window(Frame):
    def __init__(self, root):
        self.root=root
        #self.root.wm_attributes("-transparentcolor", 'black')
        self.root.title("EL VOLOVAN")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="white")
        frame.place(x=450, y=180, width= 600, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=20, y=20, width=200, height=200)

        get_str = Label(frame, text="Opciones\npara Admin", font =("sans-serif", 50, "bold"), fg="darkorange", bg="white")
        get_str.place(x=225, y=45)
        
        #Label 
        initdaybtn = Button(frame,command=self.gotoInitDay, text="Iniciar Día",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        initdaybtn.place(x=125, y= 230, width=150, height=50)

        enddaybtn = Button(frame,command=self.gotoEndDay, text="Finalizar Día",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        enddaybtn.place(x=325, y= 230, width=150, height=50)


        registerBoxbtn = Button(frame,command=self.gotoRegisterBox, text="Usar Caja",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        registerBoxbtn.place(x=125, y= 290, width=150, height=50)

        makeReportbtn = Button(frame,command=self.gotoMakeReport, text="Hacer Reporte",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        makeReportbtn.place(x=325, y= 290, width=150, height=50)

        newProductbtn = Button(frame,command=self.gotoNewProduct, text="Nuevo Producto",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        newProductbtn.place(x=125, y= 350, width=150, height=50)

        produccionbtn = Button(frame,command=self.production, text="Producción",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        produccionbtn.place(x=325, y= 350, width=150, height=50)



        exitbtn = Button(frame,command=self.exit, text="Salir",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=15, y= 420, width=100, height=50)


    def gotoRegisterBox(self): 
        self.root.switch_frame(RegisterBox_window)

    def gotoMakeReport(self): 
        pass

    def gotoNewProduct(self): 
        self.root.switch_frame(New_Product_window)

    def production(self):
        self.root.switch_frame(Production_window)

    def gotoInitDay(self): 
        pass

    def gotoEndDay(self): 
        pass

    def exit(self): 
        self.root.switch_frame(Login_window)


class RegisterBox_window(Frame):
    def __init__(self, root):
        self.root=root
        #self.root.wm_attributes("-transparentcolor", 'black')
        self.root.title("EL VOLOVAN")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="white")
        frame.place(x=450, y=180, width= 600, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=20, y=20, width=200, height=200)

        get_str = Label(frame, text="Cajara\nRegistradora", font =("sans-serif", 40, "bold"), fg="darkorange", bg="white")
        get_str.place(x=225, y=45)
        
        #Label 
        cajaStorebtn = Button(frame,command=self.gotoVentas, text="Ir a Caja",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        cajaStorebtn.place(x=50, y= 230, width=150, height=50)

        makePedidosbtn = Button(frame,command=self.gotoMakePedidos, text="Hacer Pedidos",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        makePedidosbtn.place(x=225, y= 230, width=150, height=50)

        getPedidosbtn = Button(frame,command=self.gotoGetPedidos, text="Ver Entregas",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        getPedidosbtn.place(x=400, y= 230, width=150, height=50)

        extraIngbtn = Button(frame,command=self.gotoIngresos, text="Ingreso Extra",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        extraIngbtn.place(x=125, y= 290, width=150, height=50)

        extraGastbtn = Button(frame,command=self.gotoGastos, text="Gasto Extra",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        extraGastbtn.place(x=325, y= 290, width=150, height=50)

        checkIngbtn = Button(frame,command=self.df_checkIngresos, text="Revisar Ingreso Extra",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        checkIngbtn.place(x=75, y= 350, width=200, height=50)

        checkGastbtn = Button(frame,command=self.df_checkGastos, text="Revisar Gasto Extra",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        checkGastbtn.place(x=325, y= 350, width=200, height=50)

        exitbtn = Button(frame,command=self.exit, text="Salir",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=15, y= 420, width=100, height=50)


    def gotoVentas(self): 
        pass

    def gotoIngresos(self): 
        pass

    def gotoGastos(self): 
        pass

    def df_checkIngresos(self): 
        pass

    def df_checkGastos(self): 
        pass

    def gotoMakePedidos(self): 
        pass

    def gotoGetPedidos(self): 
        pass

    def exit(self): 
        self.root.switch_frame(Login_window)


#Registrar Nuevo Usuario
class New_Product_window(Frame):
    def __init__(self, root):
        self.root=root
        #self.root.wm_attributes("-transparentcolor", 'black')
        self.root.title("EL VOLOVAN")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="white")
        frame.place(x=250, y=180, width= 900, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=20, y=20, width=200, height=200)



        get_str = Label(frame, text="Nuevo\nProducto", font =("sans-serif", 50, "bold"), fg="darkorange", bg="white")
        get_str.place(x=250, y=40)
        
        #Label 
        name=Label(frame, text="Nombre", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        name.place(x=20, y=240)

        self.txtname = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtname.place(x=170, y=240, width=250)

        description=Label(frame, text="Descripción", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        description.place(x=450, y=240)

        self.txtdescription = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtdescription.place(x=620, y=240, width=250)
        
        precioUnitario=Label(frame, text="Precio", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        precioUnitario.place(x=20, y=320)

        self.txtprecioUnitario = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtprecioUnitario.place(x=170, y=320, width=250)

        categoria=Label(frame, text="Categoria", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        categoria.place(x=450, y=320)

        self.txtcategoria = ttk.Combobox(frame,font =("sans-serif", 20, "bold"), state="readonly",values=["volovan salado", "volovan dulce", "especial"])
        self.txtcategoria.place(x=620, y=320, width=250)

        #Login Button
        createProductbtn=Button(frame,command=self.createProduct, text="Crear Producto",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        createProductbtn.place(x=230, y=400, width=140, height=35)

        #Register Button
        exitbtn=Button(frame,command=self.exit, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=530, y=400, width=140, height=35)

    def exit(self): 
        self.root.switch_frame(Admin_window)

    def createProduct(self):
        pass 

#Agregando producción
class Production_window(Frame):
    def __init__(self, root):
        self.root=root
        #self.root.wm_attributes("-transparentcolor", 'black')
        self.root.title("EL VOLOVAN")
        self.root.geometry("1550x800+0+0")
        bg = Image.open("img/background.jpg")
        bg = bg.resize( (1550, 800), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(bg)
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="white")
        frame.place(x=450, y=180, width= 600, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=20, y=20, width=200, height=200)



        get_str = Label(frame, text="Producción", font =("sans-serif", 40, "bold"), fg="darkorange", bg="white")
        get_str.place(x=250, y=50)
        
        #Label 

        
        nombre=Label(frame, text="Nombre", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        nombre.place(x=100, y=240)

        self.txtnombre = ttk.Combobox(frame, font =("sans-serif", 20, "bold"), state="readonly",values=[])
        self.txtnombre.place(x=300, y=240, width=250)

        cantidad=Label(frame, text="Cantidad", font =("sans-serif", 20, "bold"), fg="teal", bg="white")
        cantidad.place(x=100, y=290)

        self.txtcantidad = ttk.Entry(frame, font =("sans-serif", 20, "bold"))
        self.txtcantidad.place(x=300, y=290, width=250)


        #Login Button
        exitbtn=Button(frame,command=self.exit, text="Salir",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=130, y=400, width=140, height=35)

        #Register Button
        aggProdbtn=Button(frame,command=self.agregarProduccion, text="Agregar",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        aggProdbtn.place(x=330, y=400, width=140, height=35)

    def agregarProduccion(self): 
        pass
        

    def exit(self): 
        self.root.switch_frame(Admin_window)

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