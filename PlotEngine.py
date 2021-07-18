from tkinter import *
import os.path

src = "C:/Users/jkang/OneDrive/Desktop/CTS/" #THIS ONE IS FOR WINDOWS
#src = "/Users/username/Desktop/Stories/" #THIS ONE IS FOR MAC

roots = []
newRoot = Tk()
roots.append(newRoot)
root = roots[0]

tkLabels = []
lines = []
tkEButtons = []
tkOButtons = []
gridY = 1;

curfile = "";

editFont = "Arial 12"
root.option_add("*font", editFont)


def ReadFile(filename):
    root.title(filename)
    global lines, curfile
    newfile = src + filename + ".txt"
    curfile = newfile
    if not os.path.exists(curfile):
        f = open(curfile, 'a')
        f.close()
    f = open(newfile, "r")
    lines = f.readlines()
    f.close()
    ShowLines()

#Write all lines [from 'lines'] to Labels [in 'tkLabels']
def ShowLines():
    global gridY
    gridY = 1;
    for l in lines:
        l = l.strip() #remove newlines
        if l[0] != '[':
            tkL = Label(root, text = l)
            tkL.grid(row = gridY, column = 0)
            tkLabels.append(tkL)
        else: #Add options
            AddOptionButton(l[1:len(l) - 1])

        gridY += 1

    ShowEditButtons()
    ShowAddButton()
    saveButton = Button(root, text = "SAVE", command = SaveFile)
    saveButton.grid(row=101, column=0)

def ShowEditButtons():
    cGridY = 1;
    lCount = 0;
    for tl in tkLabels:
        thisLabel = tkLabels[lCount]
        tkEdit = Button(root, text = "edit")
        tkEdit.config(command = lambda tL=thisLabel, tb=tkEdit:EditLine(tL, tb))
        tkEdit.grid(row = cGridY, column = 1)
        tkEButtons.append(tkEdit)
        cGridY += 1
        lCount += 1

#txt = string to go into the new button
def AddOptionButton(txt):
    global gridY
    tkOFile = txt[txt.index('|')+1:len(txt)]
    tkO = Button(root, text=txt, command=lambda:OpenNew(tkOFile))
    tkO.grid(row = gridY, column = 0)
    tkOButtons.append(tkO)
    tkOEdit = Button(root, text="Edit", command = lambda:EditLine(tkO, tkOEdit))
    tkOEdit.grid(row = gridY, column = 1)
    gridY+=1


def ShowAddButton():
    tkAddOE = Entry(root)
    tkAddOE.grid(row = 100, column = 0) #Place this real low, may want to change this later
    tkAddOB = Button(root, text="Add new option", command=lambda:AddOptionButton(tkAddOE.get()))
    tkAddOB.grid(row = 100, column = 1)

def SaveFile():
    global curfile
    writel = []
    for l in tkLabels:
        writel.append(l["text"] + '\n')
    for l in tkOButtons:
        newl = '['
        newl += l["text"] + ']'
        writel.append(newl + '\n')
    f = open(curfile, 'w')
    f.writelines(writel)
    f.close()


#tkL = Label to change, tkB = the current button
def EditLine(tkL, tkB):
    tkLGrid = tkL.grid_info()
    tkL.grid_forget()
    newE = Entry(root)
    newE.insert(0, tkL["text"])
    newE.grid(row = tkLGrid["row"], column = tkLGrid["column"])
    tkB.config (text="done", command = lambda:DoneEdit(tkL, tkB, newE))
#tkL = Label to re-activate, tkB = the current button, tkE = entry box to disable
def DoneEdit(tkL, tkB, tkE):
    newText = tkE.get()
    tkEGrid = tkE.grid_info();
    tkL.config(text = newText)
    tkL.grid(row = tkEGrid["row"], column = tkEGrid["column"])
    tkE.destroy()
    tkB.config(text="edit", command = lambda:EditLine(tkL, tkB))

def OpenNew(nextF):
    global root, roots
    SaveFile() #Save, then destroy

    croot = Tk()
    roots.append(croot)
    root = croot

    tkLabels.clear()
    lines.clear()
    tkEButtons.clear()
    tkOButtons.clear()
    #dList = root.winfo_children()
    #for d in dList:
    #    d.destroy()
    ReadFile(nextF)



ReadFile("newFile")

