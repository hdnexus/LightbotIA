#classe do robô
class Robot:
    def __init__(self, x, y, direction, height, firstBlueBlock, secondBlueBlock):
        self.x = x
        self.y = y
        self.direction = direction
        self.height = height
        self.firstBlueBlock = firstBlueBlock
        self.secondBlueBlock = secondBlueBlock
    
    def returnState(self):
        return (self.x, self.y, self.direction, self.height, self.firstBlueBlock, self.secondBlueBlock)
    

