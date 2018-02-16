#!/usr/bin python3
# -*- coding: utf-8 -*-

# TEAM JBZZ
# INSA CVL - Projet Programmation - __init__.py
# 2017/10/08

from .components    import *
from .watch         import *
from .filewatch     import *
from .randwatch     import *
from .scorewatch    import *
from .evalgo        import *

__all__= []
__all__+= components.__all__
__all__+= watch.__all__
__all__+= filewatch.__all__
__all__+= randwatch.__all__
__all__+= scorewatch.__all__
