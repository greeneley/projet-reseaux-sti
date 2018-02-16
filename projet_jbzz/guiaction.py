#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - guiaction.py
# 2017/11/04

from tkinter import filedialog

import watch
from guiwatch   import *
from guiwindow  import *
from uiconst    import *

#Kill the algorithm when you click on the red cross
def exit_app(gui):
    gui.algo.end()
    gui.alive= False


#Determine available buttons while you click on the Start button and then start the algorithm if he's not already running
def start_algo(gui):
    gui.startButton.config(state=   'disabled')
    gui.nextButton.config(state=    'disabled')
    gui.stopButton.config(state=    'normal')
    gui.resetButton.config(state=   'normal')
    gui.wsaveButton.config(state=   'disabled')
    gui.popsaveButton.config(state= 'disabled')
    gui.poploadButton.config(state= 'disabled')
    gui.wloadButton.config(state=   'disabled')

    if not gui.algo.alive:
        print(START_MSG)
    else:
        print(RESUME_MSG)

    gui.algo.resume()


#Determine available buttons while you click on the Stop button and stop the algorithm
def stop_algo(gui):
    gui.startButton.config(state=   'normal')
    gui.nextButton.config(state=    'normal')
    gui.stopButton.config(state=    'disabled')
    gui.resetButton.config(state=   'normal')
    gui.wsaveButton.config(state=   'normal')
    gui.popsaveButton.config(state= 'normal')
    gui.poploadButton.config(state= 'normal')
    gui.wloadButton.config(state=   'normal')

    print(STOP_MSG)
    gui.algo.stop()

#Start the algorithm until you find a better watch
def next_algo(gui):
    start_algo(gui)
    gui.algo.stopAtBest= True

#Stop the algorithm, clean the population, and start it again
def reset_algo(gui):
    print(RESET_MSG)
    gui.bWatch= watch.Watch()
    gui.graphFrame.log= (list(), list())
    gui.algo.reset()

#Save the actual best watch
def save_watch(gui):
    fileName= filedialog.asksaveasfilename(
        parent= gui.window,
        title= SAVE_WATCH_WINDOW_NAME,
        filetypes= (WATCH_FILE_NAME,ALL_FILE_NAME)
    )
    with open(fileName, 'wb') as openFile:
        watch.save_watch(gui.algo.bWatch, openFile)

#Save the population
def save_pop(gui):
    fileName= filedialog.asksaveasfilename(
        parent= gui.window,
        title= SAVE_POPULATION_WINDOW_NAME,
        filetypes= (POP_FILE_NAME,ALL_FILE_NAME)
    )
    with open(fileName, 'wb') as openFile:
        watch.save_pop(gui.algo.pop, openFile)

#Load a population from an existing file
def load_pop(gui):
    openFile= filedialog.askopenfile(
        parent= gui.window,
        mode= 'rb',
        title= OPEN_POPULATION_WINDOW_NAME,
        filetypes= (POP_FILE_NAME,ALL_FILE_NAME)
    )

    pop= watch.open_pop(openFile)
    openFile.close()
    gui.bWatch= watch.Watch()
    gui.algo.reset(pop)



#Load a watch from an existing file
def load_watch(gui):

    openFile= filedialog.askopenfile(
        parent= gui.window,
        mode= 'rb',
        title= OPEN_WATCH_WINDOW_NAME,
        filetypes= (WATCH_FILE_NAME,ALL_FILE_NAME)
    )

    w= watch.open_watch(openFile)
    openFile.close()
    print(w)
    display_watch(w)

#Open the help window
def help_menu(gui):
    o= helpWindow(gui.window)
