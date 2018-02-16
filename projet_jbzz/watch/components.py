#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - components.py
# 2017/10/05

import math
import copy

__all__= ['Hand', 'Axis', 'GearWheel', 'Engine', 'Balance', 'color_caption', 'TYPES_DICT']

# CLASS

class Component(object):
    """Common class for Component object
    """

    componentsCount= 0

    _type= None
    _color= '\033[0m'

    featureLimits= (0, 0)
    priceFactor= 1


    def __init__(self): #Initializes the components
        Component.componentsCount+= 1
        super().__init__()

        self.__speed=   .0 # tr/min
        self.__energy=  .0 # tr
        self._weight=   .0 # g
        self._cost=     .0 # $
        self._radius=   .0 #

        self._ID= 0

    def __str__(self): #Returns the component in somtehing that can be written
        return "{:>8} {:>8} {:>8.8} {:>8.8} {:>8.8} {:>8.8} {:>8.8} {:>8.8}".format(
            str(self.ID),
            str(self.type),
            str(self.feature),
            str(self.speed),
            str(self.energy),
            str(self.calcul_duration()),
            str(self.weight),
            str(self.cost),
        )

    def __repr__(self): #Represents the component for the line interface
        return self.color + str(self.ID) + '\033[0m'


    @property
    def type(self):
        """ Return the str type of the component.
        """
        return self._type


    @property
    def color(self):
        """ Return the ANSI code color of the component.
        """
        return self._color


    @property
    def ID(self):
        """ Return the unique ID of the component.
        """
        return self._ID


    @property
    def speed(self):
        """ Return the rotation speed (tr/min) of the component.
        """
        return self.__speed

    @speed.setter
    def speed(self, speed):
        """ Set the speed of the component.
        """
        self.__speed= speed


    @property
    def energy(self):
        """ Return the energy (tr) of the component.
        """
        return self.__energy

    @energy.setter
    def energy(self, energy):
        """ Set the energy of the component.
        """
        self.__energy= energy


    @property
    def weight(self):
        """ Return the weight (g) of the component.
        """
        return self._weight

    @property
    def cost(self):
        """ Return the cost of the component.
        """
        return self._cost*self.priceFactor

    @property
    def feature(self):
        return 0

    @feature.setter
    def feature(self, feature):#It is abstract
        pass


    @property
    def diameter(self):
        """ Return the diameter of the component.
        """
        return self._radius * 2

    @property
    def radius(self):
        """ Return the radius of the component.
        """
        return self._radius


    def transmit_speed(self, other):
        """ Transmit the speed of the component to an other.
        Return the transmitted speed.
        """
        return 0

    def transmit_energy(self, other):
        """ Transmit the energy of the component to an other.
        Return the transmitted energy.
        """
        return 0



    def calcul_duration(self, unit= "min"):
        """ Return the work duration in minutes.
        """

        if abs(self.__speed) < .0000001:
            return .0

        time= abs(self.__energy / self.__speed)

        if unit ==      "min":#Unity conversions
            return time
        elif unit ==    "sec":
            return time * 60
        elif unit ==    "hour":
            return time / 60
        elif unit ==    "day":
            return time / (60*24)
        elif unit ==    "week":
            return time / (60*24*7)

    def copy(self):#Uses the deepcopy function to copy a component
        c= copy.deepcopy(self)
        return c



class Hand(Component): # aiguille
    """ Class for Hand component.
    """

    _type= 'hand'#name of the type
    _color= '\033[90m'#color of a hand

    def __init__(self):#initial values of a hand
        super().__init__()
        self._weight= 1
        self._cost= 2
        self._radius= 200



class Axis(Component): # axe
    """ Class for Axis component.
    """

    _type= 'axis'
    _color= '\033[91m'

    def __init__(self):#initialization
        super().__init__()
        self._weight= 3
        self._cost= 1
        self._radius= 4


    def transmit_speed(self, other):#the axis can transmit speed and energy

        if isinstance(other, (GearWheel, Hand, Engine)):
            other.speed= self.speed

        return other.speed

    def transmit_energy(self, other):

        if isinstance(other, (GearWheel, Hand)):
            other.energy= self.energy

        return other.energy


