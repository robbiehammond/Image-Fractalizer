from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.ttk import *
import threading
import imgAnalyzer as IA

file = None
save = None
divSize = 10  # default value

root = Tk()
root.title("Image Fractalizer")

divLabel = Label(root, text="Enter Division Size:") # Div size explanation - 1 new pixel = (Div Size)^2 old pixels
divLabel.grid(sticky=W)

chooseDivSize = Entry(root, width=10)
chooseDivSize.insert(1, "10")
chooseDivSize.grid(row=0, column=0, pady=5)

defaultName = StringVar()
newImgName = Entry(root, width=40, textvariable=defaultName)
defaultName.set("My Fractalized Image")
newImgName.grid(row=3, pady = 5)

nameLabel = Label(root, text="    Type New\n<- Image Name\n    (without extension)")
nameLabel.grid(row=3, column = 1)


filePath = Text(root, width=40, height=3)
filePath.insert(1.0, "Image path will be displayed here.")
filePath.configure(state='disabled')
filePath.grid(row=1, column=0, padx=5, pady=5)

savePath = Text(root, width=40, height=3)
savePath.insert(1.0, "Path to save to will be displayed here.")
savePath.configure(state='disabled')
savePath.grid(row=2, column=0, padx=5, pady=5)

progress = Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress.grid(row=5, column=0, pady=5)

state = Text(root, width=20, height=1)
state.grid(row=6, column=0, pady=5)


def updateProgress():
    progress['value'] = IA.getPercentDone()
    root.after(2000, updateProgress)
    if IA.dividingImage:
        clearStateBar()
        state.insert('end', "Dividing Image...")
    elif IA.fractalizing:
        clearStateBar()
        state.insert('end', "Fractalizing...")
    elif IA.finishingUp:
        clearStateBar()
        state.insert('end', "Finishing Up...")


def background(func, args):
    t1 = threading.Thread(target=func, args=args)
    t1.start()

def clearStateBar():
    state.delete('1.0', END)


def startFractalize():
    clearStateBar()
    state.insert('end', "Starting Process...")
    updateDivSize()
    IA.fractalize(file, divSize, save, newImgName.get())
    clearStateBar()
    state.insert('end', "Done!")
    root.after(5000, IA.setPercentDone, (0,))
    root.after(5000, clearStateBar)


def getFilePath():
    global file
    file = askopenfilename(title="Select Image", filetypes=[("JPG, JPEG, or PNG Files", "*.jpg *.jpeg *.png")])
    filePath.configure(state='normal')
    filePath.delete('1.0', END)
    filePath.insert(1.0, file)
    filePath.configure(state='disabled')


def updateDivSize():
    global divSize
    temp = str(chooseDivSize.get())
    if temp.isdigit():
        divSize = temp
    else:
        clearStateBar()
        state.insert("Error Has Occurred.")
        divSize = 0
        pass


def getSavePath():
    global save
    save = askdirectory()
    savePath.configure(state='normal')
    savePath.delete('1.0', END)
    savePath.insert(1.0, save)
    savePath.configure(state='disabled')


fractButton = Button(root, text="fractalize", command=lambda: background(startFractalize, ()))
fileChooseButton = Button(root, text="Choose Img", command=getFilePath)
saveChooseButton = Button(root, text="Save To...", command=getSavePath)

fractButton.grid(row=4, column=0)
fileChooseButton.grid(row=1, column=1)
saveChooseButton.grid(row=2, column=1)

root.after(2000, updateProgress)
root.mainloop()