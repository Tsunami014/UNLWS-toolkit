from util.button import *

def DIALOG(WIN, CLOCK, buttons, x, y):
    run = True
    while run:
        WIN.fill((0, 0, 0))
        updates = [buttons[i].update(x, y + sum([buttons[j].nsurface.get_height() + 20 for j in range(i)])) for i in range(len(buttons))]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for i in [buttons[j] for j in range(len(buttons)) if updates[j]]:
                        return i
        pygame.display.update()
        CLOCK.tick(60)
