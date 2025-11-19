#
# Developed by Remon Verbraak
# Date: 7-11-2025
#   
# Description:
# This code makes a double pendulum using pymunk and pygame and classes  
#  
# To achieve this, pymunk must be coupled to drawing functions from pygame. Therefore
# classes have been used to make reusable physics objects with their own drawing functions
#
# Inheritance has been applied to inherit common drawing and pymunk functions.
# Pymunk divides a physics object into a body and a shape, this has been mirrored in the
# classes. First the body is a class with common body functions, shapes are seperated
# classes for exclusive functions.
# 
# the code can be roughly divided into four sections
# 1. Initialization of the pygame screen and helper functions
# 2. Definition and implementation of the objects classes
# 3. Initialization of the physics objects
# 4. Main 'game loop' for drawing. 


#%%imports
import pygame
import pymunk
from PhysicsObject import *
#from DoublePendulum import *
#from RockerBogie import *
import random as rand
from Button import *

#%%initialize
pygame.init()
pygame.font.init()

#%%Helper variables
screenx,screeny = 800,600   #screen dimensions
cx,cy = screenx/2,screeny/2 #screen center
center = (cx,cy)


#Set up the game window
screen = pygame.display.set_mode((screenx, screeny))
screen.fill((255,255,255))
pygame.display.flip()
pygame.display.set_caption("Hello PyPendulum!")

wheel = 'wheel.png.png'
bar = 'Bar.png.png'


clock = pygame.time.Clock()   # Pygame clock for FPS limiting
space = pymunk.Space()        # The 'space' where pymunk simulates
space.gravity = 0   ,373      # Set its gravity
space.damping = 1             # Global dampening variable from 0 (full) to 1 (none)
fps = 50                      # Max fps






#%% Game loop
def main():
    running = True
    Pmanager = PhysicsManager(screen,FLAG_DRAW_SURFACES=True,FLAG_DRAW_SHAPES=False, FLAG_DRAW_BODIES=False)
    
    #Creating the pendulum objects and joints
    world_point = Circle(center,10,10,pymunk.Body.STATIC)
    Segment1 = Segment(center,100,0,10,10)
    Segment2 = Segment(Segment1.body.local_to_world(Segment1.shape.b),100,0,10,10)
    j1 = pymunk.PinJoint(Segment1.body,world_point.body,Segment1.shape.a,(0,0))
    j2 = pymunk.PinJoint(Segment1.body,Segment2.body,Segment1.shape.b,Segment2.shape.a)

    world_point.attach_image(wheel)
    Segment1.attach_image(bar)
    Segment2.attach_image(bar)

    physicsObjects.append(j1)
    physicsObjects.append(j2)

    segment_group = 0b100   #segments are group 1 (ob1)
    segment_mask = 0b000    #Segments dont collide with group 1 (ob0) 
    Segment1.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
    Segment2.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
    world_point.shape.filter = pymunk.ShapeFilter(group=segment_group, mask = segment_mask)


    next_button = button(((cx +75),(cy + 220)),(100,50),(0,255,255),'Next body')
    prev_button = button(((cx -175),(cy + 220)),(100,50),(0,255,255),'Prev body')

    camera1 = camera(Pmanager,world_point,center)

    selector_i = 0
    selector_min = 0
    selector_max = len(Object_list)-1

    while running:
        #Get mouse information 
        mouse_pos = pygame.mouse.get_pos() #Get mouse position
        Pmanager.add_objects(space)        #Add objects if any are in queue
        

        
       
        #%%
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit Pygame
                pygame.quit()

            #Detecting for clicks on buttons. The button needs to be debounced by detecting
            #if the key is down.
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                print(selector_i)
                if left & next_button.update(mouse_pos):
                    selector_i = selector_i +1
                    
                    if selector_i > selector_max:
                        selector_i = selector_min
                    camera1.assign_to(Object_list[selector_i],center)
                if left & prev_button.update(mouse_pos):
                    selector_i = selector_i - 1
                    if selector_i < selector_min:
                        selector_i = selector_max
                    camera1.assign_to(Object_list[selector_i],center)


            if event.type == pygame.KEYDOWN:
                #rvr.get_input(event)
                print('A key has been pressed')

                if event.key == pygame.K_a:
                    TranslateVector = (-10,0)
                if event.key == pygame.K_d:
                    TranslateVector = (10,0)
                if event.key == pygame.K_w:
                    TranslateVector = (0,-100)
                if event.key == pygame.K_s:
                    TranslateVector = (0,100)

        camera1.update(1/fps)
                    


        screen.fill((255,255,255))
        Pmanager.draw()
        next_button.draw(screen)
        prev_button.draw(screen)
        #updating the entire game
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
        
  
if __name__ == "__main__":
    main()


# %%
