#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - cliaction.py
# 2017/01/06

import tkinter as tk

import watch
from uiconst import *
import guiwatch

def action(cli, cmd, *args):

    actions= {
        'start':    start_algo,
        'stop':     stop_algo,
        'resume':   resume_algo,
        'next':     next_algo,
        'reset':    reset_algo,
        'load':     load_pop,
        'wsave':    save_bWatch,
        'psave':    save_pop,
        'exit':     exit_app,
        'display':  display,
        'help':     help_app
    }

    if cmd in actions:
        actions[cmd](cli, *args) # call command action
    else:
        cli.insert_line(COMMAND_ERROR_404_MSG)



def start_algo(cli, *args):
    if not cli.algo.is_running():
        cli.insert_line(START_MSG)
        cli.algo.resume()
    elif not cli.algo.is_stopped():
        cli.insert_line(ALREADY_START_MSG)
    else:
        cli.insert_line(RESUME_MSG)
        cli.algo.resume()



def stop_algo(cli, *args):
    if not cli.algo.is_running():
        cli.insert_line(NOT_START_MSG)
    elif cli.algo.is_stopped():
        cli.insert_line(ALREADY_STOP_MSG)
    else:
        cli.insert_line(STOP_MSG)
        cli.algo.gGoal= 0
        cli.algo.stop()



def resume_algo(cli, *args):
    if not cli.algo.is_stopped():
        cli.insert_line(ALREADY_START_MSG)
    else:
        cli.insert_line(RESUME_MSG)
        cli.algo.resume()



def next_algo(cli, *args):
    if not cli.algo.is_running():
        start_algo(cli)

    if not args:
        cli.insert_line(RUN_TILL_BEST_MSG)
        cli.algo.resume()
        cli.algo.stopAtBest= True
    else:
        try:
            if len(args) == 1:
                cli.algo.gGoal= int(args[0])
            elif len(args) == 2 and args[0] == '+':
                cli.algo.gGoal= cli.algo.gCount + int(args[1])
            cli.insert_line(RUN_TILL_GEN_MSG.format(cli.algo.gGoal))
            cli.algo.stop()
        except:
            cli.insert_line(COMMAND_WRONG_MSG)



def reset_algo(cli, *args):
    cli.insert_line(RESET_MSG)
    cli.algo.reset()



def load_pop(cli, *args):
    openFiles= list()
    try:
        openFiles=[open(a, 'rb') for a in args]
    except:
        cli.insert_line(OPEN_FILE_ERROR_MSG)
        return

    try:
        pop= watch.open_pop(*openFiles)
    except:
        cli.insert_line(INVALID_FILE_ERROR_MSG)
        return

    cli.insert_line(POP_LOADED_GENETIC_STARTED_MSG)
    cli.algo.reset(pop)



def save_bWatch(cli, *args):
    if not cli.algo.alive:
        cli.insert_line(FIRST_START_GEN_ERROR_MSG)
    elif not cli.algo.is_stopped():
        cli.insert_line(STOP_FIRST_GEN_ERROR_MSG)
    elif len(args) != 1:
        cli.insert_line(COMMAND_WRONG_MSG)
    else:
        try:
            cli.insert_line(WATCH_SAVED_MSG)
            watch.save_watch(cli.algo.bWatch, open(args[0], 'wb'))
        except:
            cli.insert_line(OPEN_ONE_FILE_ERROR_MSG)



def save_pop(cli, *args):
    if not cli.algo.alive:
        cli.insert_line(FIRST_START_GEN_ERROR_MSG)
    elif not cli.algo.is_stopped():
        cli.insert_line(STOP_FIRST_GEN_ERROR_MSG)
    elif len(args) != 1:
        cli.insert_line(COMMAND_WRONG_MSG)
    else:
        try:
            watch.save_pop(cli.algo.pop, open(args[0], 'wb'))
            cli.insert_line(POP_SAVED_MSG)
        except:
            cli.insert_line(OPEN_ONE_FILE_ERROR_MSG)



def exit_app(cli, *args):
    cli.algo.end()
    cli.alive= False

def help_app(cli, *arg):
    if not cli.algo.is_stopped():
        cli.insert_line(STOP_FIRST_GEN_ERROR_MSG)
    else:
        cli.watchScr.clear()
        cli.watchScr.border()

        helps= {
            'start':    HELP_START,
            'stop':     HELP_STOP,
            'resume':   HELP_RESUME,
            'next':     HELP_NEXT,
            'next X':   HELP_NEXT_X,
            'next + X': HELP_NEXT_PLUS_X,
            'reset':    HELP_RESET,
            'load':     HELP_LOAD,
            'wsave':    HELP_WSAVE,
            'psave':    HELP_PSAVE,
            'exit':     HELP_EXIT,
            'display':  HELP_EXIT,
        }

        y= 1
        cli.watchScr.move(1, 1)
        for h in helps:
            cli.watchScr.addstr("{:10}: {}".format(h, helps[h]))
            y+= 1
            cli.watchScr.move(y, 1)

        cli.watchScr.refresh()


def display(cli, *args):
    if not cli.algo.alive:
        cli.insert_line(FIRST_START_GEN_ERROR_MSG)
    elif not cli.algo.is_stopped():
        cli.insert_line(STOP_FIRST_GEN_ERROR_MSG)
    else:
        cli.insert_line(DISPLAY_BEST_WATCH_MSG)
        guiwatch.display_watch(cli.algo.bWatch)
