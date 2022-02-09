from Robot import *
from State import *
from queue import Queue


openList = Queue()

def func():
    openList.put(1)
    openList.put(2)

func()
final_state = Robot(0,2,0,2,True,True)
robotState = (final_state.x, final_state.y, final_state.direction, final_state.height, final_state.firstBlueBlock, final_state.secondBlueBlock) 
finalState = (0,2,0,2,True,True)
print(robotState)
if(robotState == finalState):
    print("Achou")

