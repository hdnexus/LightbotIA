from copy import deepcopy
from Node import *
from Robot import *
from State import *
from breadthFirstSearch import breadthSearch
from orderedSearch import orderedSearch
from depthFirstSearch import depthSearch
from greedySearch import greedySearch
from aStarSearch import aStarSearch 

#Estado inicial do problema
initial_state = Robot(3,7,0,2,False,False)
#Estado final do problema (estado solução)
final_state = Robot(2,0,0,2,True,True)


def searchSelection():
    choice = int(input('-> Digite o número da busca desejada: '))
    while choice != 6:
        if choice == 1:
            breadthSearch(initial_state, final_state)
        elif choice == 2:
            depthSearch(initial_state, final_state)
        elif choice == 3:
            orderedSearch(initial_state, final_state)
        elif choice == 4:
            greedySearch(initial_state, final_state)
        elif choice == 5:
            aStarSearch(initial_state, final_state)
        else:
            print('Opção inválida!')
            print('')
            print('**Tente um valor válido, olhe as opções disponíveis no menu novamente!**')	
        printMenu()
        choice = int(input('-> Digite o número da busca desejada: '))

def printMenu():
    print('- Opções de busca -')
    print('1. Busca em largura')
    print('2. Busca em profundidade')
    print('3. Busca ordenada')
    print('4. Busca Gulosa')
    print('5. Busca A*')
    print('6. Sair')



def main():
    printMenu()
    searchSelection()

main()