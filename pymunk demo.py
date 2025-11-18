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
import random as rand

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

wheel = pygame.image.load('wheel.png.png').convert_alpha()

clock = pygame.time.Clock()
space = pymunk.Space()     # Create a Space which contain the simulation
space.gravity = 0   ,373      # Set its gravity
space.damping = 0.90

fps = 50

floor = Segment((0,500),screenx,0,10,10,pymunk.Body.KINEMATIC) #kinematic objects can have collision but wont move by collision

rvr = rocker_bogie()
rvr.bogie.wheel1.attach_image('wheel.png.png')
rvr.bogie.wheel2.attach_image('wheel.png.png')
rvr.rocker.wheel.attach_image('wheel.png.png')

floor_list = [floor]

rand.seed()
def create_new_floor(floor):
    len = rand.randint(100,220)
    angle = rand.randint(-15,15)
    new_floor = Segment(floor.body.local_to_world(floor.shape.b), len,angle,10,10, pymunk.Body.KINEMATIC)
    #Object_list.append(new_floor) 
    floor_list.append(new_floor)
   
#%%Adding the physics object list to the physics space
#magic function :spooky: This function adds all segment bodies and shapes to the physics space. I have abstracted it.



create_new_floor(floor_list[0])
#add_objects(space) 
print(Object_list)

Pmanager = PhysicsManager(screen,FLAG_DRAW_SURFACES=True,FLAG_DRAW_SHAPES=True)
Pmanager.add_objects(space)
camera1 = camera(Pmanager,rvr.bogie.structure,(100,0))

#%% Game loop
def main():
    selected_object = None  
    var=True
    running = True
    score = 0

    while running:
        mouse_pos = pygame.mouse.get_pos()
        query_info = space.point_query(mouse_pos,0,shape_filter=pymunk.ShapeFilter(group=0b001, mask= 0b001))
        #print(query_info)

        #%%
      

        #%%
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit Pygame
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                rvr.get_input(event)
                print('A key has been pressed')
                if event.key == pygame.K_a:
                    TranslateVector = (-10,0)
                if event.key == pygame.K_d:
                    TranslateVector = (10,0)
                if event.key == pygame.K_w:
                    TranslateVector = (0,-100)
                if event.key == pygame.K_s:
                    TranslateVector = (0,100)
        rvr.update()


        camera1.update(1/fps)
                    

        #als floor[1].body gets past 2/3 of screenx, create a new floor
        #if floor[0].body.local_to_world(shape.b) gets -10 its off the screen, delete it.
        if floor_list[-1].body.position[0] < (screenx * 0.66) and var:
            create_new_floor(floor_list[-1])
            score += 1
            print(f'Segments generated(score):{score}' )
            Pmanager.add_objects(space)

        if query_info != []:
            shape_id = id(query_info[0][0])
            for obj in Object_list:
                shape_list = list(obj.body.shapes)
                obj_id = id(shape_list[0])
                if obj_id == shape_id:
                    obj.draw_shape(screen,(255,0,0))
                    print(type(obj))

        screen.fill((255,255,255))
        Pmanager.draw()

     

        #updating the entire game
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
        
  
if __name__ == "__main__":
    main()


# %%
