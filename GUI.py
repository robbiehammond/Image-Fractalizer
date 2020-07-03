from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import threading
import imgAnalyzer as IA

file = None
save = None
divSize = 10


root = Tk()

chooseDivSize = Entry(root, width=4)
chooseDivSize.grid(row=0, column=0)

filePath = Text(root, width=40, height=3)
filePath.insert(1.0, "Image path will be displayed here.")
filePath.configure(state='disabled')
filePath.grid(row=1, column=0)

savePath = Text(root, width=40, height=3)
savePath.insert(1.0, "Path to save to will be displayed here.")
savePath.configure(state='disabled')
savePath.grid(row=2, column=0)

def startFractalize():
    IA.fractalize(file, divSize, save)

def chooseFile():
    global file
    file = askopenfilename(title="Select Image", filetypes=[("JPG, JPEG, or PNG Files", "*.jpg *.jpeg *.png")])
    filePath.configure(state='normal')
    filePath.delete('1.0', END)
    filePath.insert(1.0, file)
    filePath.configure(state='disabled')


def getDivSize():
    global divSize
    temp = str(chooseDivSize.get())
    if temp.isdigit():
        divSize = temp
        print(divSize)
    else:
        # do something to alter this is invalid input
        pass

def getSavePath():
    global save
    save = askdirectory()
    savePath.configure(state='normal')
    savePath.delete('1.0', END)
    savePath.insert(1.0, save)
    savePath.configure(state='disabled')




fractButton = Button(root, text="fractalize", command=startFractalize)
fileChooseButton = Button(root, text="Choose Img", command=chooseFile)
saveChooseButton = Button(root, text="Save To...", command=getSavePath)
confirmDivButton = Button(root, text="Confirm Division Size", command=getDivSize)


fractButton.grid(row=3,column=0)
fileChooseButton.grid(row=1, column=2)
saveChooseButton.grid(row=2, column=2)
confirmDivButton.grid(row=0, column=2)

root.mainloop()
