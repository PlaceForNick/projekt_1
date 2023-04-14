import numpy as np
from math import *

class Transformacje():
    
    # a = 6378137.000
    # e2 = 0.00669438002290
    
    def __init__(self, podany_X, podany_Y, podany_Z): #self - parametr, ktory reprezentuje obiekt sam w sobie
        self.X = podany_X
        self.Y = podany_Y
        self.Z = podany_Z
        self.a = 6378137.000
        self.e2 = 0.00669438002290
        
        # print(a)
    # @classmethod
    
    # def Np(self, f): #promien krzywizny w I wertykale
    #     a = self.a 
    #     e2 = self.e2 
    #     N = a / np.sqrt(1 - e2 * np.sin(f)**2)
    #     return(N) 
    
    def xyz2flh(self): #HIRVONEN
        X = self.X 
        Y = self.Y
        Z = self.Z
        a = self.a 
        e2 = self.e2 
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p * (1 - e2)))
        while True:
            # N = Np(self, f)
            N = a / np.sqrt(1 - e2 * np.sin(f)**2)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - e2 * N / (N + h))))
            if abs(fp - f) < (0.000001/206265):
                break
        # N = Np(self, f)
        N = a / np.sqrt(1 - e2 * np.sin(f)**2)
        h = (p / np.cos(f)) - N
        l = np.arctan2(Y, X)
        return(f, l, h)
        # return(self.X)
            
test = Transformacje(100, 200, 300)
print(test.xyz2flh())