try:
    from util.text import *
except ImportError:
    from text import *

import pygame
pygame.init()

class Button:
    def __init__(self, screen, txt, colour, txtcolour=(255, 255, 255), max_width=100, font=pygame.font.Font(None, 24), roundness=8):
        self.screen = screen
        self.roundness = roundness
        self.colour = colour
        self.max_width = max_width
        self.txt = txt
        self.font = font
        self.txtcolour = txtcolour
        c = screen.copy()
        self.update(0, 0)
        screen = c
    
    def __str__(self):
        return 'Button saying "%s"' % self.txt
    
    def __repr__(self):
        return str(self)
    
    def update(self, x, y):
        """
        draws the button to the screen, and returns whether the user has their mouse over it. So if the mousedown is also there, then they clicked it.

        Returns
        -------
        bool
            whether or not the user has their mouse ___***OVER***___ the button, NOT CLICKED.
        """
        lines = [self.font.render(line, True, self.txtcolour) for line in renderTextCenteredAt(self.txt, self.font, self.max_width)]

        self.nsurface = pygame.Surface((max([i.get_width() for i in lines])+20, sum([i.get_height() for i in lines])+(len(lines)+1)*10))
        col = (self.txtcolour[0], self.txtcolour[1], (self.txtcolour[2]+1 if self.txtcolour[2] < 255 else self.txtcolour[2]-1))
        self.nsurface.fill(col)
        top = 10
        for i in lines:
            self.nsurface.blit(i, (10, top))
            top += i.get_height()+10

        btn = pygame.Rect(x, y, *self.nsurface.get_size())
        pygame.draw.rect(self.screen, self.colour, btn, border_radius=self.roundness)
        self.screen.blit(self.nsurface, (x, y))
        return btn.collidepoint(pygame.mouse.get_pos())
