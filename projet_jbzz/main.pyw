#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - main.py
# 2017/11/15

import threading
import argparse

import watch

from uiconst import *

"""
parser.add_argument(
    *DISPLAY_WATCH_ARG,
    #action=
    #nargs=
    #const=
    #default=
    #type=
    #choices=
    #required=
    #help=
    #metavar=
    #dest=
)
"""

def main():

    parser= argparse.ArgumentParser(
        prog=           PROG_NAME,
        description=    PROG_DESCRIPTION,
        epilog=         PROG_EPILOG,
        prefix_chars=   "-/"
    )

    parser.add_argument(
        *RUN_ARG,
        action=     'store_true',
        help=       RUN_HELP,
        dest=       'run'
    )

    parser.add_argument(
        *STOP_AT_BEST_ARG,
        action=     'store_true',
        help=       STOP_AT_BEST_HELP,
        dest=       'stopatbest'
    )

    parser.add_argument(
        *CONSOLE_ARG,
        action=     'store_true',
        help=       CONSOLE_HELP,
        dest=       'console'
    )

    parser.add_argument(
        *DISPLAY_WATCH_ARG,
        default=    False,
        type=       str,
        help=       DISPLAY_WATCH_HELP,
        metavar=    WATCH_FILE_METAVAR,
        dest=       'displayWatch'
    )

    args= parser.parse_args()
    #print(args)

    if args.console:
        try:
            from cli import cli
        except:
            print(CONSOLE_NOT_SUPPORTED)
            exit()

        cli()   # command line interface

    elif args.run:
        algo= watch.EvAlgo()
        watch.evalgo.PRINT_INFO= True
        watch.evalgo.STOP_AT_BEST= args.stopatbest
        algo.start()

        while True:
            if not algo.datasQueue.empty():
                n, w= algo.datasQueue.get_nowait()
                print(n)

        algo.end()

    elif args.displayWatch:
        try:
            from guiwatch import display_watch
        except:
            print(GRAPHIC_NOT_SUPPORTED)
            exit()

        w= watch.open_watch(open(args.displayWatch, 'rb'))
        print(w)
        display_watch(w)

    else:
        #try:
        from gui import gui
        #except:
        #    print(GRAPHIC_NOT_SUPPORTED)
        #    exit()

        gui()       # graphic user interface



if __name__ == "__main__":
    main()
