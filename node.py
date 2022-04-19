#class for nodes
import math
import numpy as np

class node:
   
    # init method or constructor
    #nan values are used to indicate if the value needs to be determined.
    def __init__(self, num, pos_x , pos_y , dis_x , dis_y, f_x , f_y):
        self.num = num
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dis_x = dis_x
        self.dis_y = dis_y
        self.f_x = f_x
        self.f_y = f_y
 
    def print(self):
        print('num = ', self.num , '\n' , 'pos_x =', self.pos_x , '\n pos_y = ' , self.pos_y , '\n dis_x = ' , self.dis_x , '\n dis_y = ', self.dis_y , '\n f_x = ', self.f_x, '\n f_y = ', self.f_y)
        return 0
    
    def value(self):
       
        return [self.num , self.pos_x , self.pos_y , self.dis_x , self.dis_y, self.f_x, self.f_y]
        
class nodep:
    def __init__(self, num, pos_x , pos_y):
        self.num = num
        self.pos_x = pos_x
        self.pos_y = pos_y