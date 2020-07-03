from tkinter import *
import imgAnalyzer as IA


root = Tk()

e = Entry(root, width=50, fg="green", bg="purple", borderwidth=10)
e.pack()
e.insert(0, "Enter Name of image")
e1 = Entry(root, width = 10, fg="red", bg="blue")
e1.pack()
e1.insert(0, "Enter the div size")

def click():
    inputText = e.get()
    inputNum = e1.get()
    IA.fractalize(inputText, inputNum)

button = Button(root, text="fractalize", command=click, fg="blue", bg="red")
button.pack()


root.mainloop()
