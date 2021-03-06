from tkinter import *
from tkinter import filedialog #for opening and saving files
from tkinter import ttk #for resizing the window
import tkinter.messagebox as msgbox
import os #to get cwd for initial position of saving and opening window
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True) # Makes the tkinter window not look like it's 480p

root=Tk()

# Function to toggle between taskbar icon and normal window
def toggle(event):
    if event.type == EventType.Map:
        root.deiconify()
    else:
        root.withdraw()

# create the "invisible" toplevel
top = Toplevel(root)
top.geometry('0x0+10000+10000') # make it not visible
top.title('Notepad') # title for the process in task manager
top.protocol('WM_DELETE_WINDOW', root.destroy) # close root window if toplevel is closed
top.bind("<Map>", toggle)
top.bind("<Unmap>", toggle)


'''Made geometry according to screen size because if it was too low, the file menubar would not show up.
So now by default the window size is big enough to show it'''
screen_width = root.winfo_screenwidth()//2
screen_height = root.winfo_screenheight()//2
root.geometry(f"{screen_width}x{screen_height}+200+200")

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

'''Using toggle function insted
That retains the icon in taskbar even when the window is use
This method only retains it when the window is iconified and not when it's in use'''
# Function to minimize to taskbar
# minimized=False
# minimizeTurn=False 
# def toTaskbar():
#     top.iconify()


# def backFromTaskbar(event):
#     global minimized,minimizeTurn
#     root.update_idletasks()
#     if(minimized and minimizeTurn):
#         root.overrideredirect(True)
#         minimized=False
#     else:
#         minimizeTurn=True
    

#Making the titlebar
titlebg='#505050'
titlebar=Frame(root,background=titlebg,bd=1,relief=FLAT)
titlebar.pack(side=TOP, fill=X)
titleLabel=Label(titlebar,text="Notepad",fg=fgColour,bg=titlebg)
titleLabel.pack(side=LEFT)

'''Need to bind it to titlebar
First tried binding it to root, but that was giving multiple instances of map for every time it was changed
Using titlebar only invokes map once when changed'''
# titlebar.bind('<Map>',backFromTaskbar)

# Basic button functionality for the title bar
Button(titlebar,command=root.destroy,bg=titlebg,text="X",fg=fgColour,width=3,relief=FLAT,font='Helvetica 10 bold').pack(side=RIGHT)
Button(titlebar,command=fullscreen,bg=titlebg,text="O",fg=fgColour,width=3,relief=FLAT,font='Helvetica 10 bold').pack(side=RIGHT)
Button(titlebar,command=top.iconify,bg=titlebg,text="---",fg=fgColour,width=3,relief=FLAT,font='Helvetica 10 bold').pack(side=RIGHT)

# Window Movement

def moveWindow(event):
    x = root.winfo_pointerx() - root.offsetx
    y = root.winfo_pointery() - root.offsety
    root.geometry(f'+{x}+{y}')

# Coordinates where the titlebar is clicked
def click(event):
    root.offsetx=event.x
    root.offsety=event.y

titlebar.bind('<B1-Motion>',moveWindow)
titlebar.bind('<Button-1>',click)
#Binding to label otherwise the window didn't move when cursor was over the label
titleLabel.bind('<B1-Motion>',moveWindow)
titleLabel.bind('<Button-1>',click)
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
    Button(fileMenu,text="Save As",command=saveas,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
    Button(fileMenu,text="Open",command=openFunction,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
    
    Button(fileMenu,text="X",command=fileMenu.pack_forget,bg=submenubgcolour,fg=fgColour,relief=FLAT,width=3).pack(side=RIGHT,pady=2,padx=2) #To close the extra menu
#Sub functions

global filename #To store the current filename
filename=''
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
    global filename
    if filename=='':    #To check if the file hasn't been stored already
        saveas()
    else:
        raw_filename=to_raw(filename)   #Updating contents of the file
        val=getText()
        with open(raw_filename,'w') as f:
            f.write(val)


#Function to save as new file
def saveas():
    global filename
    filename=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save As",filetypes=(('Text Files','*.txt*'),("All Files", "*.*")))
    raw_filename=to_raw(filename)
    val=getText()
    with open(raw_filename,'w') as f:
        f.write(val)
    titleLabel.config(text=f"Notepad\t{filename}")

# Function to open files
def openFunction():
    global filename
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open",filetypes=(('Text Files','*.txt*'),("All Files", "*.*")))
    raw_filename=to_raw(filename)
    with open(raw_filename,'r') as f:
        val=f.read()
    textDelete()
    addText(val)
    titleLabel.config(text=f"Notepad\t{filename}")


# Function to create new file
def new():
    global filename
    filename=''
    textDelete()
    titleLabel.config(text=f"Notepad")

# Help menu functions
def help():
    helpMenu=Frame(root,bg=menubgcolour,bd=1,relief=SUNKEN)
    helpMenu.pack(side=TOP,fill=X)

    Button(helpMenu,text="About",command=about,bg=submenubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)

    Button(helpMenu,text="X",command=helpMenu.pack_forget,bg=submenubgcolour,fg=fgColour,relief=FLAT,width=3).pack(side=RIGHT,pady=2,padx=2) #To close the extra menu

#Sub functions
def about():
    msgbox.showinfo("About","Made by Bhavya Gautam\nhttps://github.com/bhavyagautam/DarkModeNotepad")



menuBar=Frame(root,bg=menubgcolour,relief=FLAT)
menuBar.pack(side=TOP,fill=X)



# File Button
Button(menuBar,text="File",command=file,bg=menubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)
# Help Button
Button(menuBar,text="Help",command=help,bg=menubgcolour,fg=fgColour,relief=FLAT).pack(side=LEFT,pady=2)

'''---------    Menubar Done    ------- '''

'''Creating Scroll Bar and it's frames'''
yscrollframe=Frame(root)
yscrollframe.pack(side=RIGHT,anchor=SE,fill=Y)
yscroll=Scrollbar(yscrollframe,troughcolor=titlebg)


#Resizing window widget
style=ttk.Style(root)
style.theme_use('classic')
style.configure('TLabel', background=titlebg,width=2)
sizegrip=ttk.Sizegrip(yscrollframe, style='TLabel')
sizegrip.pack(side=BOTTOM,anchor=SE)


'''Text'''
textFrame=Frame(root)
text=Text(textFrame,fg=fgColour,bg=rootbgcolour,insertbackground=fgColour,yscrollcommand=yscroll.set) #insertbackgorund: cursor colour
text.pack(side=TOP,fill=BOTH,expand=True)
textFrame.pack(side=BOTTOM,fill=BOTH,expand=True)

#Functions to easily manipulate data inside textbox
def getText():
    return text.get(1.0,'end-1c')

def addText(val):
    text.insert(END,val)

'''------ TEXT DONE ------'''

# Continuing scrollbar
yscroll.config(command=text.yview)
yscroll.pack(side=RIGHT,fill=Y)
'''------Scrollbar Done--------'''

root.mainloop()