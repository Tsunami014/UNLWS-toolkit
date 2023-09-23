import pygame
try:
    from util.button import Button
    from util.glyphs import get_glyph
except:
    from button import Button
    from glyphs import get_glyph

class Glyph: # for each glyph, -5 to x and y. That's how it is rendered.
    def __init__(self, name): #TODO: drag glyphs
        self.sur = get_glyph(name)

    def __call__(self, screen, x, y):
        screen.blit(self.sur, (x-5, y-5))

class Editor:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
    
    def __call__(self):
        run = True
        sidebarScroll = 0
        mainScroll = 0
        btns = [Button(self.screen, 'hi', (255, 0, 125))]
        items = [Glyph('thou'), Glyph('You')]
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
                items[it](self.screen, 20, it*100+sidebarScroll)
            pygame.display.update()
            self.clock.tick(60)
