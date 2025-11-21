#
# Developed by Remon Verbraak
# Date: 7-11-2025
#   


#%%imports
import pygame
import pymunk
from PhysicsObject import *
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
space.gravity = 0   ,373      # Set gravity
space.damping = 1             # Global dampening variable from 0 (full) to 1 (none)
fps = 50                      # Max fps

#%% Game loop
def main():
    running = True
    Pmanager = PhysicsManager(screen,FLAG_DRAW_SURFACES=True,FLAG_DRAW_SHAPES=True, FLAG_DRAW_BODIES=False)
    
    #Creating the pendulum objects and joints
    world_point = Circle(center,10,10,pymunk.Body.STATIC)
    Segment1 = Segment(center,100,0,10,10)
    Segment2 = Segment(Segment1.body.local_to_world(Segment1.shape.b),100,0,10,10)
    j1 = pymunk.PinJoint(Segment1.body,world_point.body,Segment1.shape.a,(0,0))
    j2 = pymunk.PinJoint(Segment1.body,Segment2.body,Segment1.shape.b,Segment2.shape.a)

    world_floor = Segment((0,screeny),screenx,0,0,10,pymunk.Body.STATIC)
    world_floor.attach_image(bar)
    world_point.attach_image(wheel)
    Segment1.attach_image(bar)
    Segment2.attach_image(bar)

    physicsObjects.append(j1)
    physicsObjects.append(j2)

    segment_group = 0b1  #segments are group 1 (ob1)
    segment_mask = 0b0    #Segments dont collide with group 1 (ob0) 
    Segment1.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
    Segment2.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
    #world_point.shape.filter = pymunk.ShapeFilter(group=segment_group, mask = segment_mask)


    next_button = button(((cx +75),(cy + 220)),(100,50),(0,255,255),'Next body')
    prev_button = button(((cx -175),(cy + 220)),(100,50),(0,255,255),'Prev body')

    camera1 = camera(Pmanager,world_point,center)
 
    selector_i = 0
    selector_min = 0
    selector_max = len(Object_list)-1

    ball_list = [] #fun times
    i = 0
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
                #rint(Object_list[selector_i])
                #check if next button is pressed
                if right:
                    ball = Circle(mouse_pos,10,10)
                    
                    selector_max = len(Object_list)-1
                    #ball.attach_image(wheel)
                    #ball.shape.filter = pymunk.ShapeFilter(group=0b0, mask= 0b111)
                
                if left & next_button.update(mouse_pos):
                    selector_i = selector_i +1
                    if selector_i > selector_max: #out of bounds check
                        selector_i = selector_min   #wrap around 
                    #camera1.assign_to(Object_list[selector_i],center)
                #check if previous button is pressed
                if left & prev_button.update(mouse_pos):
                    selector_i = selector_i - 1
                    if selector_i < selector_min: #out of bounds check
                        selector_i = selector_max   #wrap around
                    #camera1.assign_to(Object_list[selector_i],center)


        
        screen.fill((255,255,255))
        Pmanager.draw()
        next_button.draw(screen)
        prev_button.draw(screen)
        #updating the entire game
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
        camera1.update(Object_list[selector_i],space)
      
if __name__ == "__main__":
    main()


# %%
