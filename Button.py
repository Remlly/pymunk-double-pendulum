#%%button
import pygame
"""This file contains code from drawing a simple button"""

class button:
    """A simple press button that will execute a function"""
    def __init__(self, xy : tuple, size : tuple , colour, text : str):
        """A button is made out of a pygame rectangle, a position, contains a tekst and a
        colour"""

        self.rect = pygame.Rect(xy,size)
        self.colour = colour
        self.text = text
        self.font = pygame.font.SysFont('stylus', 25)
        self.render = self.font.render(self.text, False, (0,0,0))
        
    def draw(self,screen : pygame.surface):
        """This method will draw the shape"""
        pygame.draw.rect(screen,self.colour,self.rect)
        blit_text_at = (self.rect.centerx - self.render.get_width()/2,self.rect.centery - self.render.get_height()/2)
        screen.blit(self.render,blit_text_at)

    def update(self,xy):
        """This method will check if the coordinate is in the button, then change the
        colour"""
        state = pygame.Rect.collidepoint(self.rect,xy[0],xy[1]) 
        return state
            
    

    def callback(self):
        pass


# %%
