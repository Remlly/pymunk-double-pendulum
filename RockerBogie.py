
#%%
from PhysicsObject import *

class bogie():
    def __init__(self):
        "The bogie is the front part of the mechanism, its a triangle"
        self.structure = Segment((300,450),50,225,10,10)
        self.structure.add_segment(50,-225,10,10,self.structure.shapes[0].b)

        self.wheel1 = Circle((200,450),10,10)
        self.wheel1_joint = pymunk.PinJoint(self.structure.body,self.wheel1.body,self.structure.shapes[0].a,(0,0))
        self.wheel1_joint.distance = 0
        self.wheel1_motor = pymunk.SimpleMotor(self.wheel1.body,self.structure.body,200)
        self.wheel1.shape.friction = 0.5
        self.wheel2 = Circle((200,450),10,10)
        self.wheel2_joint = pymunk.PinJoint(self.structure.body,self.wheel2.body,self.structure.shapes[1].b,(0,0))
        self.wheel2_joint.distance = 0
        self.wheel2.shape.friction = 0.5
        physicsObjects.append(self.wheel1_joint)
        physicsObjects.append(self.wheel2_joint)
        physicsObjects.append(self.wheel1_motor)
        #disable collision'
        segment_group = 0b010
        segment_mask = 0b010

        self.structure.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel1.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.structure.shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel2.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)

class rocker():
    def __init__(self):
        "The rocker is the back part of the mechanism, its looks like a hook"
        self.structure = Segment((300,400),100,0,10,10)
        self.structure.add_segment(50,90,10,10,(100,0))

        self.wheel = Circle((400,450),10,10)
        self.wheel_joint = pymunk.PinJoint(self.structure.body,self.wheel.body,self.structure.shapes[1].b,(0,0))
        self.wheel_joint.distance = 0
        physicsObjects.append(self.wheel_joint)

        
        segment_group = 0b010
        segment_mask = 0b010
        self.structure.shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)


class rocker_bogie():
    def __init__(self):
        self.bogie = bogie()
        self.rocker = rocker()
        self.frontjoint = pymunk.PinJoint(self.bogie.structure.body, self.rocker.structure.body,self.bogie.structure.shapes[0].b,(0,0))
        self.frontjoint.distance = 0
        physicsObjects.append(self.frontjoint)

        segment_group = 0b010
        segment_mask = 0b010
        self.bogie.structure.shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.rocker.structure.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
