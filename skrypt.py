import numpy as np
from math import *

class Transformacje:
    
    def __init__(self,s, alfa,z,x,y,a,e2):
        self.alfa_rad=radians(alfa)
        self.z_rad=radians(z)
        self.s=s
        self.x=x
        self.y=y
        self.z=z
        self.a=a
        self.e2
        
        
    def __Np(self, f): #promien krzywizny w I wertykale
        a = self.a 
        e2 = self.e2 
        N = a / np.sqrt(1 - e2 * np.sin(f)**2)
        return(N)
    
    
    
    def xyz2flh(self): #HIRVONEN
        x=self.x
        y=self.y
        z=self.z
        p = np.sqrt(x**2 + y**2)
        f = np.arctan(Z/(p * (1 - e2)))
        while True:
            N = Np(f, a, e2)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - e2 * N / (N + h))))
            if abs(fp - f) < (0.000001/206265):
                break
        
        N = Np(f,a,e2)
        h = (p / np.cos(f)) - N
        l = np.arctan2(Y, X)
        return(f, l, h)
        
    def saz2neu(self):
        s=self.s
        alfa=self.alfa_rad
        z=self.z
        dneu = np.array([s * np.sin(z) * np.cos(alfa),
                         s * np.sin(z) * np.sin(alfa),
                         s * np.cos(z)])
        return(dneu)
    
    def Rneu(self,f,l):

        R = np.array([[-np.sin(f) * np.cos(l), -np.sin(l), np.cos(f) * np.cos(l)],
                      [-np.sin(f) * np.sin(l), np.cos(l), np.cos(f) * np.sin(l)],
                      [np.cos(f), 0. ,np.sin(f)]])
        return(R)
    
    def neu2xyz(self,dneu):
        R = Rneu(self)
        dXYZ = R @ dneu
        return(dXYZ)
    
    






  

