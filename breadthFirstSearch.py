from Node import *
from State import *
from Robot import *
from copy import deepcopy
from queue import Queue
import time


############################# INICIO ##############################
counter = 0 #Counter que foi usado para o printState
depth = 0 #Profundidade
pathList = [] #Lista de Abertos
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
def checkRepetition(node):
    global closedList
    for auxNode in closedList:
        if auxNode == node:
            return True
    return False

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
    if(state.blue_blocks['3 7']):
        firstBlueBlock = 'Ligado'
    if(state.blue_blocks['2 0']):
        secondBlueBlock = 'Ligado'
    global counter 
    counter = counter + 1
    print('--',str(counter) + 'º', 'Estado')
    print('| Primeiro bloco azul =', firstBlueBlock,
    '| Segundo bloco azul =', secondBlueBlock, 
    '| x =', state.robot.x, '| y =', state.robot.y, 
    '| Direção =', turn_rule[state.robot.direction], '| Altura =',state.robot.height, '|')
####################################################################


############################ ACENDER ############################### 
#Função que irá checar se o bloco é azul esta aceso ou não
def checkLight(node): 
    key = f"{node.state.robot.x} {node.state.robot.y}"
        # se a posicao atual do robo é um bloco azul, o bloco recebe a negação dele mesmo ou seja se True -> False e se False -> True
    if (key in node.state.blue_blocks):
        return True
    return False

#Função que irá gerar um nó filho acendendo ou apagando um bloco azul
def lightUp(node):
    global depth
    global openList
    key = f"{node.state.robot.x} {node.state.robot.y}"
    copyState = deepcopy(node.state)
    verify = True
    if checkLight(node) == True:
        copyState.blue_blocks[key] = not copyState.blue_blocks[key]
        auxNode = Node(node, copyState)
        #printState(auxNode.state)
        auxNode.setCost(node.getCost() + 1) 
        verify = checkRepetition(auxNode)
        if verify == False:
            node.setRobotLightUp(auxNode)
            if depth < auxNode.getCost():
                depth = auxNode.getCost()
            openList.put(auxNode) #incrementa lista de abertos 
#################################################################### 


########################## ANDAR E PULAR ########################### 
#Função que irá checar qual movimento o robô irá fazer
def getMovement(node):
    print('entrou getmovement')
    x = node.state.robot.x + movement[node.state.robot.direction][0]
    y = node.state.robot.y + movement[node.state.robot.direction][1]
    height = node.state.robot.height
    nextHeight = matriz[y][x]
    print("Altura do robô: ", height)
    print("Altura do bloco: ", nextHeight)
    if (nextHeight == 0):
        return 'cant'
    if (height == nextHeight):
        return 'walk'
    if(nextHeight - height == 1 or nextHeight - height <= -1):
        return 'jump'
        

#Função para checar se o robô pode ir para uma direção
def checkMovement(node):
    x = node.state.robot.x + movement[node.state.robot.direction][0]
    y = node.state.robot.y + movement[node.state.robot.direction][1]
    if (x < 0 or x > 7):
        return False
    if (y < 0 or y > 7):
        return False
    return True


def walk(node):
    global depth
    global openList
    copyState = deepcopy(node.state)
    verify = True
    copyState.robot.x = copyState.robot.x + movement[node.state.robot.direction][0]
    copyState.robot.y = copyState.robot.y + movement[node.state.robot.direction][1]
    if (checkMovement(node) == True):
        auxNode = Node(node, copyState)
        auxNode.setCost(node.getCost() + 1) 
        verify = checkRepetition(auxNode)
        if (verify == False): #Se não existe repetição
            if (getMovement(node) == 'walk'): #Verifica qual movimento fazer
                print('Andou:')
                node.setRobotWalk(auxNode)
                if depth < auxNode.getCost():
                    depth = auxNode.getCost()
                openList.put(auxNode)
                print('Quantidade de abertos walk:')
                print(openList.qsize())
                

def jump(node):
    global depth
    global openList
    copyStateJump = deepcopy(node.state)
    verify = True
    copyStateJump.robot.x = copyStateJump.robot.x + movement[node.state.robot.direction][0]
    copyStateJump.robot.y = copyStateJump.robot.y + movement[node.state.robot.direction][1]
    copyStateJump.robot.height = matriz[copyStateJump.robot.y][copyStateJump.robot.x]
    if (checkMovement(node) == True):
        auxNode = Node(node, copyStateJump)
        auxNode.setCost(node.getCost() + 1) 
        verify = checkRepetition(auxNode)
        if (verify == False): #Se não existe repetição
            if (getMovement(node) == 'jump'): #Verifica qual movimento fazer
                print('Pulou:')
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
    copyState = deepcopy(node.state)
    verify = True #Considero que existe repetição 
    copyState.robot.direction = (copyState.robot.direction - 1) % 4
    auxNode = Node(node, copyState)
    verify = checkRepetition(auxNode) #Irá checar se não existe repetição
    if (verify == False): #Se não existe repetição
        auxNode.setCost(node.getCost() + 1)
        printState(auxNode.state)
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
    copyState = deepcopy(node.state)
    verify = True
    copyState.robot.direction = (copyState.robot.direction + 1) % 4
    auxNode = Node(node, copyState)
    verify = checkRepetition(auxNode)
    if (verify == False):
        auxNode.setCost(node.getCost() + 1)
        printState(auxNode.state)
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
    c = 0
    while failure == False and sucess == False:
        if openList.empty() == True:
            print('Entrou aqui!')
            failure = True
            break
        else:
            print('Quantidade de abertos:')
            print(openList.qsize())
            node = openList.get() #Metodo get() retira e retorna o primeiro elemento da fila
            printState(node.state)
            print('Estado do robô andar: ')
            print(node.getRobotWalk()) 
            print('Quantidade de abertos depois:')
            print(openList.qsize())
            if(node == finalState):
                sucess = True
                solutionNode = node
            else:
                lightUp(node)
                #walk(node)
                #jump(node)
                #turnLeft(node)
                #turnRight(node)
                closedList.append(node)
                print('Lista fechada depois:')
                print(closedList)

    stopTime = time.time()
    executionTime = stopTime - startTime

    if sucess == True:
        print("-->Tempo:", executionTime)
        print("-->Profundidade:", depth)
        getPath(solutionNode)
        print('-->Caminho da Solução:', pathList)
        print('-->Custo:', solutionNode.getCost())
        #print('-->Quantidade de estados fechados: ', len(closedList))
        #print('-->Quantidade de estados abertos: ', len(openList))
        #print('-->Lista de estados abertos: ', openList)
        #print('-->Lista de estados fechados: ', closedList)
    else:
        print("--> Tempo:", executionTime)
        print("Não foi possível encontrar a solução")

