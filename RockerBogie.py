

from PhysicsObject import *


#%%Welcome to nesting hell. 
class bogie():
    def __init__(self):
        "The bogie is the front part of the mechanism, its a triangle"
        self.wheelSize = 15
        self.segmentScale = 1
        self.SegmentSize = 50 * self.segmentScale
        self.wheelfriction = 0.3
        self.motor_rate = 0

        #Here we are creating the bogie structure.
        self.structure = Segment((300,450),self.SegmentSize,225,10,10)
        self.structure.add_segment(self.SegmentSize,-225,10,10,self.structure.shape.b)

        #we get a shape list through the body, this will be used as points to attach
        #wheels.
        shape_list = list(self.structure.body.shapes)

        #wheelpoints are local coordinates where the wheel should be attached, cast to the
        #world coordinates. So later the wheel can be instantiated at that point.
     
        self.wheel1Point = self.structure.body.local_to_world(shape_list[0].a)
        self.wheel2Point = self.structure.body.local_to_world(shape_list[1].b)

        #creation of the first wheel, with motor.
        self.wheel1 = Circle(self.wheel1Point,10,self.wheelSize)

        self.wheel1_joint = pymunk.PinJoint(self.structure.body,self.wheel1.body,shape_list[0].a,(0,0))
        self.wheel1_motor = pymunk.SimpleMotor(self.wheel1.body,self.structure.body,self.motor_rate)
        self.wheel1.shape.friction = self.wheelfriction

        #creation of the second wheel, without motor
        self.wheel2 = Circle(self.wheel2Point,10,self.wheelSize)
        self.wheel2_joint = pymunk.PinJoint(self.structure.body,self.wheel2.body,shape_list[1].b,(0,0))
        self.wheel2.shape.friction = self.wheelfriction

        #appending joints to the physics list 
        physicsObjects.append(self.wheel1_joint)
        physicsObjects.append(self.wheel2_joint)
        physicsObjects.append(self.wheel1_motor)

        #disable collision
        #:spooky: something about bitshifting.
        segment_group = 0b010
        segment_mask = 0b010

        shape_list[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel1.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        shape_list[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel2.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)

class rocker():
    def __init__(self,xy):
        "The rocker is the back part of the mechanism, its looks like a hook"
        self.wheelSize = 15
        self.segmentScale = 1
        self.SegmentSize = 100 * self.segmentScale
        self.wheelfriction = 0.3
        self.motor_rate = 0
        
        #creating the structure
        self.structure = Segment(xy,self.SegmentSize,0,10,10) #the rocker should be created at bogie shapes[0].b (middle of the triangle)
        self.structure.add_segment(self.SegmentSize/2,90,10,10,(self.SegmentSize,0))

        #we get a shape list through the body, this will be used as points to attach
        #wheels.
        shape_list = list(self.structure.body.shapes)


        #creating the wheel, with motor
        self.wheelPoint = self.structure.body.local_to_world(shape_list[1].b)
        self.wheel = Circle(self.wheelPoint,10,self.wheelSize)
        self.wheel_joint = pymunk.PinJoint(self.structure.body,self.wheel.body,shape_list[1].b,(0,0))
        self.wheel1_motor = pymunk.SimpleMotor(self.wheel.body,self.structure.body,self.motor_rate)
        
        #appending joints
        physicsObjects.append(self.wheel_joint)
        physicsObjects.append(self.wheel1_motor)

        #disabling collision :spooky:
        segment_group = 0b010
        segment_mask = 0b010
        shape_list[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.wheel.shape.filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)


class rocker_bogie():
    def __init__(self):
        self.bogie = bogie()
        bogie_shapes = list(self.bogie.structure.body.shapes) 
        self.rocker = rocker(self.bogie.structure.body.local_to_world(bogie_shapes[0].b))

        
        #we need to get shape lists so we can use it for collision and a pinjoint. 
        rocker_shapes = list(self.rocker.structure.body.shapes)


        self.frontjoint = pymunk.PinJoint(self.bogie.structure.body, self.rocker.structure.body,bogie_shapes[0].b,(0,0))
        self.frontjoint.distance = 0
        physicsObjects.append(self.frontjoint)

        segment_group = 0b010
        segment_mask = 0b010
        
        bogie_shapes[1].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        rocker_shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)

        self.max_rate = 500
        self.current_rate = 0

    def get_input(self, event):
            print(self.current_rate)
            if event.key == pygame.K_LEFT:
               #going left
                if not self.current_rate < -self.max_rate:
                    #if current is not smaller than max_rate #negative
                    self.current_rate -= 10
                else: 
                    self.current_rate = - self.max_rate
            if event.key == pygame.K_RIGHT:
                #going right
                if not self.current_rate > self.max_rate:
                    #if current speed is not bigger than max rate
                    self.current_rate += 10
                else:
                    self.current_rate = self.max_rate
            #self.update()
    def update(self):
        self.rocker.wheel1_motor.rate = self.current_rate
        self.bogie.wheel1_motor.rate = self.current_rate