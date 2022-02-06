#classe do robô
class Robot:
    def __init__(self, x, y, direction, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.height = height
    
    '''
    def __hash__(self):
        return hash(( self.x, self.y, self.direction, self.height ))
    '''
