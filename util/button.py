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
        txts = []
        h = 10
        for line in renderTextCenteredAt(self.txt, self.font, self.max_width):
            r = self.font.render(line, True, self.txtcolour)
            txts.append((r, (x+10, y+h)))
            h += r.get_height() + 10
        
        btn = pygame.Rect(x, y, max([i[0].get_width() for i in txts])+20, h)
        pygame.draw.rect(self.screen, self.colour, btn, border_radius=self.roundness)
        for i in txts: self.screen.blit(*i)
        return btn.collidepoint(pygame.mouse.get_pos())
