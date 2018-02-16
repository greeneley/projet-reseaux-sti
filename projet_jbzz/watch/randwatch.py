#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - randwatch.py
# 2017/10/09


import random
import math

from . import components
from . import watch

__all__= ['COMPONENTS_COUNT_LIMITS', 'random_watch', 'random_edges', 'random_component']

COMPONENTS_COUNT_LIMITS= (0, 50)


def random_component(componentType= None):
    """ Return a random component of type componentType
    """
    if componentType == None:
        componentType= random.choice(list(components.TYPES_DICT.keys()))

    funcDict= {
        "hand":     random.randint,
        "axis":     random.randint,
        "gear":     random.randint,
        "engine":   random.uniform,
        "balance":  random.uniform,
    }

    component= components.TYPES_DICT[componentType]()
    component.feature= funcDict[componentType](*component.featureLimits)

    return component



def random_edges(w):
    """ Make random edges between the components of the watch
    """
    chanceEdge= 0.5
    componentsList= w.components
    for i, c1 in enumerate(componentsList):
        for c2 in componentsList[i+1:]:
            if w.is_valid_edge(c1, c2) and random.random() < chanceEdge:
                w.add_edge(c1, c2)



def random_watch():
    """Return a random watch
    """

    w= watch.Watch()
    listTypes= list(components.TYPES_DICT.keys())

    for _ in range(random.randint(*COMPONENTS_COUNT_LIMITS)):
        w+= random_component(random.choice(listTypes))

    random_edges(w)

    w.transmission()
    return w


def fusion(father, mother):
    #copulation with 2 parents watch, returns the new watch created
    w= watch.Watch()

    componentsList= [c.copy() for c in father.components + mother.components]
    if not componentsList:
        return w

    componentCounts= random.randint(COMPONENTS_COUNT_LIMITS[0], len(componentsList))
    while len(w) < componentCounts:
        w+= random.choice(componentsList)

    random_edges(w)
    w.transmission()
    return w


def mutate(w):
    #mutation of a watch, returns the modified watch
    w= w.copy()
    #mutation types :
    m= 0 if not w else random.randint(0, 2)
    if m == 0:
        # add component
        for i in range(random.randint(1,20)):
            component= random_component()
            w+= component
            for c in w:
                if component != c and w.is_valid_edge(c, component):
                    w*= (c, component)

    elif m == 1:
        # delete component
        component= random.choice(w.components)
        del w[component]

    elif m == 2:
        # replace component
        component= random.choice(w.components)
        w.replace(component, random_component(component.type))

    w.transmission()
    return w



if __name__ == "__main__":

    #print(components.color_caption())
    w1= random_watch()
    w2= mutate(w1)
    w3= fusion(w1, w2)

    print(w1)
    print(w2)
    print(w3)
