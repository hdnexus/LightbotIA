from Node import *
from copy import deepcopy
import time

depth = 0
pathList = []
closedList = []
openList = []

def aStarSearch(initialState, finalState):
    global depth