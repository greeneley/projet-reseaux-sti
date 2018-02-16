#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - uiconst.py (user interface contants)
# 2017/12/20


PROG_NAME=                     "Mon(s)tre by TEAMJBZZ"
PROG_DESCRIPTION=               """ {} is a programm - using an evolutionary algorithm - to generate a
                                population of watch in order to create the best one. In graphics mode,
	                            you can visualise in real time the best watch generated so far and a
	                            graph showing the best score obtained my the actual generation

                                The programm is launched in graphics interface by default.
                                """.format(PROG_NAME)



PROG_EPILOG=                    """
                                If you are a competent programmer and are willing to spend time on our
                                programm in order to improve it.
                                Please contact us at iohann.bucaille@insa-cvl.fr
                                """

# COMMAND ARGUMENT
DISPLAY_WATCH_ARG=              ('--display', '-d', '/d')
RUN_ARG=                        ('--run', '-r', '/r')
CONSOLE_ARG=                    ('--console', '-c', '/c')
STOP_AT_BEST_ARG=               ('--stopatbest', '-s', '/s')

# COMMAND HELP
RUN_HELP=                       "Run the programm in hard mode (for developpement)"
STOP_AT_BEST_HELP=              "Stop the algorithm at each best watch (for hard mode)"
DISPLAY_WATCH_HELP=             "Display the watch in the file. Doesn't run the algorithm."
CONSOLE_HELP=                   "Run the console line interface"


# METAVAR
WATCH_FILE_METAVAR=             "WATCH_FILE"

# GUI COLORS
BACKGROUND_COLOR_1=             "#21252B"
BACKGROUND_COLOR_2=             "#282C34"

FONT_COLOR_1=                   "#ABB2BF"
FONT_COLOR_2=                   "#61AFEF"

HAND_COLORS=                    ("#B39DDB", "#C5E1A5", "#9FA8DA", "#90CAF9", "#CE93D8", "#F48FB1", "#EF9A9A", "#80CBC4", "#E6EE9C", "#A5D6A7")
AXIS_COLOR=                     "#E06C75"
GEAR_COLOR=                     "#98C36E"
ENGINE_COLOR=                   "#D19A66"
BALANCE_COLOR=                  "#61AFEF"
DEBUG_COLOR=                    "#EE22B0"

# RSC PATH
HELP_IMG_PATH=                  r"rsc/help.png"
SPLASH_SCREEN_PATH=             r"rsc/monstres.png"
ICON_PATH=                      r"rsc/icon.png"
START_ICON_PATH=                r"rsc/start_icon.png"
NEXT_ICON_PATH=                 r"rsc/next_icon.png"
RESET_ICON_PATH=                r"rsc/reset_icon.png"
STOP_ICON_PATH=                 r"rsc/stop_icon.png"
WSAVE_ICON_PATH=                r"rsc/save_icon.png"
POPSAVE_ICON_PATH=              r"rsc/saveall_icon.png"
POPLOAD_ICON_PATH=              r"rsc/openall_icon.png"
WLOAD_ICON_PATH=                r"rsc/open_icon.png"
HELP_ICON_PATH=                 r"rsc/help_icon.png"

# WINDOWS NAME
MAIN_WINDOW_NAME=               PROG_NAME
SAVE_WATCH_WINDOW_NAME=         "Save watch"
SAVE_POPULATION_WINDOW_NAME=    "Save population"
OPEN_WATCH_WINDOW_NAME=         "Open watch"
OPEN_POPULATION_WINDOW_NAME=    "Open population"
HELP_WINDOW_NAME=               "Option"

RUN_MENU_NAME=                  "Run"
RUN_POPULATION_MENU_NAME=       "Run from population"

OPEN_WATCH_MENU_NAME=           "Open watch"
HELP_MENU_NAME=                 "Help"
CREDIT_MENU_NAME=               "Credits"

# FILE NAME
WATCH_FILE_NAME=                ("Watch file", "*.watch")
ALL_FILE_NAME=                  ("all files", "*.*")
POP_FILE_NAME=                  ("Population file", "*.pop")


