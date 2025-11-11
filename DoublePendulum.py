from PhysicsObject import *


class double_pendulum():
    "This is a double pendulum as a simple class with magic variables."
    def __init__(self,center):
        cx,cy = center
        #%%Initialization of physiscs objects
        self.segment1 = Segment(center, 100,0,10,10)
        self.segment1.add_segment(100,90,5,10,(25,0))
        self.segment2 = Segment((cx+100,cy),100,0,10,10)
        self.segment2.add_segment(100,90,5,10,(25,0))
        self.center_joint = Circle(center,10,10,pymunk.Body.STATIC)



        #%%Joining the togheter
        joint1 = Joint(pymunk.PinJoint, self.center_joint,self.segment1,(0,0), self.segment1.shapes[0].a)
        joint1.body.distance = 0 #this is because pymunk automatically calculates joint distance, and we dont place the segments correctly.
        joint2 = Joint(pymunk.PinJoint, self.segment1, self.segment2, self.segment1.shapes[0].b,self.segment2.shapes[0].a)
        joint2.body.distance = 0

        segment_group = 0b100   #segments are group 1 (ob1)
        segment_mask = 0b000    #Segments dont collide with group 1 (ob0) 
        self.segment1.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.segment2.shapes[0].filter = pymunk.ShapeFilter(group=segment_group, mask= segment_mask)
        self.center_joint.shape.filter = pymunk.ShapeFilter(group=segment_group, mask = segment_mask)

        DrawedObjects.append(self.segment1)
        DrawedObjects.append(self.segment2)
        DrawedObjects.append(self.center_joint)
    
    def draw_bodies(self, sc):
        self.center_joint.draw_body(sc)
        self.segment1.draw_body(sc)
        self.segment2.draw_body(sc)