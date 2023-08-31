import pygame

class Button:
    def __init__(self, screen, txt, colour, txtcolour=(255, 255, 255), font=pygame.font.Font(None, 24), roundness=8):
        self.screen = screen
        self.button = pygame.Rect(400, 560, 200, 30)
        self.roundness = roundness
        self.colour = colour
        self.txt = txt
        self.text = font.render(txt, True, txtcolour)
    
    def __str__(self):
        return 'Button saying "%s"' % self.txt
    
    def __repr__(self):
        return str(self)
    
    def update(self):
        """
        draws the button to the screen, and returns whether the user has their mouse over it. So if the mousedown is also there, then they clicked it.

        Returns
        -------
        bool
            whether or not the user has their mouse ___***OVER***___ the button, NOT CLICKED.
        """
        pygame.draw.rect(self.screen, self.colour, self.button, border_radius=self.roundness)
        self.screen.blit(self.text, (self.button.centerx - 45, self.button.centery - 10))
        return self.button.collidepoint(pygame.mouse.get_pos())
