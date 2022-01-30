from tkinter import *
root=Tk()
root.geometry(f"800x600+100+100")
root.minsize(200,200)
root.title("Notepad")
root.overrideredirect(True)
# Dark mode colour
root.config(background="#1e1e1e")
# Foreground colour
fgColour='#c0c8c6'

'''Making a custom title bar because background of titlebar cannot be changed in tkinter
and without changing the background, dark mode doesn't really look good'''
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


root.mainloop()