import numpy as np
from math import *
   
class Transformacje:

    def __init__(self, podane_f, podane_l, podane_h = 'BRAK', podane_X2 = 'BRAK', podane_Y2 = 'BRAK', podane_Z2 = 'BRAK', podane_s = 'BRAK', podane_alfa = 'BRAK', podane_z = 'BRAK'):
        if type(podane_f) == str:
            self.f = self.__fromdms(podane_f)
        else:
            self.f = radians(podane_f)
        if type(podane_l) == str:
            self.l = self.__fromdms(podane_l)
        else:
            self.l = radians(podane_l)
        self.h = podane_h
        self.X2 = podane_X2
        self.Y2 = podane_Y2
        self.Z2 = podane_Z2
        self.s = podane_s
        try:
            self.alfa = radians(podane_alfa)
            self.z = radians(podane_z)
        except TypeError:
            pass
        self.a = 6378137
        self.e2 = 0.00669438002290
    
    def __dms(self, x): #zamiana wyswietlania sie stopni z ukladu 10 na uklad 60 
        znak = ' '
        if x < 0:
            znak = '-'
            x = abs(x)
        x = x * 180/pi
        d = int(x)
        m = int((x - d) *  60)
        s = (x - d - (m/60)) * 3600
        return(f"{znak}{d:3d}°{m:2d}'{s:8.5f}''")

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
       
    def __saz2neu(self):
        s = self.s
        alfa = self.alfa
        z = self.z
        dX = np.array([s * np.sin(z) * np.cos(alfa),
                          s * np.sin(z) * np.sin(alfa),
                          s * np.cos(z)])
        return(dX)

    def __Rneu(self, f, l):
        R = np.array([[-np.sin(f) * np.cos(l), -np.sin(l), np.cos(f) * np.cos(l)],
                      [-np.sin(f) * np.sin(l), np.cos(l), np.cos(f) * np.sin(l)],
                      [np.cos(f), 0. ,np.sin(f)]])
        return(R)
        
    def xyz2neu(self):
        f=self.f
        l=self.l
        try:        
            dX = [self.X2, self.Y2, self.Z2]
            R = self.__Rneu(f, l)
            return(R.T @ dX)
        except:
            dX = self.__saz2neu()
            R = self.__Rneu(f, l)
            return(R.T @ dX)
    
if __name__=='__main__':
    proba1 = Transformacje('-52 34 28.9', 15, podane_h=130, podane_s = 100, podane_alfa= 45, podane_z= 25)
    print(proba1.xyz2neu())
    proba2 = Transformacje('-52 34 28.9', 15, podane_h=130, podane_X2 = 100, podane_Y2= 100, podane_Z2= 100)
    print(proba2.xyz2neu())