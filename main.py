import pygame
#from editor import Editor # TODO: make the editor and implement it

pygame.init()

class Main:
    def __init__(self):
        self.WIN = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    def __call__(self):
        pygame.event.get()
        pygame.display.update()
        self.clock.tick(60)

if __name__ == '__main__':
    m = Main()
    while True:
        m()
