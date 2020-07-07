from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askdirectory
import numpy as np
from PIL import Image
import threading
import os
import fractalizer as fract


# pops up if the image is found to likely take a long time
class PopupWindow:
    window = None
    message = None
    shouldResize = False
    back = False

    def __init__(self, message):
        self.message = message
        self.window = Tk()
        self.window.title("You Sure About This?")
        if os.name == "nt":  # only display icon on windows
            root.wm_iconbitmap('Logo.ico')
        self.window.protocol("WM_DELETE_WINDOW", self.disableExit)
        self.window.resizable(False, False)
        label = Label(self.window, text=self.message)
        label.pack(padx=5, pady=10)
        self.setUpButtons()
        self.window.mainloop()

    # window is destroyed if any of the buttons are clicked
    def setUpButtons(self):
        goAnywayButton = Button(self.window, text="Leave it be and Fractalize Anyway",
                                command=self.window.destroy)
        goAnywayButton.pack()

        resizeAndGoButton = Button(self.window, text="Resize and Fractalize",
                                   command=lambda: self.updateShouldResize())
        resizeAndGoButton.pack()

        goBackButton = Button(self.window, text="Don't Fractalize, Go Back",
                              command=lambda: self.updateBack())
        goBackButton.pack()

    def updateShouldResize(self):
        self.window.destroy()
        self.shouldResize = True

    def updateBack(self):
        self.window.destroy()
        self.back = True

    # if the exit button is clicked, do nothing - the user must make a selection
    def disableExit(self):
        pass


file = None
save = None
divSize = 10  # default value

# GUI setup for everything but buttons, which are defined later


root = Tk()
root.title("Image Fractalizer")
root.geometry("600x400")
if os.name == "nt":  # if on windows
    root.wm_iconbitmap('Logo.ico')
root.resizable(False, False)

divLabel = Label(root, text="Enter Division Size (A Positive Integer):")
divLabel.place(relx=.30, rely=.05, anchor=CENTER)

chooseDivSize = Entry(root, width=10)
chooseDivSize.insert(1, divSize)
chooseDivSize.place(relx=.6, rely=.05, anchor=CENTER)

defaultName = StringVar()
defaultName.set("My Fractalized Image")
newImgName = Entry(root, width=50, textvariable=defaultName)
newImgName.place(relx=.4, rely=.6, anchor=CENTER)

nameLabel = Label(root, text="Type New Image Name\n(Without File Extension)")
nameLabel.place(relx=.85, rely=.6, anchor=CENTER)

creationLabel = Label(root, text="Made by Robbie Hammond", font=(None, 10))
creationLabel.place(relx=1, rely=.98, anchor="e")

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
state.configure(state='disabled')
state.tag_config('Complete', foreground='green')
state.tag_config('Problem', foreground='red')
state.tag_config('Default')


# functions for GUI

# necessary to keep window active while fractalizer runs
def startNewThread(func, args):
    thread = threading.Thread(target=func, args=args)
    thread.start()


def clearStateBar():
    state.configure(state='normal')
    state.delete('1.0', END)
    state.configure(state='disabled')


def insertInStateBar(msg, tag):
    state.configure(state='normal')
    state.insert('end', msg, tag)
    state.configure(state='disabled')


def buttonDown(button):
    button['state'] = DISABLED
    button.configure(text="Please Wait")


def buttonUp(button):
    button['state'] = NORMAL
    if button == fractButton:
        button.configure(text='Fractalize!')
    elif button == stopButton:
        button.configure(text='Stop!')


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
    temp = str(chooseDivSize.get())  # only take first 100 characters if more than 100 were inputted
    if temp.isdigit():
        divSize = temp
    else:
        divSize = 0


def updateProgress():
    progress['value'] = fract.getPercentDone()
    root.after(2000, updateProgress)

    # get and display progress from the variables in fractalizer.py
    if not fract.mustStop:
        if fract.dividingImage:
            clearStateBar()
            insertInStateBar('Dividing Image...', 'Default')
        elif fract.fractalizing:
            clearStateBar()
            insertInStateBar('Fractalizing...', 'Default')
        elif fract.finishingUp:
            clearStateBar()
            insertInStateBar('Finishing Up...', 'Default')


