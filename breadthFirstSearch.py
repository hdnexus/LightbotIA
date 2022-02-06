from Node import *
from State import *
from Robot import *
from copy import deepcopy
from queue import Queue
import time

counter = 0
depth = 0
pathList = []
closedList = []
openList = Queue()

#Mapa do jogo, o valor das matrizes é a quantidade de blocos(altura)
matriz = [[0,0,2,0,0,0,0,0],
          [0,0,2,0,0,0,0,0],
          [0,0,2,0,0,0,0,0],
          [0,0,4,4,0,0,0,0],
          [0,1,2,3,0,0,0,0],
          [0,0,3,4,0,0,0,0],
          [0,0,2,2,0,0,0,0],
          [0,0,0,2,0,0,0,0]]

#Obter a direção de acordo com os valores 0,1,2,3
turn_rule = ['Norte', 'Leste', 'Sul', 'Oeste']

#Movimentos do robô para cada direção respectiva
movement = {
    0 : (0, -1), # norte
    1 : ( 1,0), # leste
    2 : (0, 1), # sul
    3 : (-1,0), # oeste
}

#Função que irá percorrer o caminho da solução
def getPath(node):
    global pathList
    pathList.append(node)
    auxNode = node.getNodeFather()
    while auxNode != None:
        pathList.append(auxNode)
        auxNode = auxNode.getNodeFather()
    pathList.reverse() 

#Função que servirá pra imprimir um determinado estado
def printState(state):
    firstBlueBlock = 'Apagado'
    secondBlueBlock = 'Apagado'
    if(state.blue_blocks['7 3']):
        firstBlueBlock = 'Ligado'
    if(state.blue_blocks['0 2']):
        secondBlueBlock = 'Ligado'
    global counter 
    counter = counter + 1
    print('--',str(counter) + 'º', 'Estado')
    print('| Primeiro bloco azul =', firstBlueBlock,
    '| Segundo bloco azul =', secondBlueBlock, 
    '| x =', state.robot.x, '| y =', state.robot.y, 
    '| Direção =', turn_rule[state.robot.direction], '| Altura =',state.robot.height, '|')

############################ ACENDER ############################# 
#Função que irá checar se o bloco é azul e se esta aceso ou não
def checkLight(node): 
    key = f"{node.state.robot.x} {node.state.robot.y}"
        # se a posicao atual do robo é um bloco azul, o bloco recebe a negação dele mesmo ou seja se True -> False e se False -> True
    if (key in node.state.blue_blocks):
        node.state.blue_blocks[key] = not node.state.blue_blocks[key]
        return True
    return False

#Função que irá acender os blocos azuis
def lightUp(node):
    global depth
    global openList
    verify = False
    if checkLight(node) == True:
        #atualizar estado
        #criar nó auxiliar
        #nó auxiliar custo node.setCost(node.getCost() + 1)
        #cria filho com nó auxiliar node.setRobotLightUp(node) 
        openList.put(node) #incrementa lista de abertos 
#################################################################### 

########################## ANDAR E PULAR ########################## 
#Função para checar se o robô pode ir para um determinado bloco
def checkMovement(state, movement):
    if (state.x + movement[0] < 0 or state.x + movement[0] > 7):
        return False
    if (state.y + movement[1] < 0 or state.y + movement[1] > 7):
        return False
    return True

#Função para pegar o bloco na frente do robô
def get_next_state(robot, movement):
    if (checkMovement(robot, movement)):
        return Robot(robot.x + movement[0], robot.y + movement[1], robot.height)
    else:
        return None
####################################################################

####################### VIRAR PARA ESQUERDA ######################## 
####################################################################

####################### VIRAR PARA DIREITA ######################### 
####################################################################


#Função que irá realizar a busca em largura
def breadthSearch(initialState, finalState):
    global depth
    global closedList
    global openList
    startTime = time.time()
    sucess = False
    failure = False
    solutionNode = None
    openList.put(initialState) 
    root = Node(None, initialState)
    root.setCost(0)
    while sucess == False and failure == False:
        if openList.empty() == True:
            failure = True
            break
        else:
            node = openList.get()
            if(node.state == finalState):
                sucess = True
                solutionNode = node
            else:
                lightUp(node)
                walk(node)
                jump(node)
                turnLeft(node)
                turnRight(node)
                closedList.append(node)

    stopTime = time.time()
    executionTime = stopTime - startTime
    print("Execution time: ", executionTime)
    print("Depth: ", depth)
    if sucess == True:
        getPath(solutionNode)
        print('Path: ', pathList)