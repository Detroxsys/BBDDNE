from email import message
from tkinter import* #pip install tk 
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
import pandas as pd 
import numpy as np
from cassandra.cluster import Cluster
from pandastable import Table, TableModel 

dfsuper = pd.read_csv('DatosBBDDE_test.csv')
universal_categorias = ['Académico', 'Autoayuda', 'Autobiografía', 'Ciencia Ficción','Cuento', 'Divulgación',
                        'Drama', 'Ensayo', 'Fantasia', 'Fantasia Oscura', 'Ficcion Distópica', 'Ficción Doméstica',
                        'Misterio', 'Novela', 'Novela Filosófica', 'Novela Realista', 'Realismo Mágico', 'Suspenso',
                        'Teatro', 'Terror', 'Thriller', 'Thriller histórico', 'Tragedia', 'Wuxia', 'Xianxia']

#Conexion al cluster
#Es importante haber mapeado el puerto usando -p 9042:9042 al crear el contenedor
cluster = Cluster(['127.0.0.1'], port=9042)
#session = cluster.connect('bdnosql') #El keyspace lo creé desde la terminal
session = cluster.connect()
session.set_keyspace('bd_libros')

supertemporalUser=None
#Ventas de interfaz grafica
class Login_window(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        self.bg = ImageTk.PhotoImage(file="img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width= 340, height=400)

        img1 = Image.open("img/img_logo.png")
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
        img2 = Image.open("img/img_user.png")
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
            usernameVal = self.txtuser.get()
            existe_usuario = session.execute(
                """
                SELECT * FROM libros_por_cliente
                WHERE id_cliente = %s
                LIMIT 1
                """,
                [usernameVal]
            )
            if existe_usuario:
                global supertemporalUser 
                supertemporalUser=usernameVal
                messagebox.showinfo("Success", f"Bienvenido {supertemporalUser}")
                self.root.switch_frame(Updating_books)
            else: 
                self.txtuser.delete(0,END)
                messagebox.showerror("Error", "Usuario no existe,debe registrarse")

class Register(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width= 340, height=600)

        img1 = Image.open("img/img_logo.png")
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
        img2 = Image.open("img/img_user.png")
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
        usernameVal= self.txtuser.get() 
        countrieVal= self.txtcountrie.get() 
        membershipVal= self.txtmembership.get()
        nameVal      =  self.txtname.get()
        if usernameVal=="" or membershipVal=="" or countrieVal=="" or nameVal=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return None
        else:
            existe_usuario = session.execute(
                """
                SELECT * FROM libros_por_cliente
                WHERE id_cliente = %s
                LIMIT 1
                """,
                [usernameVal]
            )
            if existe_usuario:
                messagebox.showerror("Error", "El usuario ya existe, favor de hacer login")
                self.root.switch_frame(Login_window)
            else: 
                session.execute(
                    """
                    INSERT INTO libros_por_cliente
                    (id_cliente, nombre_cliente, pais, membresia)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (usernameVal, nameVal, countrieVal, membershipVal)
                )      
                
                global supertemporalUser
                supertemporalUser=usernameVal
                messagebox.showinfo("Success", f"Registro Exitoso, bienvenido {supertemporalUser}")
                self.root.switch_frame(Updating_books)

class Updating_books(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width= 340, height=600)

        img1 = Image.open("img/img_logo.png")
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


        #Buttons
        submitbtn=Button(frame,command=self.ranking, text="Rankear",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        submitbtn.place(x=110, y=410, width=120, height=35)

        viewbtn=Button(frame,command=self.my_ratings, text="Mis ratings",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        viewbtn.place(x=110, y=460, width=120, height=35)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightblue")
        exitbtn.place(x=110, y=510, width=120, height=35)
    
    def my_ratings(self):
        global supertemporalUser
        if supertemporalUser==None:
            return 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)

        resultado = session.execute(
            """
            SELECT titulo_libro, autor_libro, categoria, calificacion FROM libros_por_cliente
            WHERE id_cliente=%s
            """,
            [supertemporalUser]
        )

        res= pd.DataFrame(resultado.all())
        pt = Table(f, dataframe=res,
                                showtoolbar=True, showstatusbar=True)
        pt.show()

    def login_window(self): 
        global supertemporalUser
        supertemporalUser=None
        self.root.switch_frame(Login_window)

    def ranking(self): 
        global supertemporalUser
        id_cliente = supertemporalUser
        titulo_libro= self.txtbook.get() 
        autor_libro= self.txtauthor.get() 
        calificacion= int(self.txtrating.get())
        categoria = self.txtcategory.get()
        if titulo_libro=="" or autor_libro=="" or calificacion=="" or categoria=="":
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        else:
            if supertemporalUser:
                existe_calif = session.execute(
                    """
                    SELECT categoria, calificacion FROM libros_por_cliente
                    WHERE id_cliente=%s AND titulo_libro=%s  AND autor_libro=%s
                    LIMIT 1
                    """, [id_cliente, titulo_libro, autor_libro])
                info_previa = existe_calif.one()

                if existe_calif:
                    # pedir a usuario confirma que desea cambiar la calificacion
                    confirmacion_del_usuario = messagebox.askyesno(title='Confirmation',
                    message='La calificación ya existe ¿desea actualizar?')  #respuesta del usuario
                    if not confirmacion_del_usuario:
                        self.txtbook.delete(0, END)
                        self.txtauthor.delete(0,END)
                        self.txtrating.set('')
                        self.txtcategory.set('')                        
                        return

                    info_previa = existe_calif.one()

                    #Borrar la calificacion anterior
                    session.execute(
                        """
                        DELETE FROM clientes_por_libro
                        WHERE titulo_libro=%s
                        AND autor_libro=%s
                        AND calificacion=%s
                        AND id_cliente=%s
                        """,
                        (titulo_libro, autor_libro, info_previa.calificacion, id_cliente))
                    session.execute(
                        """
                        DELETE FROM categorias_por_cliente
                        WHERE id_cliente=%s 
                        AND categoria=%s
                        AND titulo_libro=%s
                        AND autor_libro=%s
                        AND calificacion=%s
                        """, (id_cliente, info_previa.categoria, titulo_libro, autor_libro,
                            info_previa.calificacion))

                #Agregar la nueva calificación
                session.execute(
                    """
                    INSERT INTO libros_por_cliente 
                    (id_cliente, titulo_libro, autor_libro, categoria, calificacion)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (id_cliente, titulo_libro, autor_libro, categoria, calificacion))
                session.execute(
                    """
                    INSERT INTO clientes_por_libro 
                    (titulo_libro, autor_libro, id_cliente, calificacion, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (titulo_libro, autor_libro, id_cliente, calificacion, categoria))
                session.execute(
                    """
                    INSERT INTO categorias_por_cliente 
                    (id_cliente, titulo_libro, autor_libro, categoria, calificacion)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (id_cliente, titulo_libro, autor_libro, categoria, calificacion))

                #Actualizar calificaciones promedio
                calificacion_promedio = session.execute(
                    """
                    SELECT AVG(calificacion) FROM clientes_por_libro
                    WHERE titulo_libro=%s
                    AND autor_libro=%s
                    """, (titulo_libro, autor_libro))
                calificacion_promedio = round(calificacion_promedio.one()[0], 2)

                categorias_del_libro = session.execute(
                    """
                    SELECT categoria FROM clientes_por_libro
                    WHERE titulo_libro =%s
                    AND autor_libro = %s
                    """, (titulo_libro, autor_libro))

                alguna_categoria = categorias_del_libro.one().categoria

                promedio_anterior = session.execute(
                    """
                    SELECT calificacion_promedio FROM libros_por_categoria
                    WHERE categoria =%s
                    AND titulo_libro =%s
                    AND autor_libro = %s
                    """, (alguna_categoria, titulo_libro, autor_libro))
                if promedio_anterior:
                    promedio_anterior = promedio_anterior.one().calificacion_promedio

                #En caso de que sea la única review que asigna esa categoría al libro y se cambie la categoría, necesitamos
                #eliminar la fila de la tabla libros_por_categoría
                if info_previa is not None:
                    if info_previa.categoria != categoria:
                        unica_calificacion = True

                        for row in categorias_del_libro:
                            if row.categoria == info_previa.categoria:  #entonces hay otras reviews que categorizan igual al libro
                                unica_calificacion = False

                            #Actualizar libros_por_categoria
                            session.execute(
                                """
                                INSERT INTO libros_por_categoria
                                (categoria, titulo_libro, autor_libro, calificacion_promedio)
                                VALUES (%s, %s, %s, %s)
                                """, (row.categoria, titulo_libro, autor_libro,
                                    calificacion_promedio))

                            #Actualizar calificaciones_por_categoria
                            ## Borrar promedio anterior
                            if promedio_anterior:
                                session.execute(
                                    """
                                    DELETE FROM calificaciones_por_categoria
                                    WHERE categoria=%s
                                    AND calificacion_promedio=%s
                                    AND titulo_libro=%s
                                    AND autor_libro= %s
                                    """, (row.categoria, promedio_anterior, titulo_libro,
                                        autor_libro))
                            ## Insertar promedio nuevo
                            session.execute(
                                """
                                INSERT INTO calificaciones_por_categoria
                                (categoria, calificacion_promedio, titulo_libro, autor_libro)
                                VALUES (%s, %s, %s, %s)
                                """, (row.categoria, calificacion_promedio, titulo_libro,
                                    autor_libro))

                        if unica_calificacion:
                            session.execute(
                                """
                                DELETE FROM libros_por_categoria
                                WHERE categoria=%s
                                AND titulo_libro=%s
                                AND autor_libro=%s
                                """, (info_previa.categoria, titulo_libro, autor_libro))
                            session.execute(
                                """
                                DELETE FROM calificaciones_por_categoria
                                WHERE categoria=%s
                                AND calificacion_promedio=%s
                                AND titulo_libro=%s
                                AND autor_libro=%s
                                """, (info_previa.categoria, promedio_anterior,
                                    titulo_libro, autor_libro))

                else:
                    for row in categorias_del_libro:
                        #Actualizar libros_por_categoria
                        session.execute(
                            """
                            INSERT INTO libros_por_categoria
                            (categoria, titulo_libro, autor_libro, calificacion_promedio)
                            VALUES (%s, %s, %s, %s)
                            """, (row.categoria, titulo_libro, autor_libro,
                                calificacion_promedio))

                        #Actualizar calificaciones_por_categoria
                        ## Borrar promedio anterior
                        if promedio_anterior:
                            session.execute(
                                """
                                DELETE FROM calificaciones_por_categoria
                                WHERE categoria=%s
                                AND calificacion_promedio=%s
                                AND titulo_libro=%s
                                AND autor_libro= %s
                                """, (row.categoria, promedio_anterior, titulo_libro,
                                    autor_libro))
                        #Insertar promedio nuevo
                        session.execute(
                            """
                            INSERT INTO calificaciones_por_categoria
                            (categoria, calificacion_promedio, titulo_libro, autor_libro)
                            VALUES (%s, %s, %s, %s)
                            """, (row.categoria, calificacion_promedio, titulo_libro,
                                autor_libro))
                self.txtbook.delete(0, END)
                self.txtauthor.delete(0,END)
                self.txtrating.set('')
                self.txtcategory.set('')
                messagebox.showinfo("Success", "Libro rankeado")
            else: 
                messagebox.showerror("Listillo", "No deberías estar aquí sin loguearte")

class Admin_options(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="img/background.jpg")
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

        clientsperbook_author=Label(frame, text="Autor:", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        clientsperbook_author.place(x=110, y=180)

        self.author = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.author.place(x=400, y=180, width=240)

        bookspercategory=Label(frame, text="Libros destacados de la categoría:", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        bookspercategory.place(x=70, y=220)

        self.categoryname = ttk.Combobox(frame, state="readonly", values=universal_categorias)
        self.categoryname.place(x=400, y=220, width=240)

        numberbooks=Label(frame, text="Se desea obtener los mejores:", font =("calibri", 15, "bold"), fg="lightblue", bg="black")
        numberbooks.place(x=70, y=260)

        self.numberbooks = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.numberbooks.place(x=400, y=260, width=240)

        #Login Button
        q1=Button(frame,command=self.query1, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q1.place(x=650, y=100, width=120, height=30)

        q2=Button(frame,command=self.query2, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q2.place(x=650, y=140, width=120, height=30)

        q2=Button(frame,command=self.query3, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q2.place(x=650, y=220, width=120, height=30)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightblue")
        exitbtn.place(x=50, y=350, width=120, height=30)
    
    def query1(self):
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)

        usernameVal = self.username.get()

        resultado = session.execute(
            """
            SELECT categoria, AVG(calificacion) FROM categorias_por_cliente
            WHERE id_cliente=%s
            GROUP BY categoria
            """,
            [usernameVal]
        )

        resultado = pd.DataFrame(resultado.all(), columns=['cateogoria', 'avg_calificacion'])
        resultado = resultado.sort_values(by='avg_calificacion', ascending=False)
        resultado = resultado.values[0]
        res=pd.DataFrame([(resultado[0], resultado[1])], columns=["Categoria", "Calificacion"])

        pt = Table(f, dataframe=res,
                                showtoolbar=True, showstatusbar=True)
        pt.show()

    def query2(self): 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)


        booknameVal= self.bookname.get()
        authorVal  = self.author.get()


        resultado_max_calif = session.execute(
            """
            SELECT MAX(calificacion) FROM clientes_por_libro
            WHERE titulo_libro=%s
            AND autor_libro=%s
            LIMIT 1
            """,
            (booknameVal, authorVal)
        )

        if resultado_max_calif is None:
            messagebox.showerror('Error', 'No hay ratings para este libro')
            return

        max_calif = resultado_max_calif.one()[0]

        resultado_clientes = session.execute(
            """
            SELECT id_cliente, calificacion FROM clientes_por_libro
            WHERE titulo_libro=%s
            AND autor_libro=%s
            AND calificacion=%s
            """, 
            (booknameVal, authorVal, max_calif)
        )
            
        res= pd.DataFrame(resultado_clientes.all())
        pt = Table(f, dataframe=res,
                                showtoolbar=True, showstatusbar=True)
        pt.show()


    def query3(self): 
        newWindow = Toplevel(self.root)
        Frame.__init__(self)
        newWindow.geometry('600x400+200+100')
        newWindow.title('Tabla')
        f = Frame(newWindow)
        f.pack(fill=BOTH,expand=1)

        categoria= self.categoryname.get()
        n        = int(self.numberbooks.get())
        resultado = session.execute(
            """
            SELECT titulo_libro, autor_libro, calificacion_promedio FROM calificaciones_por_categoria
            WHERE categoria=%s
            ORDER BY calificacion_promedio DESC
            LIMIT %s;
            """, 
            (categoria, n)
        )

        res=pd.DataFrame(resultado.all())
        pt = Table(f, dataframe=res,
                                showtoolbar=True, showstatusbar=True)
        pt.show()


    def login_window(self): 
        global supertemporalUser
        supertemporalUser =None
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