# USER MSG
PARAMS_MSG=                     "" #No message inserted
VIEW_INFOS_MSG=                 "View hand infos"

GRAPH_TITLE=                    ""
GRAPH_X_AXIS_CAPTION=           "Number of generation"
GRAPH_Y_AXIS_CAPTION=           "Average fitness"

MSG_MATPLOTLIB=                 "To view the graph, you must install the Matplotlib plotting library.\npython -m pip install matplotlib\n"
LINK_MATPLOTLIB=                "https://matplotlib.org/"

COMMAND_ERROR_404_MSG=          "Command not found (help)"
COMMAND_WRONG_MSG=              "Wrong use of command"
OPEN_FILE_ERROR_MSG=            "Cannot open one or more files"
OPEN_ONE_FILE_ERROR_MSG=        "Cannot open file"
INVALID_FILE_ERROR_MSG=         "One or more files are invalid"
FIRST_START_GEN_ERROR_MSG=      "Start the evolutionary algorithm first (start)"
STOP_FIRST_GEN_ERROR_MSG=       "Stop the evolutionary algorithm first (stop)"
CONSOLE_TOO_SMALL_ERROR_MSG=    "Console too small for the appliation"

CONSOLE_NOT_SUPPORTED=          "Console line interface not supported"
GRAPHIC_NOT_SUPPORTED=          "Graphic user interface not supported"

START_MSG=                      "Algorithm started"
NOT_START_MSG=                  "Algorithm not started"
ALREADY_START_MSG=              "Algorithm already started"
RESUME_MSG=                     "Algorithm resumed"
STOP_MSG=                       "Algorithm stopped"
ALREADY_STOP_MSG=               "Algorithm already stopped"
A_WAY_TO_IMPROVE_LIFE_MSG=      "A way to improve life is easter egg"
RESET_MSG=                      "Algorithm reset"
END_MSG=                        "Algorithm ended"

WATCH_SAVED_MSG=                "Watch saved"
DISPLAY_BEST_WATCH_MSG=         "Display best watch"


POP_SAVED_MSG=                  "population saved"

RUN_TILL_BEST_MSG=              "Algorithm run until new best watch"
RUN_TILL_GEN_MSG=               "Algorithm running until generation {}"
POP_LOADED_GENETIC_STARTED_MSG= "Population loaded and evolutionary algorithm started"

NUMBER_OF_GEN_MSG=              "Generation: {:d}"

# GENERATION CARASTERISTICS
GEN_COUNT_LABEL=                "Generation count: "
BEST_WATCH_LABEL=               "BEST WATCH"
SCORE_LABEL=                    "Score: "
COST_LABEL=                     "Cost: "
WEIGHT_LABEL=                   "Weight: "
COMPOENENTS_COUNT_LABEL=        "Components count: "
HANDS_COUNT_LABEL=              "Hands count: "
AXES_COUNT_LABEL=               "Axis count: "
GEARWHEELS_COUNT_LABEL=         "Gearwheels count: "
ENGINES_COUNT_LABEL=            "Engines count: "
BALANCES_COUNT_LABEL=           "Balances count: "

HAND_LABEL=                     "Hand"
AXIS_LABEL=                     "Axis"
GEARWHEEL_LABEL=                "Gearwheel"
ENGINE_LABEL=                   "Engine"
BALANCE_LABEL=                  "Balance"


# HELP
HELP_START=                     "Start the evolutionary algorithm"
HELP_STOP=                      "Stop the evolutionary algorithm"
HELP_RESUME=                    "Resume the evolutionary algorithm"
HELP_NEXT=                      "Run the evolutionary algorithm until the next best watch"
HELP_NEXT_X=                    "Run the evolutionary algorithm until generation X"
HELP_NEXT_PLUS_X=               "Run the evolutionary algorithm for X more generations"
HELP_RESET=                     "Reset the evolutionary algorithm"
HELP_LOAD=                      "Load a population, if you load many poulations it mixes them"
HELP_WSAVE=                     "Save the current best watch"
HELP_PSAVE=                     "Save the current population"
HELP_EXIT=                      "Exit the appliation"
HELP_DISPLAY=                   "Display the current best watch"
