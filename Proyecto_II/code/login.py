from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
import pandas as pd 
from pandastable import Table, TableModel 
dfsuper = pd.read_csv('Proyecto_II/data/DatosBBDDE_test.csv')
universal_categorias = ['Fatansia', 'Ciencia Ficcion', 'Horror', 'AutoAyuda', 'Random']

class Login_window(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="Proyecto_II/img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width= 340, height=400)

        img1 = Image.open("Proyecto_II/img/img_logo.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoImage1, bg="black", borderwidth=0)
        lblimg1.place(x=730, y=175, width=100, height=100)

        get_str = Label(frame, text="Login", font =("calibri", 20, "bold"), fg="lightblue", bg="black")
        get_str.place(x=125, y=100)
        
        #Label 
        username=Label(frame, text="Username", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        username.place(x=70, y=155)

        self.txtuser = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=240)

        #Icon Image
        img2 = Image.open("Proyecto_II/img/img_user.png")
        img2 = img2.resize((25,25), Image.ANTIALIAS)
        self.photoImage2= ImageTk.PhotoImage(img2)
        lblimg1=Label(image=self.photoImage2, bg="black", borderwidth=0)
        lblimg1.place(x=650, y=323, width=25, height=25)

        #Login Button
        loginbtn=Button(frame,command=self.login, text="Login",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        loginbtn.place(x=110, y=230, width=120, height=35)

        #Register Button
        registerbtn=Button(frame,command=self.register_window, text="Registrate",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightblue")
        registerbtn.place(x=110, y=280, width=120, height=35)

    def register_window(self): 
        self.root.switch_frame(Register)

    def login(self): 
        if self.txtuser.get()=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        elif self.txtuser.get()=="admin":
            self.root.switch_frame(Admin_options)
            messagebox.showinfo("Success", "Bienvenido Administrador")
        else: 
            self.root.switch_frame(Updating_books)
            messagebox.showinfo("Success", "Bienvenido Usuario")



class Register(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="Proyecto_II/img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width= 340, height=600)

        img1 = Image.open("Proyecto_II/img/img_logo.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(img1)
        lblimg=Label(image=self.photoImage1, bg="black", borderwidth=0)
        lblimg.place(x=730, y=175, width=100, height=100)

        get_str = Label(frame, text="Registrate/Actualiza", font =("calibri", 20, "bold"), fg="lightblue", bg="black")
        get_str.place(x=60, y=100)

        #Label 
        username=Label(frame, text="Username", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        username.place(x=70, y=155)

        self.txtuser = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=240)

        name= Label(frame, text="Nombre", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        name.place(x=70, y=215)

        self.txtname = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtname.place(x=40, y=240, width=240)

        countrie=Label(frame, text="País", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        countrie.place(x=70, y=275)

        self.txtcountrie = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtcountrie.place(x=40, y=300, width=240)

        membership=Label(frame, text="Membresía", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        membership.place(x=70, y=335)

        self.txtmembership = ttk.Combobox(frame, state="readonly",values=["Premium", "Regular", "Básico", "Gratis"])
        self.txtmembership.place(x=40, y=370, width=240)

        #Icon Image
        img2 = Image.open("Proyecto_II/img/img_user.png")
        img2 = img2.resize((25,25), Image.ANTIALIAS)
        self.photoImage2= ImageTk.PhotoImage(img2)
        lblimg1=Label(image=self.photoImage2, bg="black", borderwidth=0)
        lblimg1.place(x=650, y=323, width=25, height=25)

        #Login Button
        registerbtn=Button(frame,command=self.register, text="Registrar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        registerbtn.place(x=40, y=420, width=120, height=35)

        loginnowbtn=Button(frame,command=self.login_window, text="Ir a Login",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        loginnowbtn.place(x=170, y=420, width=120, height=35)

    def login_window(self): 
        self.root.switch_frame(Login_window)

    def register(self): 
        self.root.switch_frame(Updating_books)
        usernameVal= self.txtuser.get() 
        countrieVal= self.txtcountrie.get() 
        membershipVal= self.txtmembership.get()
        nameVal      =  self.txtname.get()
        if usernameVal=="" or membershipVal=="" or countrieVal=="" or nameVal=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else:
            messagebox.showinfo("Success", "Registro Exitoso")


class Updating_books(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="Proyecto_II/img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width= 340, height=600)

        img1 = Image.open("Proyecto_II/img/img_logo.png")
        img1 = img1.resize((100,100), Image.ANTIALIAS)
        self.photoImage1= ImageTk.PhotoImage(img1)
        lblimg=Label(image=self.photoImage1, bg="black", borderwidth=0)
        lblimg.place(x=730, y=175, width=100, height=100)

        get_str = Label(frame, text="Rankear Libro", font =("calibri", 20, "bold"), fg="lightblue", bg="black")
        get_str.place(x=60, y=100)

        #Label 
        bookname=Label(frame, text="Libro", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        bookname.place(x=70, y=155)

        self.txtbook = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtbook.place(x=40, y=180, width=240)

        author=Label(frame, text="Autor", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        author.place(x=70, y=215)

        self.txtauthor = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.txtauthor.place(x=40, y=240, width=240)

        rating=Label(frame, text="Rating", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        rating.place(x=70, y=275)

        self.txtrating = ttk.Combobox(frame, state="readonly",values=[1,2,3,4,5,6,7,8,9,10])
        self.txtrating.place(x=40, y=300, width=240)

        category=Label(frame, text="Categoría", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        category.place(x=70, y=330)

        self.txtcategory = ttk.Combobox(frame, state="readonly", values=universal_categorias)
        self.txtcategory.place(x=40, y=355, width=240)


        #Login Button
        submitbtn=Button(frame,command=self.ranking, text="Rankear",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        submitbtn.place(x=110, y=410, width=120, height=35)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightblue")
        exitbtn.place(x=110, y=460, width=120, height=35)

    def login_window(self): 
        self.root.switch_frame(Login_window)

    def ranking(self): 
        booknameVal= self.txtbook.get() 
        authorVal= self.txtauthor.get() 
        rateVal= self.txtrating.get()
        categoryVal = self.txtcategory.get()
        if booknameVal=="" or authorVal=="" or rateVal=="" or categoryVal=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else:
            messagebox.showinfo("Success", "Libro rankeado")


class Admin_options(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="Proyecto_II/img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=300, y=200, width= 900, height=400)

        get_str = Label(frame, text="Administrador Panel", font =("calibri", 20, "bold"), fg="lightblue", bg="black")
        get_str.place(x=30, y=50)

        #Label 
        categoryprefer=Label(frame, text="Categoría Preferida de:", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        categoryprefer.place(x=70, y=100)

        self.username = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.username.place(x=400, y=100, width=240)

        clientsperbook=Label(frame, text="Clientes que más les gusta el libro:", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        clientsperbook.place(x=70, y=140)

        self.bookname = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.bookname.place(x=400, y=140, width=240)

        bookspercategory=Label(frame, text="Libros destcadas de la categoría:", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        bookspercategory.place(x=70, y=180)

        self.categoryname = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.categoryname.place(x=400, y=180, width=240)

        #Login Button
        q1=Button(frame,command=self.query1, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q1.place(x=650, y=100, width=120, height=30)

        q2=Button(frame,command=self.query2, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q2.place(x=650, y=140, width=120, height=30)

        q2=Button(frame,command=self.query3, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q2.place(x=650, y=180, width=120, height=30)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightblue")
        exitbtn.place(x=50, y=350, width=120, height=30)
    
    def query1(self):
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        df = dfsuper.copy()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()

    def query2(self): 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        df = dfsuper.copy()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
    def query3(self): 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)
        df = dfsuper.copy()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()


    def login_window(self): 
        self.root.switch_frame(Login_window)

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