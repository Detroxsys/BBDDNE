from tkinter import*
from tkinter import ttk
from unicodedata import category
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox

class Admin_options(Frame):
    def __init__(self, root):
        self.root=root
        self.root.title("Booksr")
        self.root.geometry("1550x800+0+0")
        
        self.bg = ImageTk.PhotoImage(file="./img/background.jpg")
        lbl_bg  = Label(self.root, image= self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        Frame.__init__(self, root)
        frame = Frame(self.root, bg="black")
        frame.place(x=100, y=50, width= 1300, height=700)

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
        bookspercategory.place(x=70, y=400)

        self.categoryname = ttk.Entry(frame, font =("calibri", 15, "bold"))
        self.categoryname.place(x=400, y=400, width=240)

        #Login Button
        q1=Button(frame,command=self.query1, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q1.place(x=650, y=100, width=120, height=30)

        q2=Button(frame,command=self.query2, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q2.place(x=650, y=140, width=120, height=30)

        q2=Button(frame,command=self.query3, text="Consultar",font =("calibri", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="lightblue")
        q2.place(x=650, y=400, width=120, height=30)

        exitbtn=Button(frame,command=self.login_window, text="Salir",font =("calibri", 15, "bold"),bd=3, relief=RIDGE, fg="white", bg="lightblue")
        exitbtn.place(x=50, y=650, width=120, height=30)
    
    def query1(self):
        pass
    def query2(self): 
        pass
    def query3(self): 
        pass


    def login_window(self): 
        self.root.switch_frame(Login_window)

if __name__ == '__main__':
    root = Tk()
    app = Admin_options(root)
    root.mainloop()