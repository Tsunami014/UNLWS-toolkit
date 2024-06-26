import pygame, math
from util.button import Button
from util.glyphs import RelLine, getAllGlyphs

SPACING = 24
GLYPHSZE = 100 + SPACING

def DistanceToBox(r, p):
	if p[0] > r[2]:
		xdist = p[0] - r[2]
	elif p[0] < r[0]:
		xdist = r[0] - p[0]
	else:
		xdist = 0
	if p[1] > r[3]:
		ydist = p[1] - r[3]
	elif p[1] < r[1]:
		ydist = r[1] - p[1]
	else:
		ydist = 0
	return xdist + ydist

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
        relLines = []
        holding = None
        while run:
            self.screen.fill((0, 0, 0))
            sidebar_w = 20/100 * self.screen.get_width()

            updates = [btns[i].update(200, 0 + sum([btns[j].nsurface.get_height() + 20 for j in range(i)])) for i in range(len(btns))]
            
            shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    elif (not shift) and holding is not None and holding[0] != -1:
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            g = onscreens[holding[0]]
                            g.rotate(g.rotation - 45)
                            bps = g.getBps((0, 0), GLYPHSZE)
                            mpos = pygame.mouse.get_pos()
                            onscreens[holding[0]].moveto(mpos[0] - bps[holding[1]][0], mpos[1] - bps[holding[1]][1])
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            g = onscreens[holding[0]]
                            g.rotate(g.rotation + 45)
                            bps = g.getBps((0, 0), GLYPHSZE)
                            mpos = pygame.mouse.get_pos()
                            onscreens[holding[0]].moveto(mpos[0] - bps[holding[1]][0], mpos[1] - bps[holding[1]][1])
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
            ks = pygame.key.get_pressed()
            keys = [(ks[pygame.K_RIGHT] or ks[pygame.K_d]), (ks[pygame.K_LEFT] or ks[pygame.K_a])]
            if (holding is not None) and shift and any(keys):
                g = onscreens[holding[0]]
                g.rotate(g.rotation + 2 * (1 if keys[0] else -1))
                bps = g.getBps((0, 0), GLYPHSZE)
                mpos = pygame.mouse.get_pos()
                onscreens[holding[0]].moveto(mpos[0] - bps[holding[1]][0], mpos[1] - bps[holding[1]][1])
            
            ClosestCollBp = None
            for it in onscreens:
                if holding is not None and holding[0] == onscreens.index(it):
                    continue
                r = it.getRect(GLYPHSZE-SPACING, SPACING)
                mpos = pygame.mouse.get_pos()
                collides = r.collidepoint(mpos)
                it.draw(self.screen, (10, 255, 125), GLYPHSZE-SPACING, dotColours=(90, 255, 200), show_bps=collides, highlight=((255,228,181) if collides else None))
                collidingBp = None
                if collides:
                    bps = it.getBps(it.position, GLYPHSZE-SPACING)
                    for b in range(len(bps)):
                        if abs(mpos[0] - bps[b][0]) + abs(mpos[1] - bps[b][1]) < 12:
                            pygame.draw.circle(self.screen, (10, 125, 255), bps[b], 15)
                            collidingBp = b
                            break
                if collidingBp is not None and pygame.mouse.get_pressed()[0] and holding is None:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        ln = RelLine([bps[collidingBp], pygame.mouse.get_pos()])
                        ln.connections = {0: (it, collidingBp)}
                        it.connections[collidingBp] = (ln, 0)
                        relLines.append(ln)
                        holding = (-1, ln)
                    else:
                        holding = (onscreens.index(it), collidingBp)
                elif collidingBp is not None:
                    ClosestCollBp = (it, collidingBp, bps[collidingBp])
            
            for li in relLines:
                if holding is None or li != holding[1]:
                    mpos = pygame.mouse.get_pos()
                    lps = li.points
                    if lps[0] == lps[1]:
                        collides = abs(mpos[0] - lps[0][0]) + abs(mpos[1] - lps[0][1]) < 8
                    else:
                        nom = abs((lps[1][0]-lps[0][0])*(lps[0][1]-mpos[1])-(lps[0][0]-mpos[0])*(lps[1][1]-lps[0][1])) # Thanks to https://stackoverflow.com/questions/66424638/find-point-distance-from-line-python
                        denom = math.sqrt((lps[1][0]-lps[0][0])**2+(lps[1][1]-lps[0][1])**2)
                        bdist = DistanceToBox((*lps[0], *lps[1]), mpos)
                        if bdist != 0:
                            dist = (nom/denom + bdist) / 2
                        else:
                            dist = nom/denom
                        collides = dist < 8
                    li.draw(self.screen, (10, 255, 125), dotColours=(90, 255, 200), show_bps=collides, highlight=((255,228,181) if collides else None))
                    collidingBp = None
                    if collides:
                        i = 0
                        for b in li.getBps():
                            if abs(mpos[0] - b[0]) + abs(mpos[1] - b[1]) < 12:
                                pygame.draw.circle(self.screen, (10, 125, 255), b, 15)
                                collidingBp = b
                                ClosestCollBp = (li, i, b)
                                break
                            i += 1
                    if collidingBp is not None and holding is not None and pygame.mouse.get_pressed()[0]:
                        if b == li.points[0]:
                            li.points.reverse()
                            li.connections = {1-i: li.connections[i] for i in li.connections}
                            holding = (-1, li)
            
            in_bar = pygame.mouse.get_pos()[0] < sidebar_w
            
            pygame.draw.rect(self.screen, (120, 120, 120), (0, 0, sidebar_w, self.screen.get_height()))
            
            for it in range(len(items)):
                pos = (20, it*120+sidebarScroll+20)
                items[it].connections = {}
                items[it].moveto(pos[0] + SPACING/2, pos[1] + SPACING/2)
                r = items[it].getRect(GLYPHSZE-SPACING, SPACING)
                mpos = pygame.mouse.get_pos()
                collides = r.collidepoint(mpos) and holding is None
                items[it].draw(self.screen, (10, 255, 125), GLYPHSZE-SPACING, dotColours=(90, 255, 200), show_bps=collides, highlight=((255,228,181) if collides else None))
                collidingBp = None
                if collides:
                    bps = items[it].getBps(items[it].position, GLYPHSZE-SPACING)
                    for b in range(len(bps)):
                        if abs(mpos[0] - bps[b][0]) + abs(mpos[1] - bps[b][1]) < 12:
                            pygame.draw.circle(self.screen, (10, 125, 255), bps[b], 15)
                            collidingBp = b
                            break
                if collidingBp is not None and pygame.mouse.get_pressed()[0]:
                    bps = items[it].getBps((0, 0), GLYPHSZE)
                    newg = items[it].copy()
                    newg.moveto(mpos[0] - bps[collidingBp][0], mpos[1] - bps[collidingBp][1])
                    onscreens.append(newg)
                    holding = (len(onscreens)-1, collidingBp)
            
            if holding is not None:
                if holding[0] == -1:
                    if 1 in holding[1].connections:
                        holding[1].connections[1][0].connections.pop(holding[1].connections[1][1])
                        holding[1].connections.pop(1)
                    holding[1].draw(self.screen, (10, 255, 125), dotColours=(90, 255, 200), show_bps=collides, highlight=((255,228,181) if collides else None))
                    pygame.draw.circle(self.screen, (10, 125, 255), holding[1].getBps()[1], 15)
                    holding[1].points[1] = pygame.mouse.get_pos()
                    if not pygame.mouse.get_pressed()[0]:
                        if ClosestCollBp is not None: # From the item check for all ones in the editor area
                            holding[1].connections[1] = (ClosestCollBp[0], ClosestCollBp[1])
                            ClosestCollBp[0].connections[ClosestCollBp[1]] = (holding[1], 1)
                            holding[1].points[1] = ClosestCollBp[2]
                        holding = None
                else:
                    if in_bar:
                        pygame.draw.rect(self.screen, (255, 50, 90), (0, 0, sidebar_w + 1, self.screen.get_height()))
                    it = onscreens[holding[0]]
                    if holding[1] in it.connections:
                        it.connections[holding[1]][0].connections.pop(it.connections[holding[1]][1])
                        it.connections.pop(holding[1])
                    bps = it.getBps((0, 0), GLYPHSZE-SPACING)
                    mpos = pygame.mouse.get_pos()
                    it.moveto(mpos[0] - bps[holding[1]][0], mpos[1] - bps[holding[1]][1])
                    it.draw(self.screen, (10, 255, 125), GLYPHSZE-SPACING, show_bps=False, highlight=(255,228,181))
                    pygame.draw.circle(self.screen, (10, 255, 125), (it.position[0] + bps[holding[1]][0], it.position[1] + bps[holding[1]][1]), 15)
                    if not pygame.mouse.get_pressed()[0]:
                        if in_bar:
                            onscreens.pop(holding[0])
                        else:
                            if ClosestCollBp is not None: # From the item check for all ones in the editor area
                                it.connections[holding[1]] = (ClosestCollBp[0], ClosestCollBp[1])
                                ClosestCollBp[0].connections[ClosestCollBp[1]] = (it, holding[1])
                                it.moveto(ClosestCollBp[2][0] - bps[holding[1]][0], ClosestCollBp[2][1] - bps[holding[1]][1])
                        holding = None
            pygame.display.update()
            self.clock.tick(60)
