#class for elements
import math
import numpy as np
import node

class ele:
   
    # init method or constructor 
    #nan values are used to indicate if the value needs to be determined.
    def __init__(self, num, length , area , ym , theta, node_a , node_b):
        self.num = num
        self.length = length
        self.area = area
        self.ym = ym
        self.theta = theta
        self.node_a = node_a
        self.node_b = node_b
        
    def print(self):
        print('num = ', self.num , '\n' , 'length=', self.length , '\n area = ' , self.area , '\n youngs modulus = ' , self.ym , '\n theta = ', self.theta , '\n node_a = ', self.node_a, '\n node_b = ', self.node_b)
        return 0
    
    def value(self):
        return [self.num, self.length , self.area , self.ym , self.theta , self.node_a.num, self.node_b.num]
    
    def stiff(self):
        ang = self.theta
        c2 = (math.cos(ang))**2
        cs = math.sin(ang) * math.cos(ang)
        s2 = (math.sin(ang))**2
        mat = np.array([[c2 , cs , -c2 , -cs],
                    [cs , s2 , -cs , -s2],
                    [-c2 , -cs , c2 , cs],
                    [-cs , -s2 , cs , s2]])
        return ((self.ym * self.area) / self.length) * mat
    
class elep:
    def __init__(self, num, node_a , node_b):
        self.num = num
        self.node_a = node_a 
        self.node_b = node_b