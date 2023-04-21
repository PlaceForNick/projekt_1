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
        
    def __init__(self, model, X='', Y='', Z='', f='', l='', h='', X2='', Y2='', Z2='', s='', alfa='', z = ''):
        
        self.X = []
        self.Y = []
        self.Z = []
        self.h = []
        self.X2 = []
        self.Y2 = []
        self.Z2 = []
        self.s = []
        
        (self.X).append(X)
        (self.Y).append(Y)
        (self.Z).append(Z)
        (self.h).append(h)
        (self.X2).append(X2)
        (self.Y2).append(Y2)
        (self.Z2).append(Z2)
        (self.s).append(s)

        
        if   model  == 'kra':
            self.a= 6378245
            self.b= 6356863.01877
        elif  model == "wgs84":
            self.a = 6378137.0 
            self.b = 6356752.31424518 
        elif  model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        else:
            raise NotImplementedError(f"{model} ten model elipsoidy nie jest obsługiwany")
        self.splasz = (self.a - self.b) / self.a
        self.e2 = (2 * self.splasz - self.splasz ** 2)
        print(model,self.b)  
            
        
        if f =='':
            self.f = f
        elif type(f) == str:
            self.f = self.__fromdms(f)
        else:
            self.f = radians(f)
            
        if l =='':
            self.l = l
        elif type(l) == str:
            self.l = self.__fromdms(l)
        else:
            self.l = radians(l)
                    
        if alfa =='':
            self.alfa = alfa
        elif type(alfa) == str:
            self.alfa = self.__fromdms(alfa)
        else:
            self.alfa = radians(alfa)
            
        if z =='':
            self.z = z
        elif type(z) == str:
            self.z =self.__fromdms(z)
        else:
            self.z = radians(z)

     
    def __fromdms(self,X): #zmiana ze stopni w ukladzie dms na radiany oraz stopnie dziesietne 
        '''
        Funkcja przelicza wartosc kąta z stopni na radiany
        
        Argumenty
        ---------
        X - wartosc kata w stopniach | TYPE : float
        
        Wynik
        ---------
        Z - wartosc kata w radianach | TYPE : float
        
        '''
        
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
        '''
        Funkcja służąca do transformacji współrzędnych ortokartezjańskich (prostokątnych) x, y, z 
        na współrzędne geodezyjne B, L, h.
        
        Argumenty:
        ----------
        X : TYPE: FLOAT
            Współrzędna X w układzie ortokartezjańskim
        Y : TYPE: FLOAT
            Współrzędna Y w układzie ortokartezjańskim
        Z : TYPE: FLOAT
            Współrzędna Z w układzie ortokartezjańskim
            
        Wynik:
        ----------
        
        f : TYPE: FLOAT
            Szerokokosc geodezyjna [stopnie]
        l: TYPE: FLOAT
            Długosc geodezyjna [stopnie]
        h : TYPE: FLOAT
            Wysokosc elipsoidalna [metry]
        
        '''
        
        a = self.a 
        e2 = self.e2 
        f_st = []
        l_st = []
        f_ost = []
        l_ost = []
        h_ost = []
        i = 0
        
        while i < len(self.X):
            X = self.X[i]
            Y = self.Y[i]
            Z = self.Z[i]
            
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
            
            f_st.append(self.__dms(f))
            l_st.append(self.__dms(l))
            h_ost.append(h)
            f_ost.append(f)
            l_ost.append(l)
            i += 1
            
        self.f = f_ost
        self.l = l_ost
        self.h = h_ost
        
        return(f_st, l_st, h_ost)
     
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
        '''
        Funkcja przelicza współrzędne geodezyjne na współrzędne prostokątne układu 2000.

        Parameters
        ----------
        f : TYPE : [float] : Szerokość geodezyjna [stopnie]
        l : TYPE : [float] : Długość geodezyjna [stopnie]
        
        m0 : TYPE, optional
            DESCRIPTION. The default is 0.999923.

        Raises
        ------
        NieprawidlowaWartosc
            DESCRIPTION.

        Returns
        -------
        x2000 : TYPE : [float] : współrzędna X w układzie 2000 [metry]
        y2000 : TYPE : [float] : współrzędna Y w układzie 2000 [metry]

        '''

        if self.f =='' or self.l =='':
            self.xyz2flh()
        f=self.f
        l=self.l
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
        '''
        Funkcja przelicza współrzędne geodezyjne na współrzędne prostokątne układu 1992.

        Parameters
        ----------
        f : TYPE : [float] : Szerokość geodezyjna [stopnie]
        l : TYPE : [float] : Długość geodezyjna [stopnie]
        
        l0 : TYPE, optional
            DESCRIPTION. The default is radians(19).
        m0 : TYPE, optional
            DESCRIPTION. The default is 0.9993.

        Returns
        -------
        x1992 : TYPE : [float] : współrzędna X w układzie 1992 [metry]
        y1992 : TYPE : [float] : współrzędna Y w układzie 1992 [metry]

        '''
        a=self.a
        e2=self.e2
        if self.f =='' or self.l =='':
            self.xyz2flh()
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
        x1992 = xgk * m0 - 5300000
        y1992 = ygk * m0 + 500000
        return(x1992,y1992)
      
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
        '''
        Funckja obliczająca wektor w układzie NEU
        
        Parameters:
        -----------
        X: TYPE : FLOAT
            Wspolrzedna X prostokatna[m]
        Y: TYPE : FLOAT
            Wspolrzedna Y prostokatna[m]
        Z: TYPE : FLOAT
            Wspolrzedna Z prostokatna[m]

        Returns
        -------
        NEU: TYPE : LIST 
            Współrzedne topocentryczne (North , East (E), Up (U))'''

        if self.f =='' or self.l =='':
            self.xyz2flh()

        f=self.f
        l=self.l
            
        if self.X2 =='' or self.Y2 =='' or self.Z2 =='':  
            dX = self.__saz2neu()
        else:
            dX = [self.X2, self.Y2, self.Z2]

        R = self.__Rneu(f, l)
        # print(R)
        NEU= R.T @ dX
        return(NEU)
        
    def flh2xyz(self):
        '''
        Funkcja przelicza ze współrzędnych krzywoliniowych na współrzędne prostokątne.
        
        Parameters:
        ----------
        
        phi - szerokość geograficzna punktu | typ: lista
        lam - długość geograficzna punktu   | typ: lista
        hel - wysokość punktu               | typ: float lub int

        Returns
        -------
        X - współrzędna prostokątna X punktu [metry] | typ: float
        Y - współrzędna prostokątna Y punktu [metry] | typ: float
        Z - współrzędna prostokątna Z punktu [metry] | typ: float

        '''
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
    
    def wczytajplik(self, plik, typ):
        dane = np.genfromtxt(plik, delimiter=',')#, skip_header = 4)
        
        if typ == 'XYZ':
            # self.X, self.Y, self.Z = (j[0], j[1], j[2])
            self.X = []
            self.Y = []
            self.Z = []
            for i, j in enumerate(dane):
                (self.X).append(j[0])
                (self.Y).append(j[1])
                (self.Z).append(j[2])
            # print(self.X, self.Y, self.Z)
            # if typ == 'flh':
            #     self.f, self.l, self.h = (j[0], j[1], j[2])
            # if typ == 'saz':
            #     self.s, self.alfa, self.a = (j[0], j[1], j[2])
            # if typ == 'XYZ2':
            #     self.X2, self.Y2, self.Z2 = (j[0], j[1], j[2])

 


