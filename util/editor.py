import pygame
from util.button import Button
from util.glyphs import getAllGlyphs

class Editor:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
    
    def __call__(self):
        run = True
        sidebarScroll = 0
        mainScroll = 0
        btns = [Button(self.screen, 'hi', (255, 0, 125))]
        alls = getAllGlyphs()
        items = [alls[i] for i in alls]
        while run:
            self.screen.fill((0, 0, 0))
            sidebar_w = 20/100 * self.screen.get_width()
            pygame.draw.rect(self.screen, (120, 120, 120), (0, 0, sidebar_w, self.screen.get_height()))

            updates = [btns[i].update(200, 0 + sum([btns[j].nsurface.get_height() + 20 for j in range(i)])) for i in range(len(btns))]
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for i in [btns[j] for j in range(len(btns)) if updates[j]]:
                            print(i)
            for it in range(len(items)):
                items[it].draw(self.screen, (10, 255, 125), (20, it*100+sidebarScroll), 100)
            pygame.display.update()
            self.clock.tick(60)
