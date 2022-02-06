#classe do nó
class Node():
    def __init__(self, father, state):
        self.robotWalk = None #nó filho de andar
        self.robotJump = None #nó filho de pular
        self.robotLightUp = None #nó filho de acender
        self.robotTurnLeft = None #nó filho de virar para esquerda
        self.robotTurnRight = None #nó filho de virar para direita
        self.cost = 0 #custo
        self.greedyCost = 0 #custo guloso
        self.nodeFather = father #nó pai
        self.state = state #estado do nó

    
    def setState(self, state):
        self.state = state
    def getState(self):
        return self.state
    
    def getRobotWalk(self):
        return self.robotWalk
    def setRobotWalk(self, node):
        self.robotWalk = node

    def getRobotJump(self):
        return self.robotJump
    def setRobotJump(self, node):
        self.robotJump = node

    def getRobotLightUp(self):
        return self.robotLightUp
    def getRobotLightUp(self, node):
        self.robotLightUp = node


    def getRobotTurnLeft(self):
        return self.robotTurnLeft
    def setRobotTurnLeft(self, node):
        self.robotTurnLeft = node
    
    def getRobotTurnRight(self):
        return self.robotTurnRight
    def setRobotTurnRight(self, node):
        self.robotTurnRight = node
    
    def getNodeFather(self):
        return self.nodeFather
    def setNodeFather(self, node):
        self.nodeFather = node

    def getCost(self):
        return self.cost
    def setCost(self, cost):
        self.cost = cost

    def getGreedyCost(self):
        return self.greedyCost
    def setGreedyCost(self, gcost):
        self.greedyCost = gcost