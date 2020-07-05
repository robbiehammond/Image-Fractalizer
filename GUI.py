from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.ttk import *
import threading
import os
import fractalizer as fract

file = None
save = None
divSize = 10  # default value

root = Tk()
root.title("Image Fractalizer")
root.geometry("500x300")
root.wm_iconbitmap('Logo.ico')

root.resizable(False, False)

divLabel = Label(root, text="Enter Division Size:")
divLabel.place(relx=.35, rely=.05, anchor=CENTER)

chooseDivSize = Entry(root, width=10)
chooseDivSize.insert(1, divSize)
chooseDivSize.place(relx=.55, rely=.05, anchor=CENTER)

defaultName = StringVar()
newImgName = Entry(root, width=50, textvariable=defaultName)
defaultName.set("My Fractalized Image")
newImgName.place(relx=.4, rely=.6, anchor=CENTER)

nameLabel = Label(root, text="Type New Image Name\n(Without File Extension)")
nameLabel.place(relx=.85, rely=.6, anchor=CENTER)

filePath = Text(root, width=50, height=3)
filePath.insert(1.0, "Original image path will be displayed here")
filePath.configure(state='disabled')
filePath.place(relx=.4, rely=.2, anchor=CENTER)

savePath = Text(root, width=50, height=3)
savePath.insert(1.0, "Save path for the new image will be displayed here")
savePath.configure(state='disabled')
savePath.place(relx=.4, rely=.4, anchor=CENTER)

progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
progress.place(relx=.5, rely=.85, anchor=CENTER)

state = Text(root, width=20, height=1)
state.place(relx=.5, rely=.95, anchor=CENTER)


def startNewThread(func, args):
    thread = threading.Thread(target=func, args=args)
    thread.start()


def clearStateBar():
    state.delete('1.0', END)


def updateFilePath():
    global file
    file = askopenfilename(title="Select Image", filetypes=[("JPG, JPEG, or PNG Files", "*.jpg *.jpeg *.png")])
    filePath.configure(state='normal')
    filePath.delete('1.0', END)
    filePath.insert(1.0, file)
    filePath.configure(state='disabled')


def updateSavePath():
    global save
    save = askdirectory()
    savePath.configure(state='normal')
    savePath.delete('1.0', END)
    savePath.insert(1.0, save)
    savePath.configure(state='disabled')


def updateDivSize():
    global divSize
    temp = str(chooseDivSize.get())
    if temp.isdigit():
        divSize = temp
    else:
        divSize = 0


def startFractalize():
    clearStateBar()

    state.insert('end', "Starting Process...")
    if not paramsAreValid():
        return

    fract.fractalize(file, divSize, save, newImgName.get())

    updateProgress()
    clearStateBar()
    state.insert('end', "Done!")
    root.after(5000, fract.setPercentDone, (0,))
    root.after(5000, clearStateBar)


def paramsAreValid():
    # checks if the division size is not a number or if it is less than 0.
    updateDivSize()
    if not str(divSize).isdigit() or int(divSize) <= 0:
        clearStateBar()
        state.insert('end', 'Invalid Div Size!')
        return False

    # checks if a path has not been written to the file variable and that the path exists
    if file is None or not os.path.exists(file):
        clearStateBar()
        state.insert('end', 'Invalid File Path!')
        return False

    # checks if a path has not been written to the save variable and that the path exists
    if save is None or not os.path.exists(save):
        clearStateBar()
        state.insert('end', 'Invalid Save Path!')
        return False

    return True


def updateProgress():
    progress['value'] = fract.getPercentDone()
    root.after(2000, updateProgress)

    # get and display progress from the variables in fractalizer.py
    if fract.dividingImage:
        clearStateBar()
        state.insert('end', "Dividing Image...")
    elif fract.fractalizing:
        clearStateBar()
        state.insert('end', "Fractalizing...")
    elif fract.finishingUp:
        clearStateBar()
        state.insert('end', "Finishing Up...")


fractButton = Button(root, text="Fractalize!", command=lambda: startNewThread(startFractalize, ()))
fileChooseButton = Button(root, text="Choose Image", command=updateFilePath)
saveChooseButton = Button(root, text="Save To...", command=updateSavePath)

fractButton.place(relx=.5, rely=.75, anchor=CENTER)
fileChooseButton.place(relx=.85, rely=.2, anchor=CENTER)
saveChooseButton.place(relx=.85, rely=.4, anchor=CENTER)


root.after(2000, updateProgress)
root.mainloop()