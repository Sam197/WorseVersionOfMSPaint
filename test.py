from tkinter import *
from tkinter import messagebox

messagebox.askquestion('Test', 'Load or Save')

response = messagebox.askyesnocancel()
print(response)