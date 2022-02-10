from Node import *
from Robot import *
from copy import deepcopy
import time


############################# INICIO ##############################
gs = open('gs.txt', 'w')
counter = 0  # Counter que foi usado para o printState
pathList = []  # Lista de Abertos
hashClosedList = []
solutionCost = 0
iterationCounter = 2
closedList = []  # Lista de fechados
openList = []  # Queue é um método FIFO (First In First Out)

# Mapa do jogo, o valor das matrizes é a quantidade de blocos(altura)
matriz = [[0, 0, 2, 0, 0, 0, 0, 0],
          [0, 0, 2, 0, 0, 0, 0, 0],
          [0, 0, 2, 0, 0, 0, 0, 0],
          [0, 0, 4, 4, 0, 0, 0, 0],
          [0, 1, 2, 3, 0, 0, 0, 0],
          [0, 0, 3, 4, 0, 0, 0, 0],
          [0, 0, 2, 2, 0, 0, 0, 0],
          [0, 0, 0, 2, 0, 0, 0, 0]]

# Obter a direção de acordo com os valores 0,1,2,3
turn_rule = ['Norte', 'Leste', 'Sul', 'Oeste']

# Movimentos do robô para cada direção respectiva
movement = {
    0: (0, -1),  # norte
    1: (1, 0),  # leste
    2: (0, 1),  # sul
    3: (-1, 0),  # oeste
}
####################################################################


######################### AUXILIARES ###############################
# Função que irá checar se não existe repetição
def checkHash(node):
    robotState = (node.robot.x, node.robot.y, node.robot.direction,
                  node.robot.height, node.robot.firstBlueBlock, node.robot.secondBlueBlock)
    hashNode = hash(robotState)
    for hashValue in hashClosedList:
        if hashValue == hashNode:
            return True
    return False


def getEuclidean(node):
    x = node.robot.x
    y = node.robot.y
    return ((x-2)**2 + (y-0)**2)**(1/2)
####################################################################


########################### CAMINHO ################################
# Função que irá percorrer o caminho da solução
def getPath(node):
    global pathList
    global solutionCost
    pathList.append(node)
    solutionCost = node.getGreedyCost()
    auxNode = node.getNodeFather()
    while auxNode != None:
        pathList.append(auxNode)
        solutionCost = solutionCost + auxNode.getGreedyCost()
        auxNode = auxNode.getNodeFather()
    pathList.reverse()


def printFirstIteration():  # Função para printar a iteração inicial com nó raiz
    stringOpen = str((3, 7, 0, 2, True, False))
    stringClosed = ''
    print('--', str(1) + 'º', 'Iteração')
    print('--', 'Abertos:', stringOpen)
    print('--', 'Fechados:', stringClosed)
    print('------------------------------------------------------')

    gs.write('--' + str(1) + 'º' + 'Iteração' + '\n')
    gs.write('--' + 'Abertos:' + str(stringOpen) + '\n')
    gs.write('--' + 'Fechados:' + str(stringClosed + '\n'))
    gs.write(('------------------------------------------------------') + '\n')


def printLists():
    global iterationCounter
    print('--', str(iterationCounter) + 'º', 'Iteração')

    gs.write('--' + str(iterationCounter) + 'º' + 'Iteração' + '\n')

    i = 0
    j = 0
    stringOpen = ''
    stringClosed = ''
    for i in range(len(openList)):
        if i == 0:  # Primeiro elemento da lista de abertos
            stringOpen = str(openList[i].robot.returnState())
        else:  # Restante dos elementos da lista de abertos
            stringOpen = stringOpen + ',' + \
                str(openList[i].robot.returnState())
    for j in range(len(closedList)):
        if j == 0:  # Primeiro elemento da lista de fechados
            stringClosed = str(closedList[j].robot.returnState())
        else:  # Restante dos elementos da lista de fechados
            stringClosed = stringClosed + ',' + \
                str(closedList[j].robot.returnState())
    print('--', 'Abertos:', stringOpen)
    print('--', 'Fechados:', stringClosed)
    print('------------------------------------------------------')

    gs.write('--' + 'Abertos:' + str(stringOpen) + '\n')
    gs.write('--' + 'Fechados:' + str(stringClosed) + '\n')
    gs.write('------------------------------------------------------' + '\n')

    iterationCounter += 1
# Função que servirá pra imprimir o caminho solução


def solutionPathPrint(node):
    getPath(node)
    count = 1
    for robotState in pathList:
        print('--', str(count) + 'º', 'Estado')
        print('| Primeiro bloco azul =', robotState.robot.firstBlueBlock,
              '| Segundo bloco azul =', robotState.robot.secondBlueBlock,
              '| x =', robotState.robot.x, '| y =', robotState.robot.y,
              '| Direção =', turn_rule[robotState.robot.direction], '| Altura =', robotState.robot.height, '|')
        
        gs.write('--' + str(count) + 'º' + 'Estado' + '\n')
        gs.write('| Primeiro bloco azul =' + str(robotState.robot.firstBlueBlock) +
                 '| Segundo bloco azul =' + str(robotState.robot.secondBlueBlock) +
                 '| x =' + str(robotState.robot.x) + '| y =' + str(robotState.robot.y) +
                 '| Direção =' + str(turn_rule[robotState.robot.direction]) + '| Altura =' + str(robotState.robot.height) + '|' + '\n')
        
        count = count + 1
####################################################################


############################ ACENDER ###############################
# Função que irá checar se o bloco é azul
def checkLight(node):
    if(node.robot.y == 0 and node.robot.x == 2):
        return True
    return False

