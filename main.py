import pygame
from util import DIALOG, Button, Gap
#from editor import Editor # TODO: make the editor and implement it

pygame.init()

class Main:
    def __init__(self):
        self.WIN = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    def __call__(self):
        choose = DIALOG(self.WIN, self.clock, 
                     [
                         Button(self.WIN, 'Editor', (255, 0, 0), (255, 255, 255), 100, roundness=10), 
                         Gap(0, 2),
                         Button(self.WIN, 'Sample button', (0, 255, 0), (255, 255, 255), 100, roundness=10)
                     ], 10, 10)
        #if choose.txt == 'Editor':
        #    Editor(self.WIN, self.clock)()
        

if __name__ == '__main__':
    m = Main()
    while True:
        m()
