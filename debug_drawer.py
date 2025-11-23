"""This file contains a debug draw method that will allow you to assign up to 16 variables
to and draw them live on the screen. No more console needed :cool:"""

from pygame import font
from pygame import rect
from pygame import draw
from pygame import Surface

class debugscreen:
    def __init__(self, xy_loc : tuple, xy_size : tuple):
        self.fontsize = 15
        self.i = font.SysFont('stylus', self.fontsize)
        
        self.texts = dict()
        self.set_size(xy_loc,xy_size)
        self.colour_out = (0,0,0)
        self.colour_in  = (100,100,100,0)
        self.DRAW_FLAG = False

        self.title = self.i.render("Debug", False, (255,0,0))


    def set_size(self, xy_loc,xy_size):
        self.inner_rect = rect.Rect(xy_loc[0]+2, xy_loc[1]+2, xy_size[0], xy_size[1]-4)
        self.outer_rect = rect.Rect(xy_loc[0],xy_loc[1], xy_size[0],xy_size[1])
        self.xy_loc = xy_loc
        self.xy_size = xy_size
        
    def set_text(self, name : str, text : str):
        """The text is set with name and the text value as a string"""
        self.texts[name] = text


    def draw(self,screen : Surface):
        """This function will draw the debug screen and all values up to 16"""
        #debug_surface = Surface(self.xy_size)
        #debug_surface.fill((255,255,255,0))
        if(self.DRAW_FLAG):
            draw.rect(screen,self.colour_out, self.outer_rect)
            draw.rect(screen,self.colour_in, self.inner_rect)
            
            
            y = self.xy_loc[1] + self.fontsize/2
            x = self.xy_loc[0] + 3
            screen.blit(self.title, (x,y))
            y += self.fontsize
            for i in self.texts:
                key = str(i)
                value = str(self.texts[i])
                string = key + " : " + value
                render = self.i.render(string ,False,(255,255,255))
                screen.blit(render, (x,y))
                y += self.fontsize

        #screen.blit(debug_surface,self.xy_loc)