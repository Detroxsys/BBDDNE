from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk  #pip install pillow
from tkinter import messagebox
import pandas as pd
from pandastable import Table, TableModel

dfsuper = pd.read_csv('./data/DatosBBDDE_test.csv')



if __name__ == '__main__':
    root = Tk()
    app = Admin_options(root)
    root.mainloop()