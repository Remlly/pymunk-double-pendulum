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


def to_pygame(p):
    """Small helper to convert Pymunk vec2d to Pygame integers"""
    
    return round(p.x), round(p.y)

def polar_to_2dvec(p):
    pass

#%%'Inheriting some fun :)'
class PhysicsBody:
    def __init__(self,xy,radius,body_type):
        "All physics objects are made out of pymunk body and a pymunk shape, "
        "The shape will be defined in the child class. Radius will be its width"
        self.radius = radius
        self.body = pymunk.Body(body_type=body_type)
        self.body.position = xy
        self.shape = None

    def draw_body(self):
        "This function will draw the body in green"
        x,y = to_pygame(self.body.position)
        pygame.draw.circle(screen, (0,255,0),(x,y),self.radius)
        
    def add_to_space(self,space):
        "Adds the physics body and the physics shape to the given physics space"
        space.add(self.body,self.shape)

#%%child objects inherit from PhysicsBody
class childSegment(PhysicsBody):
    def __init__(self, xy, length, angle, mass, radius, body_type=pymunk.Body.DYNAMIC):
        "Inherits the PhysicsObject functions and variables, then defines the shape as segment"
        super().__init__(xy,radius,body_type)
        self.body.position += pymunk.Vec2d.from_polar(length/2,angle)                   #Centre of gravity needs to be offset
        self.shape = pymunk.Segment(self.body, (-length/2,0),(length/2,0),self.radius)  #local shape for physics
        self.shape.mass = mass

    def draw_at_body(self):
        "Draws the (rotated) segment at the location of the physics body"
        p1 = self.body.position + self.shape.a.rotated(self.body.angle) #translate point to body pos and body angle 
        p2 = self.body.position + self.shape.b.rotated(self.body.angle) #translate point to body pos and body angle
        p1 = to_pygame(p1)
        p2 = to_pygame(p2)
        pygame.draw.lines(screen, (0,0,0), False, [p1,p2],self.radius)

#%%child objects inherit from PhysicsBody
class childCircle(PhysicsBody):
    def __init__(self, xy, mass, radius,body_type=pymunk.Body.DYNAMIC):
        "Inherits the PhysicsObject functions and variables, then defines the shape as circle"
        super().__init__(xy,radius,body_type=body_type)
        self.body.position = xy
        self.shape = pymunk.Circle(self.body,radius)
        self.shape.mass = mass

    def draw_at_body(self): 
        "Draws the circle at the body with the set radius"
        centerx,centery = to_pygame(self.body.position)
        pygame.draw.circle(screen, (0,0,0),(centerx,centery),self.radius)


#%%Initialization of physiscs objects
segment1 = childSegment(center,100,0,10,5)
segment2 = childSegment((cx+100,cy),100,0,10,5)
center_joint = childCircle(center,10,10,pymunk.Body.STATIC)

#%%Initialization of joints
joint1 = pymunk.PinJoint(center_joint.body, segment1.body,(0,0),(segment1.shape.a))
joint2 = pymunk.PinJoint(segment1.body,segment2.body,segment1.shape.b,segment2.shape.a)
joint1.distance = 0
joint2.distance = 0  

#%%adding physics objects to physics space
bodies = [segment1,segment2,center_joint]
for x in bodies:
    x.add_to_space(space) #visual studio code no longer recognizes the inherited function :)
                            #because all bodies inherit the add to space function, we can do this.

space.add(joint1,joint2) #joints hebben geen eigen functie :(


#%%Disable collision between segments
segment_group = 0b100   #segments are group 1 (ob1)
segment_mask = 0b000    #Segments dont collide with group 1 (ob0) 
segment1.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
segment2.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)



#%% Game loop
def main():
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit Pygame
                pygame.quit()
        
        screen.fill((255,255,255))
    
        center_joint.draw_at_body()
        segment1.draw_at_body()
        segment2.draw_at_body()
        
        #shapes inherit the draw_body function.
        center_joint.draw_body()
        segment1.draw_body()
        segment2.draw_body()

        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)

if __name__ == "__main__":
    main()


# %%
