#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - guiwindow.py
# 2017/01/04

import tkinter as tk


from uiconst import *

#class of the loading/splash screen that appear at the start of the programm

class Splash(tk.Toplevel):

    def __init__(self, master, **kwargs):
        super().__init__(master, bg= BACKGROUND_COLOR_1)
        #self.title("Splash")

        scrnWt= master.winfo_screenwidth()
        scrnHt= master.winfo_screenheight()

        img= tk.PhotoImage(file= SPLASH_SCREEN_PATH)
        imgWt= img.width()
        imgHt= img.height()

        imgXPos= (scrnWt/2) - (imgWt/2)
        imgYPos= (scrnHt/2) - (imgHt/2)

        # Create the splash screen
        self.overrideredirect(1)
        self.geometry('+%d+%d' % (imgXPos, imgYPos))

        l= tk.Label(self, image= img, cursor= 'watch', bg= BACKGROUND_COLOR_1)
        l.pack()
        self.update_idletasks()
        self.update()

#class of the help window

class helpWindow(tk.Toplevel):

    def __init__(self, master, **kwargs):
        super().__init__(master, bg= BACKGROUND_COLOR_1)

        alive= True
        def exit_display():
            nonlocal alive
            alive= False
            self.destroy()

        self.protocol('WM_DELETE_WINDOW', exit_display)
        self.title(HELP_WINDOW_NAME)
        self.resizable(False, False)

        img= tk.PhotoImage(file= HELP_IMG_PATH)
        l= tk.Label(self, image= img, bg= BACKGROUND_COLOR_1)
        l.pack(fill= tk.BOTH, expand= True)

        while alive:
            self.update_idletasks()
            self.update()
