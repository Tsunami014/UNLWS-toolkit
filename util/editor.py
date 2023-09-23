import pygame
try:
    from util.button import Button
except:
    from button import Button

class Editor:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
    
    def __call__(self):
        run = True
        sidebarScroll = 0
        mainScroll = 0
        btns = [Button(self.screen, 'hi', (255, 0, 125))]
        items = []
        while run:
            self.screen.fill((0, 0, 0))
            sidebar_w = 20/100 * self.screen.get_width()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                elif event.type == pygame.MOUSEWHEEL:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < sidebar_w:
                        sidebarScroll += event.y
                    else:
                        mainScroll += event.y
            pygame.draw.rect(self.screen, (120, 120, 120), (0, 0, sidebar_w, self.screen.get_height()))
            pygame.display.update()
            self.clock.tick(60)
