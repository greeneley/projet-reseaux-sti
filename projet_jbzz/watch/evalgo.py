#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - evalgo.py (evolutionary algorithm)
# 2017/09/26

import queue
import threading
import random

from . import watch
from . import randwatch


__all__= ['EvAlgo']

#DEBUG OPTIONS
PRINT_INFO= False
STOP_AT_BEST= False           # stop the algo after a new best watch


class EvAlgo(threading.Thread):

    def __init__(self):
        #population and evolution characteristics
        super().__init__()

        self.popSize=       100
        self.retainCount=   3
        self.parentsCount=  20

        self.chanceRetain=  0.20
        self.chanceMutate=  0.7

        self.alive=         False
        self.stopped=       True
        self.reseted=       False
        self.stopAtBest=    False
        self.startPop=      None
        self.datasQueue=    queue.Queue(1)


    def run(self):
        #rum the algorithm loop
        self.alive= True
        self.bWatch=   watch.Watch()
        self.pop=      [randwatch.random_watch() for _ in range(self.popSize)]
        self.gCount=   0
        self.gGoal=    0
        self.datasQueue= queue.Queue(1)
        while self.alive:

            if self.reseted:
                self.reseted=  False
                self.bWatch=   watch.Watch()
                self.pop=      self.startPop if self.startPop != None else [randwatch.random_watch() for _ in range(self.popSize)]
                self.gCount=   0
                self.gGoal=    0
                self.datasQueue= queue.Queue(1)
                self.update()

            if not self.is_stopped():
                self.evolve()
                self.gCount+= 1
                self.update()


    def update(self):
        #update the best watch

        self.pop= sorted(self.pop, key= lambda x: x.score, reverse= True)
        w= self.pop[0]
        if self.bWatch.score < w.score:
            self.bWatch= w.copy()
            self.datasQueue.put((self.gCount, self.bWatch))
            if self.stopAtBest:
                self.stopAtBest=    False
                self.stopped=       True
        else:
            self.datasQueue.put((self.gCount, None))



    def evolve(self):
        # Make the given population evolving to his next generation.

        # Filter the top graded individuals
        retained= self.pop[:self.retainCount]
        parents= self.pop[self.retainCount:self.parentsCount]

        # Randomly add other individuals to promote genetic diversity
        for w in self.pop[self.parentsCount:]:
            if random.random() < self.chanceRetain:
                parents.append(w)

        # Mutate some individuals
        mutants= list()
        for w in retained:
            if random.random() < self.chanceMutate:
                mutants.append(randwatch.mutate(w))

        for i, w in enumerate(parents):
            if random.random() < self.chanceMutate:
                parents[i]= randwatch.mutate(w)


        parents= retained + mutants + parents

        # Crossover parents to create children
        children = list()
        for _ in range(self.popSize - len(parents)):
            father, mother= None, None
            while father == mother:
                father, mother= random.choice(parents), random.choice(parents)
            children.append(randwatch.fusion(father, mother))


        # The next generation is ready
        self.pop= parents + children


    def stop(self):
        #stop the algorithm
        self.stopped= True

    def reset(self, pop= None):
        #reset the algorithm
        self.reseted= True
        self.startPop= pop

    def resume(self):
        #resume the algorithm
        self.stopped= False

    def end(self):
        #finish the algorithm
        self.alive= False
        while not self.datasQueue.empty():
            self.datasQueue.get_nowait()

    def is_stopped(self):
        return self.stopped and self.gGoal <= self.gCount

    def is_running(self):
        return self.alive



if __name__ == '__main__':

    EvAlgo().start()
