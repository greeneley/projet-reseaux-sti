#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - guiframe.py
# 2017/12/18

import tkinter as tk

import watch
import guiwatch
from uiconst import *




class InfosFrame(tk.Frame): # Frame for statistic

    def __init__(self, master, **kwargs):
        super().__init__(master, bg= BACKGROUND_COLOR_1, **kwargs)

        frame= tk.Frame(self, bg= BACKGROUND_COLOR_1)
        frame.pack(expand= 1)
        rowCount= 0

        self.gCount=       tk.StringVar()

        tk.Label(frame, text= GEN_COUNT_LABEL, bg= BACKGROUND_COLOR_1, fg= FONT_COLOR_1).grid(row= rowCount, column= 0, sticky= 'w')
        tk.Label(frame,
            textvariable= self.gCount,
            bg= BACKGROUND_COLOR_1,
            fg= FONT_COLOR_1).grid(row= rowCount, column= 1, sticky= 'w')
        rowCount+= 1


        tk.Label(frame, bg= BACKGROUND_COLOR_1).grid(row= rowCount); rowCount+= 1
        tk.Label(frame, text= BEST_WATCH_LABEL, bg= BACKGROUND_COLOR_1, fg= FONT_COLOR_1).grid(row= rowCount, column= 0, columnspan= 2)
        rowCount+= 1


        self.score=     tk.StringVar()
        self.cost=      tk.StringVar()
        self.weight=    tk.StringVar()

        self.hand=      tk.StringVar()
        self.axis=      tk.StringVar()
        self.gear=      tk.StringVar()
        self.engine=    tk.StringVar()
        self.balance=   tk.StringVar()

        A= (self.score, self.cost, self.weight, self.hand, self.axis, self.gear, self.engine, self.balance)
        B= (SCORE_LABEL, COST_LABEL, WEIGHT_LABEL, HANDS_COUNT_LABEL, AXES_COUNT_LABEL, GEARWHEELS_COUNT_LABEL, ENGINES_COUNT_LABEL, BALANCES_COUNT_LABEL)
        for a, b in zip(A, B):
            tk.Label(frame, text= b, bg= BACKGROUND_COLOR_1, fg= FONT_COLOR_1).grid(row= rowCount, column= 0, sticky= 'w')
            tk.Label(frame,
                textvariable= a,
                bg= BACKGROUND_COLOR_1,
                fg= FONT_COLOR_1).grid(row= rowCount, column= 1, sticky= 'w')
            rowCount+= 1

    def update(self, gCount, bWatch):

        self.gCount.set("{:d}".format(gCount))

        self.score.set("{:.2f}".format(bWatch.score))
        self.cost.set("{:.2f}".format(bWatch.cost))
        self.weight.set("{:.2f}".format(bWatch.weight))

        self.hand.set("{:d}".format(bWatch.component_count('hand')))
        self.axis.set("{:d}".format(bWatch.component_count('axis')))
        self.gear.set("{:d}".format(bWatch.component_count('gear')))
        self.engine.set("{:d}".format(bWatch.component_count('engine')))
        self.balance.set("{:d}".format(bWatch.component_count('balance')))



class GraphFrame(tk.Frame): # Frame for statistic

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        #w, h= self.winfo_width(), self.winfo_height()
        self.plotlib=   False
        self.log=       (list(), list())

        try:

            import matplotlib
            matplotlib.use('TkAgg')
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure

            figure= Figure(figsize= (5,4), dpi=100)
            logPlot= figure.add_subplot(111)
            self.line,= logPlot.plot([], [])

            logPlot.set_title(GRAPH_TITLE)
            logPlot.set_xlabel(GRAPH_X_AXIS_CAPTION)
            logPlot.set_ylabel(GRAPH_Y_AXIS_CAPTION)

            self.plotCanvas= FigureCanvasTkAgg(figure, self)
            self.plotCanvas.show()
            self.plotCanvas.get_tk_widget().config(height= 0, width =0, bg= BACKGROUND_COLOR_1)
            self.plotCanvas.get_tk_widget().pack(fill= tk.BOTH, expand= 1)

            self.plotlib= True

        except ImportError:

            f= tk.Frame(self)
            f.pack_propagate(False)
            f.pack(fill= tk.BOTH, expand= 1)

            text= tk.Text(f, relief= tk.FLAT, bd= 30, bg= BACKGROUND_COLOR_1, highlightthickness= 0)
            text.pack(expand= tk.YES, fill= tk.BOTH)
            text.tag_config('default', foreground= FONT_COLOR_1)
            text.tag_config('link', foreground= FONT_COLOR_2, underline= 1)

            text.insert(tk.END, MSG_MATPLOTLIB, 'default')
            text.insert(tk.END, LINK_MATPLOTLIB, 'link')
            text.configure(state= 'disabled')



    def update(self, gCount, bWatch):

        if not self.plotlib: return
        if bWatch.score != -float('inf'):
            self.log[0].append(gCount)
            self.log[1].append(bWatch.score)

            self.line.set_data(*self.log)
            ax= self.plotCanvas.figure.axes[0]
            ax.set_xlim(self.log[0][0], self.log[0][-1])
            ax.set_ylim(min(self.log[1]), max(self.log[1])*1.5)
            self.plotCanvas.draw()




class CostFrame(tk.Frame): # Frame for statistic

    def __init__(self, master, **kwargs):
        super().__init__(master, bg= BACKGROUND_COLOR_1, bd= 5, **kwargs)

        tk.Label(self, text= PARAMS_MSG, bg= BACKGROUND_COLOR_1, fg= FONT_COLOR_1).pack()

        frame= tk.Frame(self, bg= BACKGROUND_COLOR_1)
        frame.pack(fill= tk.X, expand= 1)

        self.hand= tk.Entry(frame)
        self.hand.insert(tk.INSERT, str(watch.Hand.priceFactor))

        self.axis= tk.Entry(frame)
        self.axis.insert(tk.INSERT, str(watch.Axis.priceFactor))

        self.gear= tk.Entry(frame)
        self.gear.insert(tk.INSERT, str(watch.GearWheel.priceFactor))

        self.balance= tk.Entry(frame)
        self.balance.insert(tk.INSERT, str(watch.Balance.priceFactor))

        self.engine= tk.Entry(frame)
        self.engine.insert(tk.INSERT, str(watch.Engine.priceFactor))


        A= (self.hand, self.axis, self.gear, self.balance, self.engine)
        B= (HAND_LABEL, AXIS_LABEL, GEARWHEEL_LABEL, BALANCE_LABEL, ENGINE_LABEL)
        for a, b in zip(A, B):
            tk.Label(frame, text= b, bg= BACKGROUND_COLOR_1, fg= FONT_COLOR_1).pack()
            a.config(
                justify= tk.CENTER,
                bg= BACKGROUND_COLOR_2,
                fg= FONT_COLOR_1,
                highlightthickness= 0,
                bd= 1,
            )
            a.pack(fill= tk.X, expand= 1)


        self.text= tk.BooleanVar()
        tk.Checkbutton(
            frame,
            text= VIEW_INFOS_MSG,
            bg= BACKGROUND_COLOR_1,
            fg= FONT_COLOR_1,
            variable= self.text
        ).pack()


    def update(self):

        A= (self.hand, self.axis, self.gear, self.balance, self.engine)
        B= (watch.Hand, watch.Axis, watch.GearWheel, watch.Balance, watch.Engine)
        for a, b in zip(A, B):
            try:
                b.priceFactor=         float(a.get())
            except:
                pass

        guiwatch.VIEW_TEXT= bool(self.text.get())
