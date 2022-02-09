#classe de estado do problema
class State:
    def __init__(self, blue_blocks, robot):
        self.blue_blocks = blue_blocks
        self.robot = robot
    
    def hash(self):
        return hash(( self.robot, hash(tuple(self.blue_blocks.values())) ))
    
    '''
    
    def jump(self):
        pass

    def turn_on(self):
        key = f"{self.robot.x} {self.robot.y}"
        # se a posicao atual do robo é um bloco azul, o bloco recebe a negação dele mesmo ou seja se True -> False e se False -> True
        if (key in self.blue_blocks):
            self.blue_blocks[key] = not self.blue_blocks[key]
            return True
        return False

    def walk(self):

        pass

    def turn_right(self):
        self.robot.direction = (self.robot.direction + 1) % 4
        return True

    def turn_left(self):
        self.robot.direction = (self.robot.direction - 1) % 4
        return True

    def make_transition(self, index):
        transitions = [self.jump, self.turn_on, self.walk, self.turn_right, self.turn_left]
        transition = transitions[index]
        transition(self)
    
    
    def __hash__(self):
        return hash(( self.robot, hash(tuple(self.blue_blocks.values())) ))
    
    ##Verifica se o estado atual é solução
    def is_solution(self, currentState):
        if currentState == final_state:
            return True
        return False
    '''