if __name__=='__main__':
    
    proba1 = Transformacje(f='52 0 5.72012',
                            l='16 0 21.66234',
                            h=289.08952781930566,
                            s=43000.0,
                            alfa=230,
                            z=90,
                            X=3782450,
                            Y=1085030,
                            Z=5003140,
                            model='grs80')
    
    print('flh2xyz\n', proba1.flh2xyz())
    # print('PL1992\n', proba1.fl2PL1992())
    # print('PL2000\n', proba1.fl2PL2000())
    # print('NEU\n', proba1.xyz2neu())
    # print('HIRVONEN\n', proba1.xyz2flh())

    # proba2 = Transformacje(f='52 0 5.72012',
    #                         l='16 0 21.66234',
    #                         h=289.08952781930566,
    #                         s=43000.0,
    #                         alfa=230,
    #                         z=90,
    #                         X=[3782450, 3782450],
    #                         Y=[1085030, 1085030],
    #                         Z=[5003140, 5003140])
    
    # print('flh2xyz\n', proba2.flh2xyz())
    # print('PL1992\n', proba2.fl2PL1992())
    # print('PL2000\n', proba2.fl2PL2000())
    # print('NEU\n', proba2.xyz2neu())
    # print('HIRVONEN\n', proba2.xyz2flh())
    
    proba3 = Transformacje(model='kra')
    proba3.wczytajplik('test.txt', 'XYZ')
    # print(proba3.wczytajplik('test.txt', 'XYZ'))
    proba3.xyz2flh()
    print(proba3.xyz2flh())
   