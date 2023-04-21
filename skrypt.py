import numpy as np
from math import *
import os

os.system("")

class Style():
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Underline = '\033[4m'
    Reset = '\033[0m'
    
class NieprawidlowaWartosc(Exception):
    '''Bład oznaczający podanie niepoprawnej lub/i nieobsługiwanej przez program wartości.
    
        liczba - błędna wartość podana przez użytkowanika
        minimum - (opcjonalnie) - minimalna wymagana wartość
        maksimum - (opcjonalnie) - maksymalna wymagana wartość
        '''
    def __init__(self, liczba, minimum = 'brak', maksimum = 'brak'):
        Exception.__init__(self)
        self.liczba = liczba
        self.minimum  = minimum
        self.maksimum = maksimum





class Transformacje():
    
    # a = 6378137.000
    # e2 = 0.00669438002290
    
    def __init__(self, X='', Y='', Z='', f='', l='', h='', X2='', Y2='', Z2='', s='', alfa='', z = ''):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.h = h
        self.X2 = X2
        self.Y2 = Y2
        self.Z2 = Z2
        self.s = s
        
        self.a = 6378137.000
        self.e2 = 0.00669438002290
        
        if f =='':
            pass
        elif type(f) == str:
            self.f = self.__fromdms(f)
        else:
            self.f = radians(f)
            
        if l =='':
            pass
        elif type(l) == str:
            self.l = self.__fromdms(l)
        else:
            self.l = radians(l)
                    
        if alfa =='':
            pass
        elif type(alfa) == str:
            self.alfa = self.__fromdms(alfa)
        else:
            self.alfa = radians(alfa)
            
        if z =='':
            pass
        elif type(z) == str:
            self.z =self.__fromdms(z)
        else:
            self.z = radians(z)

     
    def __fromdms(self,X): #zmiana ze stopni w ukladzie dms na radiany oraz stopnie dziesietne 
        '''
        Funkcja przelicza wartosc kąta z stopni na radiany
        Argumenty
        ---------
        X - warto
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
        
    def xyz2flh(self): #HIRVONEN
        X = self.X 
        Y = self.Y
        Z = self.Z
        a = self.a 
        e2 = self.e2 
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p * (1 - e2)))
        while True:
            N = self.__Np(f)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - e2 * N / (N + h))))
            if abs(fp - f) < (0.000001/206265):
                break
        N = self.__Np(f)
        h = (p / np.cos(f)) - N
        l = np.arctan2(Y, X)
        f = self.__dms(f)
        l = self.__dms(l)
        return(f, l, h)
     
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
        try:
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
                raise NieprawidlowaWartosc(self.__dms(l), minimum = 13.5, maksimum = 25.5)
        except NieprawidlowaWartosc as nw:
            print(Style.Red + 'NieprawidlowaWartosc: ' + Style.Reset + #Style.Underline +
                  f'podana wartość l znajduje się poza zakresem stref odwzorowawcych układu współrzędnych PL2000. '
                  f'Obsługiwany zakres to {nw.minimum}° - {nw.maksimum}° '
                  f'Podana przez Ciebie wartość to {nw.liczba}')
        else:         
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
            return(x2000,y2000)

    def fl2PL1992(self,l0=radians(19), m0 = 0.9993):
        a=self.a
        e2=self.e2
        f=self.f
        l=self.l
        b2 = a**2*(1 - e2)
        ep2 = (a**2 - b2)/b2
        dl = l - l0
        t = tan(f)
        n2 = ep2 * cos(f)**2
        N = self.__Np(f)
        sigm =self.__sigma(f)
        xgk = sigm + (dl**2/2) * N * sin(f)*cos(f)*(1 + (dl**2/12)*cos(f)**2*(5-t**2+9*n2+4*n2**2)+ ((dl**4)/360)*cos(f)**4*(61 - 58*t**2 + t**4 + 270*n2 - 330*n2*t**2))
        ygk = dl*N*cos(f)*(1+(dl**2/6)*cos(f)**2*(1 - t**2 + n2) + (dl**4/120)*cos(f)**4*(5 - 18*t**2 + t**4 + 14*n2 - 58*n2*t**2))
        x92 = xgk * m0 - 5300000
        y92 = ygk * m0 + 500000
        return(x92,y92)
      
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
        
    def flh2xyz(self):
        f=self.f
        l=self.l
        h=self.h
        a=self.a
        e2=self.e2
        N = self.__Np(f)
        x = (N+h)*np.cos(f)*np.cos(l)
        y = (N+h)*np.cos(f)*np.sin(l)
        z = ((N*(1-e2)+h))*np.sin(f)
        return(x,y,z)

if __name__=='__main__':
    
    proba1 = Transformacje(f='52 0 5.72012',
                           l='16 0 21.66234',
                           h=289.08952781930566,
                           s=43000.0,
                           alfa=230,
                           z=90,
                           X=3782450,
                           Y=1085030,
                           Z=5003140)
    
    print('flh2xyz\n', proba1.flh2xyz())
    print('PL1992\n', proba1.fl2PL1992())
    print('PL2000\n', proba1.fl2PL2000())
    print('NEU\n', proba1.xyz2neu())
    print('HIRVONEN\n', proba1.xyz2flh())

#xyz2NEU liczy nie wiadomo co
#fl2PL2000 wybiera sb zle strefy odwzorowawcze
#reszta liczy ok
