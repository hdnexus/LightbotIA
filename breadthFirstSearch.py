from Node import *
from State import *
from Robot import *
from copy import deepcopy
from queue import Queue
import time


############################# INICIO ##############################
f = open('example.txt', 'w')
counter = 0 #Counter que foi usado para o printState
depth = 0 #Profundidade
pathList = [] #Lista de Abertos
hashClosedList = []
closedList = [] #Lista de fechados
openList = Queue() #Queue é um método FIFO (First In First Out)

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
#################################################################### 


######################### AUXILIARES ############################### 
#Função que irá checar se não existe repetição
def checkHash(node):
    robotState = (node.robot.x, node.robot.y, node.robot.direction, node.robot.height, node.robot.firstBlueBlock, node.robot.secondBlueBlock)
    hashNode = hash(robotState)
    for hashValue in hashClosedList:
        if hashValue == hashNode:
            return True         
    return False
#################################################################### 


########################### CAMINHO ################################
#Função que irá percorrer o caminho da solução
def getPath(node):
    global pathList
    pathList.append(node)
    auxNode = node.getNodeFather()
    while auxNode != None:
        pathList.append(auxNode)
        auxNode = auxNode.getNodeFather()
    pathList.reverse() 

#Função que servirá pra imprimir o caminho solução
def solutionPathPrint(node):
    getPath(node)
    count = 0
    for robotState in pathList:
        print('--',str(count) + 'º', 'Estado')
        print('| Primeiro bloco azul =', robotState.robot.firstBlueBlock,
        '| Segundo bloco azul =', robotState.robot.secondBlueBlock, 
        '| x =', robotState.robot.x, '| y =', robotState.robot.y, 
        '| Direção =', turn_rule[robotState.robot.direction], '| Altura =',robotState.robot.height, '|')
        count = count + 1
####################################################################


############################ ACENDER ############################### 
#Função que irá checar se o bloco é azul
def checkLight(node): 
    if((node.robot.y == 7 and node.robot.x == 3) or (node.robot.y == 0 and node.robot.x == 2) ):
        return True
    return False

#Função que irá gerar um nó filho acendendo ou apagando um bloco azul
def lightUp(node):
    global depth
    global openList
    copyState = deepcopy(node.robot)
    verify = True
    if checkLight(node) == True:
        if(node.robot.y == 7 and node.robot.x == 3): #Se for o primeiro bloco azul
            copyState.firstBlueBlock = not copyState.firstBlueBlock
        if(node.robot.y == 0 and node.robot.x == 2): #Se for o segundo bloco azul
            copyState.secondBlueBlock = not copyState.secondBlueBlock
        auxNode = Node(node, copyState) #Nó filho receberá os valores atualizados
        verify = checkHash(auxNode)
        if verify == False:
            auxNode.setCost(node.getCost() + 1) 
            node.setRobotLightUp(auxNode)
            if depth < auxNode.getCost():
                depth = auxNode.getCost()
            openList.put(auxNode) #incrementa lista de abertos 
#################################################################### 


########################## ANDAR E PULAR ########################### 
#Função que irá checar qual movimento o robô irá fazer
def getMovement(node):
    x = node.robot.x + movement[node.robot.direction][0]
    y = node.robot.y + movement[node.robot.direction][1]
    height = node.robot.height
    nextHeight = matriz[y][x]
    if (nextHeight == 0):
        return 'cant'
    if (height == nextHeight):
        return 'walk'
    if(nextHeight - height == 1 or nextHeight - height <= -1):
        return 'jump'
        

#Função para checar se o robô pode ir para uma direção
def checkMovement(node):
    x = node.robot.x + movement[node.robot.direction][0]
    y = node.robot.y + movement[node.robot.direction][1]
    if (x < 0 or x > 7):
        return False
    if (y < 0 or y > 7):
        return False
    return True


