try:
    from util.text import *
except ImportError:
    from text import *

import pygame
pygame.init()

class Gap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nsurface = pygame.Surface((width, height))
    
    def update(self, x, y):
        return False

class Button:
    def __init__(self, screen, txt, colour, txtcolour=(255, 255, 255), max_width=100, font=pygame.font.Font(None, 24), roundness=8):
        self.roundness = roundness
        self.colour = colour
        self.max_width = max_width
        self.txt = txt
        self.font = font
        self.txtcolour = txtcolour
        self.screen = pygame.Surface((0, 0))
        self.update(0, 0)
        self.screen = screen
    
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

        self.nsurface = pygame.Surface((max([i.get_width() for i in lines]), sum([i.get_height() for i in lines])+(len(lines)-1)*10))
        self.nsurface.fill(self.colour)
        top = 0
        for i in lines:
            self.nsurface.blit(i, (0, top))
            top += i.get_height()+10

        btn = pygame.Rect(x, y, self.nsurface.get_width() + 20, self.nsurface.get_height() + 20)
        pygame.draw.rect(self.screen, self.colour, btn, border_radius=self.roundness)
        self.screen.blit(self.nsurface, (x+10, y+10))
        return btn.collidepoint(pygame.mouse.get_pos())
