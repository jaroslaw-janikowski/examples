import tkinter as tk
import tkinter.ttk as ttk


root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())

label = tk.Label(root, text='test')
label.pack()

root.mainloop()
