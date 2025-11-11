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
from DoublePendulum import *

#%%initialize
# Initialize Pygame
pygame.init()
#screenwidth
screenx,screeny = 800,600
#screen center
cx,cy = screenx/2,screeny/2 #screen center
center = (cx,cy)

#Set up the game window
screen = pygame.display.set_mode((screenx, screeny))
screen.fill((255,255,255))
pygame.display.flip()
pygame.display.set_caption("Hello Pygame")


clock = pygame.time.Clock()
space = pymunk.Space()     # Create a Space which contain the simulation
space.gravity = 0,981      # Set its gravity
fps = 50


#%%Initialization of physiscs objects
segment1 = Segment(center, 100,0,10,10)
segment1.add_segment(100,90,5,10,(25,0))
segment2 = Segment((cx+100,cy),100,0,10,10)
segment2.add_segment(100,90,5,10,(25,0))
center_joint = Circle(center,10,10,pymunk.Body.STATIC)

#%%adding objects the drawing list.
DrawedObjects.append(segment1)
DrawedObjects.append(segment2)
DrawedObjects.append(center_joint)

#%%Initialization of joints
joint1 = Joint(pymunk.PinJoint, center_joint,segment1,(0,0), segment1.shapes[0].a)
joint1.body.distance = 0 #this is because pymunk automatically calculates joint distance, and we dont place the segments correctly.
joint2 = Joint(pymunk.PinJoint, segment1, segment2, segment1.shapes[0].b,segment2.shapes[0].a)
joint2.body.distance = 0

pendulum1 = double_pendulum((500,400))

#%%Disable collision between segments
segment_group = 0b100   #segments are group 1 (ob1)
segment_mask = 0b000    #Segments dont collide with group 1 (ob0) 
segment1.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
segment2.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
center_joint.shape.filter = pymunk.ShapeFilter(group=segment_group, mask = segment_mask)
#%%adding physics objects to physics space
add_objects(space)


#%% Game loop
def main():
    running = True

    while running:
        TranslateVector = pymunk.Vec2d(0,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit Pygame
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print('A key has been pressed')
                if event.key == pygame.K_a:
                    TranslateVector = (-10,0)
                if event.key == pygame.K_d:
                    TranslateVector = (10,0)
                if event.key == pygame.K_w:
                    TranslateVector = (0,-10)
                if event.key == pygame.K_s:
                    TranslateVector = (0,10)
                print(TranslateVector)
                for obj in DrawedObjects:
                    obj.translate_body(TranslateVector)
                    
        

        screen.fill((255,255,255))
        draw_to_screen(screen)
        
        #shapes inherit the draw_body function.
        center_joint.draw_body(screen)
        segment1.draw_body(screen)
        segment2.draw_body(screen)
        #pendulum1.draw_bodies(sc=screen)
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)

if __name__ == "__main__":
    main()


# %%
