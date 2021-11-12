import tkinter as tk
from tkinter import font

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # #designing and layout.
        self.config(background='black')
        # self.geometry('600x400')
        # self.configure(bg='black')

        #font
        self.myFont = font.Font(family='Georgia',size='12')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.button = tk.Button(self,text='Execute', font=self.myFont)
        self.button.grid()

root = tk.Tk()
app = Application(master=root)
app.mainloop()

# from tkinter import *
# from tkinter import font
# app = Tk()

# #designing and layout.
# app.geometry('600x400')
# app.configure(bg='black')

# #font
# myFont = font.Font(family='Georgia',size='12')

# #widgets
# button = Button(app,text='Execute', font=myFont)
# button.grid()

# app.resizable(False, False)
# app.mainloop()