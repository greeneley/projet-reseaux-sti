#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - filewatch.py
# 2017/10/26

import pickle
import random

__all__= ['save_watch', 'open_watch', 'save_pop', 'open_pop']

def save_watch(w, openFile):
    pickle.dump(w, openFile, protocol= pickle.HIGHEST_PROTOCOL)

def open_watch(openFile):
    return pickle.load(openFile)



def save_pop(population, openFile):
    for w in population:
        pickle.dump(w, openFile, protocol= pickle.HIGHEST_PROTOCOL)


def open_pop(*openFiles):
    if len(openFiles) == 1:
        return _open_pop(openFiles[0])

    populations= list()
    for openFile in openFiles:
        populations.append(_open_pop(openFile))

    pop= list()
    for i, p in enumerate(populations[0]):
        pop.append(random.choice(populations)[i])
    return pop

def _open_pop(openFile):
    pop= list()
    while True:
        try:
            pop.append(pickle.load(openFile))
        except EOFError:
            break

    return pop



if __name__=="__main__":


    #population= [randwatch.random_watch() for _ in range(10)]
    #save_pop(population)

    import watch
    import randwatch
    w= watch.Watch()

    i= randwatch.random_component("gear")
    j= randwatch.random_component("gear")
    a= randwatch.random_component("axis")
    w.add_edge(randwatch.random_component("engine"), a)
    w.add_edge(i, a)
    w.add_edge(i, j)
    w.add_edge(i, randwatch.random_component("gear"))
    w.add_edge(j, randwatch.random_component("gear"))
    w.add_edge(j, randwatch.random_component("gear"))
    a= randwatch.random_component("axis")
    w.add_edge(j, a)
    w.add_edge(a, randwatch.random_component("hand"))
    w.add_edge(j, randwatch.random_component("balance"))

    w.transmission()

    print(w)

    with open("mywatch.watch", "wb") as openFile:
        save_watch(w, openFile)
    #print(load_watch())
