from Node import *
from copy import deepcopy
import time

depth = 0
pathList = []
closedList = []
openList = []

def depthSearch(initialState, finalState):
    global depth