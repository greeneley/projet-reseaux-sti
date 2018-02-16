#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - cli.py (command line interface)
# 2017/01/05

import curses

import watch

import cliaction
from uiconst import *


HIGHT_MIN= 32
WIDTH_MIN= 100


def cli():
    try:
        curses.wrapper(Cli().main)
    except Exception as e:
        print(e)

class Cli(object):
    def __init__(self):
        super().__init__()


    def main(self, stdscr):
        self.alive=         True

        self.cmdLog=        list()
        self.logIndex=      0
        self.inputBuffer=   str()
        self.inputMinX=     0

        self.algo= watch.EvAlgo()
        self.algo.start()
        self.bWatch= watch.Watch()

        self.inputScr= stdscr # screen for input, also standart screen
        curses.noecho() # be able to read keys and only display them under certain circumstances
        curses.cbreak() # react to keys instantly, without requiring the Enter key to be pressed
        self.inputScr.keypad(True) # enable keypad mode
        self.inputScr.timeout(16)
        self.inputScr.clear()
        self.inputScr.refresh()

        self.scrSize= self.inputScr.getmaxyx()
        if self.scrSize[0] < HIGHT_MIN or self.scrSize[1] < WIDTH_MIN:#check if the window is big enough for the application
            raise Exception(CONSOLE_TOO_SMALL_ERROR_MSG)

        self.progSize=  3, 100
        self.progPos=   0, 0

        self.inputSize= 1, self.scrSize[1]
        self.inputPos=  self.scrSize[0]-1, 0
        self.cmdSize=   3, self.scrSize[1]
        self.cmdPos=    self.inputPos[0] - self.cmdSize[0], 0

        self.genSize=   self.cmdPos[0] - self.progSize[0], 25
        self.genPos=    self.progSize[0], 0
        self.watchSize= self.genSize[0], 75
        self.watchPos=  self.genPos[0], self.genPos[1] + self.genSize[1]


        self.progScr= curses.newwin(*(self.progSize + self.progPos)) # screen for genetic algorithme infos
        self.progScr.move(1, 1)
        self.progScr.addstr(("{:^{width}}").format(PROG_NAME, width= str(self.progSize[1]-2)))
        self.progScr.border()
        self.progScr.refresh()

        self.genScr= curses.newwin(*(self.genSize + self.genPos)) # screen for genetic algorithme infos
        self.genScr.move(1, 1)
        self.genScr.border()
        self.genScr.refresh()

        self.watchScr= curses.newwin(*(self.watchSize + self.watchPos)) # screen for genetic algorithme infos
        self.watchScr.move(1, 1)
        self.watchScr.border()
        self.watchScr.refresh()

        self.cmdScr= curses.newwin(*(self.cmdSize + self.cmdPos)) # sreen for command infos
        self.cmdScr.move(self.cmdSize[0]-1, 1)

        self.inputScr.move(self.scrSize[0]-1, 0)
        self.clear_input()

        self.main_loop()
        curses.endwin()


    def main_loop(self):
        while self.alive:
            self.key_action(self.inputScr.getch()) # get user input key by key
            if not self.algo.datasQueue.empty():
                n, w= self.algo.datasQueue.get_nowait()
                if w != None:
                    self.bWatch= w.copy()
                    if self.algo.is_stopped(): self.insert_line(STOP_MSG)

                self.genScr.clear()
                self.watchScr.clear()
                self.genScr.border()
                self.watchScr.border()


                self.genScr.move(1, 1)
                self.genScr.addstr(GEN_COUNT_LABEL + str(n))

                self.genScr.move(3, 1)
                self.genScr.addstr(("{:^{width}}").format(BEST_WATCH_LABEL, width= str(self.genSize[1]-2)))

                self.genScr.move(4, 1)
                self.genScr.addstr(SCORE_LABEL + "{:>8.8}".format(self.bWatch.score))

                self.genScr.move(5, 1)
                self.genScr.addstr(WEIGHT_LABEL + "{:>8.8}".format(self.bWatch.weight))

                self.genScr.move(6, 1)
                self.genScr.addstr(COST_LABEL + "{:>8.8}".format(self.bWatch.cost))

                self.genScr.move(7, 1)
                self.genScr.addstr(COMPOENENTS_COUNT_LABEL + str(len(self.bWatch)))

                y= 1
                self.watchScr.move(1, 1)
                self.watchScr.addstr("{:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8}".format("ID", "Type", "Feature", "Speed", "Energy", "Time", "Weight", "Cost"))
                for i, component in enumerate(self.bWatch): component._ID= i
                for component in self.bWatch:
                    y+= 1
                    if y > self.watchSize[0]: break
                    self.watchScr.move(y, 1)
                    self.watchScr.addstr(str(component))


                self.genScr.refresh()
                self.watchScr.refresh()




    def key_action(self, key):

        keyActions= {
            curses.KEY_ENTER:       self.input_command,
            ord('\r'):              self.input_command,
            ord('\n'):              self.input_command,
            curses.KEY_BACKSPACE:   self.delete_char,
            ord('\b'):              self.delete_char,
            curses.KEY_LEFT:        self.move_left,
            curses.KEY_RIGHT:       self.move_right,
            curses.KEY_UP:          self.move_up,
            curses.KEY_DOWN:        self.move_down,
        }

        if key in keyActions:
            keyActions[key]() # call key action
        elif key < 0:
            pass
        else: # default action
            self.add_char(key)



    def clear_input(self):
        self.inputScr.deleteln() # clear user input screen
        self.inputBuffer= str() # clear buffer
        self.inputScr.move(self.inputPos[0], 0)
        self.inputScr.addstr(" > ")
        y, self.inputMinX= self.inputScr.getyx()
        self.inputScr.refresh()

    def input_command(self): # USER INPUT A COMMAND
        cmd= self.inputBuffer.split()
        cmd= ["xxx"] if not cmd else cmd
        cliaction.action(self, cmd[0], *cmd[1:])
        self.cmdLog.insert(0, self.inputBuffer)
        self.logIndex= 0
        self.clear_input()

    def add_char(self, key):
        y, x= self.inputScr.getyx() # get cursor position
        if x < self.scrSize[1]-1:
            i= x-self.inputMinX
            self.inputBuffer= self.inputBuffer[:i] + chr(key) + self.inputBuffer[i:] # insert character in buffer
            self.inputScr.insch(key) # insert character, cusor doesn't move
            self.inputScr.move(y, x + 1) # move the cursor
            self.inputScr.refresh()

    def delete_char(self):
        y, x= self.inputScr.getyx() # get cursor position
        if self.inputMinX < x:
            i= x-self.inputMinX
            self.inputBuffer= self.inputBuffer[:i-1] + self.inputBuffer[i:] # insert character in buffer
            self.inputScr.delch(y, x-1) # delete character before the cursor, move the cursor authomaticaly
            self.inputScr.refresh()

    def move_left(self):
        y, x= self.inputScr.getyx() # get cursor position
        if self.inputMinX < x:
            self.inputScr.move(y, x-1)

    def move_right(self):
        y, x= self.inputScr.getyx() # get cursor position
        if x < self.scrSize[1] and x-self.inputMinX < len(self.inputBuffer):
            self.inputScr.move(y, x+1)

    def move_up(self):
        l= len(self.cmdLog)
        if self.logIndex < l:
            self.clear_input()
            self.logIndex+= 1
            self.inputBuffer= self.cmdLog[self.logIndex-1]
            self.inputScr.insstr(self.inputBuffer)

    def move_down(self):
        if self.logIndex > 1:
            self.clear_input()
            self.logIndex-= 1
            self.inputBuffer= self.cmdLog[self.logIndex-1]
            self.inputScr.insstr(self.inputBuffer)


    def insert_line(self, line):
        y, x= self.cmdScr.getyx()
        self.cmdScr.move(0, 0)
        self.cmdScr.insdelln(-1)
        self.cmdScr.move(y, 1)
        self.cmdScr.insstr(line)
        self.cmdScr.refresh()



if __name__ == "__main__":
    cli()
