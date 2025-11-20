import pygame
import pymunk
import math

physicsObjects = []
Object_list = []


def to_pygame(p):
    """Small helper to convert Pymunk vec2d to Pygame integers"""
    return round(p.x), round(p.y)


class PhysicsManager():
    def __init__(self, screen: pygame.display, FLAG_DRAW_BODIES = False, FLAG_DRAW_SHAPES = False, FLAG_DRAW_SURFACES = False):
        """Instead of a bunch of functions, An object handler will handle the moving
        drawing and addition of objects"""
        self.FLAG_DRAW_BODIES = FLAG_DRAW_BODIES
        self.FLAG_DRAW_SHAPES = FLAG_DRAW_SHAPES
        self.FLAG_DRAW_SURFACES = FLAG_DRAW_SURFACES
        self.screen = screen
        
    def add_objects(self,space):
        """This method will add all objects to the given physics space and clear the queue"""
        
        if physicsObjects != []: #if list is not empty
            for Obj in physicsObjects:
                space.add(Obj)
            physicsObjects.clear()

    def Translate(self,dxy):
        """This will translate all bodies with xy"""
        for obj in Object_list:    
            obj.translate_body(dxy)

    def draw(self):
        """This method will draw objects according to the set flags. Flags are 
        FLAG_DRAW_BODIES
        FLAG_DRAW_SHAPES
        FLAG_DRAW_SURFACES"""
        for Obj in Object_list:
            if self.FLAG_DRAW_SHAPES:
                Obj.draw_shape(self.screen)
            if self.FLAG_DRAW_BODIES:
                Obj.draw_body(self.screen)
            if self.FLAG_DRAW_SURFACES:
                Obj.draw_image(self.screen)

#%%
class PhysicsBody:
    def __init__(self,xy,radius,body_type):
        """All pymunk Objects have a shape and a body. The PhysicsBody will only contain
        functions that will do something with the body. like translation. This will allow
        more complex shapes to inherit common body functions."""
        self.body = pymunk.Body(body_type=body_type)
        self.body.position = xy
        self.shape = None
        self.image = None
        self.radius = radius
        physicsObjects.append(self.body)
        Object_list.append(self)

    def draw_body(self,screen):
        "This function will draw the body in green"
        x,y = to_pygame(self.body.position)
        pygame.draw.circle(screen, (0,255,0),(x,y),self.radius)
    
    def translate_body(self, xy):
        """This function translates the body by an x and a y coordinate. 
        usefull for mimicking a camera."""
        self.body.position += xy

    def attach_image(self, image_path):
        """This function attaches a pygame image to the body"""
        self.image = pygame.image.load(image_path).convert_alpha()

    def draw_image(self,screen):
        pass 
    
    def get_cog(self):
        return self.body.local_to_world(self.body.center_of_gravity)

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
        #self.shapes = []
        self.add_segment(l,angle,mass,radius)
        self.set_angle = angle
        self.set_length = l
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
        #self.shapes.append(self.shape)                               #adds to defined segment to the list of shapes.
        physicsObjects.append(self.shape)                             #Shape needs to be added to the physics list to calculate moment of inertia and cog
    
    def draw_image(self, screen):
        if self.image != None:
            #scale image to radius
            scaling_factor = (1,self.radius/(self.image.get_height()/2))
            scaled = pygame.transform.scale_by(self.image,scaling_factor)

            #rotate image
            rotated_image = pygame.transform.rotate(scaled,math.degrees(-self.body.angle))
            for i in range(0,self.set_length,32):
                blit_at = self.body.position + pymunk.Vec2d(i,0).rotated(self.body.angle) - (rotated_image.get_width()/2,rotated_image.get_height()/2)
                screen.blit(rotated_image,blit_at)

    def draw_shape(self, screen, color = (0,0,0)):
        """Draws the (rotated) segments at the location of the physics body
        The body keeps a reference to the shapes in a dictionary, this can be used to draw."""
        self.shapes = list(self.body.shapes)
        for segment in self.shapes:
            p1 = self.body.local_to_world(segment.a) 
            p2 = self.body.local_to_world(segment.b) 
            p1 = to_pygame(p1)
            p2 = to_pygame(p2)
            pygame.draw.lines(screen, color, False, [p1,p2],self.radius)


#%%child objects inherit from PhysicsBody
class Circle(PhysicsBody):
    def __init__(self, xy, mass, radius,body_type=pymunk.Body.DYNAMIC):
        "Inherits the PhysicsObject functions and variables, then defines the shape as circle"
        super().__init__(xy,radius,body_type=body_type)
        self.body.position = xy
        self.shape = pymunk.Circle(self.body,radius)
        self.shape.mass = mass
        physicsObjects.append(self.shape)
        
    def draw_shape(self,screen, color = (0,0,0)): 
        pass
        "Draws the circle at the body with the set radius"
        centerx,centery = to_pygame(self.body.position)
        pygame.draw.circle(screen, color,(centerx,centery),self.radius)

    def draw_image(self,screen):
        """rotates the original image by the body angle,  then draws it at body location"""
        rotated_image = pygame.transform.rotate(self.image,-self.body.angle)
        blit_at = self.body.position - (rotated_image.get_width()/2, rotated_image.get_height()/2)
        screen.blit(rotated_image,blit_at)

class camera:
    def __init__(self, manager : PhysicsManager, object, xy = (0,0)):
        """A camera is bound to an object, it can have an offset from that body but will
        always follow it. A static pymunk body is a valid object"""

        self.manager = manager
        self.assign_to(object,xy)  
        self.xy = xy
        self.attached_to = object
        self.current = self.attached_to.body.position
        self.dxy = 0
        self.deadband = 0
          

    def update(self,dt):
        """This will update the camera using a simple integration to get the next position """
        self.current = self.attached_to.body.position
        self.next = self.attached_to.body.position + self.attached_to.body.velocity * dt
        self.dxy = self.next - self.current
        self.manager.Translate(self.dxy)
        print(self.dxy)

    def update(self, object : PhysicsBody):
        """Updates camera based on previous location"""

        self.current = object.get_cog()               #get a new current position
        self.dxy = self.xy - self.current             #calculate the changed position to the set position

        print(f'body_pos{self.current}, camera {self.dxy}')
        #possible to pixelate or debounce the camera by setting self.deadband
        if (self.dxy > pymunk.Vec2d(self.deadband,self.deadband) or self.dxy < pymunk.Vec2d(-self.deadband,-self.deadband)):
            self.manager.Translate(self.dxy)
        
    def get_dxy(self):
        """This function will calculate the delta x and delta y position of the attached
        body and return it."""
        return self.previous - self.attached_to.body.position
    
    def assign_to(self, object : pymunk.body ,xy, offset = (0,0)):
        """This method will assign the camera to a object, and move all objects such that
        its in the middle of specified location"""
        x,y = xy
        Objx, Objy = object.body.position
        dx,dy = x-Objx,y-Objy
        self.attached_to = object
        self.manager.Translate((dx,dy))