def paramsAreValid():
    updateDivSize()
    if not str(divSize).isdigit() or int(divSize) <= 0:  # if the division size is not a number or if it is not positive
        clearStateBar()
        insertInStateBar('Invalid Div Size!', 'Problem')
        return False

    if file is None or not os.path.exists(file):
        clearStateBar()
        insertInStateBar('Invalid File Path!', 'Problem')
        return False

    if save is None or not os.path.exists(save):
        clearStateBar()
        insertInStateBar('Invalid Save Path!', 'Problem')
        return False

    # check that the division size actually makes sense for this particular image
    Img = Image.open(file)
    imAr = np.asarray(Img)
    # div size must be smaller than the smallest dimension (width or height) of the picture to be valid
    if int(divSize) > min(imAr.shape[1], imAr.shape[0]):
        clearStateBar()
        insertInStateBar('Div Size>Image Size!', 'Problem')
        return False

    return True


def stop():
    if fract.dividingImage or fract.fractalizing or fract.finishingUp:
        buttonDown(stopButton)
        fract.mustStop = True
        clearStateBar()
        insertInStateBar('Stopping...', 'Default')
    else:
        clearStateBar()
        insertInStateBar('Nothing to Stop.', 'Default')


def startFractalize():
    clearStateBar()
    buttonDown(fractButton)

    insertInStateBar("Starting Process...", "Default")

    # check to make sure every input makes sense to prevent fractalizing errors
    if not paramsAreValid():
        buttonUp(fractButton)
        return

    im = Image.open(file)

    # check to see if this might take a long time BEFORE doing any real work
    takeLongTime = fract.isAboveThreshold(file, divSize)
    if takeLongTime:
        buttonDown(stopButton)
        popup = PopupWindow("The program has found that the combination of your image's dimensions and the "
                            "chosen division size exceed\na threshold, meaning that this image may take a long "
                            "time (likely greater than 10 minutes) to fractalize with \n"
                            "its current parameters.\n\n"
                            "If you would like to continue without changing image dimensions, "
                            "click \"Leave it be and Fractalize Anyway\".\n\n"
                            "If you would like to have the program shrink the image so that it will "
                            "take less time, click \"Resize and Fractalize\".\n\n"
                            "If you would like to go back and edit the program parameters "
                            "click \"Don't Fractalize, Go Back\".")

        buttonUp(stopButton)

        if popup.shouldResize:
            im = fract.forceBelowThreshold(im, divSize)
        if popup.back:
            buttonUp(fractButton)
            clearStateBar()
            return

    fract.fractalize(im, divSize, save, newImgName.get()[:100])  # only use the first 100 letters to name the file

    # if the program was told to stop during the process
    if fract.mustStop:
        fract.setPercentDone(0)
        updateProgress()
        clearStateBar()
        insertInStateBar("Cancelled by User.", "Default")
        root.after(3000, buttonUp, (stopButton))
    # otherwise, it completed the process
    else:
        updateProgress()
        clearStateBar()
        insertInStateBar("Done!", 'Complete')

    # Regardless, wait a bit and then clear everything
    root.after(3000, fract.setPercentDone, (0))
    root.after(3000, clearStateBar)
    root.after(3000, buttonUp, (fractButton))


# button setup on GUI - below the rest of the setup due to the commands


fractButton = Button(root, text="Fractalize!", command=lambda: startNewThread(startFractalize, ()))
stopButton = Button(root, text="Stop!", command=stop)  # switch it's state?
fileChooseButton = Button(root, text="Choose Image", command=updateFilePath)
saveChooseButton = Button(root, text="Save To...", command=updateSavePath)

fractButton.place(relx=.4, rely=.75, anchor=CENTER)
stopButton.place(relx=.6, rely=.75, anchor=CENTER)
fileChooseButton.place(relx=.85, rely=.2, anchor=CENTER)
saveChooseButton.place(relx=.85, rely=.4, anchor=CENTER)

root.after(2000, updateProgress)  # update progress bar every 2 seconds
root.mainloop()

os._exit(1)  # using os._exit() instead of sys.exit() in case the fractalizing thread is still going
