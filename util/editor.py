import pygame
from util.button import Button
from util.glyphs import getAllGlyphs

GLYPHSZE = 100

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
        onscreens = []
        holding = None
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
                pos = (20, it*120+sidebarScroll+20)
                r = pygame.rect.Rect(*pos, GLYPHSZE, GLYPHSZE)
                mpos = pygame.mouse.get_pos()
                collides = r.collidepoint(mpos) and holding is None
                items[it].draw(self.screen, (10, 255, 125), (pos[0] + 6, pos[1] + 6), GLYPHSZE-12, dotColour=(90, 255, 200), show_bps=collides)
                collidingBp = None
                if collides:
                    bps = items[it].getBps((pos[0] + 6, pos[1] + 6), GLYPHSZE-12)
                    for b in range(len(bps)):
                        if abs(mpos[0] - bps[b][0]) + abs(mpos[1] - bps[b][1]) < 12:
                            pygame.draw.circle(self.screen, (10, 125, 255), bps[b], 15)
                            collidingBp = b
                            break
                if collidingBp is not None and pygame.mouse.get_pressed()[0]:
                    bps = items[it].getBps((0, 0), GLYPHSZE)
                    onscreens.append([items[it].copy(), (mpos[0] - bps[collidingBp][0], mpos[1] - bps[collidingBp][1])])
                    holding = (len(onscreens)-1, collidingBp)
            for it in onscreens:
                r = pygame.rect.Rect(*it[1], GLYPHSZE, GLYPHSZE)
                mpos = pygame.mouse.get_pos()
                collides = r.collidepoint(mpos) and not (holding is not None and holding[0] == onscreens.index(it))
                it[0].draw(self.screen, (10, 255, 125), (it[1][0] + 6, it[1][1] + 6), GLYPHSZE-12, dotColour=(90, 255, 200), show_bps=collides)
                collidingBp = None
                if collides:
                    bps = it[0].getBps((it[1][0] + 6, it[1][1] + 6), GLYPHSZE-12)
                    for b in range(len(bps)):
                        if abs(mpos[0] - bps[b][0]) + abs(mpos[1] - bps[b][1]) < 12:
                            pygame.draw.circle(self.screen, (10, 125, 255), bps[b], 15)
                            collidingBp = b
                            break
                if collidingBp is not None and pygame.mouse.get_pressed()[0] and holding is None:
                    holding = (onscreens.index(it), collidingBp)
            if holding is not None:
                bps = onscreens[holding[0]][0].getBps((0, 0), GLYPHSZE)
                mpos = pygame.mouse.get_pos()
                pygame.draw.circle(self.screen, (10, 125, 255), onscreens[holding[0]][0].getBps(onscreens[holding[0]][1], GLYPHSZE)[holding[1]], 15)
                onscreens[holding[0]][1] = (mpos[0] - bps[holding[1]][0], mpos[1] - bps[holding[1]][1])
                if not pygame.mouse.get_pressed()[0]:
                    holding = None
            pygame.display.update()
            self.clock.tick(60)
