#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - gui.py (graphic user interface)
# 2017/11/04

import queue
from functools import partial

import tkinter as tk

import watch
from guiaction  import *
from guiwatch   import *
from guiwindow  import *
from guiframe   import *
from uiconst    import *

def gui():
    Gui().main()


class Gui(object):
    def __init__(self):
        super().__init__()

    def main(self):
        self.alive= True
        self.bWatch= watch.Watch()

        self.window= tk.Tk()
        self.window.configure(background= BACKGROUND_COLOR_1)

        self.window.withdraw()

        #Launch the splash window in order to let the programm load itself
        splash= Splash(self.window)

        self.window.title(MAIN_WINDOW_NAME)
        img= tk.PhotoImage(file= ICON_PATH)
        self.window.tk.call('wm', 'iconphoto', self.window._w, img)
        self.window.protocol('WM_DELETE_WINDOW', partial(exit_app, self))

        screenWidth, screenHeight=  self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        windowWidth, windowHeight=  map(int, (screenWidth*0.8, screenHeight*0.8))


        #window.rowconfigure(0, minsize= int(windowHeight*0.0), weight=1)
        self.window.rowconfigure(1, minsize= int(windowHeight*0.5), weight= 1)
        self.window.rowconfigure(2, minsize= int(windowHeight*0.5), weight= 1)
        #window.rowconfigure(3, minsize= int(windowHeight*0.02), weight=1)

        self.window.columnconfigure(0, minsize= int(windowWidth*0.3), weight= 1)
        self.window.columnconfigure(1, minsize= int(windowWidth*0.6), weight= 1)
        self.window.columnconfigure(2, minsize= int(windowWidth*0.1), weight= 1)


        top= tk.Frame(self.window, relief= tk.FLAT, background= BACKGROUND_COLOR_1)
        toolbar= tk.Frame(top, bd= 1, relief= tk.FLAT, background= BACKGROUND_COLOR_1)

        #Initialize the availability of each button at the start of the programm
        self.startButton=    tk.Button(toolbar)
        self.nextButton=     tk.Button(toolbar)
        self.stopButton=     tk.Button(toolbar, state= 'disabled')
        self.resetButton=    tk.Button(toolbar, state= 'disabled')
        self.wsaveButton=    tk.Button(toolbar, state= 'disabled')
        self.popsaveButton=  tk.Button(toolbar, state= 'disabled')
        self.poploadButton=  tk.Button(toolbar)
        self.wloadButton=    tk.Button(toolbar)
        self.helpButton=     tk.Button(toolbar)

        #Connect each button with his icon and what it does
        A= (
            (self.startButton,      START_ICON_PATH,    start_algo),
            (self.nextButton,       NEXT_ICON_PATH,     next_algo),
            (self.stopButton,       STOP_ICON_PATH,     stop_algo),
            (self.resetButton,      RESET_ICON_PATH,   reset_algo),
            (self.wsaveButton,      WSAVE_ICON_PATH,    save_watch),
            (self.popsaveButton,    POPSAVE_ICON_PATH,  save_pop),
            (self.poploadButton,    POPLOAD_ICON_PATH,  load_pop),
            (self.wloadButton,      WLOAD_ICON_PATH,    load_watch),
            (self.helpButton,       HELP_ICON_PATH,     help_menu)
        )
        for a, b, c in A:
            img= tk.PhotoImage(file= b)
            a.config(
                image=              img,
                command=            partial(c, self),
                relief=             tk.FLAT,
                bg=                 BACKGROUND_COLOR_1,
                bd=                 2,
                highlightthickness= 0,
                activebackground=   BACKGROUND_COLOR_2
            )
            a.image= img
            a.pack(side= tk.LEFT)

        #Load each part of the interface
        self.costFrame=      CostFrame(self.window)
        self.watchCanvas=    WatchCanvas(self.window)
        self.infosFrame=     InfosFrame(self.window)
        self.graphFrame=     GraphFrame(self.window)

        top.grid(row= 0, column= 0, columnspan= 1, sticky= 'nesw')
        toolbar.pack()

        self.costFrame.grid(row= 1, column= 2, rowspan=2, sticky= 'nesw')
        self.watchCanvas.grid(row= 1, column= 1, rowspan= 2, sticky= 'nesw')
        self.infosFrame.grid(row= 1, column= 0, sticky= 'nesw')
        self.graphFrame.grid(row= 2, column= 0, sticky= 'nesw')

        self.algo= watch.EvAlgo()
        self.algo.start()


        self.watchCanvas.set_watch(watch.Watch())
        self.infosFrame.update(0, self.bWatch)
        self.graphFrame.update(0, self.bWatch)
        self.costFrame.update()
        self.window.update_idletasks()
        self.window.update()
        
        #Kill the splash screen and then show the main part of the programm
        splash.destroy()
        self.window.deiconify()
        self.main_loop()
        self.window.destroy()

    #main loop that update itself when a better watch is created
    def main_loop(self):
        while self.alive:

            if not self.algo.datasQueue.empty():
                n, w= self.algo.datasQueue.get_nowait()
                if w != None:
                    self.bWatch= w.copy()
                    print(NUMBER_OF_GEN_MSG.format(n))
                    print(self.bWatch)
                    self.watchCanvas.set_watch(self.bWatch)
                    if self.algo.is_stopped(): stop_algo(self)

                self.infosFrame.update(n, self.bWatch)
                self.graphFrame.update(n, self.bWatch)


            self.costFrame.update()
            self.watchCanvas.animation()
            self.window.update_idletasks()
            self.window.update()


if __name__ == "__main__":
    gui()
