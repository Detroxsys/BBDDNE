#Interfaz Grafica 
from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import *

#Python Manipulations
import pandas as pd 
import numpy as np
from pandastable import Table, TableModel 
from datetime import datetime, timedelta

#Usuario logueado en cache
superUser=None
isAdmin = False

class MakePedido_window(Frame):
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
        self.frame = Frame(self.root, bg="white")
        self.frame.place(x=250, y=180, width= 600, height=500)


        logo = Image.open("img/logo.png")
        logo = logo.resize((200,200), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(logo)
        lbllogo=Label(self.frame, image=self.photoImage1, bg="white", borderwidth=0)
        lbllogo.place(x=10, y=10, width=200, height=200)

        get_str = Label(self.frame, text="Pedido", font =("sans-serif", 40, "bold"), fg="darkorange", bg="white")
        get_str.place(x=250, y=40)
        
        #Label 

        
        nombre=Label(self.frame, text="Nombre", font =("sans-serif", 13, "bold"), fg="teal", bg="white")
        nombre.place(x=220, y=130)

        self.txtnombre = ttk.Combobox(self.frame, font =("sans-serif", 13, "bold"), state="readonly",values=["Jamon", "Pollo"])
        self.txtnombre.place(x=220, y=150, width=100)

        cantidad=Label(self.frame, text="Cantidad", font =("sans-serif", 13, "bold"), fg="teal", bg="white")
        cantidad.place(x=350, y=130)

        self.txtcantidad = ttk.Entry(self.frame, font =("sans-serif", 13, "bold"))
        self.txtcantidad.place(x=350, y=150, width=100)

        aggbtn=Button(self.frame,command=self.aggToOrder, text="Agregar",font =("calibri", 13, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        aggbtn.place(x=480, y=145, width=100, height=35)

        #Login Button
        exitbtn=Button(self.frame,command=self.exit, text="Salir",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        exitbtn.place(x=130, y=450, width=140, height=35)

        #Register Button
        makeOrderbtn=Button(self.frame,command=self.makeOrder, text="Ordenar",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightseagreen")
        makeOrderbtn.place(x=330, y=450, width=140, height=35)

        
        frame2 = Frame(self.frame, bg="white")
        frame2.place(x=50, y=220, width= 500, height=200)

        self.trv=ttk.Treeview(frame2,selectmode='browse')

        self.trv.grid(row=1,column=1,columnspan=4,padx=10,pady=10)
        self.trv["columns"]=("1","2","3")
        self.trv['show']='headings'
        self.trv.column("1",width=160,anchor='c')
        self.trv.column("2",width=160,anchor='c')
        self.trv.column("3",width=160,anchor='c')
        self.trv.heading("1",text="Producto")
        self.trv.heading("2",text="Cantidad")
        self.trv.heading("3",text="Subtotal")
        
        self.cont_iid=1
        self.trv.pack(side ='right')
        verscrlbar = ttk.Scrollbar(frame2,
                           orient ="vertical",
                           command = self.trv.yview)
        self.trv.configure(xscrollcommand = verscrlbar.set)
        verscrlbar.pack(side ='right', fill ='x')


        frame3 = Frame(self.root, bg="white")
        frame3.place(x=900, y=180, width= 300, height=500)
        get_str3 = Label(frame3, text="Fecha Entrega", font =("sans-serif", 20, "bold"), fg="darkorange", bg="white")
        get_str3.place(x=20, y=20)

        cal = Calendar(
                frame3, 
                selectmode="day", 
                year=2022, 
                month=5,
                day=6
                )
        cal.pack(pady=60)

        self.hour_sb = ttk.Spinbox(frame3,from_=7,to=20,width=40, wrap=True, state="readonly",font=('sans-serif', 20),justify=CENTER)
        self.min_sb = ttk.Spinbox(frame3,from_=0,to=59,width=40, wrap=True, state="readonly", font=('sans-serif', 20),justify=CENTER)
        self.hour_sb.place(x=90,y= 275, width=50, height=25)
        self.min_sb.place(x=160,y= 275, width=50, height=25)
        msg = Label(frame3, text="Hora     Minuto",font=("sans-serif", 12, "bold"),fg="teal", bg = "white")
        msg.place(x=100, y=300)

    def aggToOrder(self): 
        producto = self.txtnombre.get()
        cantidad = self.txtcantidad.get()
        self.trv.insert("",'end',
                values=(producto, cantidad, 30.0))
        self.cont_iid +=1
        total=Label(self.frame, text=f"Total: 30.0", font =("sans-serif", 14, "bold"), fg="black", bg="white")
        total.place(x=250, y=190)



    def makeOrder(self): 
        pass
    
    def exit(self): 
        self.root.switch_frame(RegisterBox_window)

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(MakePedido_window)

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