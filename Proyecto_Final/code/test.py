from tkinter import *

main=Tk()
photo=PhotoImage(file='img/logo.png')
Label(main,image=photo,bg='grey').pack()
#your other label or button or ...
main.wm_attributes("-transparentcolor", 'grey')
main.mainloop()