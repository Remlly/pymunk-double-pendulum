
#%%Welcome to nesting hell. 
from PhysicsObject import *

class bogie():
    def __init__(self):
        "The bogie is the front part of the mechanism, its a triangle"
        self.wheelSize = 15
        self.segmentScale = 1
        self.SegmentSize = 50 * self.segmentScale
        self.wheelfriction = 0.5
        
        #Here we are creating the bogie structure.
        self.structure = Segment((300,450),self.SegmentSize,225,10,10)
        self.structure.add_segment(self.SegmentSize,-225,10,10,self.structure.shapes[0].b)

        #wheelpoints are local coordinates where the wheel should be attached, cast to the
        #world coordinates. So later the wheel can be instantiated at that point.
        self.wheel1Point = self.structure.body.local_to_world(self.structure.shapes[0].a)
        self.wheel2Point = self.structure.body.local_to_world(self.structure.shapes[1].b)

        #creation of the first wheel, with motor.
        self.wheel1 = Circle(self.wheel1Point,10,self.wheelSize)
        self.wheel1_joint = pymunk.PinJoint(self.structure.body,self.wheel1.body,self.structure.shapes[0].a,(0,0))
        self.wheel1_motor = pymunk.SimpleMotor(self.wheel1.body,self.structure.body,200)
        self.wheel1.shape.friction = self.wheelfriction

        #creation of the second wheel, without motor
        self.wheel2 = Circle(self.wheel2Point,10,self.wheelSize)
        self.wheel2_joint = pymunk.PinJoint(self.structure.body,self.wheel2.body,self.structure.shapes[1].b,(0,0))
        self.wheel2.shape.friction = self.wheelfriction

        #appending joints to the physics list 
        physicsObjects.append(self.wheel1_joint)
        physicsObjects.append(self.wheel2_joint)
        physicsObjects.append(self.wheel1_motor)

        #disable collision
        #:spooky: something about bitshifting.
        segment_group = 0b010
        segment_mask = 0b010

        self.structure.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel1.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.structure.shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel2.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)

class rocker():
    def __init__(self,xy):
        "The rocker is the back part of the mechanism, its looks like a hook"
        self.wheelSize = 15
        self.segmentScale = 1
        self.SegmentSize = 100 * self.segmentScale
        self.wheelfriction = 0.5

        #creating the structure
        self.structure = Segment(xy,self.SegmentSize,0,10,10) #the rocker should be created at bogie shapes[0].b (middle of the triangle)
        self.structure.add_segment(self.SegmentSize/2,90,10,10,(self.SegmentSize,0))

        #creating the wheel, with motor
        self.wheelPoint = self.structure.body.local_to_world(self.structure.shapes[1].b)
        self.wheel = Circle(self.wheelPoint,10,self.wheelSize)
        self.wheel_joint = pymunk.PinJoint(self.structure.body,self.wheel.body,self.structure.shapes[1].b,(0,0))
        self.wheel1_motor = pymunk.SimpleMotor(self.wheel.body,self.structure.body,200)
        #appending joints
        physicsObjects.append(self.wheel_joint)
        physicsObjects.append(self.wheel1_motor)
        #disabling collision :spooky:
        segment_group = 0b010
        segment_mask = 0b010
        self.structure.shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)


class rocker_bogie():
    def __init__(self):
        self.bogie = bogie()
        self.rocker = rocker(self.bogie.structure.body.local_to_world(self.bogie.structure.shapes[0].b))
        self.frontjoint = pymunk.PinJoint(self.bogie.structure.body, self.rocker.structure.body,self.bogie.structure.shapes[0].b,(0,0))
        self.frontjoint.distance = 0
        physicsObjects.append(self.frontjoint)

        segment_group = 0b010
        segment_mask = 0b010
        self.bogie.structure.shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.rocker.structure.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
    