def walk(node):
    global depth
    global openList
    copyState = deepcopy(node.robot)
    verify = True
    if (checkMovement(node) == True):
        copyState.x = copyState.x + movement[node.robot.direction][0]
        copyState.y = copyState.y + movement[node.robot.direction][1]
        auxNode = Node(node, copyState)
        
        verify = checkHash(auxNode)
        if (verify == False): #Se não existe repetição
            if (getMovement(node) == 'walk'): #Verifica qual movimento fazer
                auxNode.setCost(node.getCost() + 1) 
                node.setRobotWalk(auxNode)
                if depth < auxNode.getCost():
                    depth = auxNode.getCost()
                openList.put(auxNode)
                
                

def jump(node):
    global depth
    global openList
    copyStateJump = deepcopy(node.robot)
    verify = True
    if (checkMovement(node) == True):
        copyStateJump.x = copyStateJump.x + movement[node.robot.direction][0]
        copyStateJump.y = copyStateJump.y + movement[node.robot.direction][1]
        copyStateJump.height = matriz[copyStateJump.y][copyStateJump.x]
        auxNode = Node(node, copyStateJump)
        verify = checkHash(auxNode)
        if (verify == False): #Se não existe repetição
            if (getMovement(node) == 'jump'): #Verifica qual movimento fazer
                auxNode.setCost(node.getCost() + 1) 
                node.setRobotJump(auxNode)
                if depth < auxNode.getCost():
                    depth = auxNode.getCost()
                openList.put(auxNode)
        
####################################################################


####################### VIRAR PARA ESQUERDA ########################
#Função que irá gerar um nó filho com a direção do robô virado para a esquerda
def turnLeft(node):
    global depth
    global openList  
    copyState = deepcopy(node.robot)
    verify = True #Considero que existe repetição 
    copyState.direction = (copyState.direction - 1) % 4
    auxNode = Node(node, copyState)
    verify = checkHash(auxNode) #Irá checar se não existe repetição
    if (verify == False): #Se não existe repetição
        auxNode.setCost(node.getCost() + 1)
        node.setRobotTurnLeft(auxNode)
        if depth < auxNode.getCost():
            depth = auxNode.getCost()
        openList.put(auxNode)
####################################################################


####################### VIRAR PARA DIREITA ######################### 
#Função que irá gerar um nó filho com a direção do robô virado para a direita
def turnRight(node):
    global depth
    global openList  
    copyState = deepcopy(node.robot)
    verify = True
    copyState.direction = (copyState.direction + 1) % 4
    auxNode = Node(node, copyState)
    verify = checkHash(auxNode)
    if (verify == False):
        auxNode.setCost(node.getCost() + 1)
        node.setRobotTurnLeft(auxNode)
        if depth < auxNode.getCost():
            depth = auxNode.getCost()
        openList.put(auxNode)
####################################################################


#Função que irá realizar a busca em largura
def breadthSearch(initialState, finalState):
    global depth
    global closedList
    global openList 
    global pathList
    sucess = False
    failure = False
    solutionNode = None
    root = Node(None, initialState)
    openList.put(root) 
    root.setCost(0)
    startTime = time.time()
    while failure == False and sucess == False:
        if openList.empty() == True:
            failure = True
            break
        else:
            node = openList.get() #Metodo get() retira e retorna o primeiro elemento da fila
            robotState = (node.robot.x, node.robot.y, node.robot.direction, node.robot.height, node.robot.firstBlueBlock, node.robot.secondBlueBlock)
            final_State = (finalState.x, finalState.y, finalState.direction, finalState.height, finalState.firstBlueBlock, finalState.secondBlueBlock) 
            if(robotState == final_State):
                sucess = True
                solutionNode = node
            else:
                lightUp(node)
                walk(node)
                jump(node)
                turnLeft(node)
                turnRight(node)
                hashNode = hash(robotState)
                hashClosedList.append(hashNode)

    f.close()
    stopTime = time.time()
    executionTime = stopTime - startTime

    if sucess == True:
        print("-->Tempo:", executionTime)
        print("-->Profundidade:", depth)
        print('-->Custo:', solutionNode.getCost())
        print('-->Quantidade de estados que foram fechados: ', len(hashClosedList))
        print('-->Caminho da Solução:')
        solutionPathPrint(solutionNode)
    else:
        print("--> Tempo:", executionTime)
        print("Não foi possível encontrar a solução")

