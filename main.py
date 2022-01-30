from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as msgbox
import os
root=Tk()
root.geometry(f"800x600+100+100")
root.minsize(200,200)
root.title("Notepad")
root.overrideredirect(True)
# Dark mode colour
rootbgcolour="#1e1e1e"
root.config(background=rootbgcolour)
# Foreground colour
fgColour='#c0c8c6'

'''Making a custom title bar because background of titlebar cannot be changed in tkinter
and without changing the background, dark mode doesn't really look good
MOST CHALLENGING PART'''
#TODO: Show icon in taskbar at all times
# Function for fullscreen
fullscreenTurn=True
screenSize='800x600'

def fullscreen():
    global fullscreenTurn
    global screenSize
    if (fullscreenTurn): 
        root.overrideredirect(False)
        screenSize=f'{root.winfo_width()}x{root.winfo_height()}' #saving last screen size before fullscreen
        root.attributes('-fullscreen',True)
        root.overrideredirect(True)
        fullscreenTurn=False
    else:
        root.overrideredirect(False)
        root.attributes('-fullscreen',False)
        root.geometry(f"{screenSize}")
        root.overrideredirect(True)
        fullscreenTurn=True

# Function to minimize to taskbar
minimized=False
minimizeTurn=False 
def toTaskbar():
    root.overrideredirect(False)
    root.iconify()
    print("to taskbar ran")
    global minimized
    minimized=True

def backFromTaskbar(event):
    global minimized,minimizeTurn
    root.update_idletasks()
    if(minimized and minimizeTurn):
        root.overrideredirect(True)
        minimized=False
    else:
        minimizeTurn=True
    

#Making the titlebar
titlebg='#505050'
titlebar=Frame(root,background=titlebg,bd=1,relief=FLAT)
titlebar.pack(side=TOP, fill=X)
titleLabel=Label(titlebar,text="Notepad",fg=fgColour,bg=titlebg)
titleLabel.pack(side=LEFT)

'''Need to bind it to titlebar
First tried binding it to root, but that was giving multiple instances of map for every time it was changed
Using titlebar only invokes map once when changed'''
titlebar.bind('<Map>',backFromTaskbar)

# Basic button functionality for the title bar
Button(titlebar,command=root.destroy,bg=titlebg,text="X",fg=fgColour,width=3,relief=FLAT,font='Helvetica 10 bold').pack(side=RIGHT)
Button(titlebar,command=fullscreen,bg=titlebg,text="O",fg=fgColour,width=3,relief=FLAT,font='Helvetica 10 bold').pack(side=RIGHT)
Button(titlebar,command=toTaskbar,bg=titlebg,text="---",fg=fgColour,width=3,relief=FLAT,font='Helvetica 10 bold').pack(side=RIGHT)

# Window Movement
# TODO: Make the window move from the point where I click it from and not the edge
def moveWindow(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

titlebar.bind('<B1-Motion>',moveWindow)

'''----------Title Bar Done------'''

'''Menu'''
# This does not work, can't change background position or location of the menubar
'''
# Functions
def new():
    pass
def open():
    pass
def save():
    pass
def saveas():
    pass

mainMenu=Menu(root,bg=titlebg)
#File Menu
fileMenu=Menu(mainMenu,tearoff=False,background=bgcolour)
fileMenu.add_command(label="New",command=new)
fileMenu.add_command(label="Open",command=open)
fileMenu.add_command(label="Save",command=save)
fileMenu.add_command(label="Save As",command=saveas)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=root.destroy)
mainMenu.add_cascade(label="File", menu=fileMenu)

root.config(menu=mainMenu)
'''

# Creating a menu from scratch

#Functions

#File Menu Functions
menubgcolour='#414040'
submenubgcolour='#4E4B4B'

def file():
    fileMenu=Frame(root,bg=menubgcolour,bd=1,relief=SUNKEN)
    fileMenu.pack(side=TOP,fill=X)
    
    Button(fileMenu,text="New",command=new,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
    Button(fileMenu,text="Save",command=save,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
    Button(fileMenu,text="Open",command=openFunction,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
    
    Button(fileMenu,text="X",command=fileMenu.pack_forget,bg=submenubgcolour,fg=fgColour,relief=FLAT,width=3).pack(side=RIGHT,pady=2,padx=2) #To close the extra menu
#Sub functions
# To raw function to open the files with absolute path
def to_raw(string):
    newstr=''
    for val in string:
        if(val=='\\'):
            newstr+='\\'
            newstr+=val
        else:
            newstr+=val
    return str(newstr)

#Function to delete all contents of the textbox
def textDelete():
    text.delete(1.0,"end")

#Function to save the file
def save():
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Save",filetypes=(('Text Files','*.txt*'),("All Files", "*.*")))
    raw_filename=to_raw(filename)
    val=getText()
    with open(raw_filename,'w') as f:
        f.write(val)


# Function to open files
def openFunction():
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open",filetypes=(('Text Files','*.txt*'),("All Files", "*.*")))
    raw_filename=to_raw(filename)
    with open(raw_filename,'r') as f:
        val=f.read()
    textDelete()
    addText(val)



def new():
    textDelete()

# Help menu functions
def help():
    helpMenu=Frame(root,bg=menubgcolour,bd=1,relief=SUNKEN)
    helpMenu.pack(side=TOP,fill=X)

    Button(helpMenu,text="About",command=about,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)

    Button(helpMenu,text="X",command=helpMenu.pack_forget,bg=submenubgcolour,fg=fgColour,relief=FLAT,width=3).pack(side=RIGHT,pady=2,padx=2) #To close the extra menu

#Sub functions
def about():
    msgbox.showinfo("About","Made by Bhavya Gautam")



menuBar=Frame(root,bg=menubgcolour,relief=FLAT)
menuBar.pack(side=TOP,fill=X)



# File Button
Button(menuBar,text="File",command=file,bg=menubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
# Help Button
Button(menuBar,text="Help",command=help,bg=menubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)

'''---------    Menubar Done    ------- '''

'''Text'''
textFrame=Frame(root)
text=Text(textFrame,fg=fgColour,bg=rootbgcolour,insertbackground=fgColour) #insertbackgorund: cursor colour
text.pack(side=TOP,fill=BOTH,expand=True)
textFrame.pack(side=BOTTOM,fill=BOTH,expand=True)

#Functions to easily manipulate data inside textbox
def getText():
    return text.get(1.0,'end-1c')

def addText(val):
    text.insert(END,val)



root.mainloop()