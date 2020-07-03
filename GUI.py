from tkinter import *
from tkinter.filedialog import askopenfilename
import imgAnalyzer as IA

file = None
divSize = 10


root = Tk()


def startFractalize():
    IA.fractalize(file, divSize)

def chooseFile():
    global file
    file = askopenfilename(title="Select Image", filetypes=[("JPG or PNG Files", "*.jpg *.png")])


def getDivSize():
    global divSize
    temp = str(chooseDivSize.get())
    if temp.isdigit():
        print(divSize)
        divSize = temp
    else:
        # do something to alter this is invalid input
        pass


chooseDivSize = Entry(root, validate='all', validatecommand=('%i'))
chooseDivSize.pack()


fractButton = Button(root, text="fractalize", command=startFractalize, fg="blue", bg="red")
fileChooseButton = Button(root, text="Choose Img", command=chooseFile)
confirmDivButton = Button(root, text="Enter", command=getDivSize)


fractButton.pack()
fileChooseButton.pack()
confirmDivButton.pack()

root.mainloop()
