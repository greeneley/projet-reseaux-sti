#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - scorewatch.py
# 2017/10/05

import random
import math

#function two values are close to each other
try:
    isclose= math.isclose
except:
    isclose= lambda x, y: abs(x - y) < 0.0000000001


__all__= ['score_watch']


#returns the score attributed to the autonomy of a watch given in params.
def calcAutonomy(w):
    listAutonomy= [0]
    for e in w.search_component("engine"):
        if not isclose(e.speed, 0):
            listAutonomy.append(e.calcul_duration())
        else:
            listAutonomy.append(0)


    score= int(max(listAutonomy)**(1/6))
    return score

#returns the score attributed to the cost of the watch given in params.
#the cost of the watch is the sum of the costs of each component of this watch
def calcCost(w):
    score= -w.cost
    return score


#verify that a lot of hands turn in the same direction
def sensAiguilles(w):
    score = 0

    nbSpeedPos, nbSpeedNeg= 0, 0
    listOfHands=w.search_component("hand")

    for h in listOfHands:
        if h.speed < 0 and not isclose(h.energy, 0):
            nbSpeedPos+= 1
        if h.speed > 0 and not isclose(h.energy, 0):
            nbSpeedNeg+= 1

    if listOfHands:
        score+= 10 * max(nbSpeedPos, nbSpeedNeg) / len(listOfHands)
    return score


#there is a wheel
#a wheel turn
#a hand turn
def elementary(w):
    score= 0

    gearWheelList= w.search_component("gear")
    if gearWheelList:
        score+= 20

    for g in gearWheelList:
        if not isclose(g.speed, 0) and not isclose(g.energy, 0):
            score+=20
            break

    for h in w.search_component("hand"):
        if not isclose(h.speed, 0) and not isclose(h.energy, 0):
            score+=20
            break

    return score


#several gearwheels rotate at different speeds
def gear_different_speeds(w):
    score=0

    speedsList= []
    confirmedSpeedsList= []

    for g in w.search_component("gear"):
        if not isclose(g.energy, 0) and not isclose(g.speed,0):
            speedsList.append(abs(g.speed))

    for s in speedsList:

            verifRatio= False
            for s2 in confirmedSpeedsList:
                if not isDifferentRatio(s, s2):
                    verifRatio= True #gears speeds are to close from each other
                    break

            if not verifRatio and s <= 60:
                score+= 30
            confirmedSpeedsList.append(s)


    return score;


#several hands rotate at different speeds
def different_speeds(w):
    score=0

    speedsList= []
    confirmedSpeedsList= []

    for h in w.search_component("hand"):

        if not isclose(h.energy, 0) and not isclose(h.speed, 0) and abs(h.speed)<2:
            speedsList.append(abs(h.speed))

    for s in speedsList:

            verifRatio= False
            for s2 in confirmedSpeedsList:
                if not isDifferentRatio(s, s2):
                    verifRatio= True #hands speeds are to close from each other, they are not interesting
                    break

            if not verifRatio:
                score+= -20*math.sqrt(s)+50
            confirmedSpeedsList.append(s)

    return score

#comparison of the ratio between two speeds
def isDifferentRatio(s, s2):
    s= 60/s
    s2= 60/s2

    return s2 >= 10*s or s2 <= s/10

#check if the speeds are close to known times
def knownTimeRatio(w):

    score= 0
    second, minutes, hours, week, year= 0, 0, 0, 0, 0

    for h in w.search_component("hand"):

        if not isclose(h.energy, 0):

            if not isclose(gaussienne(0.2*1, 1, h.speed), 0): #second
                second = max(second, gaussienne(0.2*1, 1, h.speed))

            if not isclose(gaussienne(0.2*(1/60), 1/60, h.speed), 0): #minute
                minutes = max(minutes, gaussienne(0.2*(1/60), 1/60, h.speed))

            if not isclose (gaussienne(0.2*(1/(60*12)), 1/(60*12), h.speed), 0): #hour
                hours = max(hours, gaussienne(0.2*(1/(60*12)), 1/(60*12), h.speed))

            if not isclose (gaussienne(0.2*(1/(60*24*7)), 1/(60*24*7), h.speed), 0): #week
                week = max(hours, gaussienne(0.2*(1/(60*24*7)), 1/(60*24*7), h.speed))

            if not isclose (gaussienne(0.2*(1/(60*24*365)), 1/(60*24*365), h.speed), 0): #year
                year = max(hours, gaussienne(0.2*(1/(60*24*365)), 1/(60*24*365), h.speed))

    score += (second + minutes + hours+ week + year) * 20

    return score


#reimplementation of the Gaussian function
def gaussienne(standard_deviation, expected_value, value):
    return math.exp(-1 * ((value - expected_value)**2) / (2 * (standard_deviation**2)))


#returns the total score of a watch given in params
def score_watch(w):
    return float(sum((
        calcAutonomy(w),
        calcCost(w),
        different_speeds(w),
        gear_different_speeds(w),
        elementary(w),
        knownTimeRatio(w),
        sensAiguilles(w)
        )))


if __name__ == "__main__":

    import watch
    from components import *

    w= watch.Watch()
    w.add_edge(Axis(), GearWheel(7))
    w.add_component(Axis())

    print(score_watch(w))

    w.add_component(Engine(20))

    print(score_watch(w))
