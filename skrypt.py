import numpy as np
from math import *

class Transformacje:

    def __init__(self, podane_f, podane_l, podane_h = 'wartosc domyslna'):
        if type(podane_f) == str:
            self.f = self.__fromdms(podane_f)
        else:
            self.f = radians(podane_f)
        if type(podane_l) == str:
            self.l = self.__fromdms(podane_l)
        else:
            self.l = radians(podane_l)
        self.h = podane_h
        self.a = 6378137.000
        self.e2 = 0.00669438002290

    def __fromdms(self,X): #zmiana ze stopni w ukladzie dms na radiany oraz stopnie dziesietne 
        znak = 1
        if X[0] == '-':
             znak = -1
        Y = X.split(' ' or '"' or "'" or '°' or '-')
        d = int(Y[0])
        m = int(Y[1])
        s = float(Y[2])
        s = s/3600
        m = m/60
        Y = znak*(d+m+s)
        Z = Y * pi/180
        Y = float(f'{Y:7.5f}')
        return(Z)# Z to wartosc w [rad]

    def __Np(self, f): #promien krzywizny w I wertykale
        a = self.a 
        e2 = self.e2 
        N = a / np.sqrt(1 - e2 * np.sin(f)**2)
        return(N)

    def __sigma(self,f):
        a = self.a 
        e2 = self.e2
        A0 = 1 - e2/4 - 3 * e2**2/64 - 5 * e2**3/256
        A2 = (3/8) * (e2 + e2**2/4 + 15*e2**3/128)
        A4 = (15/256) * (e2**2 + (3 * e2**3)/4)
        A6 = 35 * e2**3/3072
        sigma = a * (A0*f - A2*sin(2*f) + A4*sin(4*f) - A6*sin(6*f))
        return(sigma)
       
    def fl2PL2000(self,m0= 0.999923):
        f = self.f
        l = self.l
        a = self.a
        e2 = self.e2
        if l < radians(16.5) and l > radians(13.5): #ns = 5
            l0 = radians(15)
            ns = 5
        elif l < radians(19.5) and l > radians(16.5): #ns = 6
            l0 = radians(18)
            ns = 6
        elif l < radians(22.5) and l > radians(19.5): #ns = 7
            l0 = radians(21)
            ns = 7
        elif l < radians(25.5) and l > radians(22.5): #ns = 8
            l0 = radians(24)
            ns = 8
        else:
            raise NameError('podana wartość l znajduje się poza zakresem stref odwzorowawcych układu współrzędnych PL2000')
                   
        b2 = a**2*(1 - e2)
        ep2 = (a**2 - b2)/b2
        dl = l - l0
        t = tan(f)
        n2 = ep2 * cos(f)**2
        N = self.__Np(f)
        sigm = self.__sigma(f)
        xgk = sigm + (dl**2/2) * N * sin(f)*cos(f)*(1 + (dl**2/12)*cos(f)**2*(5-t**2+9*n2+4*n2**2)+ ((dl**4)/360)*cos(f)**4*(61 - 58*t**2 + t**4 + 270*n2 - 330*n2*t**2))
        ygk = dl*N*cos(f)*(1+(dl**2/6)*cos(f)**2*(1 - t**2 + n2) + (dl**4/120)*cos(f)**4*(5 - 18*t**2 + t**4 + 14*n2 - 58*n2*t**2))
        x2000 = xgk * m0
        y2000 = ygk * m0 + ns * 1000000 + 500000
        return(x2000,y2000) #,xgk,ygk)

if __name__=='__main__':
    proba = Transformacje('-52 34 28.9', 40, 130)
    print(proba.fl2PL2000())
