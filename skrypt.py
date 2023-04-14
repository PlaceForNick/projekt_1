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
            N = a / np.sqrt(1 - e2 * np.sin(f)**2)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - e2 * N / (N + h))))
            if abs(fp - f) < (0.000001/206265):
                break
        N = a / np.sqrt(1 - e2 * np.sin(f)**2)
        h = (p / np.cos(f)) - N
        l = np.arctan2(Y, X)
    
        dms = []
        for x in (f,l):
            znak = ' '
            if x < 0:
                znak = '-'
                x = abs(x)
            x = x * 180/pi
            d = int(x)
            m = int((x - d) *  60)
            s = (x - d - (m/60)) * 3600
            dms.append(f"{znak}{d:3d}°{m:2d}'{s:8.5f}''")
        f_st = dms[0]
        l_st = dms[1]
        
        return(f_st,l_st,h)

if __name__ == '__main__':
    test = Transformacje(100, 200, 300)
    test.xyz2flh()
    print(test.xyz2flh())