# Função que irá gerar um nó filho acendendo ou apagando um bloco azul


def lightUp(node):
    global openList
    copyState = deepcopy(node.robot)
    verify = True
    if checkLight(node) == True:
        if(node.robot.y == 0 and node.robot.x == 2):  # Se for o segundo bloco azul
            copyState.secondBlueBlock = not copyState.secondBlueBlock
        # Nó filho receberá os valores atualizados
        auxNode = Node(node, copyState)
        verify = checkHash(auxNode)
        if verify == False:
            auxNode.setGreedyCost(getEuclidean(auxNode))
            node.setRobotLightUp(auxNode)
            openList.append(auxNode)  # incrementa lista de abertos
####################################################################


########################## ANDAR E PULAR ###########################
# Função que irá checar qual movimento o robô irá fazer
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


# Função para checar se o robô pode ir para uma direção
def checkMovement(node):
    x = node.robot.x + movement[node.robot.direction][0]
    y = node.robot.y + movement[node.robot.direction][1]
    if (x < 0 or x > 7):
        return False
    if (y < 0 or y > 7):
        return False
    return True


def walk(node):
    global openList
    copyState = deepcopy(node.robot)
    verify = True
    if (checkMovement(node) == True):
        copyState.x = copyState.x + movement[node.robot.direction][0]
        copyState.y = copyState.y + movement[node.robot.direction][1]
        auxNode = Node(node, copyState)
        verify = checkHash(auxNode)
        if (verify == False):  # Se não existe repetição
            if (getMovement(node) == 'walk'):  # Verifica qual movimento fazer
                auxNode.setGreedyCost(getEuclidean(auxNode))  # Calcula o custo
                node.setRobotWalk(auxNode)
                openList.append(auxNode)


def jump(node):
    global openList
    copyStateJump = deepcopy(node.robot)
    verify = True
    if (checkMovement(node) == True):
        copyStateJump.x = copyStateJump.x + movement[node.robot.direction][0]
        copyStateJump.y = copyStateJump.y + movement[node.robot.direction][1]
        copyStateJump.height = matriz[copyStateJump.y][copyStateJump.x]
        auxNode = Node(node, copyStateJump)
        verify = checkHash(auxNode)
        if (verify == False):  # Se não existe repetição
            if (getMovement(node) == 'jump'):  # Verifica qual movimento fazer
                auxNode.setGreedyCost(getEuclidean(auxNode))
                node.setRobotJump(auxNode)
                openList.append(auxNode)

####################################################################


####################### VIRAR PARA ESQUERDA ########################
# Função que irá gerar um nó filho com a direção do robô virado para a esquerda
def turnLeft(node):
    global openList
    copyState = deepcopy(node.robot)
    verify = True  # Considero que existe repetição
    copyState.direction = (copyState.direction - 1) % 4
    auxNode = Node(node, copyState)
    verify = checkHash(auxNode)  # Irá checar se não existe repetição
    if (verify == False):  # Se não existe repetição
        auxNode.setGreedyCost(getEuclidean(auxNode))
        node.setRobotTurnLeft(auxNode)
        openList.append(auxNode)
####################################################################


####################### VIRAR PARA DIREITA #########################
# Função que irá gerar um nó filho com a direção do robô virado para a direita
def turnRight(node):
    global openList
    copyState = deepcopy(node.robot)
    verify = True
    copyState.direction = (copyState.direction + 1) % 4
    auxNode = Node(node, copyState)
    verify = checkHash(auxNode)
    if (verify == False):
        auxNode.setGreedyCost(getEuclidean(auxNode))
        node.setRobotTurnLeft(auxNode)
        openList.append(auxNode)
####################################################################


# Função que irá realizar a busca gulosa
def greedySearch(initialState, finalState):
    global closedList
    global openList
    global pathList
    sucess = False
    failure = False
    solutionNode = None
    root = Node(None, initialState)
    openList.append(root)
    root.setGreedyCost(0)
    startTime = time.time()
    printFirstIteration()
    while failure == False and sucess == False:
        if len(openList) == 0:
            failure = True
            break
        else:
            i = 0
            j = 0
            lower = -1
            for i in range(len(openList)):
                if openList[i].getGreedyCost() < lower or lower == -1:
                    lower = openList[i].getGreedyCost()

            for j in range(len(openList)):
                if openList[j].getGreedyCost() == lower:
                    node = openList.pop(j)
                    break

            robotState = (node.robot.x, node.robot.y, node.robot.direction,
                          node.robot.height, node.robot.firstBlueBlock, node.robot.secondBlueBlock)
            final_State = (finalState.x, finalState.y, finalState.direction,
                           finalState.height, finalState.firstBlueBlock, finalState.secondBlueBlock)
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
                closedList.append(node)
                hashClosedList.append(hashNode)
        printLists()

    stopTime = time.time()
    executionTime = stopTime - startTime

    if sucess == True:
        print("-->Tempo:", executionTime)
        print('-->Custo Guloso:', "{:.2f}".format(solutionCost))
        print('-->Caminho da Solução:')
        gs.write('-->Caminho da Solução:' + '\n')
        solutionPathPrint(solutionNode)

        val = "{:.2f}".format(solutionCost)

        gs.write("-->Tempo: " + str(executionTime) + '\n')
        gs.write('-->Custo Guloso:'+ val + '\n')

        gs.close()
    else:
        print("--> Tempo:", executionTime)
        print("Não foi possível encontrar a solução")

        gs.write("-->Tempo: " + str(executionTime) + '\n')
        gs.write("Não foi possível encontrar a solução \n")

        gs.close()
