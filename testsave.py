from tkinter import *
import tkinter
from tkinter import filedialog
import pickle

root = Tk()
root.withdraw()
root.filename = filedialog.askopenfile(mode = "r")
name = root.filename.name

print(name)
root.destroy()


root = Tk()
root.withdraw()
root.filename = filedialog.asksaveasfile(mode = "w")
print(root.filename.name)