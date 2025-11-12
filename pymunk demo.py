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
from RockerBogie import *

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



floor = Segment((0,500),screenx,0,10,10,pymunk.Body.KINEMATIC) #kinematic objects can have collision but wont move by collision
test = Segment((600,490),100,0,10,7,pymunk.Body.KINEMATIC)
floor.shapes[0].friction = 0.9
test.shapes[0].friction = 0.5
rvr = rocker_bogie()

test_mount = Circle((300,300),10,10,pymunk.Body.STATIC)
mount_joint = pymunk.PinJoint(rvr.bogie.structure.body,test_mount.body,(0,0),(0,0))
mount_joint.distance = 0
#physicsObjects.append(mount_joint)

#%%all objects that need to be drawn 
DrawedObjects.append(rvr.bogie.structure)
DrawedObjects.append(rvr.rocker.structure)
DrawedObjects.append(rvr.bogie.wheel1)
DrawedObjects.append(rvr.bogie.wheel2)
DrawedObjects.append(rvr.rocker.wheel)

DrawedObjects.append(floor)
DrawedObjects.append(test)



#%%Adding the physics object list to the physics space
#magic function :spooky: This function adds all segment bodies and shapes to the physics space. I have abstracted it.
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
        #center_joint.draw_body(screen)
        #segment1.draw_body(screen)
        #segment2.draw_body(screen)
        #pendulum1.draw_bodies(sc=screen)
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)

if __name__ == "__main__":
    main()


# %%
