#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - watch.py
# 2017/10/05

import random
import copy


from . import components
from .scorewatch import score_watch

__all__= ['Watch']


N= float('inf')
VALIDITY_CONDITIONS= {
    "hand":     {"hand": 0, "axis": 1, "gear": 0, "balance": 0, "engine": 0},
    "axis":     {"hand": N, "axis": 0, "gear": N, "balance": 0, "engine": 1},
    "gear":     {"hand": 0, "axis": 1, "gear": N, "balance": 1, "engine": 0},
    "balance":  {"hand": 0, "axis": 0, "gear": 1, "balance": 0, "engine": 0},
    "engine":   {"hand": 0, "axis": 1, "gear": 0, "balance": 0, "engine": 0}
}#authorized connections



class Watch(object):

    watchCount= 0

    def __init__(self):
        super().__init__()

        Watch.watchCount+= 1

        self.__graphDict= dict()
        self.__componentsCount= {
            "hand":     0,
            "axis":     0,
            "gear":     0,
            "engine":   0,
            "balance":  0
        }


    def __iter__(self):
        for i in self.__graphDict:
            yield i

    def __getitem__(self, component):
        return self.__graphDict[component]

    def __contains__(self, component):
        return component in self.__graphDict

    def __len__(self):
        """ Returns the length of a watch
        """
        return sum(self.__componentsCount.values())

    def __bool__(self):
        return bool(self.__graphDict)

    def __iadd__(self, component):
        self.add(component)
        return self

    def __imul__(self, edge):
        self.add_edge(*edge)
        return self

    def __delitem__(self, component):
        """ Deletes a component
        """
        self.remove(component)



    def component_count(self, componentType):
        """ Returns the number of components of a certain type
        """
        return self.__componentsCount[componentType]

    @property
    def score(self):
        """ Returns the score of the watch using the function in the file scorewatch.py
        """
        return score_watch(self);

    @property
    def weight(self):
        """ Returns the weight of the watch by adding the weight of its components
        """
        return float(sum(c.weight for c in self))

    @property
    def cost(self):
        """ Returns the cost of the watch by adding the cost of its components
        """
        return float(sum(c.cost for c in self))

    @property
    def components(self):
        """ Returns a list of its components
        """
        return list(self.__graphDict.keys())


    @property
    def subwatches(self):
        """ Returns a list of subwatches from a watch
        """
        subWathes= list()
        for c in self:
            if not any(c in sub for sub in subWathes):
                subWathes.append(self.get_subwatch_of(c))

        return subWathes


    def add(self, component):
        """ Adds a new component to the watch
        """
        if component in self:
            return False

        self.__graphDict[component]= set()
        self.__componentsCount[component.type]+= 1
        return True

    def add_components(self, components):
        """ Adds one or more components to the watch
        """
        for c in components: self.add(c)


    def add_edge(self, component1, component2):
        """ Add an edge to the graph.
        If a component "component" is not in self.graphDict, a key "component" with an empty set as a value is added to the dictionary.
        """

        for c1, c2 in ((component1, component2), (component2, component1)):

            if c1 in self:
                self.__graphDict[c1].add(c2)
            else:
                self+= c1
                self.__graphDict[c1]= set([c2])


    def search_component(self, componentType):
        """Return components in the watch with type is componentType
        """
        return [c for c in self if isinstance(c, components.TYPES_DICT[componentType])]



    def remove(self, component):
        """Delete a component in the watch
        """

        if not component in self:
            return False

        self.__componentsCount[component.type]-= 1

        del self.__graphDict[component]
        for a in self:
            if component in self[a]:
                self[a].remove(component)

        return True



    def replace(self, component, by):
        """Replace a component in the watch by an other
        """
        if (not component in self) or (by in self):
            return False

        self.__componentsCount[by.type]+= 1
        self.__componentsCount[component.type]-= 1

        self.__graphDict[by]= self[component]
        del self.__graphDict[component]

        for a in self:
            if component in self[a]:
                self[a].remove(component)
                self[a].add(by)

        return True


    def is_valid_component(self, component):
        """ Checks whether if a component is valid
        """
        counts= {"hand": 0, "axis": 0, "gear": 0, "balance": 0, "engine": 0}

        for c in self[component]: counts[c.type]+= 1

        for t in VALIDITY_CONDITIONS[component.type]:
            if counts[t] > VALIDITY_CONDITIONS[component.type][t]:
                return False
        return True


    def is_valid_edge(self, c1, c2):
        """ Checks whether if an edge (liaison) is valid (using the authorized connections line 19)
        """
        c1Counts= {"hand": 0, "axis": 0, "gear": 0, "balance": 0, "engine": 0}
        c2Counts= dict(c1Counts)

        for c in self[c1]: c1Counts[c.type]+= 1
        for c in self[c2]: c2Counts[c.type]+= 1

        c1Counts[c2.type]+= 1
        c2Counts[c1.type]+= 1

        cond1= VALIDITY_CONDITIONS[c1.type][c2.type]
        cond2= VALIDITY_CONDITIONS[c2.type][c1.type]

        return c1Counts[c2.type] <= cond1 and c2Counts[c1.type] <= cond2


    def is_cyclic(self):
        """ Checks if the watch is cyclic or not (it is a physical impossibility) 
        """
        def _is_cyclic(comp, visited, parent):
            nonlocal self

            visited.add(comp)
            for c in self[comp]:
                if not c in visited:
                    if _is_cyclic(c, visited, comp):
                        return True

                elif  parent != c:
                    return True

            return False

        visited= set()
        for c in self:
            if not c in visited:
                if _is_cyclic(c, visited, None):
                    return True

        return False




    def is_valid_subwath(self):
        """ Checks if a subwatch is valid
        """
        return all(self.is_valid_component(c) for c in self) and not self.is_cyclic()



    def get_subwatch_of(self, component):
        """ Returns the subwatch that contains a particular component
        """
        def _get_subwatch(subWath, component, parents):


            subWath.__graphDict[component]= self[component]
            parents.add(component)
            for c in self[component].difference(parents):
                _get_subwatch(subWath, c, parents)

        subWath= Watch()
        _get_subwatch(subWath, component, set())
        return subWath





    def __transmission_speed(self):
        """ Transmit speed along the watch
        """

        def ts(component, parents):

            parents.add(component)

            for c in self[component].difference(parents):
                component.transmit_speed(c)
                ts(c, parents)


        balances= self.search_component("balance")
        if self.is_valid_subwath() and len(balances) < 2:
            for b in balances: ts(b, set())



    def __transmission_energy(self):
        """ Transmit energy along the watch
        """

        def te(component, parents):

            parents.add(component)

            for c in self[component].difference(parents):
                component.transmit_energy(c)
                te(c, parents)


        engines= self.search_component("engine")
        if self.is_valid_subwath() and len(engines) < 2:
            for e in engines: te(e, set())

    def transmission(self):
        """ Calls the function to transmit energy and speed along the watch
        """
        self.set_to_0()
        for sub in self.subwatches:

            sub.__transmission_speed()
            sub.__transmission_energy()

            times= set()
            for c in sub:
                if not isinstance(c, components.Balance):
                    times.add("{:.5f}".format(c.calcul_duration()))

            if len(times) > 1: sub.set_to_0()



    def set_speed_to_0(self):
        for c in self:
            c.speed= .0

    def set_energy_to_0(self):
        for c in self:
            c.energy= .0

    def set_to_0(self):
        for c in self:
            c.speed= .0
            c.energy= .0


    def __str__(self):
        """ It allows us to print the watch in an understandable way
        """
        out= str()
        out+= '\n'

        out+= "{:^8} {:^8} {:^8}\n".format("Weight", "Cost", "Score")
        out+= "{:>8.8} {:>8.8} {:>8.8}\n".format(str(self.weight), str(self.cost), str(self.score))
        out+= '\n'

        out+= "{:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8} {:^8}\n".format("ID", "Type", "Feature", "Speed", "Energy", "Time", "Weight", "Cost")
        for i, component in enumerate(self): component._ID= i
        for component in self:
            s= str(self[component]) if self[component] else str()
            out+= component.color + str(component) + "\033[0m " + s + '\n'
        out+= '\n'
        return out

    def __repr__(self):
        """ It allows us to print the watch in an understandable way, using the same code as the function below
        """
        return str(self)


    def copy(self):
        """ Return a copy of the actual watch
        """
        w= copy.deepcopy(self)
        return w






if __name__ == "__main__":


    a1= components.Axis()
    a2= components.Axis()
    g1= components.GearWheel(40)
    g2= components.GearWheel(50)
    g3= components.GearWheel(60)

    e1= components.Engine(1000)
    b1= components.Balance(2)

    w= Watch()
    w*= (e1, a1)
    w*= (a1, g1)
    w*= (g1, b1)
    w*= (g1, g2)
    w*= (g2, a2)
    w*= (a2, g3)

    w.is_valid_subwath()
    w.transmission()
    print(w.copy())
    print(w)
