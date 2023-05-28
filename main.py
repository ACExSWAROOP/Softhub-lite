from tkinter import *
import urllib
from urllib import request
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import sv_ttk as sv
import os
import requests
from ctypes import windll
import subprocess
import webbrowser
import json
import ctypes
import sys
import threading
import time
import re

def firsttimewindow():
    global firsttime
    firsttime = Toplevel()
    firsttime.overrideredirect(True)
    app_width = 1024
    app_height = 512
    screenwidth = firsttime.winfo_screenwidth()
    screenheight = firsttime.winfo_screenheight()
    x = (screenwidth / 2) - (app_width / 2)
    y = (screenheight / 2) - (app_height / 2)
    firsttime.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    firsttime.mainloop()

def nointernetwindow(x):
    if x == "mainsplash":
        mainsplash.withdraw()
    elif x == "main":
        main.withdraw()
    noint = Toplevel()
    noint.overrideredirect(True)
    app_width = 1024
    app_height = 512
    screenwidth = noint.winfo_screenwidth()
    screenheight = noint.winfo_screenheight()
    noint.attributes("-alpha", 1)
    x = (screenwidth / 2) - (app_width / 2)
    y = (screenheight / 2) - (app_height / 2)
    noint.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    bg_image1 = ImageTk.PhotoImage(Image.open(r"images\noconnection.png"))
    label2 = Label(noint, image=bg_image1)
    label2.pack()
    noint.bind("<Button-1>", lambda e: noint.destroy())
    noint.bind("<Button-3>", lambda e: intcheckapp(x))
    noint.mainloop()


def intcheckapp(x):
    def internet_stat(url="https://www.google.com/", timeout=3):
        try:
            r = requests.head(url=url, timeout=timeout)
            return True
        except requests.exceptions.ConnectionError as e:
            return False

    net_stat = internet_stat()

    if net_stat == False:
        nointernetwindow(x)

    elif net_stat == True:
        if x == "mainsplash":
            mainsplash.deiconify()
        elif x == "main":
            main.deiconify()

def themecheck():
    with open("theme.json", "r") as file:
        global mode
        data = json.load(file)
        mode = data["mode"]

with open("settings.json", "r") as x:
    data = json.load(x)
    global autoupdateval
    autoupdateval=data["autoupdate"]

themecheck()
global is_on
if mode == "light":
    is_on = True
elif mode == "dark":
    is_on = False

mainsplash = Tk()
sv.set_theme(mode)
mainsplash.overrideredirect(True)
app_width = 1024
app_height = 512
screenwidth = mainsplash.winfo_screenwidth()
screenheight = mainsplash.winfo_screenheight()
mainsplash.attributes("-alpha", 1)
x = (screenwidth / 2) - (app_width / 2)
y = (screenheight / 2) - (app_height / 2)
mainsplash.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
if mode == "dark":
    bg_image = ImageTk.PhotoImage(Image.open(r"images\softhub load dark.png"))
    label1 = Label(mainsplash, image=bg_image)
    label1.pack()
elif mode == "light":
    bg_image = ImageTk.PhotoImage(Image.open(r"images\softhub load light.png"))
    label1 = Label(mainsplash, image=bg_image)
    label1.pack()
