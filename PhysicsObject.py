import pygame
import pymunk

physicsObjects = []
DrawedObjects = []


def add_objects(space):
    "When a shape and object are made, a global list is appended"
    "this function will add that list to the physics world"
    for Obj in physicsObjects:
        space.add(Obj)

    physicsObjects.clear()

def draw_to_screen(screen):
    "Only PhysicsObject classes should be in DrawedObjects. This function will then draw them to the screen"
    for Obj in DrawedObjects:
        Obj.draw_shape(screen)

def draw_body_screen(screen):
    for Obj in DrawedObjects:
        Obj.draw_body(screen)

def to_pygame(p):
    """Small helper to convert Pymunk vec2d to Pygame integers"""
    return round(p.x), round(p.y)

#%%
class PhysicsBody:
    def __init__(self,xy,radius,body_type):
        """All pymunk Objects have a shape and a body. The PhysicsBody will only contain
        functions that will do something with the body. like translation. This will allow
        more complex shapes to inherit common body functions."""
        self.body = pymunk.Body(body_type=body_type)
        self.body.position = xy
        self.shape = None
        self.radius = radius
        physicsObjects.append(self.body)

    def draw_body(self,screen):
        "This function will draw the body in green"
        x,y = to_pygame(self.body.position)
        pygame.draw.circle(screen, (0,255,0),(x,y),self.radius)
    
    def translate_body(self, xy):
        """This function translates the body by an x and a y coordinate. 
        usefull for mimicking a camera."""
        self.body.position += xy

        
#%%child objects inherit from PhysicsBody
class Segment(PhysicsBody):

    def __init__(self, xy : tuple, l : int, angle : int, mass : int, radius : int, body_type=pymunk.Body.DYNAMIC):
        """Creates a pymunk body and creates a segment of any rotation defined of the
        positive x axis
        xy          = (x,y)     : Tuple
        l           = length    : int
        angle       = degrees   : int
        mass        = mass      : int
        radius      = radius    : int
        body_type   = pymunk.Body """
        
        super().__init__(xy,radius,body_type)
        self.shapes = []
        self.add_segment(l,angle,mass,radius)
        
    def add_segment(self, l : int, angle : int, mass : int, radius, local = (0,0)):
        """creates a segment of any rotation defined of the
        positive x axis, this function will allow the addition of extra segments at local
        coordinates
        l           = length    : Int
        angle       = degrees   : Int
        mass        = mass      : Int
        radius      = radius    : Int
        local       = coord     : Tuple"""
        
        p1 = pymunk.Vec2d(0,0).rotated_degrees(angle) + local 
        p2 = pymunk.Vec2d(l,0).rotated_degrees(angle) + local
        self.radius = radius
        self.shape = pymunk.Segment(self.body, p1, p2, self.radius)  #adds to the body the defined segment
        self.shape.mass = mass
        self.shape.friction = 0.9
        self.shapes.append(self.shape)                               #adds to defined segment to the list of shapes.
        physicsObjects.append(self.shape)
      

    def draw_shape(self, screen):
        "Draws the (rotated) segments at the location of the physics body"
        for segment in self.shapes:
            p1 = self.body.position + segment.a.rotated(self.body.angle) #translate point to body pos and body angle 
            p2 = self.body.position + segment.b.rotated(self.body.angle) #translate point to body pos and body angle
            p1 = to_pygame(p1)
            p2 = to_pygame(p2)
            pygame.draw.lines(screen, (0,0,0), False, [p1,p2],self.radius)


#%%child objects inherit from PhysicsBody
class Circle(PhysicsBody):
    def __init__(self, xy, mass, radius,body_type=pymunk.Body.DYNAMIC):
        "Inherits the PhysicsObject functions and variables, then defines the shape as circle"
        super().__init__(xy,radius,body_type=body_type)
        self.body.position = xy
        self.shape = pymunk.Circle(self.body,radius)
        self.shape.mass = mass
        physicsObjects.append(self.shape)
    def draw_shape(self,screen): 
        "Draws the circle at the body with the set radius"
        centerx,centery = to_pygame(self.body.position)
        pygame.draw.circle(screen, (0,0,0),(centerx,centery),self.radius)



#This code is only used for the pendulum. new joints can be made straight from pymunk. but
#have to appended to the body list manually.
class Joint(PhysicsBody):
    def __init__(self, joint: pymunk.constraints, *args):
        "By passing the type of constraint and the appropiate number of arguments, we can initiate any constraint within pymunk.constraints"
        "We still have to check for joint type and unpack accordingly :("
        if joint == pymunk.PinJoint:
            #unpack the first 4 variables for a pinjoint. body_a, body_b shape.a, shape.b
            body_a, body_b, shape_a, shape_b = args
            self.body = joint (body_a.body,body_b.body,shape_a,shape_b)
        elif joint == pymunk.SimpleMotor:
            #we have to only unpack the first 3 variables for a pinjoint
            body_a, body_b, speed = args
            self.body = pymunk.SimpleMotor(body_a.body,body_b.body, speed)
        
        physicsObjects.append(self.body)
        
    
    def draw_body(self):
        #we cant draw the body because joints dont keep track of their position
        #To make this work, we either have to draw on position A, or B, or an interpolated
        #position 
        pass
# %%