class GearWheel(Component): # roue dentée
    """ Class for GearWheel component.
    FR: https://fr.wikipedia.org/wiki/Roue_dentée
    """

    _type= 'gear'#type and color
    _color= '\033[92m'

    featureLimits= (5, 100)#limits of this component
    teethHeight= 5
    teethPitch= 4


    def __init__(self, teethCount= 10):
        super().__init__()
        self.teethCount= teethCount

    @property
    def teethCount(self):
        """ Return the number of teeth of the GearWheel.
        """
        return self.__teethCount

    @teethCount.setter
    def teethCount(self, teethCount):
        """ Set the number of teeth of the GearWheel.
        """
        self.__teethCount= teethCount
        self._radius= teethCount*GearWheel.teethPitch/math.pi
        self._weight= teethCount**(1/2)
        self._cost=1+ teethCount/100


    @property
    def feature(self):
        return self.__teethCount

    @feature.setter
    def feature(self, feature):
        self.teethCount= feature


    def reduction_ratio(self, other):
        """ Return the reduction ratio between the GearWheel and an other.
        """
        return other.teethCount / self.__teethCount

    def transmission_ratio(self, other):
        """ Return the transmission ratio between the GearWheel and an other.
        FR: https://fr.wikipedia.org/wiki/Engrenage
        """
        return self.__teethCount / other.teethCount

    def transmit_speed(self, other):#transmit the speed and energy, the gearwheel is allowed to

        if isinstance(other, GearWheel):
            other.speed= self.transmission_ratio(other) * self.speed * -1
        elif isinstance(other, Axis):
            other.speed= self.speed

        return other.speed

    def transmit_energy(self, other):

        if isinstance(other, GearWheel):
            other.energy= self.transmission_ratio(other) * self.energy
        elif isinstance(other, Axis):
            other.energy= self.energy

        return other.energy


class Engine(Component): # moteur
    """ Class for Engine component.
    """

    _type= 'engine'
    _color= '\033[93m'

    featureLimits= (100, 1500)

    def __init__(self, capacity= 0):#initializes the engine
        super().__init__()

        self.capacity= capacity
        self._weight= 30
        self._radius= 50

    @property
    def capacity(self):
        """ Return the capacity of the Engine.
        """
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity):
        """ Set the capacity of the Engine.
        """
        self.__capacity= capacity
        self._cost=15+ capacity/300

    @property
    def feature(self):#The feature corresponds to the capacity for an engine
        return self.__capacity

    @feature.setter
    def feature(self, feature):
        self.capacity= feature


    def transmit_energy(self, other):#An engine can only transmit energy

        if isinstance(other, Axis):
            other.energy= self.__capacity

        return other.energy

    def calcul_duration(self, unit= "min"):
        """ Returns the duration of the engine
        """
        self.energy= self.__capacity
        return Component.calcul_duration(self, unit)


class Balance(Component): # balancier
    """ Class for Balance component.
    """

    _type= 'balance'
    _color= '\033[94m'

    featureLimits= (0, 5)

    def __init__(self, frequency= 0):#initalizes the balance
        super().__init__()

        self.frequency= frequency
        self._weight= 20
        self._radius= 30

    @property
    def frequency(self):
        """ Return the frequency of the Balance.
        """
        return self.__frequency

    @frequency.setter
    def frequency(self, frequency):
        """ Set the frequency of the Engine.
        """
        self.__frequency= frequency
        self._cost= 10+10*frequency


    @property
    def feature(self):#The feature of the balance is its frequency
        return self.__frequency

    @feature.setter
    def feature(self, feature):
        self.frequency= feature

    def transmit_speed(self, other):#The balance can transmit speed

        if isinstance(other, GearWheel):
            other.speed= 60*2*self.__frequency/other.teethCount

        return other.speed




TYPES_DICT= {
    "hand": Hand,
    "axis": Axis,
    "gear": GearWheel,
    "engine": Engine,
    "balance": Balance
}#dictionnary of all the types


def color_caption():
    """Get the caption of the components
    """

    out= " - COMPONENTS CAPTION -\n"
    for ID in TYPES_DICT:
        out+= TYPES_DICT[ID]._color + ID + '\033[0m' + '\n'

    return out

if __name__ == "__main__":

    #print(color_caption()) #debug

    a= Axis()
    print(a)
