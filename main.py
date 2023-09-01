import pygame
from util import Button
#from editor import Editor # TODO: make the editor and implement it

pygame.init()

class Main:
    def __init__(self):
        self.WIN = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.btns = [Button(self.WIN, 'Hello!', (100, 255, 100)), Button(self.WIN, 'Gooooooodbye. :(', (100, 100, 255))]

    def __call__(self):
        self.WIN.fill((0, 0, 0))
        updates = [self.btns[i].update(0, i * 100) for i in range(len(self.btns))]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for i in [self.btns[j] for j in range(len(self.btns)) if updates[j]]:
                        print(i)
        pygame.display.update()
        self.clock.tick(60)

if __name__ == '__main__':
    m = Main()
    while True:
        m()
