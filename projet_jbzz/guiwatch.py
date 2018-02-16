#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - guiwatch.py
# 2017/10/13

import time
import math
import tkinter as tk

import watch
from uiconst import *



# DEBUG
VIEW_BOX=   False #display the box
VIEW_TEXT=  False #display info text (upper left oof the canvas)

#allow vectorial calculation
class Vec2(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def get_data(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Vec2: ({0}, {1})".format(self.x, self.y)


#defined points for a hand
def _hand_points(hand, center):

    a= hand.radius/4
    o= 0.4*a

    return  [
        center,
        center - Vec2(o, a),
        center - Vec2(0, hand.radius),
        center + Vec2(o, -a),
        center
    ]

#defined point for a gear
def _gear_points(gearWheel, center):

    teethCount= gearWheel.teethCount
    teethPitch= watch.GearWheel.teethPitch
    R= gearWheel.radius
    r= R - watch.GearWheel.teethHeight
    angle= -math.pi/2

    points= [center]
    for _ in range(teethCount):

        points.append(center + Vec2(r*math.cos(angle), r*math.sin(angle)))
        angle+= 2*teethPitch/(R*3)
        points.append(center + Vec2(R*math.cos(angle), R*math.sin(angle)))
        angle+= 2*teethPitch/(R*3)
        points.append(center + Vec2(R*math.cos(angle), R*math.sin(angle)))
        angle+= 2*teethPitch/(R*3)

    points.append(center + Vec2(r*math.cos(angle), r*math.sin(angle)))
    return points

#define points for circle (use in axis , balance , engine)
def _circle_points(comp, center):

    r= comp.radius

    angle= 0
    points= []
    for _ in range(360):
        points.append(center + Vec2(r*math.cos(angle), r*math.sin(angle)))
        angle+= math.pi/180

    points.append(center + Vec2(r*math.cos(angle), r*math.sin(angle)))
    return points



POINTS_FUNC_DICT= {
    'hand':     _hand_points,
    'axis':     _circle_points,
    'gear':     _gear_points,
    'engine':   _circle_points,
    'balance':  _circle_points
}



#create the frame where the watch can be place
class WatchCanvas(tk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, bg= BACKGROUND_COLOR_2, highlightthickness= 0, **kwargs)

        self.canvas= tk.Canvas(self, bg= BACKGROUND_COLOR_2, highlightthickness= 0)
        self.canvas.pack(side= tk.LEFT, fill= tk.BOTH, expand= 1)

        self.t0= .0
        self.texts= list()
        self.shapes= list()
        
        #create event for mouse clicking and drag
        self.canvas.bind('<ButtonPress-1>', self.move_start)
        self.canvas.bind('<B1-Motion>', self.move_move)

    #clic detection
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    #drag and drop detection
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain= 1)

    #show the watch in the canvas
    def set_watch(self, w):
        self.t0= time.clock()
        self.canvas.delete('all')
        self.texts= list()
        self.texts.append(self.canvas.create_text(
            (0, 0),
            fill= FONT_COLOR_1,
            anchor= 'nw',
            text= "{:^8}   {:^8}   {:^8}".format("Speed", "Energy", "Time")
        ))
        self.shapes= list()
        self._create_watch(w)

    #create a watch
    def _create_watch(self, w):
        DELTA= 20

        self.canvas.update()
        offset= Vec2(self.canvas.winfo_width()/2, 0)

        oldBox= [0, 0, 0, 0]
        for sub in w.subwatches:

            box= [0, 0, 0, 0] # nesw
            parents= set()
            compANDcenters= list()

            def branch(comp, center, angle= None):
                nonlocal w, box, parents, compANDcenters

                compANDcenters.append((comp, center))

                r= comp.radius
                box[0]= min(box[0], center.y - r)
                box[1]= max(box[1], center.x + r)
                box[2]= max(box[2], center.y + r)
                box[3]= min(box[3], center.x - r)

                n= sum(1 for c in w[comp] if isinstance(c, (watch.GearWheel, watch.Engine, watch.Balance)))
                a= 0 if not n else 2*math.pi/n
                angle= 0 if angle == None else angle + a - math.pi

                #print(comp, com, w[comp], w[comp].difference(components))

                comps= w[comp].difference(parents)
                parents.update(comps)
                for c in comps:

                    newCenter= center
                    if isinstance(comp, (watch.GearWheel, watch.Balance)) and isinstance(c, (watch.GearWheel, watch.Balance, watch.Engine)):

                        r= comp.radius + c.radius
                        newCenter= center + Vec2(r*math.cos(angle), r*math.sin(angle))
                        angle+= a

                    branch(c, newCenter, angle-a)

            parents.add(sub.components[0])
            branch(sub.components[0], Vec2(0, 0))
            offset.y= offset.y + abs(box[0] - box[2])/2 + abs(oldBox[0] - oldBox[2])/2 + DELTA
            oldBox= list(box)

            moveVec= offset - Vec2((box[1]+box[3])/2, (box[0]+box[2])/2)
            for comp, center in compANDcenters:
                self._create_component(comp, center + moveVec)

            #####
            if VIEW_BOX:
                vbox= [Vec2(box[3], box[0]), Vec2(box[1], box[0]), Vec2(box[1], box[2]), Vec2(box[3], box[2]), Vec2(box[3], box[0])]
                for i, v in enumerate(vbox):
                    vbox[i]= v + moveVec
                self.canvas.create_line([v.get_data() for v in vbox], fill= DEBUG_COLOR)
                points= [p.get_data() for p in _circle_points(watch.Axis(), offset)]
                self.canvas.create_line(points, fill= DEBUG_COLOR)
            #####

    #create watch components
    def _create_component(self, comp, center):

        widthDict= {
            'hand':     2,
            'axis':     2,
            'gear':     1,
            'engine':   3,
            'balance':  3
        }

        colorsDict= {
            'hand':     HAND_COLORS[(len(self.texts) - 1)%len(HAND_COLORS)],
            'axis':     AXIS_COLOR,
            'gear':     GEAR_COLOR,
            'engine':   ENGINE_COLOR,
            'balance':  BALANCE_COLOR
        }

        t= comp.type
        if t == 'hand':
            bbox= self.canvas.bbox(self.texts[0])
            height= bbox[3]-bbox[1]
            self.texts.append(self.canvas.create_text(
                (0, len(self.texts)*height),
                fill=colorsDict[t],
                anchor= 'nw',
                text= "{:>8.8}   {:>8.8}   {:>8.8}".format(str(comp.speed), str(comp.energy), str(comp.calcul_duration()))
            ))

        points= [p.get_data() for p in POINTS_FUNC_DICT[t](comp, center)]
        shape= self.canvas.create_line(points, fill= colorsDict[t], width= widthDict[t])
        self.shapes.append((comp, shape, center))

    #animates watch component 
    def _comp_animation(self, shape):

        comp, shape, center= shape

        t= abs(self.t0 - time.clock())
        if t > comp.calcul_duration('sec'):
            return False

        if isinstance(comp, (watch.GearWheel, watch.Hand)):
            speed= (comp.speed/60)*(2*math.pi)
            angle= t*speed

            points= POINTS_FUNC_DICT[comp.type](comp, center)
            newPoints= list()

            for p in points:

                x, y= p.x-center.x, p.y-center.y
                X= x*math.cos(angle) - y*math.sin(angle) + center.x
                Y= y*math.cos(angle) + x*math.sin(angle) + center.y
                newPoints+= X, Y

            self.canvas.coords(shape, tuple(newPoints))
        return True

    #launch to animate the watch and the info text
    def animation(self):

        for t in self.texts:
            self.canvas.itemconfig(t, state= 'normal' if VIEW_TEXT else 'hidden')

        for s in self.shapes:
            self._comp_animation(s)



#show the watch in main frame
def display_watch(w, name= '', rootWindow= None):

    #print(w)
    window= None
    if not rootWindow:
        window= tk.Tk()
        rootWindow= window
    else:
        window= tk.Toplevel(rootWindow)
        window.grab_set()

    alive= True
    def exit_display():
        nonlocal alive, window
        alive= False
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', exit_display)
    window.title(name)
    window.resizable(False, False)

    #window['bg']= 'white'

    screenWidth, screenHeight=  window.winfo_screenwidth(), window.winfo_screenheight()
    rootWidth, rootHeight=      map(int, (screenWidth*0.5, screenHeight*0.5))
    rootX, rootY=               map(int, ((screenWidth - rootWidth)/2, (screenHeight - rootHeight)/2))
    canvasWidth, canvasHeight=  map(int, (rootWidth, rootHeight))

    #print("Sreen size:\t {}x{}".format(screenWidth, screenHeight))
    #print("Window size:\t {}x{} ({}, {})".format(rootWidth, rootHeight, rootX, rootY))
    #print(" -Canvas size:\t {}x{}".format(canvasWidth, canvasHeight))


    window.geometry("{}x{}+{}+{}".format(rootWidth, rootHeight, rootX, rootY))

    canvas= WatchCanvas(window)
    canvas.pack(fill= tk.BOTH, expand= 1)
    canvas.set_watch(w)

    while alive:
        canvas.animation()
        window.update_idletasks()
        window.update()




if __name__=="__main__":


    a0= watch.Axis()
    a1= watch.Hand()
    a2= watch.Engine(766)
    a3= watch.Hand()
    a4= watch.GearWheel(5)
    a5= watch.GearWheel(94)
    a6= watch.GearWheel(10)
    a7= watch.Balance(0.0128)
    a8= watch.Axis()

    w= watch.Watch()
    w*= (a0, a3)
    w*= (a0, a6)
    w*= (a1, a8)
    w*= (a2, a8)
    w*= (a4, a5)
    w*= (a4, a6)
    w*= (a5, a6)
    w*= (a5, a7)
    w*= (a5, a8)

    print(w)
    display_watch(w, "my watch")