#intcheckapp("mainsplash")    
def checkpack(packtype):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if packtype == "🌐 Winget": 
        packages = str(subprocess.run(["winget", "list", "--source", "winget"], check=True, capture_output=True,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
    return packages

def set_appwindow(mainWindow):  # to display the window icon on the taskbar,
    # even when using main.overrideredirect(True)
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())

def minimize_me():
    main.attributes("-alpha",0) # so you can't see the window when is minimized
    main.minimized = True    
    main.bind("<FocusIn>",deminimize)    

def fake_func(event):
    return None

def deminimize(event):

    main.focus() 
    main.attributes("-alpha",1) # so you can see the window when is not minimized
    if main.minimized == True:
        main.minimized = False    

    main.bind("<FocusIn>",fake_func)


def deminimzewhenappinstalled():
    main.focus()
    main.attributes("-alpha", 1)  # so you can see the window when is not minimized
    if main.minimized == True:
        main.minimized = False


def maximize_me():
    if main.maximized == False:  # if the window was not maximized
        main.normal_size = main.geometry()
        expand_button.config(text="  🗗  ")
        main.geometry(f"{main.winfo_screenwidth()}x{main.winfo_screenheight()}+0+0")
        main.maximized = not main.maximized
        # maximized

    else:  # if the window was maximized
        expand_button.config(text="  ◻  ")
        main.geometry(main.normal_size)
        main.maximized = not main.maximized
        # not maximized

def changex_on_hovering(event):
    global close_button
    close_button['bg'] = 'red'

def returnx_to_normalstate(event):
    global close_button
    themecheck()
    if mode =="dark":
        close_button['bg'] = '#1c1c1c'
    elif mode =="light":
        close_button['bg'] = '#fafafa'

def change_size_on_hovering(event):
    global expand_button
    expand_button['bg'] = '#999999'

def return_size_on_hovering(event):
    global expand_button
    themecheck()
    if mode =="dark":
        expand_button['bg'] = '#1c1c1c'
    if mode =="light":
        expand_button['bg'] = '#fafafa'

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg'] = '#999999'

def returnm_size_on_hovering(event):
    global minimize_button
    themecheck()
    if mode =="dark":
        minimize_button['bg'] = '#1c1c1c'
    if mode =="light":
        minimize_button['bg'] = '#fafafa'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
                    
def autoupdate():
    if autoupdateval == 1:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        x=subprocess.run(["winget", "upgrade"], capture_output=True, text=True,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)
        app_names = re.findall(r'^\s*(.+?)\s{2,}', x.stdout, flags=re.MULTILINE)
        app_names = app_names[2:-1]
        for i in app_names:
            subprocess.run(["winget", "upgrade", i],stderr=subprocess.PIPE,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)
                
def mainwindow():
    global close_button
    global expand_button
    global minimize_button
    global main
    main = Toplevel()
    threading.Thread(target=autoupdate).start()
    main.tk.call('wm', 'iconphoto', main._w, ImageTk.PhotoImage(file='images\softhub.ico'))
    mainsplash.withdraw()
    screenwidth = main.winfo_screenwidth()
    screenheight = main.winfo_screenheight()
    app_height = int(screenheight) - 48
    main.geometry(f'{screenwidth}x{app_height}+0+0')
    main.title("Softhub")
    main.attributes("-alpha", 1)
    main.overrideredirect(True)
    main.minimized = False
    main.maximized = False
    title_bar = Frame(main, relief='groove', bd=0.5, highlightthickness=0)
    close_button = Button(title_bar, text='  ✕  ', command=lambda: main.destroy(), padx=2, pady=7, font=("calibri", 13),
                          bd=0, highlightthickness=0)
    expand_button = Button(title_bar, text='  ◻  ', command=lambda:maximize_me(), padx=2, pady=7, bd=0,
                           font=("calibri", 13), highlightthickness=0)
    minimize_button = Button(title_bar, text='  —  ', command=lambda:minimize_me(), padx=2, pady=7, bd=0,
                             font=("calibri", 13), highlightthickness=0)
    title_bar_title = Label(title_bar, text="Softhub", bd=0, font=("helvetica", 14),
                            highlightthickness=0)

    searchdark = PhotoImage(file=r"images\searchdark.png")
    searchdark = searchdark.subsample(11,11)
    searchlight = PhotoImage(file=r"images\searchlight.png")
    searchlight = searchlight.subsample(11,11)

    # pack the widgets
    title_bar.pack(fill=X)

    close_button.pack(side=RIGHT, ipadx=7, ipady=1)
    expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
    minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
    appicon = PhotoImage(file=r"images\softhuḃicon.png")
    appicon = appicon.subsample(6, 6)
    label = Label(title_bar, image=appicon)
    label.pack(side=LEFT)
    title_bar_title.pack(side=LEFT, padx=10)

    def checkallpack():

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #winget apps check
        winpack = str(subprocess.run(["winget", "list", "--source", "winget"], check=True, capture_output=True,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
        allpack=winpack
        installedapplist=[]

    def instwindow():
        def set_appwindow(mainWindow):  # to display the window icon on the taskbar,
            # even when using main.overrideredirect(True)
            # Some WindowsOS styles, required for task bar integration
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            # Magic
            hwnd = windll.user32.GetParent(mainWindow.winfo_id())
            stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            stylew = stylew & ~WS_EX_TOOLWINDOW
            stylew = stylew | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

            mainWindow.wm_withdraw()
            mainWindow.after(10, lambda: mainWindow.wm_deiconify())

        def minimize_me():
            instwin.attributes("-alpha",0) # so you can't see the window when is minimized
            instwin.minimized = True    
            instwin.bind("<FocusIn>",deminimize)    

        def fake_func(event):
            return None

        def deminimize(event):

            instwin.focus() 
            instwin.attributes("-alpha",1) # so you can see the window when is not minimized
            if instwin.minimized == True:
                instwin.minimized = False    

            instwin.bind("<FocusIn>",fake_func)


        def deminimzewhenappinstalled():
            instwin.focus()
            instwin.attributes("-alpha", 1)  # so you can see the window when is not minimized
            if instwin.minimized == True:
                instwin.minimized = False


        def maximize_me():
            if instwin.maximized == False:  # if the window was not maximized
                instwin.normal_size = instwin.geometry()
                expand_button.config(text="  🗗  ")
                instwin.geometry(f"{instwin.winfo_screenwidth()}x{instwin.winfo_screenheight()}+0+0")
                instwin.maximized = not instwin.maximized
                # maximized

            else:  # if the window was maximized
                expand_button.config(text="  ◻  ")
                instwin.geometry(instwin.normal_size)
                instwin.maximized = not instwin.maximized
                # not maximized

        
        global instwin
        instwin = Toplevel()
        instwin.tk.call('wm', 'iconphoto', instwin._w, ImageTk.PhotoImage(file='images\softhub.ico'))
        main.withdraw()
        screenwidth = instwin.winfo_screenwidth()
        screenheight = instwin.winfo_screenheight()
        app_height = int(screenheight) - 48
        instwin.geometry(f'{screenwidth}x{app_height}+0+0')
        instwin.title("Softhub")
        instwin.attributes("-alpha", 1)
        instwin.overrideredirect(True)
        instwin.minimized = False
        instwin.maximized = False
        title_bar = Frame(instwin, relief='groove', bd=0.5, highlightthickness=0)
        close_button = Button(title_bar, text='  ✕  ',command=lambda:[instwin.destroy(),main.destroy()], padx=2, pady=7, font=("calibri", 13),
                            bd=0, highlightthickness=0)
        expand_button = Button(title_bar, text='  ◻  ', command=lambda:maximize_me(), padx=2, pady=7, bd=0,
                            font=("calibri", 13), highlightthickness=0)
        minimize_button = Button(title_bar, text='  —  ', command=lambda:minimize_me(), padx=2, pady=7, bd=0,
                                font=("calibri", 13), highlightthickness=0)
        title_bar_title = Label(title_bar, text="Softhub", bd=0, font=("helvetica", 14),
                                highlightthickness=0)

        explore_button = ttk.Button(title_bar, text="Explore",width=15,command=lambda: [instwinremove(),updwinremove()]) 
        installed_button = ttk.Button(title_bar, text="Installed",width=15,command=lambda:[instwinremove(),updwinremove(),instwindow()])
        Update_button = ttk.Button(title_bar, text="Updates",width=15,command=lambda: [instwinremove(),updwinremove(),Updwindow()])
        
        explore_button.place(relx=0.45,rely=0.15)
        installed_button.place(relx=0.33,rely=0.15)
        Update_button.place(relx=0.57,rely=0.15)
        
        # pack the widgets
        title_bar.pack(fill=X)

        close_button.pack(side=RIGHT, ipadx=7, ipady=1)
        expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
        minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
        appicon = PhotoImage(file=r"images\softhuḃicon.png")
        appicon = appicon.subsample(6, 6)
        label = Label(title_bar, image=appicon)
        label.pack(side=LEFT)
        title_bar_title.pack(side=LEFT, padx=10)

        sidebar2= Frame(instwin, height=28, relief='groove', bd=0.5, highlightthickness=0)
        sidebar2.pack(side='top', fill='both')

        status = ttk.Label(sidebar2, text="v.0.7.Alpha", font=("Segou UI variable", 10))
        status.place(relx=0.92, rely=0.1)

        quote = ttk.Label(sidebar2, text="Simplifying software management", font=("Segou UI variable", 10))
        quote.place(relx=0.435, rely=0.1)

        headinglabel = ttk.Label(instwin,text="Installed Apps", font=("Segou UI variable", 20))
        headinglabel.pack(anchor=CENTER, pady=10)
        
        on = PhotoImage(file=r"images\darkicon.png")
        on = on.subsample(5, 5)
        off = PhotoImage(file=r"images\lighticon.png")
        off = off.subsample(5, 5)


        def switch():
            global is_on
            global mode
            if is_on == True:
                is_on = False
                mode = "dark"
                with open("theme.json", "w") as file:
                    data = {"mode": mode}
                    json.dump(data, file)
                sv.set_theme("dark")
                theme.config(image=on)
                searchbutton.config(image=searchdark)
                label.update()

            else:
                is_on = True
                mode = "light"
                with open("theme.json", "w") as file:
                    data = {"mode": mode}
                    json.dump(data, file)
                sv.set_theme("light")
                theme.config(image=off)
                searchbutton.config(image=searchlight)
                label.update()


        theme = ttk.Button(title_bar, image=on, padding=0,command=lambda: switch())
        theme.place(relx=0.79, rely=0.125)

        if mode == "light":
            theme.config(image=off)
        elif mode == "dark":
            theme.config(image=on)
    
        
        def openlink():
            webbrowser.open_new("https://github.com/ACExSWAROOP")

        abouticon = PhotoImage(file=r"images\about.png")
        abouticon = abouticon.subsample(22, 22)
        aboutbutton = ttk.Button(title_bar, image=abouticon, padding=0, command=lambda: openlink())
        aboutbutton.place(relx=0.1, rely=0.15)

        settingsicon= PhotoImage(file=r"images\settings.png")
        settingsicon = settingsicon.subsample(18, 18)
        settingsbutton = ttk.Button(title_bar, image=settingsicon, padding=0, command=lambda: settingswindow())
        settingsbutton.place(relx=0.84, rely=0.075)

        close_button.bind('<Enter>', changex_on_hovering)
        close_button.bind('<Leave>', returnx_to_normalstate)
        expand_button.bind('<Enter>', change_size_on_hovering)
        expand_button.bind('<Leave>', return_size_on_hovering)
        minimize_button.bind('<Enter>', changem_size_on_hovering)
        minimize_button.bind('<Leave>', returnm_size_on_hovering)

        # main frame
        window = Frame(instwin, highlightthickness=0)
        window.pack(expand=1, fill=BOTH)


        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            clr()
            intcheckapp("instwin")
            result = str(subprocess.run(["winget","list","--source","winget"], capture_output=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
            start = result.index("Name")
            end = result.index("stderr=b'')")
            result = result[start:end]
            result = result.strip().split("\\r\\n")
            
            for line in result[2:]:
                items = line.split()

                if len(items)==3:
                    appname = items[0:1]
                    app_id = items[1]
                elif len(items)==4:
                    appname = items[0:2]
                    app_id = items[2]
                elif len(items)==5:
                    appname = items[0:3]
                    app_id = items[3]
                elif len(items)==6:
                    appname = items[0:4]
                    app_id = items[4]
                elif len(items)==7:
                    appname = items[0:5]
                    app_id = items[5]
                elif len(items)==8:
                    appname = items[0:6]
                    app_id = items[6]
                elif len(items)==9:
                    appname = items[0:7]
                    app_id = items[7]
                elif len(items)==10:
                    appname = items[0:8]
                    app_id = items[8]
                elif len(items)==11:
                    appname = items[0:9]
                    app_id = items[9]
                elif len(items)==12:
                    appname = items[0:10]
                    app_id = items[10]
                elif len(items)==13:
                    appname = items[0:11]
                    app_id = items[11]
                elif len(items)==14:
                    appname = items[0:12]
                    app_id = items[12]
                elif len(items)==15:
                    appname = items[0:13]
                    app_id = items[13]
                elif len(items)==16:
                    appname = items[0:14]
                    app_id = items[14]
                elif len(items)==17:
                    appname = items[0:15]   
                    app_id = items[15]
                apps.append([appname,app_id])
            apps.pop()
        except NameError:
            pass
        except ValueError:
            pass
        
        def update_app(app_id):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["winget","update","--id" ,app_id ,"--include-unknown"], check=True, capture_output=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)

        def uninstall_app(app_id):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["winget","uninstall","--id" ,app_id], check=True, capture_output=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)

        canvas = Canvas(window)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas to hold the app entries
        app_frame = Frame(canvas)
        canvas.create_window((0, 0), window=app_frame, anchor="nw")

        for idx, app in enumerate(apps, start=1):
            app_name = app[0]
            app_id = app[1]

            # Create a frame for each app entry
            entry_frame = Frame(app_frame)
            entry_frame.pack(anchor="w", padx=10, pady=5)

            # Create the serial number label
            serial_label = ttk.Label(entry_frame, text=f"{idx}.")
            serial_label.pack(side="left", padx=(0, 10))

            # Create the app name label
            app_label = ttk.Label(entry_frame, text=app_name)
            app_label.pack(side="left")

            # Create the update button
            update_button = ttk.Button(entry_frame, text="Update", command=lambda id=app_id: update_app(id))
            update_button.pack(side="left", padx=10)

            # Create the uninstall button
            uninstall_button = ttk.Button(entry_frame, text="Uninstall", command=lambda id=app_id: uninstall_app(id))
            uninstall_button.pack(side="left")

            app_frame.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
            window.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
            instwin.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))

         # some settings
        instwin.bind("<FocusIn>", deminimize)  # to view the window by clicking on the window icon on the taskbar
        instwin.after(10, lambda: set_appwindow(instwin))  # to see the icon on the task bar
        instwin.mainloop()


    def Updwindow():
        def set_appwindow(mainWindow):  # to display the window icon on the taskbar,
            # even when using main.overrideredirect(True)
            # Some WindowsOS styles, required for task bar integration
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            # Magic
            hwnd = windll.user32.GetParent(mainWindow.winfo_id())
            stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            stylew = stylew & ~WS_EX_TOOLWINDOW
            stylew = stylew | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

            mainWindow.wm_withdraw()
            mainWindow.after(10, lambda: mainWindow.wm_deiconify())

        def minimize_me():
            updwin.attributes("-alpha",0) # so you can't see the window when is minimized
            updwin.minimized = True    
            updwin.bind("<FocusIn>",deminimize)    

        def fake_func(event):
            return None

        def deminimize(event):

            updwin.focus() 
            updwin.attributes("-alpha",1) # so you can see the window when is not minimized
            if updwin.minimized == True:
                updwin.minimized = False    

            updwin.bind("<FocusIn>",fake_func)


        def deminimzewhenappinstalled():
            updwin.focus()
            updwin.attributes("-alpha", 1)  # so you can see the window when is not minimized
            if updwin.minimized == True:
                updwin.minimized = False


        def maximize_me():
            if updwin.maximized == False:  # if the window was not maximized
                updwin.normal_size = updwin.geometry()
                expand_button.config(text="  🗗  ")
                updwin.geometry(f"{updwin.winfo_screenwidth()}x{updwin.winfo_screenheight()}+0+0")
                updwin.maximized = not updwin.maximized
                # maximized

            else:  # if the window was maximized
                expand_button.config(text="  ◻  ")
                updwin.geometry(updwin.normal_size)
                updwin.maximized = not updwin.maximized
                # not maximized

        global updwin
        updwin = Toplevel()
        updwin.tk.call('wm', 'iconphoto', updwin._w, ImageTk.PhotoImage(file='images\softhub.ico'))
        main.withdraw()
        screenwidth = updwin.winfo_screenwidth()
        screenheight = updwin.winfo_screenheight()
        app_height = int(screenheight) - 48
        updwin.geometry(f'{screenwidth}x{app_height}+0+0')
        updwin.title("Softhub")
        updwin.attributes("-alpha", 1)
        updwin.overrideredirect(True)
        updwin.minimized = False
        updwin.maximized = False
        title_bar = Frame(updwin, relief='groove', bd=0.5, highlightthickness=0)
        close_button = Button(title_bar, text='  ✕  ', command=lambda:[updwin.destroy(),main.destroy()], padx=2, pady=7, font=("calibri", 13),
                            bd=0, highlightthickness=0)
        expand_button = Button(title_bar, text='  ◻  ', command=lambda:maximize_me(), padx=2, pady=7, bd=0,
                            font=("calibri", 13), highlightthickness=0)
        minimize_button = Button(title_bar, text='  —  ', command=lambda:minimize_me(), padx=2, pady=7, bd=0,
                                font=("calibri", 13), highlightthickness=0)
        title_bar_title = Label(title_bar, text="Softhub", bd=0, font=("helvetica", 14),
                                highlightthickness=0)

        explore_button = ttk.Button(title_bar, text="Explore",width=15,command=lambda: [instwinremove(),updwinremove()]) 
        installed_button = ttk.Button(title_bar, text="Installed",width=15,command=lambda:[instwinremove(),updwinremove(),instwindow()])
        Update_button = ttk.Button(title_bar, text="Updates",width=15,command=lambda: [instwinremove(),updwinremove(),Updwindow()])

        
        close_button.bind('<Enter>', changex_on_hovering)
        close_button.bind('<Leave>', returnx_to_normalstate)
        expand_button.bind('<Enter>', change_size_on_hovering)
        expand_button.bind('<Leave>', return_size_on_hovering)
        minimize_button.bind('<Enter>', changem_size_on_hovering)
        minimize_button.bind('<Leave>', returnm_size_on_hovering)

        explore_button.place(relx=0.45,rely=0.15)
        installed_button.place(relx=0.33,rely=0.15)
        Update_button.place(relx=0.57,rely=0.15)
        
        # pack the widgets
        title_bar.pack(fill=X)

        close_button.pack(side=RIGHT, ipadx=7, ipady=1)
        expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
        minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
        appicon = PhotoImage(file=r"images\softhuḃicon.png")
        appicon = appicon.subsample(6, 6)
        label = Label(title_bar, image=appicon)
        label.pack(side=LEFT)
        title_bar_title.pack(side=LEFT, padx=10)

        sidebar2= Frame(updwin, height=28, relief='groove', bd=0.5, highlightthickness=0)
        sidebar2.pack(side='top', fill='both')

        status = ttk.Label(sidebar2, text="v.0.7.Alpha", font=("Segou UI variable", 10))
        status.place(relx=0.92, rely=0.1)

        quote = ttk.Label(sidebar2, text="Simplifying software management", font=("Segou UI variable", 10))
        quote.place(relx=0.435, rely=0.1)

        headinglabel = ttk.Label(updwin,text="Update Apps", font=("Segou UI variable", 20))
        headinglabel.pack(anchor=CENTER, pady=10)

        on = PhotoImage(file=r"images\darkicon.png")
        on = on.subsample(5, 5)
        off = PhotoImage(file=r"images\lighticon.png")
        off = off.subsample(5, 5)
        
        def switch():
            global is_on
            global mode
            if is_on == True:
                theme.config(image=on)
                searchbutton.config(image=searchdark)
                is_on = False
                mode = "dark"
                with open("theme.json", "w") as file:
                    data = {"mode": mode}
                    json.dump(data, file)
                sv.set_theme("dark")
                label.update()

            else:
                theme.config(image=off)
                searchbutton.config(image=searchlight)
                is_on = True
                mode = "light"
                with open("theme.json", "w") as file:
                    data = {"mode": mode}
                    json.dump(data, file)
                sv.set_theme("light")
                label.update()


        theme = ttk.Button(title_bar, image=on, padding=0,command=lambda: switch())
        theme.place(relx=0.79, rely=0.125)

        if mode == "light":
            theme.config(image=off)
        elif mode == "dark":
            theme.config(image=on)
        
        def openlink():
            webbrowser.open_new("https://github.com/ACExSWAROOP")

        abouticon = PhotoImage(file=r"images\about.png")
        abouticon = abouticon.subsample(22, 22)
        aboutbutton = ttk.Button(title_bar, image=abouticon, padding=0, command=lambda: openlink())
        aboutbutton.place(relx=0.1, rely=0.15)

        settingsicon= PhotoImage(file=r"images\settings.png")
        settingsicon = settingsicon.subsample(18, 18)
        settingsbutton = ttk.Button(title_bar, image=settingsicon, padding=0, command=lambda: settingswindow())
        settingsbutton.place(relx=0.84, rely=0.075)

        # main frame
        window = Frame(updwin, highlightthickness=0)
        window.pack(expand=1, fill=BOTH)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            clr()
            intcheckapp("updwin")
            result = str(subprocess.run(["winget","update","--source","winget"], capture_output=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
            start = result.index("Name")
            end = result.index("stderr=b'')")
            result = result[start:end]
            result = result.strip().split("\\r\\n")
            for line in result[2:-1]:
                items = line.split()
                if len(items)==4:
                    appname = items[0:1]
                    app_id = items[1]
                elif len(items)==5:
                    appname = items[0:2]
                    app_id = items[2]
                elif len(items)==6:
                    appname = items[0:3]
                    app_id = items[3]
                elif len(items)==7:
                    appname = items[0:4]
                    app_id = items[4]
                elif len(items)==8:
                    appname = items[0:5]
                    app_id = items[5]
                elif len(items)==9:
                    appname = items[0:6]
                    app_id = items[6]
                elif len(items)==10:
                    appname = items[0:7]
                    app_id = items[7]
                elif len(items)==11:
                    appname = items[0:8]
                    app_id = items[8]
                elif len(items)==12:
                    appname = items[0:9]
                    app_id = items[9]
                elif len(items)==13:
                    appname = items[0:10]
                    app_id = items[10]
                elif len(items)==14:
                    appname = items[0:11]
                    app_id = items[11]
                elif len(items)==15:
                    appname = items[0:12]
                    app_id = items[12]
                elif len(items)==16:
                    appname = items[0:13]
                    app_id = items[13]
                elif len(items)==17:
                    appname = items[0:14]   
                    app_id = items[14]
                apps.append([appname,app_id])
            apps.pop()
        except NameError:
            pass
        except ValueError:
            pass
        
        def update_app(app_id):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["winget","update","--id" ,app_id ,"--include-unknown"], check=True, capture_output=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)

        canvas = Canvas(window)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas to hold the app entries
        app_frame = Frame(canvas)
        canvas.create_window((0, 0), window=app_frame, anchor="nw")

        for idx, app in enumerate(apps, start=1):
            app_name = app[0]
            app_id = app[1]

            # Create a frame for each app entry
            entry_frame = Frame(app_frame)
            entry_frame.pack(anchor="w", padx=10, pady=5)

            # Create the serial number label
            serial_label = ttk.Label(entry_frame, text=f"{idx}.")
            serial_label.pack(side="left", padx=(0, 10))

            # Create the app name label
            app_label = ttk.Label(entry_frame, text=app_name)
            app_label.pack(side="left")

            # Create the update button
            update_button = ttk.Button(entry_frame, text="Update", command=lambda id=app_id: update_app(id))
            update_button.pack(side="left", padx=10)


            app_frame.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
            window.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
            updwin.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
         # some settings

        updwin.bind("<FocusIn>", deminimize)  # to view the window by clicking on the window icon on the taskbar
        updwin.after(10, lambda: set_appwindow(updwin))  # to see the icon on the task bar
        updwin.mainloop()

    def instwinremove():
        try:
            main.attributes("-alpha", 1)
            main.deiconify()
            instwin.destroy()
        except NameError:
            pass
    def updwinremove():
        try:
            main.attributes("-alpha", 1)
            main.deiconify()
            updwin.destroy()
        except NameError:
            pass

    explore_button = ttk.Button(title_bar, text="Explore",width=15,command=lambda: [instwinremove(),updwinremove()]) 
    installed_button = ttk.Button(title_bar, text="Installed",width=15,command=lambda:[instwinremove(),updwinremove(),instwindow()])
    Update_button = ttk.Button(title_bar, text="Updates",width=15,command=lambda: [instwinremove(),updwinremove(),Updwindow()])

    explore_button.place(relx=0.45,rely=0.15)
    installed_button.place(relx=0.33,rely=0.15)
    Update_button.place(relx=0.57,rely=0.15)

    # main frame
    window = Frame(main, highlightthickness=0)
    window.pack(expand=1, fill=BOTH)

    def close():
        settings.destroy()

    
    def settingswindow():
        def savedoptions():
            try:
                with open("settings.json", "r") as x:
                    data = json.load(x)
                    autoupdateval=data["autoupdate"]
                    if  autoupdateval == 1:
                        autoupd.set(1)
            except json.JSONDecodeError:
                pass
        global settings
        settings = Toplevel()
        settings.overrideredirect(True)
        app_width = 512
        app_height = 256
        screenwidth = settings.winfo_screenwidth()
        screenheight = settings.winfo_screenheight()
        x = (screenwidth / 2) - (app_width / 2)
        y = (screenheight / 2) - (app_height / 2)
        settings.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        main.bind("<Button-3>", lambda e: close())
        settings.bind("<Button-3>", lambda e: close())
        main.bind("<Button-1>", lambda e: close())
        global autoupd
        autoupd = IntVar()
        
        def saveconfig():
            checkvalues= {}
            checkvalues["autoupdate"] = autoupd.get()

            with open("settings.json", "w") as json_file:
                json.dump(checkvalues, json_file)

        pref =ttk.Label(settings,text="Settings", font=("Segou UI variable", 20))
        atupdate = ttk.Checkbutton(settings,text="Enable Auto Update", variable=autoupd)
        
        savebutton= ttk.Button(settings,text="Save",width=15,command=lambda: [saveconfig(),settings.destroy(),main.attributes("-alpha", 1)])
        pref.place(relx=0.38,rely=0.15)
        atupdate.place(relx=0.335,rely=0.3)
        savebutton.place(relx=0.35,rely=0.8)
        
        savedoptions()
        
        settings.mainloop()

    def selectcategory(x):
        x=listbox.get(ACTIVE)
        if x == "3D modeling and animation apps":
            my_canvas.yview("moveto", 0)
        elif x == '3D printing apps':
            my_canvas.yview("moveto",0.00909090909090909)
        elif x == '3D rendering apps':
            my_canvas.yview("moveto",0.01818181818181818)
        elif x == '3D scanning apps':
            my_canvas.yview("moveto",0.02727272727272727)
        elif x == 'Accounting and financial management apps':
            my_canvas.yview("moveto",0.03636363636363636)
        elif x == 'Audio recording and editing apps':
            my_canvas.yview("moveto",0.045454545454545456)
        elif x == 'Augmented reality content creation apps':
            my_canvas.yview("moveto",0.05454545454545454)
        elif x == 'Backup and recovery apps':
            my_canvas.yview("moveto",0.06363636363636363)
        elif x ==  'Business apps' :
            my_canvas.yview("moveto",0.07272727272727272)
        elif x == 'CAD software':
            my_canvas.yview("moveto",0.08181818181818182)
        elif x == 'Cloud storage and syncing apps':
            my_canvas.yview("moveto",0.09090909090909091)
        elif x ==  'Code editors':
            my_canvas.yview("moveto",0.1)
        elif x ==  'Command line utilities':
            my_canvas.yview("moveto",0.10909090909090909)
        elif x ==  'Communication apps':
            my_canvas.yview("moveto",0.11818181818181818)
        elif x ==  'Creativity apps':
            my_canvas.yview("moveto",0.12727272727272726)
        elif x ==  'Customer relationship management apps' :
            my_canvas.yview("moveto",0.13636363636363635)
        elif x == 'Data backup apps' :
            my_canvas.yview("moveto",0.14545454545454545)
        elif x == 'Data recovery apps':
            my_canvas.yview("moveto",0.15454545454545454)
        elif x ==  'Database administration apps':
            my_canvas.yview("moveto",0.16363636363636364)
        elif x == 'Database design and development apps':
            my_canvas.yview("moveto",0.17272727272727273)
        elif x == 'Database management apps':
            my_canvas.yview("moveto",0.18181818181818182)
        elif x ==  'Database modeling apps' :
            my_canvas.yview("moveto",0.19090909090909092)
        elif x == 'Database reporting apps':
            my_canvas.yview("moveto",0.2)
        elif x ==  'Debugging tools' :
            my_canvas.yview("moveto",0.20909090909090908)
        elif x == 'Development apps' :
            my_canvas.yview("moveto",0.21818181818181817)
        elif x == 'Disk cleanup and management apps':
            my_canvas.yview("moveto",0.22727272727272727)
        elif x ==  'Documents' :
            my_canvas.yview("moveto",0.23636363636363636)
        elif x == 'Driver update and management apps':     
            my_canvas.yview("moveto",0.24545454545454545)
        elif x == 'E-book readers':
            my_canvas.yview("moveto",0.2545454545454545)
        elif x == 'E-commerce apps':
            my_canvas.yview("moveto",0.2636363636363636)
        elif x == 'E-mail marketing apps':
            my_canvas.yview("moveto",0.2727272727272727)
        elif x == 'Educational apps':
            my_canvas.yview("moveto",0.2818181818181818)
        elif x ==  'Educational apps for kids':
            my_canvas.yview("moveto",0.2909090909090909)
        elif x ==  'Encryption and security apps':
            my_canvas.yview("moveto",0.3)
        elif x == 'Enterprise resource planning apps' :
            my_canvas.yview("moveto",0.3090909090909091)
        elif x == 'Entertainment apps':         
            my_canvas.yview("moveto",0.3181818181818182)
        elif x == 'File conversion apps':
            my_canvas.yview("moveto",0.32727272727272727)
        elif x == 'File transfer and synchronization apps':
            my_canvas.yview("moveto",0.33636363636363636)
        elif x == 'Finance apps':
            my_canvas.yview("moveto",0.34545454545454546)
        elif x == 'Firewall and intrusion detection apps':
            my_canvas.yview("moveto",0.35454545454545455)
        elif x == 'Game development apps':
            my_canvas.yview("moveto",0.36363636363636365)
        elif x == 'Game VR and AR development apps':
            my_canvas.yview("moveto",0.37272727272727274)
        elif x == 'Game accessibility apps':
            my_canvas.yview("moveto",0.38181818181818183)
        elif x ==  'Game analytics and data visualization apps':
            my_canvas.yview("moveto",0.39090909090909093)
        elif x ==  'Game community and social media apps':
            my_canvas.yview("moveto",0.4)
        elif x == 'Game distribution and publishing apps':
            my_canvas.yview("moveto",0.4090909090909091)
        elif x == 'Game emulators':
            my_canvas.yview("moveto",0.41818181818181815)
        elif x == 'Game engines':       
            my_canvas.yview("moveto",0.42727272727272725)
        elif x == 'Game launcher':
            my_canvas.yview("moveto",0.43636363636363634)
        elif x == 'Game marketing and promotion apps':
            my_canvas.yview("moveto",0.44545454545454544)
        elif x ==  'Game monetization apps':
            my_canvas.yview("moveto",0.45454545454545453)
        elif x == 'Game motion capture apps':
            my_canvas.yview("moveto",0.4636363636363636)
        elif x ==  'Game music composition apps':
            my_canvas.yview("moveto",0.4727272727272727)
        elif x == 'Game networking apps':
            my_canvas.yview("moveto",0.4818181818181818)
        elif x ==  'Game physics apps':
            my_canvas.yview("moveto",0.4909090909090909)
        elif x == 'Game physics simulation apps':
            my_canvas.yview("moveto",0.5)
        elif x == 'Game scriptwriting and story development apps':
            my_canvas.yview("moveto",0.509090909090909)
        elif x == 'Game streaming and broadcasting apps':
            my_canvas.yview("moveto",0.5181818181818182)
        elif x == 'Graphic design apps':
            my_canvas.yview("moveto",0.5272727272727272)
        elif x == 'Health and fitness apps':          
            my_canvas.yview("moveto",0.5363636363636364)
        elif x == 'Human resources management apps':
            my_canvas.yview("moveto",0.5454545454545454)
        elif x == 'Image editing and manipulation apps':
            my_canvas.yview("moveto",0.5545454545454546)
        elif x == 'Integrated development environments (IDEs)':
            my_canvas.yview("moveto",0.5636363636363636)
        elif x ==  'Inventory management apps':
            my_canvas.yview("moveto",0.5727272727272728)
        elif x == 'Language learning apps':
            my_canvas.yview("moveto",0.5818181818181818)
        elif x ==  'Map and navigation apps':
            my_canvas.yview("moveto",0.5909090909090909)
        elif x == 'Mind and body apps':
            my_canvas.yview("moveto",0.6)
        elif x == 'Mind mapping and brainstorming apps':
            my_canvas.yview("moveto",0.6090909090909091)
        elif x == 'Multimedia':
            my_canvas.yview("moveto",0.6181818181818182)
        elif x == 'Music streaming apps':
            my_canvas.yview("moveto",0.6272727272727273)
        elif x == 'Network monitoring and management apps':
            my_canvas.yview("moveto",0.6363636363636364)
        elif x == 'News apps':
            my_canvas.yview("moveto",0.6454545454545455)
        elif x == 'Office Suite apps':
            my_canvas.yview("moveto",0.6545454545454545)
        elif x == 'PDF readers and editors':
            my_canvas.yview("moveto",0.6636363636363637)
        elif x == 'Parental control apps':
            my_canvas.yview("moveto",0.6727272727272727)
        elif x ==  'Password management apps':
            my_canvas.yview("moveto",0.6818181818181818)
        elif x == 'Payroll management apps':
            my_canvas.yview("moveto",0.6909090909090909)
        elif x == 'Personal organization apps':
            my_canvas.yview("moveto",0.7)
        elif x == 'Point-of-sale apps':
            my_canvas.yview("moveto",0.7090909090909091)
        elif x == 'Presentation and slide creation':
            my_canvas.yview("moveto",0.7181818181818181)
        elif x == 'Profiling tools':
            my_canvas.yview("moveto",0.7272727272727273)
        elif x == 'Programming and development tools':
            my_canvas.yview("moveto",0.7363636363636363)
        elif x == 'Project management apps':
            my_canvas.yview("moveto",0.7454545454545455)
        elif x == 'Remote access and control apps':
            my_canvas.yview("moveto",0.7545454545454545)
        elif x == 'Retail management apps':
            my_canvas.yview("moveto",0.7636363636363637)
        elif x ==  'SEO and analytics apps':
            my_canvas.yview("moveto",0.7727272727272727)
        elif x == 'Screenshot and screen recording apps':
            my_canvas.yview("moveto",0.7818181818181819)
        elif x == 'Social media apps':
            my_canvas.yview("moveto",0.7909090909090909)
        elif x ==  'Supply chain management apps':
            my_canvas.yview("moveto",0.8)
        elif x == 'System information and diagnostic apps':
            my_canvas.yview("moveto",0.8090909090909091)
        elif x == 'System optimization and performance apps':
            my_canvas.yview("moveto",0.8181818181818182)
        elif x == 'Tax preparation and filing apps':
            my_canvas.yview("moveto",0.8272727272727273)
        elif x == 'Terminal emulators':
            my_canvas.yview("moveto",0.8363636363636363)
        elif x == 'Text editors' :
            my_canvas.yview("moveto",0.8454545454545455)
        elif x == 'Time tracking and invoicing apps':
            my_canvas.yview("moveto",0.8545454545454545)
        elif x ==  'Travel apps':
            my_canvas.yview("moveto",0.8636363636363636)
        elif x == 'Utilities apps':
            my_canvas.yview("moveto",0.8727272727272727)
        elif x == 'VPN apps':
            my_canvas.yview("moveto",0.8818181818181818)
        elif x == 'Video and audio compression apps':
            my_canvas.yview("moveto",0.8909090909090909)
        elif x == 'Video editing apps':
            my_canvas.yview("moveto",0.9)
        elif x == 'Video streaming apps':
            my_canvas.yview("moveto",0.9090909090909091)
        elif x == 'Virtual and augmented reality apps':
            my_canvas.yview("moveto",0.9181818181818182)
        elif x == 'Virtual event and webinar apps':
            my_canvas.yview("moveto",0.9272727272727272)
        elif x == 'Virtual meeting and conference apps':
            my_canvas.yview("moveto",0.9363636363636364)
        elif x == 'Virtual reality content creation apps':
            my_canvas.yview("moveto",0.9454545454545454)
        elif x ==  'Virtualization software':
            my_canvas.yview("moveto",0.9545454545454546)
        elif x == 'Voice recognition apps' :
            my_canvas.yview("moveto",0.9636363636363636)
        elif x == 'Weather apps':
            my_canvas.yview("moveto",0.9727272727272728)
        elif x == 'Web Browsers' :
            my_canvas.yview("moveto",0.9818181818181818)
        elif x == 'Windows customization apps':
            my_canvas.yview("moveto",0.990909090909091)

    sidebar2= Frame(window, height=28, relief='groove', bd=0.5, highlightthickness=0)
    sidebar2.pack(side='top', fill='both')

    categorylabel=ttk.Label(sidebar2,text="Categories", font=("Segou UI variable", 12),borderwidth=2)
    categorylabel.place(relx=0.065,rely=0.10)

    status = ttk.Label(sidebar2, text="v.0.7.Alpha", font=("Segou UI variable", 10))
    status.place(relx=0.92, rely=0.1)

    quote = ttk.Label(sidebar2, text="Simplifying software management", font=("Segou UI variable", 10))
    quote.place(relx=0.435, rely=0.1)

    sidebar = ttk.Frame(window, width=30, height=300,relief='raised')
    sidebar.pack(side='left', fill='both')

    sidebar3= Frame(window, height=45, relief='flat', bd=0.5, highlightthickness=0)
    sidebar3.pack(side='top', fill='both')

    searchval= StringVar()

    def searchclick(event):
        if searchbar.get() == "Search:-":
            searchbar.delete(0, END)
        
    def searchempty(event):
        if searchbar.get() == "":
            searchbar.insert(0, "Search:-")

    searchbar=ttk.Entry(sidebar3,textvariable=searchval,width=25)
    searchbar.place(relx=0.42,rely=0.15) 
    searchbar.insert(0, "Search:-")
    searchbar.bind('<FocusIn>', searchclick)
    searchbar.bind('<FocusOut>', searchempty)


    def checkappexists():
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        global search
        search=searchval.get()
        foundin=[0]
        global wingetresult
        try:
            wingetresult=str(subprocess.run(["winget", "search","--Name", search], stderr=subprocess.PIPE,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
            foundin[0]=1
            if wingetresult=="No package found matching input criteria.":
                foundin[0]=0
        except subprocess.CalledProcessError:
            foundin[0]=0

        
    global apps
    apps=[]

    def clr():
        global apps
        apps=[]

    def wininstall():
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            clr()
            intcheckapp("main")
            start = wingetresult.index("['")
            end = wingetresult.index("']")
            result = wingetresult[start+2:end].split("', '")
            result = str(subprocess.run(result, capture_output=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
            start = result.index("Name")
            end = result.index("stderr=b'')")
            result = result[start:end]
            result = result.strip().split("\\r\\n")
            global apps
            for line in result[2:]:
                items = line.split()
                print(items)
                if len(items)==4:
                    appname = items[0:1]
                    app_id = items[1]
                elif len(items)==5:
                    appname = items[0:2]
                    app_id = items[2]
                elif len(items)==6:
                    appname = items[0:3]
                    app_id = items[3]
                elif len(items)==7:
                    appname = items[0:4]
                    app_id = items[4]
                elif len(items)==8:
                    appname = items[0:5]
                    app_id = items[5]
                elif len(items)==9:
                    appname = items[0:6]
                    app_id = items[6]
                elif len(items)==10:
                    appname = items[0:7]
                    app_id = items[7]
                elif len(items)==11:
                    appname = items[0:8]
                    app_id = items[8]
                elif len(items)==12:
                    appname = items[0:9]
                    app_id = items[9]
                elif len(items)==13:
                    appname = items[0:10]
                    app_id = items[10]
                elif len(items)==14:
                    appname = items[0:11]
                    app_id = items[11]
                elif len(items)==15:
                    appname = items[0:12]
                    app_id = items[12]
                elif len(items)==16:
                    appname = items[0:13]
                    app_id = items[13]
                elif len(items)==17:
                    appname = items[0:14]   
                    app_id = items[14]
                apps.append([appname,app_id])
            apps.pop()
            selectinstall("winget")
        except NameError:
            pass
        except ValueError:
            pass
    
    def selectinstall(packman):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # Create a new window for search results
        selinst = Toplevel()
        selinst.overrideredirect(True)
        app_width = 768
        app_height = 256
        screenwidth = selinst.winfo_screenwidth()
        screenheight = selinst.winfo_screenheight()
        x = (screenwidth / 2) - (app_width / 2)
        y = (screenheight / 2) - (app_height / 2)
        selinst.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        main.bind("<Button-3>", lambda e: [selinst.destroy(),clr()])
        selinst.bind("<Button-3>", lambda e:[selinst.destroy(),clr()])
        main.bind("<Button-1>", lambda e:[selinst.destroy(),clr()])
        
        # Create a canvas to hold the app widgets
        canvas = Canvas(selinst)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(selinst, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Create a frame to contain the app widgets
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=NW)
        
        frame.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
        selinst.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
        
        def on_select():
            selected_ids = []
            for index, var in enumerate(vars):
                if var.get() == 1:
                    selected_ids.append(apps[index][1])

            if packman == "winget":
                for app_id in selected_ids:
                    subprocess.run(["winget", "install", "--id", app_id], stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)
 
        applabel=ttk.Label(frame,text="Select an App to Install:- \n",font=("TkDefaultFont", 16, "bold"))
        applabel.pack(anchor=W, pady=10)

        
        appnames= []
        for i in apps:
            appnames.append(i[0])

        vars = []
        for index, app_id in enumerate(appnames):
            var = IntVar()
            checkbox = ttk.Checkbutton(frame, text=app_id, variable=var)
            checkbox.pack(anchor=W, pady=3)
            checkbox.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
            vars.append(var)

        select_button = ttk.Button(frame, text="Install", command=lambda: on_select())
        if packman == "winget":
            select_button.pack(anchor=W, pady=10)

        spacing.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
        selinst.mainloop()

    
    global searchbutton
    searchbutton =ttk.Button(sidebar3,image=searchdark,padding=0,command=lambda:[checkappexists(),wininstall()])
    searchbutton.place(relx=0.585,rely=0.15)
    if mode == "light":
        searchbutton.config(image=searchlight)
    elif mode == "dark":
        searchbutton.config(image=searchdark)

    scrollbar = ttk.Scrollbar(sidebar)
    #scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(sidebar, yscrollcommand=scrollbar.set, highlightthickness=0,width=38)
    allcategories=['3D modeling and animation apps', '3D printing apps', '3D rendering apps', '3D scanning apps', 'Accounting and financial management apps', 'Audio recording and editing apps', 'Augmented reality content creation apps', 'Backup and recovery apps', 'Business apps', 'CAD software', 'Cloud storage and syncing apps', 'Code editors', 'Command line utilities', 'Communication apps', 'Creativity apps', 'Customer relationship management apps', 'Data backup apps', 'Data recovery apps', 'Database administration apps', 'Database design and development apps', 'Database management apps', 'Database modeling apps', 'Database reporting apps', 'Debugging tools', 'Development apps', 'Disk cleanup and management apps', 'Documents', 'Driver update and management apps', 'E-book readers', 'E-commerce apps', 'E-mail marketing apps', 'Educational apps', 'Educational apps for kids', 'Encryption and security apps', 'Enterprise resource planning apps', 'Entertainment apps', 'File conversion apps', 'File transfer and synchronization apps', 'Finance apps', 'Firewall and intrusion detection apps', 'Game development apps', 'Game VR and AR development apps', 'Game accessibility apps', 'Game analytics and data visualization apps', 'Game community and social media apps', 'Game distribution and publishing apps', 'Game emulators', 'Game engines', 'Game launcher', 'Game marketing and promotion apps', 'Game monetization apps', 'Game motion capture apps', 'Game music composition apps', 'Game networking apps', 'Game physics engines', 'Game physics simulation apps', 'Game scriptwriting and story development apps', 'Game streaming and broadcasting apps', 'Graphic design apps', 'Health and fitness apps', 'Human resources management apps', 'Image editing and manipulation apps', 'Integrated development environments (IDEs)', 'Inventory management apps', 'Language learning apps', 'Map and navigation apps', 'Mind and body apps', 'Mind mapping and brainstorming apps', 'Multimedia', 'Music streaming apps', 'Network monitoring and management apps', 'News apps', 'Office Suite apps', 'PDF readers and editors', 'Parental control apps', 'Password management apps', 'Payroll management apps', 'Personal organization apps', 'Point-of-sale apps', 'Presentation and slide creation apps', 'Profiling tools', 'Programming and development apps', 'Project management apps', 'Remote access and control apps', 'Retail management apps', 'SEO and analytics apps', 'Screenshot and screen recording apps', 'Social media apps', 'Supply chain management apps', 'System information and diagnostic apps', 'System optimization and performance apps', 'Tax preparation and filing apps', 'Terminal emulators', 'Text editors', 'Time tracking and invoicing apps', 'Travel apps', 'Utilities apps', 'VPN apps', 'Video and audio compression apps', 'Video editing apps', 'Video streaming apps', 'Virtual and augmented reality apps', 'Virtual event and webinar apps', 'Virtual meeting and conference apps', 'Virtual reality content creation apps', 'Virtualization software', 'Voice recognition apps', 'Weather apps', 'Web Browsers', 'Windows customization apps']
    for i in allcategories:
        listbox.insert(END,i)
    listbox.pack(side=LEFT, fill=Y)
    scrollbar.config(command=listbox.yview)
    listbox.bind("<Button-1>",selectcategory)
    font = ("Segoe UI variable", 9)
    listbox.config(font=font)

    on = PhotoImage(file=r"images\darkicon.png")
    on = on.subsample(5, 5)
    off = PhotoImage(file=r"images\lighticon.png")
    off = off.subsample(5, 5)

    def switch():
        global is_on
        global mode
        if is_on == True:
            theme.config(image=on)
            searchbutton.config(image=searchdark)
            is_on = False
            mode = "dark"
            with open("theme.json", "w") as file:
                data = {"mode": mode}
                json.dump(data, file)
            sv.set_theme("dark")
            label.update()

        else:
            theme.config(image=off)
            searchbutton.config(image=searchlight)
            is_on = True
            mode = "light"
            with open("theme.json", "w") as file:
                data = {"mode": mode}
                json.dump(data, file)
            sv.set_theme("light")
            label.update()


    theme = ttk.Button(title_bar, image=on, padding=0,command=lambda: switch())
    theme.place(relx=0.79, rely=0.125)

    if mode == "light":
        theme.config(image=off)
    elif mode == "dark":
        theme.config(image=on)
    
    def openlink():
        webbrowser.open_new("https://github.com/ACExSWAROOP")

    abouticon = PhotoImage(file=r"images\about.png")
    abouticon = abouticon.subsample(22, 22)
    aboutbutton = ttk.Button(title_bar, image=abouticon, padding=0, command=lambda: openlink())
    aboutbutton.place(relx=0.1, rely=0.15)

    settingsicon= PhotoImage(file=r"images\settings.png")
    settingsicon = settingsicon.subsample(18, 18)
    settingsbutton = ttk.Button(title_bar, image=settingsicon, padding=0, command=lambda: settingswindow())
    settingsbutton.place(relx=0.84, rely=0.075)
    settingsbutton.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))

    """def get_pos(event):  # this is executed when the title bar is clicked to move the window
        if main.maximized == False:
            xwin = main.winfo_x()
            ywin = main.winfo_y()
            startx = event.x_root
            starty = event.y_root
            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event):  # runs when window is dragged
                main.config(cursor="fleur")
                main.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

            def release_window(event):  # runs when window is released
                main.config(cursor="arrow")

            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            expand_button.config(text="  ◻  ")
            main.maximized = not main.maximized

    title_bar.bind('<Button-1>', get_pos)  # so you can drag the window from the title bar
    title_bar_title.bind('<Button-1>', get_pos)  # so you can drag the window from the title
    """

    # button effects in the title bar when hovering over buttons
    close_button.bind('<Enter>', changex_on_hovering)
    close_button.bind('<Leave>', returnx_to_normalstate)
    expand_button.bind('<Enter>', change_size_on_hovering)
    expand_button.bind('<Leave>', return_size_on_hovering)
    minimize_button.bind('<Enter>', changem_size_on_hovering)
    minimize_button.bind('<Leave>', returnm_size_on_hovering)

    
    """    # resize the window width
    resizex_widget = Frame(window, cursor='sb_h_double_arrow')
    resizex_widget.pack(side=RIGHT, ipadx=2, fill=Y)

    def resizex(event):
        xwin = main.winfo_x()
        difference = (event.x_root - xwin) - main.winfo_width()

        if main.winfo_width() > 1024:  # 150 is the minimum width for the window
            try:
                main.geometry(f"{main.winfo_width() + difference}x{main.winfo_height()}")
            except:
                pass
        else:
            if difference > 0:  # so the window can't be too small (150x150)
                try:
                    main.geometry(f"{main.winfo_width() + difference}x{main.winfo_height()}")
                except:
                    pass

    resizex_widget.bind("<B1-Motion>", resizex)

    # resize the window height
    resizey_widget = Frame(window, cursor='sb_v_double_arrow')
    resizey_widget.pack(side=BOTTOM, ipadx=2, fill=X)

    def resizey(event):
        ywin = main.winfo_y()
        difference = (event.y_root - ywin) - main.winfo_height()

        if main.winfo_height() > 512:  # 150 is the minimum height for the window
            try:
                main.geometry(f"{main.winfo_width()}x{main.winfo_height() + difference}")
            except:
                pass
        else:
            if difference > 0:  # so the window can't be too small (150x150)
                try:
                    main.geometry(f"{main.winfo_width()}x{main.winfo_height() + difference}")
                except:
                    pass

    resizey_widget.bind("<B1-Motion>", resizey)
    """

    # some settings
    main.bind("<FocusIn>", deminimize)  # to view the window by clicking on the window icon on the taskbar
    main.after(10, lambda: set_appwindow(main))  # to see the icon on the task bar

    # installappviawinget
    def intcheck(type, id, appname,source):
        def internet_stat(url="https://www.google.com/", timeout=3):
            try:
                r = requests.head(url=url, timeout=timeout)
                return True
            except requests.exceptions.ConnectionError as e:
                return False

        net_stat = internet_stat()

        if not net_stat:
            intcheckapp("main")

        if net_stat:
            if source=="🌐 Winget":
                wingetcheck(type, id, appname)
               
    def wingetcheck(type, id, appname):
        try:
            subprocess.run(["winget", "--version"], check=True, capture_output=True)
            if type == "install":
                wingetinstall(id, appname)
            elif type == "update":
                wingetupgrade(id, appname)
            elif type == "uninstall":
                wingetuninstall(id, appname)
        except subprocess.CalledProcessError:
            subprocess.run(["powershell", "-Command",
                            "(New-Object Net.WebClient).DownloadFile("
                            "'https://github.com/microsoft/winget-cli/releases/latest/download/Winget.exe', "
                            "'winget.exe')"],
                           check=True)
            subprocess.run(["winget", "install", "--id", "Winget"], check=True)
            if type == "install":
                wingetinstall(id, appname)
            elif type == "update":
                wingetupgrade(id, appname)
            elif type == "uninstall":
                wingetuninstall(id, appname)

    def wingetinstall(id, appname):
        global installbutton,uninstallchange,updatebutton
        text = "do you want to install " + appname + "?"
        installchange.set("Installing...")
        x = messagebox.askyesno("confirmation", text)
        if x == 0:
            installchange.set("Install")
        while x == 1:
            try:
                subprocess.run(["winget", "install", "--id", id], check=True)
                installchange.set("Installed")
                uninstallchange.set("Uninstall")
                uninstallbutton["state"] = NORMAL
                updatebutton["state"] = NORMAL
                break
            except subprocess.CalledProcessError:
                uninstallchange.set("Installed")
                installbutton["state"] = DISABLED
                uninstallbutton["state"] = NORMAL
                updatebutton["state"] = NORMAL
                break

    def wingetupgrade(id, appname):
        global installbutton,uninstallchange,updatebutton
        updatechange.set("Updating...")
        text = "do you want to update " + appname + "?"
        x = messagebox.askyesno("confirmation", text)
        if x == 0:
            updatechange.set("Update")
        while x == 1:
            try:
                subprocess.run(["winget", "upgrade", "--id", id], check=True)
                updatechange.set("Updated")
                break
            except subprocess.CalledProcessError:
                updatechange.set("Updated")
                break

    def wingetuninstall(id, appname):
        global installbutton,uninstallchange,updatebutton
        uninstallchange.set("Uninstalling...")
        text = "do you want to uninstall " + appname + "?"
        x = messagebox.askyesno("confirmation", text)
        if x == 0:
            uninstallchange.set("Uninstall")
        while x == 1:
            try:
                subprocess.run(["winget", "uninstall", "--id", id], check=True)
                uninstallchange.set("Uninstalled")
                installchange.set("Install")
                installbutton["state"] = NORMAL
                updatebutton["state"] = NORMAL
                break
            except subprocess.CalledProcessError:
                uninstallchange.set("Uninstalled")
                installbutton["state"] = NORMAL
                updatebutton["state"] = DISABLED
                uninstallbutton["state"] = DISABLED
                break

    sec = Frame(window)
    sec.pack(fill=X, side=BOTTOM )

    my_canvas = Canvas(window)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    y_scrollbar = ttk.Scrollbar(window, orient=VERTICAL, command=my_canvas.yview)
    y_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))
    
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    sidebar.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
    sidebar2.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
    global count
    count = 0

    def addapps(type):
        global count
        frame = type + "_frame"
        frame2 = type + "_frame2"
        canvass = type + "_canvas"
        frame3 = type + "_frame3"
        sectionframe = type + "sectionframe"
        section = type + "section"

        frame = Frame(second_frame,relief='groove', bd=0.5, highlightthickness=0)
        frame.grid(row=count, column=0, sticky=NSEW)
        
        frame2 = Frame(frame)
        frame2.pack(fill=X, side=BOTTOM)
        
        canvass = Canvas(frame)
        canvass.pack(side=LEFT, fill=BOTH, expand=1)
    
        canvass.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
        x_scrollbar = ttk.Scrollbar(frame2, orient=HORIZONTAL, command=canvass.xview)
        #x_scrollbar.pack(side=BOTTOM, fill=X)
        label=ttk.Label(frame2,text="")
        label.pack(side=BOTTOM, fill=X)
        label.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
        x_scrollbar.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))

        canvass.configure(xscrollcommand=x_scrollbar.set)
        canvass.bind("<Configure>", lambda e: canvass.config(scrollregion=canvass.bbox(ALL)))

        frame3 = Frame(canvass)
        canvass.create_window((25, 15), window=frame3, anchor="nw")
        frame3.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
        sectionframe = Frame(frame3)
        sectionframe.grid(row=0, column=0, pady=38, padx=15)

        section = ttk.Label(sectionframe, text=type, font=("Segou UI variable", 15))
        section.grid(row=0, column=0, pady=15, padx=15)
        count += 1

        section.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
        sectionframe.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
        returns=[sectionframe,canvass]
        return returns

    def loadingscreen(e, img, name, desc, pack):
        global load
        load = Toplevel()
        load.overrideredirect(True)
        app_width = 640
        app_height = 320
        screenwidth = load.winfo_screenwidth()
        screenheight = load.winfo_screenheight()
        x = (screenwidth / 2) - (app_width / 2)
        y = (screenheight / 2) - (app_height / 2)
        load.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        if mode == "dark":
            bg_image = ImageTk.PhotoImage(Image.open(r"images\loading dark.png"))
            label1 = Label(load, image=bg_image)
            label1.pack()
        elif mode == "light":
            bg_image = ImageTk.PhotoImage(Image.open(r"images\loading light.png"))
            label1 = Label(load, image=bg_image)
            label1.pack()
        source = name.splitlines()[2]
        load.update()
        global packages
        packages=checkpack(source)
        load.after(3000,lambda: hoverwindow(img, name, desc, pack))
        load.mainloop()

    def hoverwindow(img, name, desc, pack):
        with open("settings.json", "r") as x:
            try:
                data = json.load(x)
            except json.JSONDecodeError:
                pass
        global hoverwin
        hoverwin = Toplevel()
        hoverwin.overrideredirect(True)
        app_width = 640
        app_height = 320
        screenwidth = hoverwin.winfo_screenwidth()
        screenheight = hoverwin.winfo_screenheight()
        x = (screenwidth / 2) - (app_width / 2)
        y = (screenheight / 2) - (app_height / 2)
        hoverwin.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        imglabel = ttk.Label(hoverwin, image=img)
        imglabel.place(relx=0.1, rely=0.1)
        appname = name.splitlines()[0]
        rating = name.splitlines()[1]
        source = name.splitlines()[2]
        main.lift()
        hoverwin.lift()
        main.bind("<Button-3>", lambda e: closehover("hoverwin"))
        hoverwin.bind("<Button-3>", lambda e: closehover("hoverwin"))
        main.bind("<Button-1>", lambda e: closehover("hoverwin"))

        namelabel = ttk.Label(hoverwin, text=appname, font=("Segou UI variable", 18))
        namelabel.place(relx=0.31, rely=0.1)
        namelabel1 = ttk.Label(hoverwin, text=rating, font=("Segou UI variable", 18))
        namelabel1.place(relx=0.3, rely=0.2)
        descriptionlbl = ttk.Label(hoverwin, text="Description", font=("Segou UI variable", 18))
        descriptionlbl.place(relx=0.05, rely=0.5)
        desclabel = ttk.Label(hoverwin, text=desc, font=("Segou UI variable", 10))
        desclabel.place(relx=0.05, rely=0.6)
        sourcelabel =ttk.Label(hoverwin, text=source, font=("Segou UI variable", 18))
        sourcelabel.place(relx=0.7, rely=0.2)

        global installchange
        global installbutton
        installchange = StringVar()
        installbutton = ttk.Button(hoverwin, textvariable=installchange, width=12,
                                command=lambda: intcheck("install", pack, appname, source))
        installbutton.place(relx=0.28, rely=0.325)
        global updatechange
        global updatebutton
        updatechange = StringVar()
        updatechange.set("Update")
        updatebutton = ttk.Button(hoverwin, textvariable=updatechange, width=12,
                                command=lambda: intcheck("update", pack, appname, source))
        updatebutton.place(relx=0.48, rely=0.325)
        global uninstallchange
        global uninstallbutton
        uninstallchange = StringVar()
        uninstallchange.set("Uninstall")
        uninstallbutton = ttk.Button(hoverwin, textvariable=uninstallchange, width=12,
                                    command=lambda: intcheck("uninstall", pack, appname, source))
        uninstallbutton.place(relx=0.68, rely=0.325)

        def closeloading():
            load.destroy()

        global temppack
        temppack=pack

        if temppack not in packages:
            closeloading()
            installchange.set("Install")
            uninstallbutton["state"] = DISABLED
            updatebutton["state"] = DISABLED

        elif temppack in packages:
            closeloading()
            installchange.set("Installed")
            installbutton["state"] = DISABLED

        hoverwin.mainloop()

    def closehover(winname):
        main.attributes("-alpha", 1)
        if winname == "hoverwin":
            hoverwin.destroy()
        elif winname == "instwin":
            instwin.destroy()
        elif winname =="updwin":
            updwin.destroy()
        
    def remold():
        try:
            main.attributes("-alpha", 1)
            hoverwin.destroy()
        except NameError:
            pass


    ########################appdata######################
    # brave
    braveicon = PhotoImage(file=r"images\Brave_lion_icon.svg.png")
    braveimage = braveicon.subsample(21, 21)
    bravedesc = "Brave is a free and open-source web browser developed by Brave Software, Inc. based on the " \
                "\nChromium web browser. Brave is a privacy-focused browser, which automatically blocks online " \
                "\nadvertisements and website trackers in its default settings. It also provides users the choice " \
                "\nto turn on optional ads that pay users for their attention in the form of Basic Attention Tokens " \
                "\n(BAT) cryptocurrency."
    bravepack = "Brave.Brave"
    # firefox
    firefoxicon = PhotoImage(file=r"images\Firefox_logo,_2017.svg.png")
    firefoximage = firefoxicon.subsample(17, 17)
    firefoxdesc = "Mozilla Firefox, or simply Firefox, is a free and open-source web browser developed by the " \
                  "\nMozilla Foundation and its subsidiary, the Mozilla Corporation. It uses the Gecko rendering " \
                  "\nengine to display web pages, which implements current and anticipated web standards. In " \
                  "\nNovember 2017, Firefox began incorporating new technology under the code name Quantum to " \
                  "\npromote parallelism and a more intuitive user interface. "
    firefoxpack = "Mozilla.Firefox"
    # librewolf
    librewolficon = PhotoImage(file=r"images\LibreWolf_icon.svg.png")
    librewolfimage = librewolficon.subsample(30, 30)
    librewolfdesc = "This project is a custom and independent version of Firefox, with the primary goals of privacy, " \
                    "\nsecurity and user freedom. LibreWolf is designed to increase protection against tracking and " \
                    "\nfingerprinting techniques, while also including a few security improvements. "
    librewolfpack = "Librewolf.Librewolf"
     # tor
    toricon = PhotoImage(file=r"images\Tor_Browser_icon.svg.png")
    torimage = toricon.subsample(17, 17)
    tordesc = "Tor, short for The Onion Router, is free and open-source software for enabling anonymous " \
              "\ncommunication. It directs Internet traffic through a free, worldwide, volunteer overlay network, " \
              "consisting \nof more than seven thousand relays, to conceal a user's location and usage from anyone " \
              "performing \nnetwork surveillance or traffic analysis.Using Tor makes it more difficult to trace a " \
              "user's Internet \nactivity. Tor's intended use is to protect the personal privacy of its users, " \
              "as well as their freedom and \nability to communicate confidentially through IP address anonymity " \
              "using Tor exit nodes. "
    torpack = "TorProject.TorBrowser"
    # vivaldi
    vivaldiicon = PhotoImage(file=r"images\Vivaldi_web_browser_logo.svg.png")
    vivaldiimage = vivaldiicon.subsample(15, 15)
    vivaldidesc = "Vivaldi is a user-friendly browser designed to provide customizable browsing experiences. With " \
                  "built-in \nnavigation and UI customization tools, users can customize Vivaldi any way they want. "
    vivaldipack = "VivaldiTechnologies.Vivaldi"
    # chrome
    chromeicon = PhotoImage(file=r"images\Google_Chrome_icon_(February_2022).svg.png")
    chromeimage = chromeicon.subsample(30, 30)
    chromedesc = "Google Chrome is a cross-platform web browser developed by Google. It was first released in 2008 " \
                 "for \nMicrosoft Windows, built with free software components from Apple WebKit and Mozilla Firefox. " \
                 "\nVersions were later released for Linux, macOS, iOS, and also for Android, where it is the default " \
                 "\nbrowser. "
    chromepack = "Google.Chrome"
    # msedge
    msedgeicon = PhotoImage(file=r"images\Microsoft_Edge_Dev_Icon_(2019).svg.png")
    msedgeimage = msedgeicon.subsample(32, 32)
    msedgedesc = "Microsoft Edge is a proprietary, cross-platform web browser created by Microsoft. It was first " \
                 "released \nin 2015 as part of Windows 10 and Xbox One and later ported to other platforms as a fork " \
                 "of Google's \nChromium open-source project. "
    msedgepack = "Microsoft.Edge.Dev"
    # opreagx
    operagxicon = PhotoImage(file=r"images\Opera_GX_Icon.svg.png")
    operagximage = operagxicon.subsample(18, 18)
    operagxdesc = "Opera is a multi-platform web browser developed by its namesake company Opera. The browser is " \
                  "\nbased on Chromium, but distinguishes itself from other Chromium-based browsers (Chrome, Edge, " \
                  "etc.) \nthrough its user interface and other features. "
    operagxpack = "Opera.OperaGX"
    # chromium
    chromiumicon = PhotoImage(file=r"images\Chromium_Logo.svg.png")
    chromiumimage = chromiumicon.subsample(30, 30)
    chromiumdesc = "Chromium is a free and open-source web browser project, mainly developed and maintained by " \
                   "\nGoogle. This codebase provides the vast majority of code for the Google Chrome browser, " \
                   "which is \nproprietary software and has some additional features. "
    chromiumpack = "eloston.ungoogled-chromium"
    # discord
    discordicon = PhotoImage(file=r"images\636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png")
    discordimage = discordicon.subsample(8, 8)
    discorddesc = "Discord is a free communications app that lets you share voice, video, and text chat with friends, " \
                  "\ngame communities, and developers. It has hundreds of millions of users, making it one of the " \
                  "most \npopular ways to connect with people online. "
    discordpack = "Discord.Discord"
    # teams
    teamsicon = PhotoImage(file=r"images\Microsoft_Office_Teams_(2018–present).svg.png")
    teamsimage = teamsicon.subsample(35, 35)
    teamsdesc = "Microsoft Teams is the ultimate messaging app for your organization—a workspace for real-time " \
                "\ncollaboration and communication, meetings, file and app sharing, and even the occasional emoji! " \
                "\nAll in one place, all in the open, all accessible to everyone. "
    teamspack = "Microsoft.Teams"
    # skype
    skypeicon = PhotoImage(file=r"images\174869.png")
    skypeimage = skypeicon.subsample(9, 9)
    skypedesc = "Skype is software that enables the world's conversations. Millions of individuals and businesses " \
                "\nuse Skype to make free video and voice one-to-one and group calls, send instant messages and " \
                "\nshare files with other people on Skype. "
    skypepack = "Microsoft.Skype"
    # zoom
    zoomicon = PhotoImage(file=r"images\5e8ce423664eae0004085465.png")
    zoomimage = zoomicon.subsample(5, 5)
    zoomdesc = "Zoom is a communications platform that allows users to connect with video, audio, phone, and chat. " \
               "\nUsing Zoom requires an internet connection and a supported device. Most new users will want to " \
               "\nstart by creating an account and downloading the Zoom Client for Meetings. "
    zoompack = "Zoom.Zoom"
    # slack
    slackicon = PhotoImage(file=r"images\2111615.png")
    slackimage = slackicon.subsample(9, 9)
    slackdesc = "Slack is a messaging app for business that connects people to the information that they need. By " \
                "\nbringing people together to work as one unified team, Slack transforms the way that organisations " \
                "\ncommunicate. "
    slackpack = "SlackTechnologies.Slack"
    # telegram
    telegramicon = PhotoImage(file=r"images\telegram-logo-AD3D08A014-seeklogo.com.png")
    telegramimage = telegramicon.subsample(5, 5)
    telegramdesc = "Telegram is a messaging app with a focus on speed and security, it's super-fast, simple and free. " \
                   "\nYou can use Telegram on all your devices at the same time — your messages sync " \
                   "seamlessly\nacross any number of your phones, tablets or computers. "
    telegrampack = "Telegram.TelegramDesktop"
    # viber
    vibericon = PhotoImage(file=r"images\2111705.png")
    viberimage = vibericon.subsample(8, 8)
    viberdesc = "Viber is a VoIP and instant messaging application with cross-platform capabilities that allows users " \
                "\nto exchange audio and video calls, stickers, group chats, and instant voice and video messages. " \
                "\nIt Is a product of Rakuten Viber, a multinational internet company headquartered in Setagaya-ku, " \
                "\nTokyo, Japan. "
    viberpack = "Viber.Viber"
    # whatsapp
    whatsappicon = PhotoImage(file=r"images\1753788.png")
    whatsappimage = whatsappicon.subsample(8, 8)
    whatsappdesc = "WhatsApp is a free cross-platform messaging service. It lets users of iPhone and Android " \
                   "smartphones\nand Mac and Windows PC call and exchange text, photo, audio and video messages with " \
                   "others across \nthe globe for free, regardless of the recipient's device. "
    whatsapppack = "WhatsApp.WhatsApp"
    # signal
    signalicon = PhotoImage(file=r"images\4423638.png")
    signalimage = signalicon.subsample(8, 8)
    signaldesc = "Signal is an end-to-end-encrypted instant messaging and SMS app. Users can send direct or group " \
                 "\nmessages, photos, and voice messages across multiple devices. The key advantage that it offers " \
                 "over \nsimilar apps is a strong focus on security and privacy. "
    signalpack = "OpenWhisperSystems.Signal"
    # messenger
    messengericon = PhotoImage(file=r"images\Facebook-Messenger-Icon-PNG-Clipart-Background.png")
    messengerimage = messengericon.subsample(18, 18)
    messengerdesc = "Messenger is used to send messages and exchange photos, videos, stickers, audio, and files, " \
                    "and also \nreact to other users' messages and interact with bots. The service also supports " \
                    "voice and video calling. "
    messengerpack = "Facebook.Messenger"
    # line
    lineicon = PhotoImage(file=r"images\124027.png")
    lineimage = lineicon.subsample(8, 8)
    linedesc = "LINE is a communications application for all kinds of devices, including smartphones, PCs, " \
               "and tablets. \nOne can use this app to communicate via texts, images, video, audio, and more. LINE " \
               "also supports \nVoIP calling, and both audio and video conferencing. "
    linepack = "LINE.LINE"
    # snapchat
    snapchaticon = PhotoImage(file=r"images\snapchat-logo-png-0.png")
    snapchatimage = snapchaticon.subsample(8, 8)
    snapchatdesc = "Snapchat is a mobile app that allows users to send and receive self-destructing photos and videos. " \
                   "\nPhotos and videos taken with the app are called snaps. Snapchat uses the device's camera to " \
                   "capture \nsnaps and Wi-Fi technology to send them. "
    snapchatpack = "9PF9RTKMMQ69"
    # imo
    imoicon = PhotoImage(file=r"images\1091859.png")
    imoimage = imoicon.subsample(8, 8)
    imodesc = "imo is a proprietary audio/video calling and instant messaging software service. It allows sending " \
              "music, \nvideo, PDFs and other files, along with various free stickers. It supports encrypted group " \
              "video and \nvoice calls with up to 20 participants. "
    imopack = "9NBLGGH4NZX6"
    # jitsi
    jitsiicon = PhotoImage(file=r"images\jitsi-icon.png")
    jitsiimage = jitsiicon.subsample(8, 8)
    jitsidesc = "Jitsi Meet lets you stay in touch with all your teams, be they family, friends, or colleagues. Instant " \
                "video \nconferences, efficiently adapting to your scale. * Unlimited users: There are no artificial " \
                "restrictions \non the number of users or conference participants. "
    jitsipack = "Jitsi.Meet"
    # git
    giticon = PhotoImage(file=r"images\Git-Icon-1788C.png")
    gitimage = giticon.subsample(6, 6)
    gitdesc = "Git is a free and open source distributed code management and Version control system that is " \
              "\ndistributed under the GNU General Public License version 2. In addition to software version control, " \
              "\nGit is used for other applications including configuration management and content management. "
    gitpack = "Git.Git"
    # githubdesktop
    githubdesktopicon = PhotoImage(file=r"images\768px-Github-desktop-logo-symbol.svg.png")
    githubdesktopimage = githubdesktopicon.subsample(12, 12)
    githubdesktopdesc = "GitHub Desktop is an application that enables you to interact with GitHub using a GUI " \
                        "instead of the \ncommand line or a web browser. GitHub Desktop encourages you and your team " \
                        "to collaborate \nusing best practices with Git and GitHub. "
    githubdesktoppack = "GitHub.GitHubDesktop"
    # jetbrainstoolbox
    jetbrainstoolboxicon = PhotoImage(file=r"images\toolbox_logo_300x300.png")
    jetbrainstoolboximage = jetbrainstoolboxicon.subsample(5, 5)
    jetbrainstoolboxdesc = "It offers free community versions of our popular Python and Java integrated development " \
                           "environments. \nIt provides tools for learning Python, Java, and Kotlin, designed by " \
                           "professional developers "
    jetbrainstoolboxpack = "JetBrains.Toolbox"
    # python
    pythonicon = PhotoImage(file=r"images\5968350.png")
    pythonimage = pythonicon.subsample(9, 9)
    pythondesc = "Python is a computer programming language often used to build websites and software, automate " \
                 "tasks, and conduct \ndata analysis. Python is a general-purpose language, meaning it can be used to " \
                 "create a variety of \ndifferent programs and isn't specialized for any specific problems. "
    pythonpack = "9PJPW5LDXLZ5"
    # vscode
    vscodeicon = PhotoImage(file=r"images\Visual_Studio_Code_1.35_icon.svg.png")
    vscodeimage = vscodeicon.subsample(36, 36)
    vscodedesc = "Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop and " \
                 "is \navailable for Windows, macOS and Linux. "
    vscodepack = "Microsoft.VisualStudioCode"
    # vscodium
    vscodiumicon = PhotoImage(file=r"images\i7zov9ca3ts71.png")
    vscodiumimage = vscodiumicon.subsample(18, 18)
   
    vscodiumdesc = "VSCodium is a community-driven, freely-licensed binary distribution of Microsoft's editor VS " \
                   "Code, a \nmultiplatform and multi langage source code editor. "
    vscodiumpack = "VSCodium.VSCodium"
    # nodejs
    nodejsicon = PhotoImage(file=r"images\5968322.png")
    nodejsimage = nodejsicon.subsample(9, 9)
    nodejsdesc = "Node. js (Node) is an open source, cross-platform runtime environment for executing JavaScript " \
                 "code. \nNode is used extensively for server-side programming, making it possible for developers to " \
                 "use \nJavaScript for client-side and server-side code without needing to learn an additional " \
                 "language. "
    nodejspack = "OpenJS.NodeJS"
    # rust
    rusticon = PhotoImage(file=r"images\Rust_programming_language_black_logo.svg.png")
    rustimage = rusticon.subsample(36, 36)
    rustdesc = "Rust emphasizes performance, type safety, and concurrency. Rust enforces memory safety—that is, " \
               "\nthat all references point to valid memory—without requiring the use of a garbage collector or " \
               "reference \ncounting present in other memory-safe languages. "
    rustpack = "Rustlang.Rust.GNU"
    # visualstudio
    vsstudioicon = PhotoImage(file=r"images\Visual_Studio_Icon_2022.svg.png")
    vsstudioimage = vsstudioicon.subsample(36, 36)
    vsstudiodesc = "Visual Studio 2022 is the best Visual Studio ever. Our first 64-bit IDE makes it easier to work " \
                   "\nwith even bigger projects and more complex workloads. The stuff you do every day—like typing " \
                   "code \nand switching branches—feels more fluid more responsive. "
    vsstudiopack = "Microsoft.VisualStudio.2022.Community-Preview"
    # sublime
    sublimeicon = PhotoImage(file=r"images\download.png")
    sublimeimage = sublimeicon.subsample(4, 4)
    
    sublimedesc = "Sublime Text is an application development software that helps businesses manage code refactoring, " \
                  "\ndebugging, multi-monitor editing, syntax highlighting, and more from within a unified platform. "
    sublimepack = "SublimeHQ.androidstudioText.4"
    # androidstudio
    androidstudioicon = PhotoImage(file=r"images\android-studio-icon-486x512-zp9um7zl.png")
    androidstudioimage = androidstudioicon.subsample(9, 9)

    androidstudiodesc = "Android Studio is the official integrated development environment (IDE) for Android " \
                        "application \ndevelopment. It is based on the IntelliJ IDEA, a Java integrated development " \
                        "environment for software, \nand incorporates its code editing and developer tools. "
    androidstudiopack = "Google.AndroidStudio"
    # xamarin
    xamarinicon = PhotoImage(file=r"images\download1.png")
    xamarinimage = xamarinicon.subsample(4, 4)
    xamarindesc = "Xamarin is an abstraction layer that manages communication of shared code with underlying platform " \
                  "\ncode. Xamarin runs in a managed environment that provides conveniences such as memory allocation " \
                  "\nand garbage collection. Xamarin enables developers to share an average of 90% of their " \
                  "application \nacross platforms. "
    xamarinpack = "9NBLGGH0FF9K"
    # unity
    unityicon = PhotoImage(file=r"images\5969294.png")
    unityimage = unityicon.subsample(9, 9)
    unitydesc = "Unity gives users the ability to create games and experiences in both 2D and 3D, and the engine " \
                "\noffers a primary scripting API in C# using Mono, for both the Unity editor in the form of plugins, " \
                "\nand games themselves, as well as drag and drop functionality. "
    unitypack = "Unity.Unity.2022"
    # blender
    blendericon = PhotoImage(file=r"images\7c3abb1e942ffcdb9a64676a0af8c65c0d4b4497.png")
    blenderimage = blendericon.subsample(8, 8)
    blenderdesc = "Blender is the Free and Open Source 3D creation suite. It supports the entirety of the 3D " \
                  "pipeline\n—modeling, sculpting, rigging, 3D and 2D animation, simulation, rendering, compositing, " \
                  "motion \ntracking and video editing. "
    blenderpack = "BlenderFoundation.Blender"
    # atom
    atomicon = PhotoImage(file=r"images\21752.png")
    atomimage = atomicon.subsample(9, 9)
    atomdesc = "Atom is a free and open-source text and source code editor developed by GitHub (Atom – A \nHackable " \
               "Text and Source Code Editor for Linux). Its developers call it a hackable text editor for the \n21st " \
               "Century (Atom 1.0). "
    atompack = "GitHub.Atom"
    # audacity
    audacityicon = PhotoImage(file=r"images\Audacity_Logo_nofilter.svg.png")
    audacityimage = audacityicon.subsample(36, 36)
    
    audacitydesc = "Audacity is a free, easy-to-use, multi-track audio editor and recorder for Windows, \nmacOS, " \
                   "GNU/Linux and other operating systems. The interface is translated into many languages. You \ncan " \
                   "use Audacity to: Record live audio. Record computer playback on any Windows Vista or later " \
                   "\nmachine. "
    audacitypack = "Audacity.Audacity"
    # gimp
    gimpicon = PhotoImage(file=r"images\The_GIMP_icon_-_gnome.svg.png")
    gimpimage = gimpicon.subsample(18, 18)
    
    gimpdesc = "GIMP is an acronym for GNU Image Manipulation Program. It is a freely distributed program \nfor such " \
               "tasks as photo retouching, image composition and image authoring. It has many capabilities. "
    gimppack = "GIMP.GIMP"
    # kdenlive
    kdenliveicon = PhotoImage(file=r"images\icon_12.png")
    kdenliveimage = kdenliveicon.subsample(4, 4)
    kdenlivedesc = "Kdenlive is an open source video editor. The project was started around 2003. Kdenlive \nis built " \
                   "on Qt and the KDE Frameworks libraries. Most of the video processing is done by the MLT " \
                   "\nFramework, which relies on many other open source projects like FFmpeg, frei0r, movit, ladspa, " \
                   "\nsox, etc… "
    kdenlivepack = "KDE.Kdenlive"
    # obsstudio
    obsstudioicon = PhotoImage(file=r"images\768px-OBS_Studio_Logo.svg.png")
    obsstudioimage = obsstudioicon.subsample(12, 12)
    obsstudiodesc = "Open Broadcaster Software, or OBS, is a free and open source solution for offline video " \
                    "\nrecording and live streaming that is Mac and Windows compliant. With an open canvas approach " \
                    "to \nvideo creation this tool can mix a variety of audio and video sources to a single output " \
                    "for \ncreative video and broadcast applications. "
    obsstudiopack = "OBSProject.OBSStudio"
    # golang
    golangicon = PhotoImage(file=r"images\golang-icon-398x512-eygvdisi.png")
    golangimage = golangicon.subsample(8, 8)
    golangdesc = "Go (also called Golang or Go language) is an open source programming language used for general \npurpose. Go was developed by Google engineers to create dependable and efficient software. Most \nsimilarly modeled after C, Go is statically typed and explicit."
    golangpack = "GoLang.Go.1.19"
    # swift
    swifticon = PhotoImage(file=r"images\5968371.png")
    swiftimage = swifticon.subsample(8, 8)
    swiftdesc = "Swift is a powerful and intuitive programming language for iOS, iPadOS, macOS, tvOS, and watchOS. \nWriting Swift code is interactive and fun, the syntax is concise yet expressive, and Swift \nincludes modern features developers love. Swift code is safe by design and produces software that \nruns lightning-fast."
    swiftpack = "Swift.Toolchain"
    # javeruntimeenv
    javeruntimeenvicon = PhotoImage(file=r"images\java-43-569305-1.png")
    javeruntimeenvimage = javeruntimeenvicon.subsample(5, 5)
    javeruntimeenvdesc = "The Java Runtime Environment (JRE) is software that Java programs require to run correctly. \nJava is a computer language that powers many current web and mobile applications. The JRE \nis the underlying technology that communicates between the Java program and the operating system."
    javeruntimeenvpack = "Oracle.JavaRuntimeEnvironment"
     # hwinfo
    hwinfoicon = PhotoImage(file=r"images\hwinfo-icon-512x512-8ybzko3v.png")
    hwinfoimage = hwinfoicon.subsample(8, 8)
    hwinfodesc = "HWiNFO is an all-in-one solution for hardware analysis and monitoring supporting a broad range of " \
                 "\nOSes (DOS, Microsoft Windows 95 - Windows 11, WinPE) and platforms (i8086 - Xeon Platinum). " \
                 "\nLatest components supported. "
    hwinfopack = "REALiX.HWiNFO"
    # coretemp
    coretempicon = PhotoImage(file=r"images\34454443.png")
    coretempimage = coretempicon.subsample(5, 5)
    coretempdesc = "Core Temp is a compact, no fuss, small footprint, yet powerful program to monitor processor " \
                   "temperature \nand other vital information. What makes Core Temp unique is the way it works. It is " \
                   "capable of \ndisplaying a temperature of each individual core of every processor in your system! "
    coretemppack = "ALCPU.CoreTemp"
    # sevenzip
    sevenzipicon = PhotoImage(file=r"images\1280px-7-Zip_Icon.svg.png")
    sevenzipimage = sevenzipicon.subsample(17, 17)
    sevenzipdesc = "7-Zip is a free and open-source file archiver, a utility used to place groups of files within " \
                   "compressed \ncontainers known as archives. It is developed by Igor Pavlov and was first released " \
                   "in 1999. \n7-Zip has its own archive format called 7z, but can read and write several others. "
    sevenzippack = "7zip.7zip"
    # anydesk
    anydeskicon = PhotoImage(file=r"images\unnamed.png")
    anydeskimage = anydeskicon.subsample(9, 9)
    anydeskdesc = "AnyDesk's high-performance Remote Desktop Software enables latency-free Desktop Sharing, \nstable " \
                  "Remote Control and fast and secure data transmission between devices. "
    anydeskpack = "AnyDeskSoftwareGmbH.AnyDesk"
    # cpuz
    cpuzicon = PhotoImage(file=r"images\CPU-Z_Icon.svg.png")
    cpuzimage = cpuzicon.subsample(2, 2)
    cpuzdesc = "CPU-Z is a freeware that gathers information on some of the main devices of your system : \nProcessor " \
               "name and number, codename, process, package, cache levels. Mainboard and chipset. \nMemory type, " \
               "size, timings, and module specifications (SPD). Real time measurement of each core's \ninternal " \
               "frequency, memory frequency. "
    cpuzpack = "CPUID.CPU-Z"
    # etcher
    etchericon = PhotoImage(file=r"images\avatar.png")
    etcherimage = etchericon.subsample(4, 4)
    etcherdesc = "balenaEtcher (commonly referred to and formerly known as Etcher) is a free and open-source " \
                 "\nutility used for writing image files such as . iso and . img files, as well as zipped folders " \
                 "\nonto storage media to create live SD cards and USB flash drives. It is developed by Balena, " \
                 "\nand licensed under Apache License 2.0. "
    etcherpack = "Balena.Etcher"
    # gpuz
    gpuzicon = PhotoImage(file=r"images\gpu_z_icon_by_pitmankeks_de0lyld-fullview.png")
    gpuzimage = gpuzicon.subsample(9, 9)
    gpuzdesc = "TechPowerUp GPU-Z (or just GPU-Z) is a lightweight utility designed to provide information \nabout " \
               "video cards and GPUs. The program displays the specifications of Graphics Processing Unit \n(often " \
               "shortened to GPU) and its memory; also displays temperature, core frequency, memory frequency, " \
               "\nGPU load and fan speeds. "
    gpuzpack = "TechPowerUp.GPU-Z"
    # revouninstaller
    revouninstallericon = PhotoImage(file=r"images\Revouninstallerpro_icon.png")
    revouninstallerimage = revouninstallericon.subsample(9, 9)
    revouninstallerdesc = "Revo Uninstaller acts as both a replacement and a supplement to the built-in functionality " \
                          "\nin Windows by first running the built-in uninstaller for the program, and then scanning " \
                          "\nfor leftover data afterwards, making it your best choice when it comes to completely " \
                          "\nremove stubborn programs, temporary files, and other unnecessary program data that is " \
                          "\nleft behind after the standard uninstall process. "
    revouninstallerpack = "RevoUninstaller.RevoUninstaller"
    # powertoys
    powertoysicon = PhotoImage(file=r"images\2020_PowerToys_Icon.svg.png")
    powertoysimage = powertoysicon.subsample(36, 36)
    powertoysdesc = "Microsoft PowerToys is a set of utilities for power users to tune and streamline their Windows " \
                    "\nexperience for greater productivity. "
    powertoyspack = "Microsoft.PowerToys"
    # autohotkey
    autohotkeyicon = PhotoImage(file=r"images\sBnPQRG.png")
    autohotkeyimage = autohotkeyicon.subsample(5, 5)
    autohotkeydesc = "AutoHotkey is a free and open-source custom scripting language for Microsoft Windows, initially " \
                     "\naimed at providing easy keyboard shortcuts or hotkeys, fast macro-creation and software " \
                     "\nautomation that allows users of most levels of computer skill to automate repetitive \ntasks " \
                     "in any Windows application. "
    autohotkeypack = "Lexikos.AutoHotkey"
    # bitwarden
    bitwardenicon = PhotoImage(file=r"images\1200x630bb.png")
    bitwardenimage = bitwardenicon.subsample(11, 11)
    bitwardendesc = "Generate, consolidate, and autofill strong and secure passwords for all your accounts. Bitwarden " \
                    "\ngives you power to create and manage unique passwords, so you can strengthen privacy and " \
                    "\nboost productivity online from any device or location. "
    bitwardenpack = "Bitwarden.Bitwarden"
    # everythingsearch
    everythingsearchicon = PhotoImage(file=r"images\dbc1fc0d2b9e238f5863eb19ef214629.png")
    everythingsearchimage = everythingsearchicon.subsample(5, 5)
    everythingsearchdesc = "Everything is a search engine for Windows that replaces ordinary Windows search with a " \
                           "\nconsiderably faster one. Unlike Windows search, Everything initially displays every " \
                           "file and \nfolder on your computer. You can type in a search filter to limit what files " \
                           "and folders are displayed. "
    everythingsearchpack = "voidtools.Everything"
    # passwordmanager
    """
    passwordmanagericon= PhotoImage(file = r"images\b8ac5e46-1a16-448b-9a12-bf597a95d173.png")
    passwordmanagerimage = passwordmanagericon.subsample(11,11)
    passwordmanagerurl="https://github.com/VarunAdhityaGB/Password-Manager-GUI/releases/download/v.1.2/Password_Manager_v.1.2_Setup.exe"
    passwordmanagerpath="downloads//passwordmanager.exe"
    passwordmanagerfile="downloads\\passwordmanager.exe"
    passwordmanager=ttk.Button(sectionframe,image=passwordmanagerimage,text="Password Manager\n★★★★☆ 4\n🌐 Github",width=15,compound=LEFT,command=lambda: [urlinstall(passwordmanagerurl,passwordmanagerpath,passwordmanagerfile,"passwordmanager")])
    """
    # flux
    fluxicon = PhotoImage(file=r"images\flux-icon-big.png")
    fluximage = fluxicon.subsample(5, 5)
    fluxdesc = "lux (pronounced flux) is a cross-platform computer program that adjusts a display's color temperature " \
               "\naccording to location and time of day, offering functional respite for the eyes. The program \nis " \
               "designed to reduce eye strain during night-time use, helping to reduce disruption of sleep patterns. "
    fluxpack = "flux.flux"
    # steam
    steamicon = PhotoImage(file=r"images\Steam_icon_logo.svg.png")
    steamimage = steamicon.subsample(36, 36)
    steamdesc = "Steam is a video game digital distribution service and storefront by Valve. It was launched as a " \
                "software \nclient in September 2003 as a way for Valve to provide automatic updates for their games, " \
                "and \nexpanded to distributing and offering third-party game publishers' titles in late 2005. "
    steampack = "Valve.Steam"
    # EpicGames
    EpicGamesicon = PhotoImage(file=r"images\epic-games-icon-512x512-7qpmojcd.png")
    EpicGamesimage = EpicGamesicon.subsample(9, 9)
    EpicGamesdesc = "Founded in 1991, Epic Games is an American company founded by CEO Tim Sweeney. The company \nis " \
                    "headquartered in Cary, North Carolina and has more than 40 offices worldwide. Today Epic is a " \
                    "\nleading interactive entertainment company and provider of 3D engine technology. "
    EpicGamespack = "EpicGames.EpicGamesLauncher"
    # EA
    EAicon = PhotoImage(file=r"images\732012.png")
    EAimage = EAicon.subsample(9, 9)
    EAdesc = "The EA app for Windows is Electronic Arts’ all new, enhanced PC platform, where you can easily play " \
             "\nyour favorite games. The app provides a streamlined and optimized user interface that gets you \ninto " \
             "your games faster than ever before. "
    EApack = "ElectronicArts.EADesktop"
    # GOG
    GOGicon = PhotoImage(file=r"images\gog_galaxy_macos_bigsur_icon_190152.png")
    GOGimage = GOGicon.subsample(9, 9)
    GOGdesc = "GOG.com is a digital distribution platform – an online store with a curated selection of games, " \
              "an \noptional gaming client giving you freedom of choice, and a vivid community of gamers. " \
              "Hand-\npicking the best in gaming. Customer-first approach. Gamer-friendly platform. "
    GOGpack = "GOG.Galaxy"
    # playnite
    playniteicon = PhotoImage(file=r"images\applogo.png")
    playniteimage = playniteicon.subsample(5, 5)
    playnitedesc = "Playnite is an open source video game library manager with one simple goal: To provide a unified " \
                   "\ninterface for all of your games. Download. Windows 7 and newer supported Changelog. "
    playnitepack = "Playnite.Playnite"
    # amazongames
    amazongamesicon = PhotoImage(file=r"images\games-float.png")
    amazongamesimage = amazongamesicon.subsample(9, 9)
    amazongamesdesc = "Amazon Games (formerly Amazon Game Studios) is an American video game company and division of " \
                      "the \nonline retailing company Amazon that primarily focuses on publishing video games " \
                      "\ndeveloped within the company's development divisions. "
    amazongamespack = "Amazon.Games"
    # GeForce
    GeForceicon = PhotoImage(file=r"images\d9yeb7n-e1c9d052-ef39-499a-b23d-6ad146356ed2.png")
    GeForceimage = GeForceicon.subsample(5, 5)
    GeForcedesc = "NVIDIA GeForce NOW™ transforms your device into a powerful PC gaming rig. Gamers can play PC " \
                  "titles they \nalready own or purchase new games from popular digital stores like Steam, " \
                  "Epic Games \nStore, Ubisoft Connect, and EA. Access 1500+ games, with more released every GFN " \
                  "Thursday. "
    GeForcepack = "Nvidia.GeForceNow"
    # ubisoftconnect
    ubisoftconnecticon = PhotoImage(file=r"images\Ubisoft_logo.svg.png")
    ubisoftconnectimage = ubisoftconnecticon.subsample(11, 11)
    ubisoftconnectdesc = "Ubisoft Connect is the ecosystem of players services for Ubisoft games across all " \
                         "platforms. \nIt aims at giving the best environment for all players to enjoy their games " \
                         "and connect \nwith each other whatever the device. Ubisoft Connect is a free service " \
                         "available on all devices. "
    ubisoftconnectpack = "Ubisoft.Connect"
    # spotify
    spotifyicon = PhotoImage(file=r"images\Spotify_icon.svg.png")
    spotifyimage = spotifyicon.subsample(14, 14)

    spotifydesc = "Spotify is a digital music, podcast, and video service that gives you access to millions of songs and \nother content from creators all over the world. Basic functions such as playing music are totally \nfree, but you can also choose to upgrade to Spotify Premium."
    spotifypack = "Spotify.Spotify"
    # vlc
    vlcicon = PhotoImage(file=r"images\VLC_Icon.svg.png")
    vlcimage = vlcicon.subsample(18, 18)
    vlcdesc = "VLC is a multimedia player that can play most media files on most platforms. Its wide range of \nsupported formats include multimedia files, DVDs, audio CDs, VCDs, and various streaming \nprotocols."
    vlcpack = "VideoLAN.VLC"
    # mpchc
    mpchcicon = PhotoImage(file=r"images\Media-mpc-hc-icon.png")
    mpchcimage = mpchcicon.subsample(7, 7)
    mpchcdesc = "MPC-HC is an extremely light-weight, open source media player for Windows. It supports all \ncommon video and audio file formats available for playback."
    mpchcpack = "clsid2.mpc-hc"
    # kodi
    kodiicon = PhotoImage(file=r"images\Kodi-logo-Thumbnail-light-transparent.png")
    kodiimage = kodiicon.subsample(8, 8)
    kodidesc = "Kodi is a free and feature-rich media center for various operating systems, consoles and TVs. \nWith Kodi you can manage and play movies, photos and music."
    kodipack = "XBMCFoundation.Kodi"
    # plex
    plexicon = PhotoImage(file=r"images\plex.png")
    pleximage = plexicon.subsample(7, 7)
    plexdesc = "Plex is a global streaming media service and a client–server media player platform, made by \nPlex, Inc."
    plexpack = "Plex.Plex"
    # itunes
    itunesicon = PhotoImage(file=r"images\1384061.png")
    itunesimage = itunesicon.subsample(7, 7)
    itunesdesc = "iTunes is a media player developed by Apple that also can be used to communicate with Apple \nmobile devices"
    itunespack = "Apple.iTunes"
    # onlyoffice
    onlyofficeicon = PhotoImage(file=r"images\ONLYOFFICE_logo_(symbol).svg.png")
    onlyofficeimage = onlyofficeicon.subsample(36, 36)
    onlyofficedesc = "Create, view and edit text documents, spreadsheets and presentations of any size and complexity. \nWork on documents of most popular formats; DOCX, ODT, XLSX, ODS, CSV, PPTX, ODP, etc. \nDeal with multiple files within one and the same window thanks to the tab-based user interface."
    onlyofficepack = "ONLYOFFICE.DesktopEditors"
    # adobeacrobatdc
    adobeacrobatdcicon = PhotoImage(file=r"images\images.png")
    adobeacrobatdcimage = adobeacrobatdcicon.subsample(4, 4)
    adobeacrobatdcdesc = "Adobe Acrobat Reader DC software is the free, trusted global standard for viewing, printing, \nsigning, sharing, and annotating PDFs. It's the only PDF viewer that can open and \ninteract with all types of PDF content – including forms and multimedia."
    adobeacrobatdcpack = "Adobe.Acrobat.Reader.32-bit"
    # foxitpdfeditor
    foxitpdfeditoricon = PhotoImage(file=r"images\png-clipart-foxit-reader-6-foxit-software-pdf-eed-text-orange.png")
    foxitpdfeditorimage = foxitpdfeditoricon.subsample(7, 7)
    foxitpdfeditordesc = "PhantomPDF is the PDF Editor that enables PDF document accessibility for people with disabilities \nwho use assistive technology to have access to information."
    foxitpdfeditorpack = "Foxit.PhantomPDF"
    # sumatrapdf
    sumatrapdficon = PhotoImage(file=r"images\Sumatra_PDF_logo.svg.png")
    sumatrapdfimage = sumatrapdficon.subsample(14, 14)
    sumatrapdfdesc = "Sumatra PDF is a free PDF, eBook (ePub, Mobi), XPS, DjVu, CHM, Comic Book (CBZ and CBR) viewer \nfor Windows.Sumatra PDF is powerful, small, portable and starts up very fast. Simplicity of the user \ninterface has a high priority."
    sumatrapdfpack = "SumatraPDF.SumatraPDF"
    # inkscape
    inkscapeicon = PhotoImage(file=r"images\Inkscape_Logo.svg.png")
    inkscapeimage = inkscapeicon.subsample(32, 32)
    inkscapedesc = "Inkscape is a free and open-source vector graphics editor used to create vector images, primarily \nin Scalable Vector Graphics (SVG) format. Other formats can be imported and exported."
    inkscapepack = "Inkscape.Inkscape"
    #sketchup
    sketchupicon = PhotoImage(file=r"images\00000006322.png")
    sketchupimage = sketchupicon.subsample(5, 5)
    sketchupdesc = "3D modeling software for everyone"
    sketchuppack = "Trimble.SketchUp.Pro.2022"
    #sweethome3d
    sweethome3dicon = PhotoImage(file=r"images\48077292-52581780-e1e7-11e8-88df-04bf015e6cc5.png")
    sweethome3dimage = sweethome3dicon.subsample(8, 8)
    sweethome3ddesc = "Sweet Home 3D is a free interior design application that helps you draw the plan of your \nhouse, arrange furniture on it and visit the results in 3D."
    sweethome3dpack = "eTeks.SweetHome3D"
    #freecad
    freecadicon = PhotoImage(file=r"images\freecad-icon.png")
    freecadimage = freecadicon.subsample(8, 8)
    freecaddesc = "A free and opensource multiplatform 3D parametric modeler."
    freecadpack = "FreeCAD.FreeCAD"
    #openscad
    openscadicon = PhotoImage(file=r"images\Openscad.svg.png")
    openscadimage = openscadicon.subsample(8, 8)
    openscaddesc = "OpenSCAD is software for creating solid 3D CAD objects."
    openscadpack = "OpenSCAD.OpenSCAD"
    #meshlab
    meshlabicon = PhotoImage(file=r"images\687474703a2f2f7777772e6d6573686c61622e6e65742f696d672f6d6573686c61624c6f676f2e706e67.png")
    meshlabimage = meshlabicon.subsample(6, 6)
    meshlabdesc = "MeshLab is an open source, portable, and extensible system for the processing and editing of \nunstructured large 3D triangular meshes. It is aimed to help the processing of the typical \nnot-so-small unstructured models arising in 3D scanning, providing a set of tools \nfor editing, cleaning, healing, inspecting, rendering and converting this kind of meshes."
    meshlabpack = "CNRISTI.MeshLab"
    #cura
    curaicon = PhotoImage(file=r"images\Logo_for_Cura_Software.png")
    curaimage = curaicon.subsample(5, 5)
    curadesc = "Trusted by millions of users, Ultimaker Cura is the world’s most popular 3D printing software. Prepare \nprints with a few clicks, integrate with CAD software for an easier workflow, or dive into \ncustom settings for in-depth control."
    curapack = "Ultimaker.Cura"
    #prusaslicer
    prusaslicericon = PhotoImage(file=r"images\PrusaSlicer_192px.png")
    prusaslicerimage = prusaslicericon.subsample(3, 3)
    prusaslicerdesc = "PrusaSlicer (formerly known as Slic3r Prusa Edition or Slic3r PE) is our own in-house developed \nslicer software based on the open-source project Slic3r. PrusaSlicer is an open-source, \nfeature-rich, frequently updated tool that contains everything you need to export the \nperfect print files for your Original Prusa 3D printer."
    prusaslicerpack = "Prusa3D.PrusaSlicer"
    #POVRay
    POVRayicon = PhotoImage(file=r"images\200px-POVExporterLogo.png")
    POVRayimage = POVRayicon.subsample(5, 5)
    POVRaydesc = "Free ray-tracing program for creating three-dimensional graphics."
    POVRaypack = "PersistenceOfVisionRaytracer.POVRay"
    #visualsfm
    GnuCashicon = PhotoImage(file=r"images\png-transparent-gnucash-accounting-software-free-software-finance-stub-miscellaneous-text-personal-finance-thumbnail.png")
    GnuCashimage = GnuCashicon.subsample(6, 6)
    GnuCashdesc = "Personal and small-business financial-accounting software"
    GnuCashpack = "GnuCash.GnuCash"
    #homebank
    homebankicon = PhotoImage(file=r"images\unnamed (2).png")
    homebankimage = homebankicon.subsample(9, 9)
    homebankdesc = "HomeBank is a free, open source, personal finance and money management application that can be\nused to manage your daily and monthly finance details easily as well as effectively. It has \nbuilt-in powerful filtering tools and graphs that will help you to analyze your everyday transactions. "
    homebankpack = "HomeBank.HomeBank"
    #kmymoney
    kmymoneyicon = PhotoImage(file=r"images\4dde767bbec52aeaff7d5b2c3ebeae4d9895.png")
    kmymoneyimage = kmymoneyicon.subsample(7, 7)
    kmymoneydesc = "A Personal Finance Manager for humans."
    kmymoneypack = "KDE.kmymoney"
    #oceanaudio
    oceanaudioicon = PhotoImage(file=r"images\Ocenaudio-Icon.png")
    oceanaudioimage = oceanaudioicon.subsample(5, 5)
    oceanaudiodesc = "ocenaudio is a cross-platform, easy to use, fast and functional audio editor."
    oceanaudiopack = "Ocenaudio.Ocenaudio"
    #easeustodo
    easeustodoicon = PhotoImage(file=r"images\1612772936_easeus-todo-backup.png")
    easeustodoimage = easeustodoicon.subsample(5, 5)
    easeustododesc = "EaseUS Todo Backup Home covers all backup types: individual files and folders, \nwhole drives or partitions, or a full system backup. What's more, It supports to 'restore system to dissimilar \nhardware', which is an efficient way for you to migrate the current system to dissimilar \nhardware with all necessities saved on the system partition."
    easeustodopack = "EaseUS.TodoBackup"
    #3dbuilder
    threedbuildericon = PhotoImage(file=r"images\3dca35b03582b75703c8fd763ac37464f4e4ce3b6e3b8e5faf7b52cce77b290b_200-removebg-preview.png")
    threedbuilderimage = threedbuildericon.subsample(4, 4)
    threedbuilderdesc = "View, create, and personalize 3D objects using 3D Builder."
    threedbuilderpack = "9WZDNCRFJ3T6"
    #3dviewer
    threedviewericon = PhotoImage(file=r"images\download (1).png")
    threedviewerimage = threedviewericon.subsample(4, 4)
    threedviewerdesc = " Easily view 3D models and animations in real-time. 3D Viewer lets you view 3D \nmodels with lighting controls, inspect model data and visualize different shading modes. In Mixed Reality \nmode, combine the digital and physical. Push the boundaries of reality and capture it all\nwith a video or photo to share."
    threedviewerpack = "9NBLGGH42THS"
    #shapr3d
    shapr3dicon = PhotoImage(file=r"images\download (2).png")
    shapr3dimage = shapr3dicon.subsample(5, 5)
    shapr3ddesc = " Make your design flow with Shapr3D. Go from sketching to production-ready 3D models \nand realistic previews within the same seamless workflow."
    shapr3dpack = "Shapr3D.Shapr3D"
    #snapmaker
    snapmakericon = PhotoImage(file=r"images\com.snapmaker.luban.png")
    snapmakerimage = snapmakericon.subsample(5, 5)
    snapmakerdesc = "Snapmaker 3-in-1 Software for 3D Printing, Laser Engraving and CNC Cutting."
    snapmakerpack = "SnapmakerDevTeam.SnapmakerLuban"
    #pymol
    pymolicon = PhotoImage(file=r"images\download-removebg-preview.png")
    pymolimage = pymolicon.subsample(5, 5)
    pymoldesc = " A comprehensive software package for rendering and animating 3D structures."
    pymolpack = "Schrodinger.Pymol"
    #meshhouse
    meshhouseicon = PhotoImage(file=r"images\60811978.png")
    meshhouseimage = meshhouseicon.subsample(3, 3)
    meshhousedesc = "Open-source program for catalogizing 3d models"
    meshhousepack = "MeshHouse.MeshHouse"
    #Mandelbulber2
    Mandelbulber2icon = PhotoImage(file=r"images\Screenshot 2023-05-23 185620.png")
    Mandelbulber2image = Mandelbulber2icon.subsample(3, 3)
    Mandelbulber2desc = " Mandelbulber creatively generates three-dimensional fractals."
    Mandelbulber2pack = "Mandelbulber.Mandelbulber"
    #blockbench
    blockbenchicon = PhotoImage(file=r"images\768px-Blockbench_icon.png")
    blockbenchimage = blockbenchicon.subsample(13, 13)
    blockbenchdesc = "Blockbench is a free, modern model editor for boxy models and pixel art textures."
    blockbenchpack = "JannisX11.Blockbench"
    #KoduGameLab
    KoduGameLabicon = PhotoImage(file=r"images\224-2248693_game-design-with-kodu-kodu-game-lab.png")
    KoduGameLabimage = KoduGameLabicon.subsample(6, 6)
    KoduGameLabdesc="Kodu Game Lab is a 3D game development environment that is designed to teach kids basic \nprogramming principles."
    KoduGameLabpack="InfiniteInstant.KoduGameLab"
    #pConplanner
    pConplannericon = PhotoImage(file=r"images\png-clipart-pcon-planner-service-computer-software-internet-gratis-shade-angle-service.png")
    pConplannerimage = pConplannericon.subsample(8, 8)
    pConplannerdesc=" The 3D Interior Design Software for Experts."
    pConplannerpack="EasternGraphics.pCon.plannerSTD"
    #MisfitCode.MisfitModel3D
    MisfitModel3Dicon = PhotoImage(file=r"images\mm3dlogo-small.png")
    MisfitModel3Dimage = MisfitModel3Dicon.subsample(1, 1)
    MisfitModel3Ddesc = " An OpenGL-based 3D model editor that works with triangle-based models."
    MisfitModel3Dpack = "MisfitCode.MisfitModel3D"
    #I-GIS.GeoScene3D
    GeoScene3Dicon = PhotoImage(file=r"images\127531_2470241_247474_thumbnail.jpg")
    GeoScene3Dimage = GeoScene3Dicon.subsample(5, 5)
    GeoScene3Ddesc = "Build complex models using advanced tools to visualize geological data in 3D."
    GeoScene3Dpack = "I-GIS.GeoScene3D"
    #InteriorDesign3D
    InteriorDesign3Dicon = PhotoImage(file=r"images\logo.png")
    InteriorDesign3Dimage = InteriorDesign3Dicon.subsample(2, 2)
    InteriorDesign3Ddesc = "Interior Design 3D is an expert program for home design and floor plan creation."
    InteriorDesign3Dpack = "AMSSoftware.InteriorDesign3D"
    #TRACE3DPlus
    TRACE3DPlusicon = PhotoImage(file=r"images\tc-horiz-red-logo.png")
    TRACE3DPlusimage = TRACE3DPlusicon.subsample(13,13)
    TRACE3DPlusdesc = " TRACE® 3D Plus Version 5 is the newest release for this next generation building design \nand analysis software program."
    TRACE3DPluspack = "Trane.TRACE3DPlus"
    #librecad
    librecadicon = PhotoImage(file=r"images\LibreCAD_icon.svg.png")
    librecadimage = librecadicon.subsample(20, 20)
    librecaddesc = "LibreCAD is a free Open Source CAD application for Windows, Apple and Linux. Support and \ndocumentation is free from our large, dedicated community of users, contributors and developers."
    librecadpack = "LibreCAD.LibreCAD"
    
    
    #################################################################################################################
        
    #3D modeling and animation apps
    returns = addapps("3D modeling and animation apps")
    sectionframe= returns[0]
    canvass1=returns[1]
    for i in range(1, 30, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass1.xview_scroll(-1*(event.delta//120), "units"))
    
    blender = ttk.Button(sectionframe, image=blenderimage, text="Blender\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    sketchup = ttk.Button(sectionframe, image=sketchupimage, text="Trimble SketchUp Pro\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    sweethome3d = ttk.Button(sectionframe, image=sweethome3dimage, text="Sweet Home 3D\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    freecad =ttk.Button(sectionframe, image=freecadimage, text="FreeCAD\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    openscad =ttk.Button(sectionframe, image=openscadimage, text="OpenSCAD\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    meshlab=ttk.Button(sectionframe, image=meshlabimage, text="MeshLAB \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    shapr3d=ttk.Button(sectionframe, image=shapr3dimage, text="Shapr3D \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    pymol=ttk.Button(sectionframe, image=pymolimage, text="PyMol\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    blockbench=ttk.Button(sectionframe, image=blockbenchimage, text="BlockBench\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    pConplanner=ttk.Button(sectionframe, image=pConplannerimage, text="pConplanner \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    MisfitModel3D=ttk.Button(sectionframe, image=MisfitModel3Dimage, text="Misfit Model 3D \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    GeoScene3D=ttk.Button(sectionframe, image=GeoScene3Dimage, text="GeoScene 3D \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    InteriorDesign3D=ttk.Button(sectionframe, image=InteriorDesign3Dimage, text="Interior Design 3D \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    TRACE3DPlus=ttk.Button(sectionframe, image=TRACE3DPlusimage, text="TRACE 3D Plus \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    librecad=ttk.Button(sectionframe, image=librecadimage, text="Libre CAD  \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    # placements of all 3D animation and modeling apps

    threeDanimationandmodellingappslists = ["dummy",blender,sketchup,sweethome3d,freecad,openscad,meshlab,shapr3d,pymol,blockbench,pConplanner,MisfitModel3D,GeoScene3D,InteriorDesign3D,TRACE3DPlus,librecad]
    threeDanimationandmodellingappsimgs = ["dummy",blenderimage,sketchupimage,sweethome3dimage,freecadimage,openscadimage,meshlabimage,shapr3dimage,pymolimage,blockbenchimage,pConplannerimage,MisfitModel3Dimage,GeoScene3Dimage,InteriorDesign3Dimage,TRACE3DPlusimage,librecadimage]
    threeDanimationandmodellingappsdescs = ["dummy",blenderdesc,sketchupdesc,sweethome3ddesc,freecaddesc,openscaddesc,meshlabdesc,shapr3ddesc,pymoldesc,blockbenchdesc,pConplannerdesc,MisfitModel3Ddesc,GeoScene3Ddesc,InteriorDesign3Ddesc,TRACE3DPlusdesc,librecaddesc]
    threeDanimationandmodellingappspacknames = ["dummy",blenderpack,sketchuppack,sweethome3dpack,freecadpack,openscadpack,meshlabpack,shapr3dpack,pymolpack,blockbenchpack,pConplannerpack,MisfitModel3Dpack,GeoScene3Dpack,InteriorDesign3Dpack,TRACE3DPluspack,librecadpack]
    for i in range(2, len(threeDanimationandmodellingappslists) * 2, 2):
        if i / 2 < len(threeDanimationandmodellingappslists):
            button = threeDanimationandmodellingappslists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=threeDanimationandmodellingappsimgs[i // 2], buttonname=button.cget('text'),
                                                buttondesc=threeDanimationandmodellingappsdescs[i // 2],
                                                pckg=threeDanimationandmodellingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)]),
            button.bind("<MouseWheel>", lambda event: canvass1.xview_scroll(-1*(event.delta//120), "units"))
            
    #3D printing apps
    returns = addapps("3D printing apps")
    sectionframe= returns[0]
    canvass2=returns[1]
    for i in range(1, 8, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass2.xview_scroll(-1*(event.delta//120), "units"))

    cura=ttk.Button(sectionframe, image=curaimage, text="Ultimaker Cura\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    prusaslicer=ttk.Button(sectionframe, image=prusaslicerimage, text="Prusa Slicer \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    threedbuilder=ttk.Button(sectionframe, image=threedbuilderimage, text="3D Builder \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    snapmaker=ttk.Button(sectionframe, image=snapmakerimage, text="Snapmaker Luban \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    # placements of all 3D printing apps
    threeDprintingapps = ["dummy",cura,prusaslicer,threedbuilder,snapmaker]
    threeDprintingappsimages = ["dummy",curaimage,prusaslicerimage,threedbuilderimage,snapmakerimage]
    threeDprintingappsdescs = ["dummy",curadesc,prusaslicerdesc,threedbuilderdesc,snapmakerdesc]
    threeDprintingappspacknames = ["dummy",curapack,prusaslicerpack,threedbuilderpack,snapmakerpack]

    for i in range(2, len(threeDprintingapps) * 2, 2):
        if i / 2 < len(threeDprintingapps):
            button = threeDprintingapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=threeDprintingappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=threeDprintingappsdescs[i // 2],
                                                pckg=threeDprintingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass2.xview_scroll(-1*(event.delta//120), "units"))
    
    #3D rendering apps
    returns = addapps("3D rendering apps")
    sectionframe= returns[0]
    canvass3=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass3.xview_scroll(-1*(event.delta//120), "units"))

    blender = ttk.Button(sectionframe, image=blenderimage, text="Blender\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    POVRay = ttk.Button(sectionframe, image=POVRayimage, text="POVRay\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    sweethome3d = ttk.Button(sectionframe, image=sweethome3dimage, text="Sweet Home 3D\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    freecad =ttk.Button(sectionframe, image=freecadimage, text="FreeCAD\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    openscad =ttk.Button(sectionframe, image=openscadimage, text="OpenSCAD\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    pymol=ttk.Button(sectionframe, image=pymolimage, text="PyMol\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    Mandelbulber2=ttk.Button(sectionframe, image=Mandelbulber2image, text="Mandelbulber2\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    # placements of all 3D rendering apps
    threeDrenderingapps = ["dummy",blender,POVRay,sweethome3d,freecad,openscad,pymol,Mandelbulber2]
    threeDrenderingappsimages = ["dummy",blenderimage,POVRayimage,sweethome3dimage,freecadimage,openscadimage,pymolimage,Mandelbulber2image]
    threeDrenderingappsdescs = ["dummy",blenderdesc,POVRaydesc,sweethome3ddesc,freecaddesc,openscaddesc,pymoldesc,Mandelbulber2desc]
    threeDrenderingappspacknames = ["dummy",blenderpack,POVRaypack,sweethome3dpack,freecadpack,openscadpack,pymolpack,Mandelbulber2pack]

    for i in range(2, len(threeDrenderingapps) * 2, 2):
        if i / 2 < len(threeDrenderingapps):
            button = threeDrenderingapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=threeDrenderingappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=threeDrenderingappsdescs[i // 2],
                                                pckg=threeDrenderingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass3.xview_scroll(-1*(event.delta//120), "units"))
    
    #3D scanning apps
    returns = addapps("3D scanning apps")
    sectionframe= returns[0]
    canvass4=returns[1]
    for i in range(1, 8, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass4.xview_scroll(-1*(event.delta//120), "units"))
    meshlab=ttk.Button(sectionframe, image=meshlabimage, text="MeshLAB \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    threedviewer=ttk.Button(sectionframe, image=threedviewerimage, text="3D Viewer \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    meshhouse=ttk.Button(sectionframe, image=meshhouseimage, text="MeshHouse \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    # placements of all 3D scanning appsx
    threeDscanningapps = ["dummy",meshlab,threedviewer,meshhouse]
    threeDscanningappsimages = ["dummy",meshlabimage,threedviewerimage,meshhouseimage]
    threeDscanningappsdescs = ["dummy",meshlabdesc,threedviewerdesc,meshhousedesc]
    threeDscanningappspacknames = ["dummy",meshlabpack,threedviewerpack,meshhousepack]

    for i in range(2, len(threeDscanningapps) * 2, 2):
        if i / 2 < len(threeDscanningapps):
            button = threeDscanningapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=threeDscanningappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=threeDscanningappsdescs[i // 2],
                                                pckg=threeDscanningappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass4.xview_scroll(-1*(event.delta//120), "units"))
    # Accounting and financial management apps
    returns = addapps("Accounting and financial management apps")
    sectionframe= returns[0]
    canvass5=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass5.xview_scroll(-1*(event.delta//120), "units"))
    GnuCash=ttk.Button(sectionframe, image=GnuCashimage, text="GnuCash \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    homebank=ttk.Button(sectionframe, image=homebankimage, text="Homebank \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    kmymoney=ttk.Button(sectionframe, image=kmymoneyimage, text="KMyMoney \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    # placements of all Accounting and financial management apps
    afmaapps = ["dummy",GnuCash,homebank,kmymoney]
    afmaappsimages = ["dummy",GnuCashimage,homebankimage,kmymoneyimage]
    afmaappsdescs = ["dummy",GnuCashdesc,homebankdesc,kmymoneydesc]
    afmaappspacknames = ["dummy",GnuCashpack,homebankpack,kmymoneypack]

    for i in range(2, len(afmaapps) * 2, 2):
        if i / 2 < len(afmaapps):
            button = afmaapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=afmaappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=afmaappsdescs[i // 2],
                                                pckg=afmaappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass5.xview_scroll(-1*(event.delta//120), "units"))
    
    # Audio recording and editing apps
    returns = addapps("Audio recording and editing apps")
    sectionframe= returns[0]
    canvass6=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass6.xview_scroll(-1*(event.delta//120), "units"))
    
    audacity = ttk.Button(sectionframe, image=audacityimage, text="Audacity\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    oceanaudio = ttk.Button(sectionframe, image=oceanaudioimage, text="Oceanaudio \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    
    # placements of all Audio recording and editing apps
    areapps = ["dummy",audacity,oceanaudio]
    areappsimages = ["dummy",audacityimage,oceanaudioimage]
    areappsdescs = ["dummy",audacitydesc,oceanaudiodesc]
    areappspacknames = ["dummy",audacitypack,oceanaudiopack]

    for i in range(2, len(areapps) * 2, 2):
        if i / 2 < len(areapps):
            button = areapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=areappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=areappsdescs[i // 2],
                                                pckg=areappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass6.xview_scroll(-1*(event.delta//120), "units"))
    # Augmented reality content creation apps
    returns = addapps("Augmented reality content creation apps")
    sectionframe= returns[0]
    canvass7=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass7.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Augmented reality content creation apps
    arccapps = ["dummy"]
    arccappsimages = ["dummy"]
    arccappsdescs = ["dummy"]
    arccappspacknames = ["dummy"]

    for i in range(2, len(arccapps) * 2, 2):
        if i / 2 < len(arccapps):
            button = arccapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=arccappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=arccappsdescs[i // 2],
                                                pckg=arccappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass7.xview_scroll(-1*(event.delta//120), "units"))
    # Backup and recovery apps
    returns = addapps("Backup and recovery apps")
    sectionframe= returns[0]
    canvass8=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass8.xview_scroll(-1*(event.delta//120), "units"))
    
    easeustodo = ttk.Button(sectionframe, image=easeustodoimage, text="Ease US To Do Backup\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    # placements of all Backup and recovery apps
    barapps = ["dummy",easeustodo]
    barappsimages = ["dummy",easeustodoimage]
    barappsdescs = ["dummy",easeustododesc]
    barappspacknames = ["dummy",easeustodopack]

    for i in range(2, len(barapps) * 2, 2):
        if i / 2 < len(barapps):
            button = barapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=barappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=barappsdescs[i // 2],
                                                pckg=barappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass8.xview_scroll(-1*(event.delta//120), "units"))

    # Business apps
    returns = addapps("Business apps")
    sectionframe= returns[0]
    canvass9=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass9.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Business apps
    businessapps = ["dummy"]
    businessappsimages = ["dummy"]
    businessappsdescs = ["dummy"]
    businessappspacknames = ["dummy"]

    for i in range(2, len(businessapps) * 2, 2):
        if i / 2 < len(businessapps):
            button = businessapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=businessappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=businessappsdescs[i // 2],
                                                pckg=businessappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass9.xview_scroll(-1*(event.delta//120), "units"))
    
    # CAD software
    returns = addapps("CAD software")
    sectionframe= returns[0]
    canvass10=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass10.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all CAD software
    cadapps = ["dummy"]
    cadappsimages = ["dummy"]
    cadappsdescs = ["dummy"]
    cadappspacknames = ["dummy"]

    for i in range(2, len(cadapps) * 2, 2):
        if i / 2 < len(cadapps):
            button = cadapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=cadappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=cadappsdescs[i // 2],
                                                pckg=cadappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass10.xview_scroll(-1*(event.delta//120), "units"))
    
    # Cloud storage and syncing apps
    returns = addapps("Cloud storage and syncing apps")
    sectionframe= returns[0]
    canvass11=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass11.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Cloud storage and syncing apps
    cssapps = ["dummy"]
    cssappsimages = ["dummy"]
    cssappsdescs = ["dummy"]
    cssappspacknames = ["dummy"]

    for i in range(2, len(cssapps) * 2, 2):
        if i / 2 < len(cssapps):
            button = cssapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=cssappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=cssappsdescs[i // 2],
                                                pckg=cssappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass11.xview_scroll(-1*(event.delta//120), "units"))
    
    # Code editors
    returns = addapps("Code editors")
    sectionframe= returns[0]
    canvass12=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass12.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Code editors
    codeeditorapps = ["dummy"]
    codeeditorappsimages = ["dummy"]
    codeeditorappsdescs = ["dummy"]
    codeeditorappspacknames = ["dummy"]

    for i in range(2, len(codeeditorapps) * 2, 2):
        if i / 2 < len(codeeditorapps):
            button = codeeditorapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=codeeditorappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=codeeditorappsdescs[i // 2],
                                                pckg=codeeditorappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass12.xview_scroll(-1*(event.delta//120), "units"))
    # Command line utilities
    returns = addapps("Command line utilities")
    sectionframe= returns[0]
    canvass13=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass13.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Command line utilities
    cluapps = ["dummy"]
    cluappsimages = ["dummy"]
    cluappsdescs = ["dummy"]
    cluappspacknames = ["dummy"]

    for i in range(2, len(cluapps) * 2, 2):
        if i / 2 < len(cluapps):
            button = cluapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=cluappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=cluappsdescs[i // 2],
                                                pckg=cluappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass13.xview_scroll(-1*(event.delta//120), "units"))

    # communication apps
    returns = addapps("Communication apps")
    sectionframe= returns[0]
    canvass14=returns[1]
    for i in range(1, 28, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass14.xview_scroll(-1*(event.delta//120), "units"))
    discord = ttk.Button(sectionframe, image=discordimage, text="Discord\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    teams = ttk.Button(sectionframe, image=teamsimage, text="Teams\n★★★☆☆ 3.5\n🌐 Winget", width=15, compound=LEFT)
    skype = ttk.Button(sectionframe, image=skypeimage, text="Skype\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    zoom = ttk.Button(sectionframe, image=zoomimage, text="Zoom \n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    slack = ttk.Button(sectionframe, image=slackimage, text="Slack\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    telegram = ttk.Button(sectionframe, image=telegramimage, text="Telegram\n★★★☆☆ 3.5\n🌐 Winget", width=15,
                          compound=LEFT)
    viber = ttk.Button(sectionframe, image=viberimage, text="Viber\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    whatsapp = ttk.Button(sectionframe, image=whatsappimage, text="Whatsapp Web\n★★★★☆ 4.3\n🌐 Winget", width=15,
                          compound=LEFT)
    signal = ttk.Button(sectionframe, image=signalimage, text="Signal\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    messenger = ttk.Button(sectionframe, image=messengerimage, text="Messenger\n★★★★☆ 4.8\n🌐 Winget", width=15,
                           compound=LEFT)
    line = ttk.Button(sectionframe, image=lineimage, text="Line\n★★★☆☆ 3.5\n🌐 Winget", width=15, compound=LEFT)
    snapchat = ttk.Button(sectionframe, image=snapchatimage, text="Snapchat Web\n★★★☆☆ 3.9\n🌐 Winget", width=15,
                          compound=LEFT)
    imo = ttk.Button(sectionframe, image=imoimage, text="Imo\n★★★☆☆ 3.7\n🌐 Winget", width=15, compound=LEFT)
    jitsi = ttk.Button(sectionframe, image=jitsiimage, text="jitsi\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    # placement of communication apps
    commlists = ["dummy", discord, teams, skype, zoom, slack, telegram, viber, whatsapp, signal, messenger, line,
                 snapchat, imo, jitsi]
    commimgs = ["dummy", discordimage, teamsimage, skypeimage, zoomimage, slackimage, telegramimage, viberimage,
                whatsappimage, signalimage, messengerimage, lineimage, snapchatimage, imoimage, jitsiimage]
    commdescs = ["dummy", discorddesc, teamsdesc, skypedesc, zoomdesc, slackdesc, telegramdesc, viberdesc, whatsappdesc,
                 signaldesc, messengerdesc, linedesc, snapchatdesc, imodesc, jitsidesc]
    commpacknames = ["dummy", discordpack, teamspack, skypepack, zoompack, slackpack, telegrampack, viberpack,
                     whatsapppack, signalpack, messengerpack, linepack, snapchatpack, imopack, jitsipack]
    for i in range(2, len(commlists) * 2, 2):
        if i / 2 < len(commlists):
            button = commlists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=commimgs[i // 2], buttonname=button.cget('text'),
                                             buttondesc=commdescs[i // 2], pckg=commpacknames[i // 2]: [remold(),loadingscreen(
                event, buttonimg, buttonname, buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass14.xview_scroll(-1*(event.delta//120), "units"))

    # Creativity apps
    returns = addapps("Creativity apps")
    sectionframe= returns[0]
    canvass15=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass15.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Creativity apps
    Creativityapps = ["dummy"]
    Creativityappsimages = ["dummy"]
    Creativityappsdescs = ["dummy"]
    Creativityappspacknames = ["dummy"]

    for i in range(2, len(Creativityapps) * 2, 2):
        if i / 2 < len(Creativityapps):
            button = Creativityapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Creativityappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Creativityappsdescs[i // 2],
                                                pckg=Creativityappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass15.xview_scroll(-1*(event.delta//120), "units"))

    # Customer relationship management apps
    returns = addapps("Customer relationship management apps")
    sectionframe= returns[0]
    canvass16=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass16.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Customer relationship management apps
    crmapps = ["dummy"]
    crmappsimages = ["dummy"]
    crmappsdescs = ["dummy"]
    crmappspacknames = ["dummy"]

    for i in range(2, len(crmapps) * 2, 2):
        if i / 2 < len(crmapps):
            button = crmapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=crmappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=crmappsdescs[i // 2],
                                                pckg=crmappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass16.xview_scroll(-1*(event.delta//120), "units"))
    # Data backup apps
    returns = addapps("Data backup apps")
    sectionframe= returns[0]
    canvass17=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass17.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Data backup apps
    dbapps = ["dummy"]
    dbappsimages = ["dummy"]
    dbappsdescs = ["dummy"]
    dbappspacknames = ["dummy"]

    for i in range(2, len(dbapps) * 2, 2):
        if i / 2 < len(dbapps):
            button = dbapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dbappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=dbappsdescs[i // 2],
                                                pckg=dbappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass17.xview_scroll(-1*(event.delta//120), "units"))
    # Data recovery apps
    returns = addapps("Data recovery apps")
    sectionframe= returns[0]
    canvass18=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass18.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Data recovery apps
    drapps = ["dummy"]
    drappsimages = ["dummy"]
    drappsdescs = ["dummy"]
    drappspacknames = ["dummy"]

    for i in range(2, len(drapps) * 2, 2):
        if i / 2 < len(drapps):
            button = drapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=drappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=drappsdescs[i // 2],
                                                pckg=drappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass18.xview_scroll(-1*(event.delta//120), "units"))
    # Database administration apps
    returns = addapps("Database administration apps")
    sectionframe= returns[0]
    canvass19=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass19.xview_scroll(-1*(event.delta//120), "units"))

    # placements of all Database administration apps
    daapps = ["dummy"]
    daappsimages = ["dummy"]
    daappsdescs = ["dummy"]
    daappspacknames = ["dummy"]

    for i in range(2, len(daapps) * 2, 2):
        if i / 2 < len(daapps):
            button = daapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=daappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=daappsdescs[i // 2],
                                                pckg=daappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass19.xview_scroll(-1*(event.delta//120), "units"))
    # Database design and development apps
    returns = addapps("Database design and development apps")
    sectionframe= returns[0]
    canvass20=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass20.xview_scroll(-1*(event.delta//120), "units"))

    # placements of all Database design and development apps
    dddapps = ["dummy"]
    dddappsimages = ["dummy"]
    dddappsdescs = ["dummy"]
    dddappspacknames = ["dummy"]

    for i in range(2, len(dddapps) * 2, 2):
        if i / 2 < len(dddapps):
            button = dddapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dddappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=dddappsdescs[i // 2],
                                                pckg=dddappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass20.xview_scroll(-1*(event.delta//120), "units"))
    # Database management apps
    returns = addapps("Database management apps")
    sectionframe= returns[0]
    canvass21=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass21.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Database management apps
    dmapps = ["dummy"]
    dmappsimages = ["dummy"]
    dmappsdescs = ["dummy"]
    dmappspacknames = ["dummy"]

    for i in range(2, len(dmapps) * 2, 2):
        if i / 2 < len(dmapps):
            button = dmapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dmappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=dmappsdescs[i // 2],
                                                pckg=dmappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass21.xview_scroll(-1*(event.delta//120), "units"))
    # Database modelling apps
    returns = addapps("Database modelling apps")
    sectionframe= returns[0]
    canvass22=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass22.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Database modelling apps
    dmodaapps = ["dummy"]
    dmodappsimages = ["dummy"]
    dmodappsdescs = ["dummy"]
    dmodappspacknames = ["dummy"]

    for i in range(2, len(dmodaapps) * 2, 2):
        if i / 2 < len(dmodaapps):
            button = dmodaapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dmodappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=dmodappsdescs[i // 2],
                                                pckg=dmodappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass22.xview_scroll(-1*(event.delta//120), "units"))

    # Database reporting apps
    returns = addapps("Database reporting apps")
    sectionframe= returns[0]
    canvass23=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass23.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Database reporting apps
    drepapps = ["dummy"]
    drepappsimages = ["dummy"]
    drepappsdescs = ["dummy"]
    drepappspacknames = ["dummy"]

    for i in range(2, len(drepapps) * 2, 2):
        if i / 2 < len(drepapps):
            button = drepapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=drepappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=drepappsdescs[i // 2],
                                                pckg=drepappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass23.xview_scroll(-1*(event.delta//120), "units"))
    # debugging tools
    returns = addapps("Debugging tools")
    sectionframe= returns[0]
    canvass24=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass24.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all debugging tools
    debuggingtoolapps = ["dummy"]
    debuggingtoolappsimages = ["dummy"]
    debuggingtoolappsdescs = ["dummy"]
    debuggingtoolappspacknames = ["dummy"]

    for i in range(2, len(debuggingtoolapps) * 2, 2):
        if i / 2 < len(debuggingtoolapps):
            button = debuggingtoolapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=debuggingtoolappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=debuggingtoolappsdescs[i // 2],
                                                pckg=debuggingtoolappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass24.xview_scroll(-1*(event.delta//120), "units"))
    # development apps
    returns = addapps("Development apps")
    sectionframe= returns[0]
    canvass25=returns[1]
    for i in range(1, 44, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass25.xview_scroll(-1*(event.delta//120), "units"))
    git = ttk.Button(sectionframe, image=gitimage, text="Git\n★★★★☆ 4.8\n🌐 Winget", width=15, compound=LEFT)
    githubdesktop = ttk.Button(sectionframe, image=githubdesktopimage, text="Github Desktop\n★★★★☆ 4.5\n🌐 Winget",
                               width=15, compound=LEFT)
    jetbrainstoolbox = ttk.Button(sectionframe, image=jetbrainstoolboximage, text="Jetbrains Toolbox\n★★★★☆ 4.7\n🌐 Winget",
                                  width=13, compound=LEFT)
    python = ttk.Button(sectionframe, image=pythonimage, text="Python\n★★★★☆ 4.8\n🌐 Winget", width=15, compound=LEFT)
    vscode = ttk.Button(sectionframe, image=vscodeimage, text="VS Code\n★★★★☆ 4.8\n🌐 Winget", width=15, compound=LEFT)
    vscodium = ttk.Button(sectionframe, image=vscodiumimage, text="VS Codium\n★★★★☆ 4.8\n🌐 Winget", width=15, compound=LEFT)
    nodejs = ttk.Button(sectionframe, image=nodejsimage, text="Node JS\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    rust = ttk.Button(sectionframe, image=rustimage, text="Rust\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    vsstudio = ttk.Button(sectionframe, image=vsstudioimage, text="Visual Studio 2022\n★★★★☆ 4.6\n🌐 Winget", width=15,
                          compound=LEFT)
    sublime = ttk.Button(sectionframe, image=sublimeimage, text="Sublime\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    androidstudio = ttk.Button(sectionframe, image=androidstudioimage, text="Android Studio\n★★★★☆ 4.9\n🌐 Winget",
                               width=15, compound=LEFT)    
    xamarin = ttk.Button(sectionframe, image=xamarinimage, text="Xamarin\n★★★★☆ 4.4\n🌐 Winget", width=15, compound=LEFT)
    unity = ttk.Button(sectionframe, image=unityimage, text="Unity\n★★★★☆ 4.7\n🌐 Winget", width=15, compound=LEFT)
    blender = ttk.Button(sectionframe, image=blenderimage, text="Blender\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    atom = ttk.Button(sectionframe, image=atomimage, text="Atom\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    audacity = ttk.Button(sectionframe, image=audacityimage, text="Audacity\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    gimp = ttk.Button(sectionframe, image=gimpimage, text="GIMP\n★★★★☆ 4.9\n🌐 Winget", width=15, compound=LEFT)
    kdenlive = ttk.Button(sectionframe, image=kdenliveimage, text="Kdenlive\n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    obsstudio = ttk.Button(sectionframe, image=obsstudioimage, text="OBS Studio\n★★★★☆ 4.5\n🌐 Winget", width=15,
                           compound=LEFT)
    golang = ttk.Button(sectionframe, image=golangimage, text="GO Lang\n★★★★☆ 4.5\n🌐 Winget", width=15,
                           compound=LEFT)
    swift = ttk.Button(sectionframe, image=swiftimage, text="Swift\n★★★★☆ 4.5\n🌐 Winget", width=15,
                           compound=LEFT)
    javeruntimeenv = ttk.Button(sectionframe, image=javeruntimeenvimage, text="Oracle Java runtime environment\n★★★★☆ 4.5\n🌐 Winget", width=17,
                           compound=LEFT)     

    # placement of dev apps
    devlists = ["dummy", git, githubdesktop, jetbrainstoolbox, python, vscode, vscodium, nodejs, rust, vsstudio,
                sublime, androidstudio, xamarin, unity, blender, atom, audacity, gimp, kdenlive, obsstudio,golang,swift,javeruntimeenv]
    devimgs = ["dummy", gitimage, githubdesktopimage, jetbrainstoolboximage, pythonimage, vscodeimage, vscodiumimage,
               nodejsimage, rustimage, vsstudioimage, sublimeimage, androidstudioimage, xamarinimage, unityimage,
               blenderimage, atomimage, audacityimage, gimpimage, kdenliveimage, obsstudioimage,golangimage,swiftimage,javeruntimeenvimage]
    devdescs = ["dummy", gitdesc, githubdesktopdesc, jetbrainstoolboxdesc, pythondesc, vscodedesc, vscodiumdesc,
                nodejsdesc, rustdesc, vsstudiodesc, sublimedesc, androidstudiodesc, xamarindesc, unitydesc, blenderdesc,
                atomdesc, audacitydesc, gimpdesc, kdenlivedesc, obsstudiodesc,golangdesc,swiftdesc,javeruntimeenvdesc]
    devpacknames = ["dummy", gitpack, githubdesktoppack, jetbrainstoolboxpack, pythonpack, vscodepack, vscodiumpack,
                    nodejspack, rustpack, vsstudiopack, sublimepack, androidstudiopack, xamarinpack, unitypack,
                    blenderpack, atompack, audacitypack, gimppack, kdenlivepack, obsstudiopack,golangpack,swiftpack,javeruntimeenvpack]

    for i in range(2, len(devlists) * 2, 2):
        if i / 2 < len(devlists):
            button = devlists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=devimgs[i // 2], buttonname=button.cget('text'),
                                             buttondesc=devdescs[i // 2], pckg=devpacknames[i // 2]: [remold(),loadingscreen(event,
                                                                                                                 buttonimg,
                                                                                                                 buttonname,
                                                                                                                 buttondesc,
                                                                                                                 pckg)])
            button.bind("<MouseWheel>", lambda event: canvass25.xview_scroll(-1*(event.delta//120), "units"))

    # Disk cleanup and management apps
    returns = addapps("Disk cleanup and management apps")
    sectionframe= returns[0]
    canvass26=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass26.xview_scroll(-1*(event.delta//120), "units"))

    # placements of all Disk cleanup and management apps
    dcmapps = ["dummy"]
    dcmappsimages = ["dummy"]
    dcmappsdescs = ["dummy"]
    dcmappspacknames = ["dummy"]

    for i in range(2, len(dcmapps) * 2, 2):
        if i / 2 < len(dcmapps):
            button = dcmapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dcmappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=dcmappsdescs[i // 2],
                                                pckg=dcmappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass26.xview_scroll(-1*(event.delta//120), "units"))

    # Documents
    returns = addapps("Documents")
    sectionframe= returns[0]
    canvass27=returns[1]
    for i in range(1, 16, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass27.xview_scroll(-1*(event.delta//120), "units"))
    onlyoffice = ttk.Button(sectionframe, image=onlyofficeimage, text="ONLYOFFICE \n★★★★☆ 4.5\n🌐 Winget", width=15,
                                compound=LEFT)
    adobeacrobatdc = ttk.Button(sectionframe, image=adobeacrobatdcimage, text="Adobe Acrobat DC\n★★★★☆ 4.5\n🌐 Winget", width=15,
                                compound=LEFT)
    foxitpdfeditor = ttk.Button(sectionframe, image=foxitpdfeditorimage, text="Foxit PDF Editor\n★★★★☆ 4.5\n🌐 Winget", width=15,
                                compound=LEFT)
    sumatrapdf = ttk.Button(sectionframe, image=sumatrapdfimage, text="Sumatra PDF\n★★★★☆ 4.3\n🌐 Winget", width=15,
                                compound=LEFT)
    inkscape = ttk.Button(sectionframe, image=inkscapeimage, text="Inkscape\n★★★★☆ 4\n🌐 Winget", width=15,
                                compound=LEFT)

    # placement of Documents
    Documentslists = ["dummy",onlyoffice,adobeacrobatdc,foxitpdfeditor,sumatrapdf,inkscape]
    Documentsimgs = ["dummy",onlyofficeimage,adobeacrobatdcimage,foxitpdfeditorimage,sumatrapdfimage,inkscapeimage]
    Documentsdescs = ["dummy",onlyofficedesc,adobeacrobatdcdesc,foxitpdfeditordesc,sumatrapdfdesc,inkscapedesc]
    Documentspacknames = ["dummy",onlyofficepack,adobeacrobatdcpack,foxitpdfeditorpack,sumatrapdfpack,inkscapepack]

    for i in range(2, len(Documentslists) * 2, 2):
        if i / 2 < len(Documentslists):
            button = Documentslists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Documentsimgs[i // 2], buttonname=button.cget('text'),
                                             buttondesc=Documentsdescs[i // 2], pckg=Documentspacknames[i // 2]:[remold(), loadingscreen(
                event, buttonimg, buttonname, buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass27.xview_scroll(-1*(event.delta//120), "units"))

    # Driver update and management apps
    returns = addapps("Driver update and management apps")
    sectionframe= returns[0]
    canvass28=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass28.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Driver update and management apps
    dumapps = ["dummy"]
    dumaappsimages = ["dummy"]
    dumappsdescs = ["dummy"]
    dumappspacknames = ["dummy"]

    for i in range(2, len(dumapps) * 2, 2):
        if i / 2 < len(dumapps):
            button = dumapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dumaappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=dumappsdescs[i // 2],
                                                pckg=dumappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass28.xview_scroll(-1*(event.delta//120), "units"))
    # E-book readers
    returns = addapps("E-book readers")
    sectionframe= returns[0]
    canvass29=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass29.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all E-book readers
    ebookapps = ["dummy"]
    ebookappsimages = ["dummy"]
    ebookappsdescs = ["dummy"]
    ebookappspacknames = ["dummy"]

    for i in range(2, len(ebookapps) * 2, 2):
        if i / 2 < len(ebookapps):
            button = ebookapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=ebookappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=ebookappsdescs[i // 2],
                                                pckg=ebookappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass29.xview_scroll(-1*(event.delta//120), "units"))

    # E-commerce apps
    returns = addapps("E-commerce apps")
    sectionframe= returns[0]
    canvass30=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass30.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all E-commerce apps
    ecompps = ["dummy"]
    ecomappsimages = ["dummy"]
    ecomappsdescs = ["dummy"]
    ecomappspacknames = ["dummy"]

    for i in range(2, len(ecompps) * 2, 2):
        if i / 2 < len(ecompps):
            button = ecompps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=ecomappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=ecomappsdescs[i // 2],
                                                pckg=ecomappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass30.xview_scroll(-1*(event.delta//120), "units"))
    # E-mail marketing apps
    returns = addapps("E-mail marketing apps")
    sectionframe= returns[0]
    canvass31=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass31.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all E-mail marketing apps
    emmpps = ["dummy"]
    emmappsimages = ["dummy"]
    emmappsdescs = ["dummy"]
    emmappspacknames = ["dummy"]

    for i in range(2, len(emmpps) * 2, 2):
        if i / 2 < len(emmpps):
            button = emmpps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=emmappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=emmappsdescs[i // 2],
                                                pckg=emmappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass31.xview_scroll(-1*(event.delta//120), "units"))

    # Educational apps
    returns = addapps("Educational apps")
    sectionframe= returns[0]
    canvass32=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass32.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Educational apps
    eduapps = ["dummy"]
    eduappsimages = ["dummy"]
    eduappsdescs = ["dummy"]
    eduappspacknames = ["dummy"]

    for i in range(2, len(eduapps) * 2, 2):
        if i / 2 < len(eduapps):
            button = eduapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=eduappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=eduappsdescs[i // 2],
                                                pckg=eduappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass32.xview_scroll(-1*(event.delta//120), "units"))

    # Educational apps for kids
    returns = addapps("Educational apps for kids")
    sectionframe= returns[0]
    canvass33=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass33.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Educational apps
    edukapps = ["dummy"]
    edukappsimages = ["dummy"]
    edukappsdescs = ["dummy"]
    edukappspacknames = ["dummy"]

    for i in range(2, len(edukapps) * 2, 2):
        if i / 2 < len(edukapps):
            button = edukapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=edukappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=edukappsdescs[i // 2],
                                                pckg=edukappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass33.xview_scroll(-1*(event.delta//120), "units"))
    
    # Encryption and security apps
    returns = addapps("Encryption and security apps")
    sectionframe= returns[0]
    canvass34=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass34.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Encryption and security apps
    encsecapps = ["dummy"]
    encsecappsimages = ["dummy"]
    encsecappsdescs = ["dummy"]
    encsecappspacknames = ["dummy"]

    for i in range(2, len(encsecapps) * 2, 2):
        if i / 2 < len(encsecapps):
            button = encsecapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=encsecappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=encsecappsdescs[i // 2],
                                                pckg=encsecappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass34.xview_scroll(-1*(event.delta//120), "units"))
    
    # Enterprise resource planning apps
    returns = addapps("Enterprise resource planning apps")
    sectionframe= returns[0]
    canvass35=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass35.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Enterprise resource planning apps
    erpapps = ["dummy"]
    erpappsimages = ["dummy"]
    erpappsdescs = ["dummy"]
    erpappspacknames = ["dummy"]

    for i in range(2, len(erpapps) * 2, 2):
        if i / 2 < len(erpapps):
            button = erpapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=erpappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=erpappsdescs[i // 2],
                                                pckg=erpappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass35.xview_scroll(-1*(event.delta//120), "units"))

    # Entertainment apps
    returns = addapps("Entertainment apps")
    sectionframe= returns[0]
    canvass36=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass36.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Entertainment apps
    entertainmentapps = ["dummy"]
    entertainmentappsimages = ["dummy"]
    entertainmentappsdescs = ["dummy"]
    entertainmentappspacknames = ["dummy"]

    for i in range(2, len(entertainmentapps) * 2, 2):
        if i / 2 < len(entertainmentapps):
            button = entertainmentapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=entertainmentappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=entertainmentappsdescs[i // 2],
                                                pckg=entertainmentappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass36.xview_scroll(-1*(event.delta//120), "units"))
    # File conversion apps
    returns = addapps("File conversion apps")
    sectionframe= returns[0]
    canvass37=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass37.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all File conversion apps
    fconvapps = ["dummy"]
    fconvappsimages = ["dummy"]
    fconvappsdescs = ["dummy"]
    fconvappspacknames = ["dummy"]

    for i in range(2, len(fconvapps) * 2, 2):
        if i / 2 < len(fconvapps):
            button = fconvapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=fconvappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=fconvappsdescs[i // 2],
                                                pckg=fconvappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass37.xview_scroll(-1*(event.delta//120), "units"))
    # File transfer and sychronization apps
    returns = addapps("File transfer and sychronization apps")
    sectionframe= returns[0]
    canvass38=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass38.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all File transfer and sychronization apps
    ftsapps = ["dummy"]
    ftsappsimages = ["dummy"]
    ftsappsdescs = ["dummy"]
    ftsappspacknames = ["dummy"]

    for i in range(2, len(ftsapps) * 2, 2):
        if i / 2 < len(ftsapps):
            button = ftsapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=ftsappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=ftsappsdescs[i // 2],
                                                pckg=ftsappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass38.xview_scroll(-1*(event.delta//120), "units"))
    # Finance apps
    returns = addapps("Finance apps")
    sectionframe= returns[0]
    canvass39=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass39.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Finance apps
    Financeapps = ["dummy"]
    Financeappsimages = ["dummy"]
    Financeappsdescs = ["dummy"]
    Financeappspacknames = ["dummy"]

    for i in range(2, len(Financeapps) * 2, 2):
        if i / 2 < len(Financeapps):
            button = Financeapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Financeappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Financeappsdescs[i // 2],
                                                pckg=Financeappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass39.xview_scroll(-1*(event.delta//120), "units"))
    # Firewall and intrusion detection apps
    returns = addapps("Firewall and intrusion detection apps")
    sectionframe= returns[0]
    canvass40=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass40.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Firewall and intrusion detection apps
    fidapps = ["dummy"]
    fidappsimages = ["dummy"]
    fidappsdescs = ["dummy"]
    fidappspacknames = ["dummy"]

    for i in range(2, len(fidapps) * 2, 2):
        if i / 2 < len(fidapps):
            button = fidapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=fidappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=fidappsdescs[i // 2],
                                                pckg=fidappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass40.xview_scroll(-1*(event.delta//120), "units"))
    #Game development apps
    returns = addapps("Game development apps")
    sectionframe= returns[0]
    canvass41=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass41.xview_scroll(-1*(event.delta//120), "units"))
    
    KoduGameLab= ttk.Button(sectionframe, image=KoduGameLabimage, text="KoduGameLab \n★★★★☆ 4.2\n🌐 Winget", width=15, compound=LEFT)
    
    # placements of all Game development apps
    gameaiapps = ["dummy",KoduGameLab]
    gameaiappsimages = ["dummy",KoduGameLabimage]
    gameaiappsdescs = ["dummy",KoduGameLabdesc]
    gameaiappspacknames = ["dummy",KoduGameLabpack]

    for i in range(2, len(gameaiapps) * 2, 2):
        if i / 2 < len(gameaiapps):
            button = gameaiapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gameaiappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gameaiappsdescs[i // 2],
                                                pckg=gameaiappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass41.xview_scroll(-1*(event.delta//120), "units"))
    # Game VR and AR development apps
    returns = addapps("Game VR and AR development apps")
    sectionframe= returns[0]
    canvass42=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass42.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game VR and AR development apps
    gamevrarapps = ["dummy"]
    gamevrarappsimages = ["dummy"]
    gamevrarappsdescs = ["dummy"]
    gamevrarappspacknames = ["dummy"]

    for i in range(2, len(gamevrarapps) * 2, 2):
        if i / 2 < len(gamevrarapps):
            button = gamevrarapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gamevrarappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gamevrarappsdescs[i // 2],
                                                pckg=gamevrarappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass42.xview_scroll(-1*(event.delta//120), "units"))
    # Game accessibility apps
    returns = addapps("Game accessibility apps")
    sectionframe= returns[0]
    canvass43=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass43.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game accessibility apps
    gameaccapps = ["dummy"]
    gameaccappsimages = ["dummy"]
    gameaccappsdescs = ["dummy"]
    gameaccappspacknames = ["dummy"]

    for i in range(2, len(gameaccapps) * 2, 2):
        if i / 2 < len(gameaccapps):
            button = gameaccapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gameaccappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gameaccappsdescs[i // 2],
                                                pckg=gameaccappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass43.xview_scroll(-1*(event.delta//120), "units"))
    # Game analytics and visualisation apps
    returns = addapps("Game analytics and visualisation apps")
    sectionframe= returns[0]
    canvass44=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass44.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game analytics and visualisation apps
    gameanalvisualapps = ["dummy"]
    gameanalvisualappsimages = ["dummy"]
    gameanalvisualappsdescs = ["dummy"]
    gameanalvisualappspacknames = ["dummy"]

    for i in range(2, len(gameanalvisualapps) * 2, 2):
        if i / 2 < len(gameanalvisualapps):
            button = gameanalvisualapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gameanalvisualappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gameanalvisualappsdescs[i // 2],
                                                pckg=gameanalvisualappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass44.xview_scroll(-1*(event.delta//120), "units"))
    # Game community and social media apps
    returns = addapps("Game community and social media apps")
    sectionframe= returns[0]
    canvass48=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass48.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game community and social media apps
    gamecommapps = ["dummy"]
    gamecommappsimages = ["dummy"]
    gamecommappsdescs = ["dummy"]
    gamecommappspacknames = ["dummy"]

    for i in range(2, len(gamecommapps) * 2, 2):
        if i / 2 < len(gamecommapps):
            button = gamecommapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gamecommappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gamecommappsdescs[i // 2],
                                                pckg=gamecommappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass48.xview_scroll(-1*(event.delta//120), "units"))

    # Game distribution and publishing apps
    returns = addapps("Game distribution and publishing apps")
    sectionframe= returns[0]
    canvass50=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass50.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game distribution and publishing apps
    gdpapps = ["dummy"]
    gdpappsimages = ["dummy"]
    gdpappsdescs = ["dummy"]
    gdpappspacknames = ["dummy"]

    for i in range(2, len(gdpapps) * 2, 2):
        if i / 2 < len(gdpapps):
            button = gdpapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gdpappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gdpappsdescs[i // 2],
                                                pckg=gdpappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass50.xview_scroll(-1*(event.delta//120), "units"))
    # Game emulators
    returns = addapps("Game emulators")
    sectionframe= returns[0]
    canvass53=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass53.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game emulators
    gameemuapps = ["dummy"]
    gameemuappsimages = ["dummy"]
    gameemuappsdescs = ["dummy"]
    gameemuappspacknames = ["dummy"]

    for i in range(2, len(gameemuapps) * 2, 2):
        if i / 2 < len(gameemuapps):
            button = gameemuapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gameemuappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gameemuappsdescs[i // 2],
                                                pckg=gameemuappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass53.xview_scroll(-1*(event.delta//120), "units"))
    # Game engines
    returns = addapps("Game engines")
    sectionframe= returns[0]
    canvass54=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass54.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game engine apps
    gengineapps = ["dummy"]
    gengineappsimages = ["dummy"]
    gengineappsdescs = ["dummy"]
    gengineappspacknames = ["dummy"]

    for i in range(2, len(gengineapps) * 2, 2):
        if i / 2 < len(gengineapps):
            button = gengineapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gengineappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gengineappsdescs[i // 2],
                                                pckg=gengineappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass54.xview_scroll(-1*(event.delta//120), "units"))
    # Games launcher

    returns = addapps("Game launcher")
    sectionframe= returns[0]
    canvass128=returns[1]
    for i in range(1, 16, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass128.xview_scroll(-1*(event.delta//120), "units"))

    steam = ttk.Button(sectionframe, image=steamimage, text="Steam\n★★★★☆ 4.3\n🌐 Winget", width=15, compound=LEFT)
    EpicGames = ttk.Button(sectionframe, image=EpicGamesimage, text="Epic Games\n★★★★☆ 4\n🌐 Winget", width=15,
                           compound=LEFT)
    EA = ttk.Button(sectionframe, image=EAimage, text="Electronic Arts\n★★★★☆ 4\n🌐 Winget", width=15, compound=LEFT)
    GOG = ttk.Button(sectionframe, image=GOGimage, text="GOG-Galaxy \n★★★★☆ 4\n🌐 Winget", width=15, compound=LEFT)
    playnite = ttk.Button(sectionframe, image=playniteimage, text="Playnite \n★★★★☆ 4\n🌐 Winget", width=15, compound=LEFT)
    amazongames = ttk.Button(sectionframe, image=amazongamesimage, text="AmazonGames\n★★★★☆ 4\n🌐 Winget", width=15,
                             compound=LEFT)
    GeForce = ttk.Button(sectionframe, image=GeForceimage, text="Nvidea GeForce \n★★★★☆ 4\n🌐 Winget", width=15,
                         compound=LEFT)
    ubisoftconnect = ttk.Button(sectionframe, image=ubisoftconnectimage, text="Ubisoft Connect \n★★★★☆ 4\n🌐 Winget", width=15,
                                compound=LEFT)
    
    # placement of game apps
    gamelists = ["dummy", steam, EpicGames, EA, GOG, playnite, amazongames, GeForce, ubisoftconnect]
    gameimgs = ["dummy", steamimage, EpicGamesimage, EAimage, GOGimage, playniteimage, amazongamesimage, GeForceimage,
                ubisoftconnectimage]
    gamedescs = ["dummy", steamdesc, EpicGamesdesc, EAdesc, GOGdesc, playnitedesc, amazongamesdesc, GeForcedesc,
                 ubisoftconnectdesc]
    gamepacknames = ["dummy", steampack, EpicGamespack, EApack, GOGpack, playnitepack, amazongamespack, GeForcepack,
                     ubisoftconnectpack]

    for i in range(2, len(gamelists) * 2, 2):
        if i / 2 < len(gamelists):
            button = gamelists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gameimgs[i // 2], buttonname=button.cget('text'),
                                             buttondesc=gamedescs[i // 2], pckg=gamepacknames[i // 2]: [remold(),loadingscreen(
                event, buttonimg, buttonname, buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass128.xview_scroll(-1*(event.delta//120), "units"))
    
    # Game marketing and promotion apps
    returns = addapps("Game marketing and promotion apps")
    sectionframe= returns[0]
    canvass58=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass58.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game marketing and promotion apps
    gmpapps = ["dummy"]
    gmpappsimages = ["dummy"]
    gmpappsdescs = ["dummy"]
    gmpappspacknames = ["dummy"]

    for i in range(2, len(gmpapps) * 2, 2):
        if i / 2 < len(gmpapps):
            button = gmpapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gmpappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gmpappsdescs[i // 2],
                                                pckg=gmpappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass58.xview_scroll(-1*(event.delta//120), "units"))
    # Game monetisation apps
    returns = addapps("Game monetisation apps")
    sectionframe= returns[0]
    canvass60=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass60.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game monetisation apps
    gmonetapps = ["dummy"]
    gmonetappsimages = ["dummy"]
    gmonetappsdescs = ["dummy"]
    gmonetappspacknames = ["dummy"]

    for i in range(2, len(gmonetapps) * 2, 2):
        if i / 2 < len(gmonetapps):
            button = gmonetapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gmonetappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gmonetappsdescs[i // 2],
                                                pckg=gmonetappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass60.xview_scroll(-1*(event.delta//120), "units"))
    # Game motion capture apps
    returns = addapps("Game motion capture apps")
    sectionframe= returns[0]
    canvass61=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass61.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game motion capture apps
    gmotionapps = ["dummy"]
    dgmotionappsimages = ["dummy"]
    gmotionappsdescs = ["dummy"]
    gmotionappspacknames = ["dummy"]

    for i in range(2, len(gmotionapps) * 2, 2):
        if i / 2 < len(gmotionapps):
            button = gmotionapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=dgmotionappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gmotionappsdescs[i // 2],
                                                pckg=gmotionappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass61.xview_scroll(-1*(event.delta//120), "units"))
    # Game music composition apps
    returns = addapps("Game music composition apps")
    sectionframe= returns[0]
    canvass62=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass62.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game music composition apps
    gmusicapps = ["dummy"]
    gmusicappsimages = ["dummy"]
    gmusicappsdescs = ["dummy"]
    gmusicappspacknames = ["dummy"]

    for i in range(2, len(gmusicapps) * 2, 2):
        if i / 2 < len(gmusicapps):
            button = gmusicapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gmusicappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gmusicappsdescs[i // 2],
                                                pckg=gmusicappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass62.xview_scroll(-1*(event.delta//120), "units"))
    # Game networking apps
    returns = addapps("Game networking apps")
    sectionframe= returns[0]
    canvass63=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass63.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game networking apps
    gnetworkapps = ["dummy"]
    gnetworkappsimages = ["dummy"]
    gnetworkappsdescs = ["dummy"]
    gnetworkappspacknames = ["dummy"]

    for i in range(2, len(gnetworkapps) * 2, 2):
        if i / 2 < len(gnetworkapps):
            button = gnetworkapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gnetworkappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gnetworkappsdescs[i // 2],
                                                pckg=gnetworkappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass63.xview_scroll(-1*(event.delta//120), "units"))
    # Game physics engines
    returns = addapps("Game physics engines")
    sectionframe= returns[0]
    canvass64=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass64.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game physics engines
    gphyapps = ["dummy"]
    gphyappsimages = ["dummy"]
    gphyappsdescs = ["dummy"]
    gphyappspacknames = ["dummy"]

    for i in range(2, len(gphyapps) * 2, 2):
        if i / 2 < len(gphyapps):
            button = gphyapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gphyappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gphyappsdescs[i // 2],
                                                pckg=gphyappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass64.xview_scroll(-1*(event.delta//120), "units"))
    # Game physics simulation apps
    returns = addapps("Game physics simulation apps")
    sectionframe= returns[0]
    canvass65=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass65.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game physics simulation apps
    gphysimapps = ["dummy"]
    gphysimappsimages = ["dummy"]
    gphysimappsdescs = ["dummy"]
    gphysimappspacknames = ["dummy"]

    for i in range(2, len(gphysimapps) * 2, 2):
        if i / 2 < len(gphysimapps):
            button = gphysimapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gphysimappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gphysimappsdescs[i // 2],
                                                pckg=gphysimappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass65.xview_scroll(-1*(event.delta//120), "units"))
    # Game Scriptwriting and Story development apps
    returns = addapps("Game Scriptwriting and Story development apps")
    sectionframe= returns[0]
    canvass67=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass67.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game Scriptwriting and Story development apps
    gstoryapps = ["dummy"]
    gstoryappsimages = ["dummy"]
    gstoryappsdescs = ["dummy"]
    gstoryappspacknames = ["dummy"]

    for i in range(2, len(gstoryapps) * 2, 2):
        if i / 2 < len(gstoryapps):
            button = gstoryapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gstoryappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gstoryappsdescs[i // 2],
                                                pckg=gstoryappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass67.xview_scroll(-1*(event.delta//120), "units"))
    # Game streaming and broadcasting apps
    returns = addapps("Game streaming and broadcasting apps")
    sectionframe= returns[0]
    canvass69=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass69.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Game streaming and broadcasting apps
    gstreamapps = ["dummy"]
    gstreamappsimages = ["dummy"]
    gstreamappsdescs = ["dummy"]
    gstreamappspacknames = ["dummy"]

    for i in range(2, len(gstreamapps) * 2, 2):
        if i / 2 < len(gstreamapps):
            button = gstreamapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gstreamappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gstreamappsdescs[i // 2],
                                                pckg=gstreamappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass69.xview_scroll(-1*(event.delta//120), "units"))
    # Graphic design apps
    returns = addapps("Graphic design apps")
    sectionframe= returns[0]
    canvass78=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass78.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Graphic design apps
    graphicapps = ["dummy"]
    graphicappsimages = ["dummy"]
    graphicappsdescs = ["dummy"]
    graphicappspacknames = ["dummy"]

    for i in range(2, len(graphicapps) * 2, 2):
        if i / 2 < len(graphicapps):
            button = graphicapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=graphicappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=graphicappsdescs[i // 2],
                                                pckg=graphicappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass78.xview_scroll(-1*(event.delta//120), "units"))
    # Health and fitness apps
    returns = addapps("Health and fitness apps")
    sectionframe= returns[0]
    canvass79=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass79.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Health and fitness apps
    healthapps = ["dummy"]
    healthappsimages = ["dummy"]
    healthappsdescs = ["dummy"]
    healthappspacknames = ["dummy"]

    for i in range(2, len(healthapps) * 2, 2):
        if i / 2 < len(healthapps):
            button = healthapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=healthappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=healthappsdescs[i // 2],
                                                pckg=healthappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass79.xview_scroll(-1*(event.delta//120), "units"))
    # Human resource apps
    returns = addapps("Human resources and management apps")
    sectionframe= returns[0]
    canvass80=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass80.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Human resource apps
    hrapps = ["dummy"]
    hrappsimages = ["dummy"]
    hrappsdescs = ["dummy"]
    hrappspacknames = ["dummy"]

    for i in range(2, len(hrapps) * 2, 2):
        if i / 2 < len(hrapps):
            button = hrapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=hrappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=hrappsdescs[i // 2],
                                                pckg=hrappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass80.xview_scroll(-1*(event.delta//120), "units"))
    # Image editing and manipulation apps    
    returns = addapps("Image editing and manipulation apps    ")
    sectionframe= returns[0]
    canvass81=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass81.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Image editing and manipulation apps     
    imgeditapps = ["dummy"]
    imgeditappsimages = ["dummy"]
    imgeditappsdescs = ["dummy"]
    imgeditappspacknames = ["dummy"]

    for i in range(2, len(imgeditapps) * 2, 2):
        if i / 2 < len(imgeditapps):
            button = imgeditapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=imgeditappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=imgeditappsdescs[i // 2],
                                                pckg=imgeditappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass81.xview_scroll(-1*(event.delta//120), "units"))
    # Ide's
    returns = addapps("Integrated development environments(IDE's)")
    sectionframe= returns[0]
    canvass82=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass82.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Integrated development environments(IDE's)
    ideapps = ["dummy"]
    ideappsimages = ["dummy"]
    ideappsdescs = ["dummy"]
    ideappspacknames = ["dummy"]

    for i in range(2, len(ideapps) * 2, 2):
        if i / 2 < len(ideapps):
            button = ideapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=ideappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=ideappsdescs[i // 2],
                                                pckg=ideappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass82.xview_scroll(-1*(event.delta//120), "units"))
    # Inventory management apps
    returns = addapps("Inventory management apps")
    sectionframe= returns[0]
    canvass83=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass83.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Inventory management apps
    gnetworkapps = ["dummy"]
    gnetworkappsimages = ["dummy"]
    gnetworkappsdescs = ["dummy"]
    gnetworkappspacknames = ["dummy"]

    for i in range(2, len(gnetworkapps) * 2, 2):
        if i / 2 < len(gnetworkapps):
            button = gnetworkapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=gnetworkappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=gnetworkappsdescs[i // 2],
                                                pckg=gnetworkappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass83.xview_scroll(-1*(event.delta//120), "units"))
    
    # Language learning apps
    returns = addapps("Language learning apps")
    sectionframe= returns[0]
    canvass84=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass84.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Language learning apps
    langapps = ["dummy"]
    langappsimages = ["dummy"]
    langappsdescs = ["dummy"]
    langappspacknames = ["dummy"]

    for i in range(2, len(langapps) * 2, 2):
        if i / 2 < len(langapps):
            button = langapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=langappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=langappsdescs[i // 2],
                                                pckg=langappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass84.xview_scroll(-1*(event.delta//120), "units"))
    # Map and navigation apps
    returns = addapps("Map and navigation apps")
    sectionframe= returns[0]
    canvass85=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass85.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Map and navigation apps
    mapapps = ["dummy"]
    mapappsimages = ["dummy"]
    mapappsdescs = ["dummy"]
    mapappspacknames = ["dummy"]

    for i in range(2, len(mapapps) * 2, 2):
        if i / 2 < len(mapapps):
            button = mapapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=mapappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=mapappsdescs[i // 2],
                                                pckg=mapappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass85.xview_scroll(-1*(event.delta//120), "units"))
    # Mind and body apps
    returns = addapps("Mind and body apps")
    sectionframe= returns[0]
    canvass86=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass86.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Mind and body apps
    mindapps = ["dummy"]
    mindappsimages = ["dummy"]
    mindappsdescs = ["dummy"]
    mindappspacknames = ["dummy"]

    for i in range(2, len(mindapps) * 2, 2):
        if i / 2 < len(mindapps):
            button = mindapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=mindappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=mindappsdescs[i // 2],
                                                pckg=mindappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass86.xview_scroll(-1*(event.delta//120), "units"))
    # Mind mapping and brainstorming apps
    returns = addapps("Mind mapping and brainstorming apps")
    sectionframe= returns[0]
    canvass87=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass87.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Mind mapping and brainstorming apps
    mindmappingapps = ["dummy"]
    mindmappingappsimages = ["dummy"]
    mindmappingappsdescs = ["dummy"]
    mindmappingappspacknames = ["dummy"]

    for i in range(2, len(mindmappingapps) * 2, 2):
        if i / 2 < len(mindmappingapps):
            button = mindmappingapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=mindmappingappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=mindmappingappsdescs[i // 2],
                                                pckg=mindmappingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass87.xview_scroll(-1*(event.delta//120), "units"))

    # Multimedia
    returns = addapps("Multimedia")
    sectionframe= returns[0]
    canvass129=returns[1]
    for i in range(1, 12, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass129.xview_scroll(-1*(event.delta//120), "units"))
    spotify = ttk.Button(sectionframe, image=spotifyimage, text="Spotify\n★★★★☆ 4.5\n🌐 Winget", width=15,
                                compound=LEFT)
    vlc = ttk.Button(sectionframe, image=vlcimage, text="VLC Media Player\n★★★★☆ 4.5\n🌐 Winget", width=15,
                                compound=LEFT)
    mpchc = ttk.Button(sectionframe, image=mpchcimage, text="MPC-HC\n★★★★☆ 4.5\n🌐 Winget", width=15,
                                compound=LEFT)
    kodi = ttk.Button(sectionframe, image=kodiimage, text="Kodi \n★★★★☆ 4.2\n🌐 Winget", width=15,
                                compound=LEFT)
    plex = ttk.Button(sectionframe, image=pleximage, text="Plex \n★★★★☆ 4\n🌐 Winget", width=15,
                                compound=LEFT)
    itunes = ttk.Button(sectionframe, image=itunesimage, text="iTunes \n★★★★☆ 4.8\n🌐 Winget", width=15,
                                compound=LEFT)

    # placement of multimedia apps
    multimedialists = ["dummy",spotify,vlc,mpchc,kodi,plex,itunes]
    multimediaimgs = ["dummy",spotifyimage,vlcimage,mpchcimage,kodiimage,pleximage,itunesimage]
    multimediadescs = ["dummy",spotifydesc,vlcdesc,mpchcdesc,kodidesc,plexdesc,itunesdesc]
    multimediapacknames = ["dummy",spotifypack,vlcpack,mpchcpack,kodipack,plexpack,itunespack]

    for i in range(2, len(multimedialists) * 2, 2):
        if i / 2 < len(multimedialists):
            button = multimedialists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=multimediaimgs[i // 2], buttonname=button.cget('text'),
                                             buttondesc=multimediadescs[i // 2], pckg=multimediapacknames[i // 2]:[remold(), loadingscreen(
                event, buttonimg, buttonname, buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass129.xview_scroll(-1*(event.delta//120), "units"))

    # Music streaming apps
    returns = addapps("Music streaming apps")
    sectionframe= returns[0]
    canvass88=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass88.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Music streaming apps
    musicapps = ["dummy"]
    musicappsimages = ["dummy"]
    musicappsdescs = ["dummy"]
    musicappspacknames = ["dummy"]

    for i in range(2, len(musicapps) * 2, 2):
        if i / 2 < len(musicapps):
            button = musicapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=musicappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=musicappsdescs[i // 2],
                                                pckg=musicappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass88.xview_scroll(-1*(event.delta//120), "units"))
    # Network management and monitoring apps
    returns = addapps("Network monitoring and management apps")
    sectionframe= returns[0]
    canvass89=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass89.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Network management and monitoring apps
    networkapps = ["dummy"]
    networkappsimages = ["dummy"]
    networkappsdescs = ["dummy"]
    networkappspacknames = ["dummy"]

    for i in range(2, len(networkapps) * 2, 2):
        if i / 2 < len(networkapps):
            button = networkapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=networkappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=networkappsdescs[i // 2],
                                                pckg=networkappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass89.xview_scroll(-1*(event.delta//120), "units"))
    # News apps
    returns = addapps("News apps")
    sectionframe= returns[0]
    canvass90=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass90.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all News apps
    Newsapps = ["dummy"]
    Newsappsimages = ["dummy"]
    Newsappsdescs = ["dummy"]
    Newsappspacknames = ["dummy"]

    for i in range(2, len(Newsapps) * 2, 2):
        if i / 2 < len(Newsapps):
            button = Newsapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Newsappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Newsappsdescs[i // 2],
                                                pckg=Newsappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass90.xview_scroll(-1*(event.delta//120), "units"))
    # Office suite apps
    returns = addapps("Office suite apps")
    sectionframe= returns[0]
    canvass91=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass91.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Office suite apps
    offsuiteapps = ["dummy"]
    offsuiteappsimages = ["dummy"]
    offsuiteappsdescs = ["dummy"]
    offsuiteappspacknames = ["dummy"]

    for i in range(2, len(offsuiteapps) * 2, 2):
        if i / 2 < len(offsuiteapps):
            button = offsuiteapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=offsuiteappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=offsuiteappsdescs[i // 2],
                                                pckg=offsuiteappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass91.xview_scroll(-1*(event.delta//120), "units"))
    # PDF readers and editors
    returns = addapps("PDF readers and editors")
    sectionframe= returns[0]
    canvass92=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass92.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all PDF readers and editors
    pdfapps = ["dummy"]
    pdfappsimages = ["dummy"]
    pdfappsdescs = ["dummy"]
    pdfappspacknames = ["dummy"]

    for i in range(2, len(pdfapps) * 2, 2):
        if i / 2 < len(pdfapps):
            button = pdfapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=pdfappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=pdfappsdescs[i // 2],
                                                pckg=pdfappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass92.xview_scroll(-1*(event.delta//120), "units"))
    # Parental control apps
    returns = addapps("Parental control apps")
    sectionframe= returns[0]
    canvass93=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass93.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Parental control apps
    parentapps = ["dummy"]
    parentappsimages = ["dummy"]
    parentappsdescs = ["dummy"]
    parentappspacknames = ["dummy"]

    for i in range(2, len(parentapps) * 2, 2):
        if i / 2 < len(parentapps):
            button = parentapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=parentappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=parentappsdescs[i // 2],
                                                pckg=parentappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass93.xview_scroll(-1*(event.delta//120), "units"))
    # Password management apps
    returns = addapps("Password management apps")
    sectionframe= returns[0]
    canvass94=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass94.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Password management apps
    passmanapps = ["dummy"]
    passmanappsimages = ["dummy"]
    passmanappsdescs = ["dummy"]
    passmanappspacknames = ["dummy"]

    for i in range(2, len(passmanapps) * 2, 2):
        if i / 2 < len(passmanapps):
            button = passmanapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=passmanappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=passmanappsdescs[i // 2],
                                                pckg=passmanappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass94.xview_scroll(-1*(event.delta//120), "units"))
    # Payroll management apps
    returns = addapps("Payroll management apps")
    sectionframe= returns[0]
    canvass95=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass95.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Payroll management apps
    payrollapps = ["dummy"]
    payrollappsimages = ["dummy"]
    payrollappsdescs = ["dummy"]
    payrollappspacknames = ["dummy"]

    for i in range(2, len(payrollapps) * 2, 2):
        if i / 2 < len(payrollapps):
            button = payrollapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=payrollappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=payrollappsdescs[i // 2],
                                                pckg=payrollappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass95.xview_scroll(-1*(event.delta//120), "units"))
    # Personal organisation apps
    returns = addapps("Personal organisation apps")
    sectionframe= returns[0]
    canvass96=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass96.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Personal organisation apps
    personalorgapps = ["dummy"]
    personalorgappsimages = ["dummy"]
    personalorgappsdescs = ["dummy"]
    personalorgappspacknames = ["dummy"]

    for i in range(2, len(personalorgapps) * 2, 2):
        if i / 2 < len(personalorgapps):
            button = personalorgapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=personalorgappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=personalorgappsdescs[i // 2],
                                                pckg=personalorgappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass96.xview_scroll(-1*(event.delta//120), "units"))
    # Point-of-sale apps
    returns = addapps("Point-of-sale apps")
    sectionframe= returns[0]
    canvass97=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass97.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Point-of-sale apps
    posapps = ["dummy"]
    posappsimages = ["dummy"]
    posappsdescs = ["dummy"]
    posappspacknames = ["dummy"]

    for i in range(2, len(posapps) * 2, 2):
        if i / 2 < len(posapps):
            button = posapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=posappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=posappsdescs[i // 2],
                                                pckg=posappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass97.xview_scroll(-1*(event.delta//120), "units"))
    # Presentation and slide creation apps
    returns = addapps("Presentation and slide creation apps")
    sectionframe= returns[0]
    canvass98=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass98.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Presentation and slide creation apps
    presapps = ["dummy"]
    presappsimages = ["dummy"]
    presappsdescs = ["dummy"]
    presappspacknames = ["dummy"]

    for i in range(2, len(presapps) * 2, 2):
        if i / 2 < len(presapps):
            button = presapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=presappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=presappsdescs[i // 2],
                                                pckg=presappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass98.xview_scroll(-1*(event.delta//120), "units"))
    # Profiling apps
    returns = addapps("Profiling apps")
    sectionframe= returns[0]
    canvass100=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass100.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Profiling apps
    Profilingapps = ["dummy"]
    Profilingappsimages = ["dummy"]
    Profilingappsdescs = ["dummy"]
    Profilingappspacknames = ["dummy"]

    for i in range(2, len(Profilingapps) * 2, 2):
        if i / 2 < len(Profilingapps):
            button = Profilingapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Profilingappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Profilingappsdescs[i // 2],
                                                pckg=Profilingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass100.xview_scroll(-1*(event.delta//120), "units"))
    # Programming and development apps
    returns = addapps("Programming and development apps")
    sectionframe= returns[0]
    canvass101=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass101.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Programming and development apps
    Programmingapps = ["dummy"]
    Programmingappsimages = ["dummy"]
    Programmingappsdescs = ["dummy"]
    Programmingappspacknames = ["dummy"]

    for i in range(2, len(Programmingapps) * 2, 2):
        if i / 2 < len(Programmingapps):
            button = Programmingapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Programmingappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Programmingappsdescs[i // 2],
                                                pckg=Programmingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass101.xview_scroll(-1*(event.delta//120), "units"))
    # Project management apps
    returns = addapps("Project management apps")
    sectionframe= returns[0]
    canvass102=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass102.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Project management apps
    Projectapps = ["dummy"]
    Projectappsimages = ["dummy"]
    Projectappsdescs = ["dummy"]
    Projectappspacknames = ["dummy"]

    for i in range(2, len(Projectapps) * 2, 2):
        if i / 2 < len(Projectapps):
            button = Projectapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Projectappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Projectappsdescs[i // 2],
                                                pckg=Projectappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass102.xview_scroll(-1*(event.delta//120), "units"))
    # Remote access apps
    returns = addapps("Remote access and control apps")
    sectionframe= returns[0]
    canvass103=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass103.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Remote access apps
    remoteaccapps = ["dummy"]
    remoteaccappsimages = ["dummy"]
    remoteaccappsdescs = ["dummy"]
    remoteaccappspacknames = ["dummy"]

    for i in range(2, len(remoteaccapps) * 2, 2):
        if i / 2 < len(remoteaccapps):
            button = remoteaccapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=remoteaccappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=remoteaccappsdescs[i // 2],
                                                pckg=remoteaccappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass103.xview_scroll(-1*(event.delta//120), "units"))
    # Retail management apps
    returns = addapps("Retail management apps")
    sectionframe= returns[0]
    canvass104=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass104.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Retail management apps
    Retailapps = ["dummy"]
    Retailappsimages = ["dummy"]
    Retailappsdescs = ["dummy"]
    Retailappspacknames = ["dummy"]

    for i in range(2, len(Retailapps) * 2, 2):
        if i / 2 < len(Retailapps):
            button = Retailapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Retailappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Retailappsdescs[i // 2],
                                                pckg=Retailappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass104.xview_scroll(-1*(event.delta//120), "units"))
    # SEO and analytics apps
    returns = addapps("SEO and analytics apps")
    sectionframe= returns[0]
    canvass105=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass105.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all SEO and analytics apps
    SEOapps = ["dummy"]
    SEOappsimages = ["dummy"]
    SEOappsdescs = ["dummy"]
    SEOappspacknames = ["dummy"]

    for i in range(2, len(SEOapps) * 2, 2):
        if i / 2 < len(SEOapps):
            button = SEOapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=SEOappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=SEOappsdescs[i // 2],
                                                pckg=SEOappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass105.xview_scroll(-1*(event.delta//120), "units"))
    # Screenshot and screen recording apps
    returns = addapps("Screenshot and screen recording apps")
    sectionframe= returns[0]
    canvass106=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass106.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Screenshot and screen recording apps
    ssapps = ["dummy"]
    ssappsimages = ["dummy"]
    ssappsdescs = ["dummy"]
    ssappspacknames = ["dummy"]

    for i in range(2, len(ssapps) * 2, 2):
        if i / 2 < len(ssapps):
            button = ssapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=ssappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=ssappsdescs[i // 2],
                                                pckg=ssappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass106.xview_scroll(-1*(event.delta//120), "units"))
    # Social media apps
    returns = addapps("Social media apps")
    sectionframe= returns[0]
    canvass107=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass107.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Social media apps
    Socialapps = ["dummy"]
    Socialappsimages = ["dummy"]
    Socialappsdescs = ["dummy"]
    Socialappspacknames = ["dummy"]

    for i in range(2, len(Socialapps) * 2, 2):
        if i / 2 < len(Socialapps):
            button = Socialapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg= Socialappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Socialappsdescs[i // 2],
                                                pckg=Socialappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass107.xview_scroll(-1*(event.delta//120), "units"))
    # Supply chain management apps
    returns = addapps("Supply chain management apps")
    sectionframe= returns[0]
    canvass108=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass108.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Supply chain management apps
    suppchainapps = ["dummy"]
    suppchainappsimages = ["dummy"]
    suppchainappsdescs = ["dummy"]
    suppchainappspacknames = ["dummy"]

    for i in range(2, len(suppchainapps) * 2, 2):
        if i / 2 < len(suppchainapps):
            button = suppchainapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=suppchainappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=suppchainappsdescs[i // 2],
                                                pckg=suppchainappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass108.xview_scroll(-1*(event.delta//120), "units"))
    # System information and diagnostic tools
    returns = addapps("System information and diagnostic tools")
    sectionframe= returns[0]
    canvass109=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass109.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all System information and diagnostic tools
    sysinfoapps = ["dummy"]
    sysinfoappsimages = ["dummy"]
    sysinfoappsdescs = ["dummy"]
    sysinfoappspacknames = ["dummy"]

    for i in range(2, len(sysinfoapps) * 2, 2):
        if i / 2 < len(sysinfoapps):
            button = sysinfoapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=sysinfoappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=sysinfoappsdescs[i // 2],
                                                pckg=sysinfoappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass109.xview_scroll(-1*(event.delta//120), "units"))
    # System Optimisation and performance apps
    returns = addapps("System Optimisation and performance apps")
    sectionframe= returns[0]
    canvass110=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass110.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all System Optimisation and performance apps
    sysperfapps = ["dummy"]
    sysperfappsimages = ["dummy"]
    sysperfappsdescs = ["dummy"]
    sysperfappspacknames = ["dummy"]

    for i in range(2, len(sysperfapps) * 2, 2):
        if i / 2 < len(sysperfapps):
            button = sysperfapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=sysperfappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=sysperfappsdescs[i // 2],
                                                pckg=sysperfappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass110.xview_scroll(-1*(event.delta//120), "units"))
    # Tax preperation and filing apps
    returns = addapps("Tax preperation and filing apps")
    sectionframe= returns[0]
    canvass111=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass111.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Tax preperation and filing apps
    taxapps = ["dummy"]
    taxappsimages = ["dummy"]
    taxappsdescs = ["dummy"]
    taxappspacknames = ["dummy"]

    for i in range(2, len(taxapps) * 2, 2):
        if i / 2 < len(taxapps):
            button = taxapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=taxappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=taxappsdescs[i // 2],
                                                pckg=taxappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass111.xview_scroll(-1*(event.delta//120), "units"))
    
    # Terminal emulators
    returns = addapps("Terminal emulators")
    sectionframe= returns[0]
    canvass112=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass112.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Terminal emulators
    terminalapps = ["dummy"]
    terminalappsimages = ["dummy"]
    terminalappsdescs = ["dummy"]
    terminalappspacknames = ["dummy"]

    for i in range(2, len(terminalapps) * 2, 2):
        if i / 2 < len(terminalapps):
            button = terminalapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=terminalappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=terminalappsdescs[i // 2],
                                                pckg=terminalappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass112.xview_scroll(-1*(event.delta//120), "units"))
    # Text editors
    returns = addapps("Text editors")
    sectionframe= returns[0]
    canvass113=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass113.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Text editors
    Texteditapps = ["dummy"]
    Texteditappsimages = ["dummy"]
    Texteditappsdescs = ["dummy"]
    Texteditappspacknames = ["dummy"]

    for i in range(2, len(Texteditapps) * 2, 2):
        if i / 2 < len(Texteditapps):
            button = Texteditapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Texteditappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Texteditappsdescs[i // 2],
                                                pckg=Texteditappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass113.xview_scroll(-1*(event.delta//120), "units"))
    # Time tracking and invoicing apps
    returns = addapps("Time tracking and invoicing apps")
    sectionframe= returns[0]
    canvass114=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass114.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Time tracking and invoicing apps
    ttiapps = ["dummy"]
    ttiappsimages = ["dummy"]
    ttiappsdescs = ["dummy"]
    ttiappspacknames = ["dummy"]

    for i in range(2, len(ttiapps) * 2, 2):
        if i / 2 < len(ttiapps):
            button = ttiapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=ttiappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=ttiappsdescs[i // 2],
                                                pckg=ttiappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass114.xview_scroll(-1*(event.delta//120), "units"))
    # Travel apps
    returns = addapps("Travel apps")
    sectionframe= returns[0]
    canvass115=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass115.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Travel apps
    Travelapps = ["dummy"]
    Travelappsimages = ["dummy"]
    Travelappsdescs = ["dummy"]
    Travelappspacknames = ["dummy"]

    for i in range(2, len(Travelapps) * 2, 2):
        if i / 2 < len(Travelapps):
            button = Travelapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Travelappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Travelappsdescs[i // 2],
                                                pckg=Travelappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass115.xview_scroll(-1*(event.delta//120), "units"))

    # utilities apps

    returns = addapps("Utilities apps")
    sectionframe= returns[0]
    canvass130=returns[1]
    for i in range(1, 26, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass130.xview_scroll(-1*(event.delta//120), "units"))
    hwinfo = ttk.Button(sectionframe, image=hwinfoimage, text="HW Info\n★★★★☆ 4\n🌐 Winget", width=15, compound=LEFT)
    coretemp = ttk.Button(sectionframe, image=coretempimage, text="Core Temp\n★★★★☆ 4\n🌐 Winget", width=15, compound=LEFT)
    sevenzip = ttk.Button(sectionframe, image=sevenzipimage, text="7Zip\n★★★★☆ 4.3\n🌐 Winget", width=15,
                          compound=LEFT)
    anydesk = ttk.Button(sectionframe, image=anydeskimage, text="Anydesk \n★★★★☆ 4.4\n🌐 Winget", width=15, compound=LEFT)
    cpuz = ttk.Button(sectionframe, image=cpuzimage, text="CPU-Z\n★★★★☆ 4.5\n🌐 Winget", width=15, compound=LEFT)
    etcher = ttk.Button(sectionframe, image=etcherimage, text="Balena Etcher \n★★★★☆ 4\n🌐 Winget", width=15, compound=LEFT)
    gpuz = ttk.Button(sectionframe, image=gpuzimage, text="GPU-Z \n★★★☆☆ 3.6\n🌐 Winget", width=15, compound=LEFT)
    revouninstaller = ttk.Button(sectionframe, image=revouninstallerimage, text="Revo Uninstaller \n★★★☆☆ 3.5\n🌐 Winget",
                                 width=15, compound=LEFT)
    powertoys = ttk.Button(sectionframe, image=powertoysimage, text="Powertoys \n★★★★☆ 4.5\n🌐 Winget", width=15,
                           compound=LEFT)
    autohotkey = ttk.Button(sectionframe, image=autohotkeyimage, text="Autohotkey \n★★★★☆ 4.4\n🌐 Winget", width=15,
                            compound=LEFT)
    bitwarden = ttk.Button(sectionframe, image=bitwardenimage, text="Bitwarden \n★★★★☆ 4\n🌐 Winget", width=15,
                        compound=LEFT)
    everythingsearch = ttk.Button(sectionframe, image=everythingsearchimage, text="Everything search \n★★★★☆ 4\n🌐 Winget",
                                  width=14, compound=LEFT)
    flux = ttk.Button(sectionframe, image=fluximage, text="Flux\n★★★★☆ 4.8\n🌐 Winget", width=15, compound=LEFT)

    # placement of dev apps
    utillists = ["dummy", hwinfo, coretemp, sevenzip, anydesk, cpuz, etcher, gpuz, revouninstaller, powertoys,
                 autohotkey, bitwarden, everythingsearch, flux]
    utilimgs = ["dummy", hwinfoimage, coretempimage, sevenzipimage, anydeskimage, cpuzimage, etcherimage, gpuzimage,
                revouninstallerimage, powertoysimage, autohotkeyimage, bitwardenimage, everythingsearchimage, fluximage]
    utildescs = ["dummy", hwinfodesc, coretempdesc, sevenzipdesc, anydeskdesc, cpuzdesc, etcherdesc, gpuzdesc,
                 revouninstallerdesc, powertoysdesc, autohotkeydesc, bitwardendesc, everythingsearchdesc, fluxdesc]
    utilpacknames = ["dummy", hwinfopack, coretemppack, sevenzippack, anydeskpack, cpuzpack, etcherpack, gpuzpack,
                     revouninstallerpack, powertoyspack, autohotkeypack, bitwardenpack, everythingsearchpack, fluxpack]

    for i in range(2, len(utillists) * 2, 2):
        if i / 2 < len(utillists):
            button = utillists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=utilimgs[i // 2], buttonname=button.cget('text'),
                                             buttondesc=utildescs[i // 2], pckg=utilpacknames[i // 2]:[remold(), loadingscreen(
                event, buttonimg, buttonname, buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass130.xview_scroll(-1*(event.delta//120), "units"))

    # VPN apps
    returns = addapps("VPN apps")
    sectionframe= returns[0]
    canvass116=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass116.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all VPN apps
    VPNapps = ["dummy"]
    VPNappsimages = ["dummy"]
    VPNappsdescs = ["dummy"]
    VPNappspacknames = ["dummy"]

    for i in range(2, len(VPNapps) * 2, 2):
        if i / 2 < len(VPNapps):
            button = VPNapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=VPNappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=VPNappsdescs[i // 2],
                                                pckg=VPNappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass116.xview_scroll(-1*(event.delta//120), "units"))
    # Video and audio compression apps
    returns = addapps("Video and audio compression apps")
    sectionframe= returns[0]
    canvass117=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass117.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Video and audio compression apps
    vacapps = ["dummy"]
    vacappsimages = ["dummy"]
    vacappsdescs = ["dummy"]
    vacappspacknames = ["dummy"]

    for i in range(2, len(vacapps) * 2, 2):
        if i / 2 < len(vacapps):
            button = vacapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=vacappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=vacappsdescs[i // 2],
                                                pckg=vacappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass117.xview_scroll(-1*(event.delta//120), "units"))
    # Video editing apps
    returns = addapps("Video editing apps")
    sectionframe= returns[0]
    canvass118=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass118.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Video editing apps
    veditapps = ["dummy"]
    veditappsimages = ["dummy"]
    veditappsdescs = ["dummy"]
    veditappspacknames = ["dummy"]

    for i in range(2, len(veditapps) * 2, 2):
        if i / 2 < len(veditapps):
            button = veditapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=veditappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=veditappsdescs[i // 2],
                                                pckg=veditappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass118.xview_scroll(-1*(event.delta//120), "units"))
    # Video streaming apps
    returns = addapps("Video streaming apps")
    sectionframe= returns[0]
    canvass119=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass119.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Video streaming apps
    vstreamapps = ["dummy"]
    vstreamappsimages = ["dummy"]
    vstreamappsdescs = ["dummy"]
    vstreamappspacknames = ["dummy"]

    for i in range(2, len(vstreamapps) * 2, 2):
        if i / 2 < len(vstreamapps):
            button = vstreamapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=vstreamappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=vstreamappsdescs[i // 2],
                                                pckg=vstreamappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass119.xview_scroll(-1*(event.delta//120), "units"))
    # Virtual and augmented reality apps
    returns = addapps("Virtual and augmented reality apps")
    sectionframe= returns[0]
    canvass120=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass120.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Virtual and augmented reality apps
    virtapps = ["dummy"]
    virtappsimages = ["dummy"]
    virtappsdescs = ["dummy"]
    virtappspacknames = ["dummy"]

    for i in range(2, len(virtapps) * 2, 2):
        if i / 2 < len(virtapps):
            button = virtapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=virtappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=virtappsdescs[i // 2],
                                                pckg=virtappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass120.xview_scroll(-1*(event.delta//120), "units"))
    # Virtual event and webinar apps
    returns = addapps("Virtual event and webinar apps")
    sectionframe= returns[0]
    canvass121=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass121.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Virtual event and webinar apps
    verteventapps = ["dummy"]
    verteventappsimages = ["dummy"]
    verteventappsdescs = ["dummy"]
    verteventappspacknames = ["dummy"]

    for i in range(2, len(verteventapps) * 2, 2):
        if i / 2 < len(verteventapps):
            button = verteventapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=verteventappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=verteventappsdescs[i // 2],
                                                pckg=verteventappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass121.xview_scroll(-1*(event.delta//120), "units"))
    # Virtual meeting and  conference apps
    returns = addapps("Virtual meeting and  conference apps")
    sectionframe= returns[0]
    canvass122=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass122.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Virtual meeting and  conference apps
    vertmeetingapps = ["dummy"]
    vertmeetingappsimages = ["dummy"]
    vertmeetingappsdescs = ["dummy"]
    vertmeetingappspacknames = ["dummy"]

    for i in range(2, len(vertmeetingapps) * 2, 2):
        if i / 2 < len(vertmeetingapps):
            button = vertmeetingapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=vertmeetingappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=vertmeetingappsdescs[i // 2],
                                                pckg=vertmeetingappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass122.xview_scroll(-1*(event.delta//120), "units"))
    # Virtual reality content creation apps
    returns = addapps("Virtual reality content creation apps")
    sectionframe= returns[0]
    canvass123=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass123.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Virtual reality content creation apps
    vrcontentapps = ["dummy"]
    vrcontentappsimages = ["dummy"]
    vrcontentappsdescs = ["dummy"]
    vrcontentappspacknames = ["dummy"]

    for i in range(2, len(vrcontentapps) * 2, 2):
        if i / 2 < len(vrcontentapps):
            button = vrcontentapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=vrcontentappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=vrcontentappsdescs[i // 2],
                                                pckg=vrcontentappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass123.xview_scroll(-1*(event.delta//120), "units"))
    # Virtualization software
    returns = addapps("Virtualization software")
    sectionframe= returns[0]
    canvass124=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass124.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Virtualization software
    Virtualizationapps = ["dummy"]
    Virtualizationappsimages = ["dummy"]
    Virtualizationappsdescs = ["dummy"]
    Virtualizationappspacknames = ["dummy"]

    for i in range(2, len(Virtualizationapps) * 2, 2):
        if i / 2 < len(Virtualizationapps):
            button = Virtualizationapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Virtualizationappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Virtualizationappsdescs[i // 2],
                                                pckg=Virtualizationappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass124.xview_scroll(-1*(event.delta//120), "units"))
    # Voice recognition apps
    returns = addapps("Voice recognition apps")
    sectionframe= returns[0]
    canvass125=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass125.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Voice recognition apps
    vrecapps = ["dummy"]
    vrecappsimages = ["dummy"]
    vrecappsdescs = ["dummy"]
    vrecappspacknames = ["dummy"]

    for i in range(2, len(vrecapps) * 2, 2):
        if i / 2 < len(vrecapps):
            button = vrecapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=vrecappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=vrecappsdescs[i // 2],
                                                pckg=vrecappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass125.xview_scroll(-1*(event.delta//120), "units"))
    # Weather apps
    returns = addapps("Weather apps")
    sectionframe= returns[0]
    canvass126=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass126.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Weather apps
    Weatherapps = ["dummy"]
    Weatherappsimages = ["dummy"]
    Weatherappsdescs = ["dummy"]
    Weatherappspacknames = ["dummy"]

    for i in range(2, len(Weatherapps) * 2, 2):
        if i / 2 < len(Weatherapps):
            button = Weatherapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=Weatherappsimages[i // 2], buttonname=button.cget('text'),
                                                buttondesc=Weatherappsdescs[i // 2],
                                                pckg=Weatherappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,
                                                                                        buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass126.xview_scroll(-1*(event.delta//120), "units"))
    
    # Web browsers
    returns = addapps("Web Browsers")
    sectionframe= returns[0]
    canvass131=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass131.xview_scroll(-1*(event.delta//120), "units"))

    bravebrowser = ttk.Button(sectionframe, image=braveimage, text="Brave\n★★★★☆ 4.2\n🌐 Winget", width=15,
                              compound=LEFT)
    firefoxbrowser = ttk.Button(sectionframe, image=firefoximage, text="Firefox\n★★★★☆ 4\n🌐 Winget", width=15,
                                compound=LEFT)
    librewolfbrowser = ttk.Button(sectionframe, image=librewolfimage, text="Librewolf\n★★★★☆ 4\n🌐 Winget", width=15,
                                  compound=LEFT)
    torbrowser = ttk.Button(sectionframe, image=torimage, text="Tor\n★★★☆☆ 3.5\n🌐 Winget", width=15, compound=LEFT)
    vivaldibrowser = ttk.Button(sectionframe, image=vivaldiimage, text="Vivaldi\n★★★☆☆ 3.5\n🌐 Winget", width=15,
                                compound=LEFT)
    chromebrowser = ttk.Button(sectionframe, image=chromeimage, text="Chrome\n★★★★☆ 4\n🌐 Winget", width=15,
                               compound=LEFT)
    msedgebrowser = ttk.Button(sectionframe, image=msedgeimage, text="MS Edge Dev\n★★★★☆ 4\n🌐 Winget", width=15,
                               compound=LEFT)
    operagxbrowser = ttk.Button(sectionframe, image=operagximage, text="Opera GX\n★★★★☆ 4\n🌐 Winget", width=15,
                                compound=LEFT)
    chromiumbrowser = ttk.Button(sectionframe, image=chromiumimage, text="Chromium\n★★★★☆ 4\n🌐 Winget", width=15,
                                compound=LEFT)
    # placements of all browsers
    browserlists = ["dummy", bravebrowser, firefoxbrowser, librewolfbrowser, torbrowser, vivaldibrowser, chromebrowser,
                    msedgebrowser, operagxbrowser, chromiumbrowser]
    browserimgs = ["dummy", braveimage, firefoximage, librewolfimage, torimage, vivaldiimage, chromeimage, msedgeimage,
                   operagximage, chromiumimage]
    browserdescs = ["dummy", bravedesc, firefoxdesc, librewolfdesc, tordesc, vivaldidesc, chromedesc, msedgedesc,
                    operagxdesc, chromiumdesc]
    browserpacknames = ["dummy", bravepack, firefoxpack, librewolfpack, torpack, vivaldipack, chromepack, msedgepack,
                        operagxpack, chromiumpack]
    for i in range(2, len(browserlists) * 2, 2):
        if i / 2 < len(browserlists):
            button = browserlists[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=browserimgs[i // 2], buttonname=button.cget('text'), buttondesc=browserdescs[i // 2],pckg=browserpacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname,buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass131.xview_scroll(-1*(event.delta//120), "units"))
        
    # Windows customisation software
    returns = addapps("Windows customisation software")
    sectionframe= returns[0]
    canvass127=returns[1]
    for i in range(1, 18, 2):
        spacing = ttk.Label(sectionframe, text=" ", font=("calibri", 95))
        spacing.grid(row=0, column=i)
        spacing.bind("<MouseWheel>", lambda event: canvass127.xview_scroll(-1*(event.delta//120), "units"))
    # placements of all Windows customisation software
    vcsapps = ["dummy"]
    vcsappsimages = ["dummy"]
    vcsappsdescs = ["dummy"]
    vcsappspacknames = ["dummy"]

    for i in range(2, len(vcsapps) * 2, 2):
        if i / 2 < len(vcsapps):
            button = vcsapps[i // 2]
            button.grid(row=0, column=i, ipady=40, ipadx=25)
            button.bind("<Button-1>", lambda event, buttonimg=vcsappsimages[i // 2], buttonname=button.cget('text'),buttondesc=vcsappsdescs[i // 2],pckg=vcsappspacknames[i // 2]: [remold(),loadingscreen(event, buttonimg, buttonname, buttondesc, pckg)])
            button.bind("<MouseWheel>", lambda event: canvass127.xview_scroll(-1*(event.delta//120),"units"))

    global allapps
    allapps=[blender,sketchup,sweethome3d,freecad,openscad,meshlab,cura,prusaslicer,POVRay,meshlab]
    # spacing for magic :}
    spacing = ttk.Label(second_frame,text="                                                                                                             Packages at your service.                                                                                                                         ")
    spacing.grid(row=150, column=0)
    spacing.bind("<MouseWheel>", lambda event: my_canvas.yview_scroll(-1*(event.delta//120), "units"))
    
    main.mainloop()

mainsplash.after(3000, mainwindow)
mainsplash.mainloop()

