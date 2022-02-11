from Node import *
from Robot import *
from copy import deepcopy
from queue import Queue #Queue é um método FIFO (First In First Out)
import time


############################# INICIO ##############################
bfs = open('1_breadth.txt', 'w')
tree = open('1_breadth-tree.txt','w')
counter = 0  # Counter que foi usado para o printState
iterationCounter = 0  # Counter que foi usado para printar iterações
pathList = []  # Lista de Abertos
hashClosedList = [] # Lista hash que irá guardar os estados já visitados
closedList = []  # Lista de fechados
openList = Queue()  # Queue é um método FIFO (First In First Out)
iterationCounter = 2
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
####################################################################


########################### CAMINHO ################################
# Função que irá percorrer o caminho da solução
def getPath(node):
    global pathList
    pathList.append(node)
    auxNode = node.getNodeFather()
    while auxNode != None:
        pathList.append(auxNode)
        auxNode = auxNode.getNodeFather()
    pathList.reverse()

#Printa a primeira iteração
def printFirstIteration():  # Função para printar a iteração inicial com nó raiz
    stringOpen = str((3, 7, 0, 2, True, False))
    stringClosed = ''
    print('--', str(1) + 'º', 'Iteração')
    print('--', 'Abertos:', stringOpen)
    print('--', 'Fechados:', stringClosed)
    print('------------------------------------------------------')

    bfs.write('--' + str(1) + 'º' + 'Iteração' + '\n')
    bfs.write('--' + 'Abertos:' + str(stringOpen) + '\n')
    bfs.write('--' + 'Fechados:' + str(stringClosed + '\n'))
    bfs.write(('------------------------------------------------------') + '\n')

#Printa a lista de abertos e fechados
def printLists():
    global iterationCounter
    print('--', str(iterationCounter) + 'º', 'Iteração')
    bfs.write('--' + str(iterationCounter) + 'º' + 'Iteração' + '\n')

    i = 0
    j = 0
    stringOpen = ''
    stringClosed = ''
    for i in range(openList.qsize()):
        if i == 0:  # Primeiro elemento da lista de abertos
            stringOpen = str(openList.queue[i].robot.returnState())
        else:  # Restante dos elementos da lista de abertos
            stringOpen = stringOpen + ',' + \
                str(openList.queue[i].robot.returnState())
    for j in range(len(closedList)):
        if j == 0:  # Primeiro elemento da lista de fechados
            stringClosed = str(closedList[j].robot.returnState())
        else:  # Restante dos elementos da lista de fechados
            stringClosed = stringClosed + ',' + \
                str(closedList[j].robot.returnState())
    print('--', 'Abertos:', stringOpen)
    print('--', 'Fechados:', stringClosed)
    print('------------------------------------------------------')

    bfs.write('--' + 'Abertos:' + str(stringOpen) + '\n')
    bfs.write('--' + 'Fechados:' + str(stringClosed) + '\n')
    bfs.write('------------------------------------------------------' + '\n')

    iterationCounter += 1

# Função que servirá pra imprimir o caminho solução
def solutionPathPrint(node):
    getPath(node)
    count = 0
    for robotState in pathList:
        print('--', str(count) + 'º', 'Estado')
        print('| Primeiro bloco azul =', robotState.robot.firstBlueBlock,
              '| Segundo bloco azul =', robotState.robot.secondBlueBlock,
              '| x =', robotState.robot.x, '| y =', robotState.robot.y,
              '| Direção =', turn_rule[robotState.robot.direction], '| Altura =', robotState.robot.height, '|')

        bfs.write('--' + str(count) + 'º' + 'Estado' + '\n')
        bfs.write('| Primeiro bloco azul =' + str(robotState.robot.firstBlueBlock) +
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

# Função que irá gerar um nó filho acendendo um bloco azul
def lightUp(node):
    global openList
    copyState = deepcopy(node.robot) #Copia o estado para altera-lo
    verify = True #Booleano pra verificar repetição, se já existe esse nó filho na lista de fechados
    if checkLight(node) == True:    
        copyState.secondBlueBlock = not copyState.secondBlueBlock #altera o estado do robô
        auxNode = Node(node, copyState) #Cria um nó filho com o estado alterado
        verify = checkHash(auxNode) #Verifica se já existe esse nó filho na lista de fechados
        if verify == False:
            node.setRobotLightUp(auxNode) #seta o nó filho com o estado alterado
            openList.put(auxNode)  #incrementa lista de abertos
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
                node.setRobotWalk(auxNode)
                openList.put(auxNode)


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
                node.setRobotJump(auxNode)
                openList.put(auxNode)

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
        node.setRobotTurnLeft(auxNode)
        openList.put(auxNode)
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
        node.setRobotTurnLeft(auxNode)
        openList.put(auxNode)
####################################################################


def appendTree(nodeFather, nodeChild):
    if nodeFather:
        # A posição na lista é o identificador do nó
        indexFather = closedList.index(nodeFather)
        indexChild = closedList.index(nodeChild)
        #  Escreva adjacência na lista
        tree.write(str(indexFather) + " -> " + str(indexChild) + ";\n")

# Função que irá realizar a busca em largura
def breadthSearch(initialState, finalState): #Fizemos o código com base no que estava nos slides
    global closedList
    global openList
    global pathList
    sucess = False
    failure = False
    solutionNode = None
    root = Node(None, initialState)
    openList.put(root)
    startTime = time.time()
    printFirstIteration()
    while failure == False and sucess == False: #loop da busca
        if openList.empty() == True: #se a lista ficou vazia, não achou solução
            failure = True
            break
        else:
            node = openList.get()  # Metodo get() com Queue retira e retorna o primeiro elemento da fila
            robotState = (node.robot.x, node.robot.y, node.robot.direction,
                          node.robot.height, node.robot.firstBlueBlock, node.robot.secondBlueBlock)
            final_State = (finalState.x, finalState.y, finalState.direction,
                           finalState.height, finalState.firstBlueBlock, finalState.secondBlueBlock)
            if(robotState == final_State):
                sucess = True
                solutionNode = node
                closedList.append(node)
                appendTree(node.getNodeFather(),node)
                break
            else:
                lightUp(node)
                walk(node)
                jump(node)
                turnLeft(node)
                turnRight(node)
                hashNode = hash(robotState)
                closedList.append(node)
                hashClosedList.append(hashNode)
                appendTree(node.getNodeFather(),node)
        printLists()

    stopTime = time.time()
    executionTime = stopTime - startTime

    tree.close()
    if sucess == True:
        print('-->Caminho da Solução:')
        bfs.write('-->Caminho da Solução:' + '\n')
        solutionPathPrint(solutionNode)
        print("-->Tempo:", executionTime)
        bfs.write("-->Tempo: " + str(executionTime) + '\n')
        bfs.close()
    else:
        print("--> Tempo:", executionTime)
        print("Não foi possível encontrar a solução")

        bfs.write("-->Tempo: " + str(executionTime) + '\n')
        bfs.write("Não foi possível encontrar a solução \n")

        bfs.close()
