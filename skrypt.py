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
        
    def __init__(self, model, zapis = False, nazwa = 'output', X='', Y='', Z='', f='', l='', h='', X2='', Y2='', Z2='', s='', alfa='', z = ''):
        
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
        # print(model,self.b)
        
        if zapis == True:
            self.zapis = zapis
            self.nazwa = nazwa + '.txt'
            self.plik = open(self.nazwa, 'w')
            self.plik.close()
        elif zapis == False:
            self.zapis = zapis
        else:
            raise NotImplementedError(f'Podana przez Ciebie wartość zapis "{zapis}" jest nieprawidłowa. Wybierz jedna z podanych ponizej wartosci:'
                                      '- False'
                                      '- True')
        if type(X) == list:
            self.X = X
        else:
            self.X = []
            (self.X).append(X)
        
        if type(Y) == list:
            self.Y = Y
        else:
            self.Y = []
            (self.Y).append(Y)
        
        if type(Z) == list:
            self.Z = Z
        else:
            self.Z = []
            (self.Z).append(Z)
        
        if type(f) == list:
            self.f = f
        else:
            self.f = []
            (self.f).append(f)
        
        if type(l) == list:
            self.l = l
        else:
            self.l = []
            (self.l).append(l)
        
        if type(h) == list:
            self.h = h
        else:
            self.h = []
            (self.h).append(h)
            
        if type(X2) == list:
            self.X2 = X2
        else:
            self.X2 = []
            (self.X2).append(X2)
            
        if type(Y2) == list:
            self.Y2 = Y2
        else:
            self.Y2 = []
            (self.Y2).append(Y2)
        
        if type(Z2) == list:
            self.Z2 = Z2
        else:
            self.Z2 = []
            (self.Z2).append(Z2)
            
        if type(s) == list:
            self.s = s
        else:
            self.s = []
            (self.s).append(s)
        
        if type(alfa) == list:
            self.alfa = alfa
        else:
            self.alfa = []
            (self.alfa).append(alfa)
            
        if type(z) == list:
            self.z = z
        else:
            self.z = []
            (self.z).append(z)
                
        f_ost = []
        i = 0  
        while True:
            try:
                f = self.f[i]
                if f =='':
                    f = f
                elif type(f) == str:
                    f = self.__fromdms(f)
                else:
                    f = radians(f)
                f_ost.append(f)
                i += 1
            except IndexError:
                break
            except TypeError:
                break
        self.f = f_ost
        
        l_ost = []
        i = 0     
        while True:
            try:
                l = self.l[i]
                if l =='':
                    l = l
                elif type(l) == str:
                    l = self.__fromdms(l)
                else:
                    l = radians(l)
                l_ost.append(l)
                i += 1
            except IndexError:
                break
            except TypeError:
                break
        self.l = l_ost
        
        alfa_ost = []
        i = 0     
        while True:
            try:
                alfa = self.alfa[i]           
                if alfa =='':
                    alfa = alfa
                elif type(alfa) == str:
                    alfa = self.__fromdms(alfa)
                else:
                    alfa = radians(alfa)
                alfa_ost.append(alfa)
                i += 1
            except IndexError:
                break
            except TypeError:
                break                
        self.alfa = alfa_ost
        
        z_ost = []
        i = 0     
        while True:
            try:
                z = self.z[i]
                if z =='':
                    z = z
                elif type(z) == str:
                    z =self.__fromdms(z)
                else:
                    z = radians(z)
                z_ost.append(z)
                i += 1
            except IndexError:
                break
            except TypeError:
                break
        self.z = z_ost
     
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
        
        if self.zapis == True:
            self.plik = open(self.nazwa, 'a')
            self.plik.write('--------------------------------------------------\n')
            self.plik.write("f [° ' '']         l [° ' '']         h [m]\n")
            self.plik.write('--------------------------------------------------\n')
            i = 0
            while i < len(f_st):
                self.plik.write(f'{f_st[i]} {l_st[i]} {h_ost[i]:10.3f}\n')
                i += 1
            self.plik.close()
        
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
        a = self.a 
        e2 = self.e2 
        x_ost = []
        y_ost = []
        i = 0
        
        while i < (len(self.f) or len(self.X)):

            if self.f == [''] or self.l == ['']:
                self.xyz2flh()
            f = self.f[i]
            l = self.l[i]

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
                
                x_ost.append(x2000)
                y_ost.append(y2000)
                i += 1
        
        if self.zapis == True:
            self.plik = open(self.nazwa, 'a')
            self.plik.write('--------------------------------------------------\n')
            self.plik.write("x 2000 [m]         y 2000 [m]\n")
            self.plik.write('--------------------------------------------------\n')
            i = 0
            while i < len(x_ost):
                self.plik.write(f'{x_ost[i]:10.3f} {y_ost[i]:10.3f}\n')
                i += 1
            self.plik.close()
            
        return(x_ost,y_ost)

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
        x_ost = []
        y_ost = []
        i = 0
        
        while i < (len(self.f) or len(self.X)):
        
            if self.f == [''] or self.l == ['']:
                self.xyz2flh()
            f = self.f[i]
            l = self.l[i]
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
            
            x_ost.append(x1992)
            y_ost.append(y1992)
            i += 1
        
        if self.zapis == True:
            self.plik = open(self.nazwa, 'a')
            self.plik.write('--------------------------------------------------\n')
            self.plik.write("x 1992 [m]         y 1992 [m]\n")
            self.plik.write('--------------------------------------------------\n')
            i = 0
            while i < len(x_ost):
                self.plik.write(f'{x_ost[i]:10.3f} {y_ost[i]:10.3f}\n')
                i += 1
            self.plik.close()
            
        return(x_ost,y_ost)
      
    def __saz2neu(self, s, alfa, z):
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

        a=self.a
        e2=self.e2
        NEU_ost = []
        i = 0
        
        while i < (len(self.f) or len(self.X)):
        
            if self.f == [''] or self.l == ['']:
                self.xyz2flh()
            f = self.f[i]
            l = self.l[i]
            
            if self.X2 == [''] or self.Y2 == [''] or self.Z2 == ['']:  
                dX = self.__saz2neu(self.s[i], self.alfa[i], self.z[i])
            else:
                dX = [self.X2[i], self.Y2[i], self.Z2[i]]
    
            R = self.__Rneu(f, l)
            NEU = R.T @ dX
            
            NEU_ost.append(NEU)
            i += 1
            print(self.s, self.alfa, self.z)
        if self.zapis == True:
            self.plik = open(self.nazwa, 'a')
            self.plik.write('--------------------------------------------------\n')
            self.plik.write("N [m]              E [m]              U [m]\n")
            self.plik.write('--------------------------------------------------\n')
            i = 0
            while i < len(NEU_ost): 
                self.plik.write(f'{NEU_ost[i][0]:10.3f} {NEU_ost[i][1]:10.3f} {NEU_ost[i][2]:10.3f}\n')
                i += 1
            self.plik.close()
            
        return(NEU_ost)
        
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
        a = self.a 
        e2 = self.e2 
        x_ost = []
        y_ost = []
        z_ost = []
        i = 0
        
        while i < len(self.f):
            f = self.f[i]
            l = self.l[i]
            h = self.h[i]

            N = self.__Np(f)
            x = (N+h)*np.cos(f)*np.cos(l)
            y = (N+h)*np.cos(f)*np.sin(l)
            z = ((N*(1-e2)+h))*np.sin(f)
            
            x_ost.append(x)
            y_ost.append(y)
            z_ost.append(z)
            i += 1
        
        if self.zapis == True:
            self.plik = open(self.nazwa, 'a')
            self.plik.write('--------------------------------------------------\n')
            self.plik.write("X [m]              Y [m]              Z [m]\n")
            self.plik.write('--------------------------------------------------\n')
            i = 0
            while i < len(x_ost):
                self.plik.write(f'{x_ost[i]:10.3f} {y_ost[i]:10.3f} {z_ost[i]:10.3f}\n')
                i += 1
            self.plik.close()
            
        return(x_ost, y_ost, z_ost)
    
    def wczytajplik(self, plik, typ, nr = 0):
        
        if typ == 'XYZ':
            dane = np.genfromtxt(plik, delimiter=',')#, skip_header = 4)
            self.X = []
            self.Y = []
            self.Z = []
            for i, j in enumerate(dane):
                (self.X).append(j[nr + 0])
                (self.Y).append(j[nr + 1])
                (self.Z).append(j[nr + 2])
                
        elif typ == 'XYZ2':
            dane = np.genfromtxt(plik, delimiter=',')#, skip_header = 4)
            self.X2 = []
            self.Y2 = []
            self.Z2 = []
            for i, j in enumerate(dane):
                (self.X2).append(j[nr + 0])
                (self.Y2).append(j[nr + 1])
                (self.Z2).append(j[nr + 2])
            
                
        elif typ == 'flh':
            dane = np.genfromtxt(plik, delimiter=',', dtype=str)#, skip_header = 4)
            self.f = []
            self.l = []
            self.h = []
            for i, j in enumerate(dane):
                i = 0
                for x in j[nr + 0]:
                    if x ==' ':
                        j[nr + 0] = (j[nr + 0])[i:]
                        i += 1
                    else:
                        break
                i = 0
                for x in j[nr + 1]:
                    if x ==' ':
                        j[nr + 1] = (j[nr + 1])[i:]
                        i += 1
                    else:
                        break
                try:
                    x = float(j[nr + 0])
                    (self.f).append(np.radians(x)) 
                except ValueError:
                    (self.f).append(self.__fromdms(j[nr + 0]))
                try:
                    x = float(j[nr + 1])
                    (self.l).append(np.radians(x))
                except ValueError:
                    (self.l).append(self.__fromdms(j[nr + 1]))
                (self.h).append(float(j[nr + 2]))
                
        elif typ == 'saz':
            dane = np.genfromtxt(plik, delimiter=',', dtype=str)#, skip_header = 4)
            self.s = []
            self.alfa = []
            self.z = []
            for i, j in enumerate(dane):
                for x in j[nr + 1]:
                    if x ==' ':
                        j[nr + 1] = (j[nr + 1])[i:]
                        i += 1
                    else:
                        break
                i = 0
                for x in j[nr + 2]:
                    if x ==' ':
                        j[nr + 2] = (j[nr + 2])[i:]
                        i += 1
                    else:
                        break
                (self.s).append(float(j[nr + 0]))
                print(j[nr + 1])
                try:
                    x = float(j[nr + 1])
                    (self.alfa).append(np.radians(x))  
                except ValueError:
                    (self.alfa).append(self.__fromdms(j[nr + 1]))
                try:
                    x = float(j[nr + 2])
                    (self.z).append(np.radians(x))           
                except ValueError:
                    (self.z).append(self.__fromdms(j[nr + 2]))
        
        else:
            raise NotImplementedError(f'Podany przez Ciebie typ danych "{typ}" jest nieporawny. Wybierz jedna z podanych ponizej wartosci:\n'
                                      '- XYZ\n'
                                      '- XYZ2\n'
                                      '- flh\n'
                                      '- saz\n')
    
if __name__=='__main__':
    
    # proba1 = Transformacje(f='52 0 5.72012',
    #                        l='16 0 21.66234',
    #                        h=289.08952781930566,
    #                        s=43000.0,
    #                        alfa=230,
    #                        z=90,
    #                        X=3782450,
    #                        Y=1085030,
    #                        Z=5003140,
    #                        model='grs80',
    #                        zapis=True)
    
    # print('\nflh2xyz\n', proba1.flh2xyz())
    # print('\nPL1992\n', proba1.fl2PL1992())
    # print('\nPL2000\n', proba1.fl2PL2000())
    # print('\nNEU\n', proba1.xyz2neu())
    # print('\nHIRVONEN\n', proba1.xyz2flh())

    # proba2 = Transformacje(f='52 0 5.72012',
    #                         l='16 0 21.66234',
    #                         h=289.08952781930566,
    #                         s=43000.0,
    #                         alfa=230,
    #                         z=90,
    #                         X=[3782450, 3782450],
    #                         Y=[1085030, 1085030],
    #                         Z=[5003140, 5003140],
    #                         model='grs80')
    
    # print('\nflh2xyz\n', proba2.flh2xyz())
    # print('\nPL1992\n', proba2.fl2PL1992())
    # print('\nPL2000\n', proba2.fl2PL2000())
    # print('\nNEU\n', proba2.xyz2neu())
    # print('\nHIRVONEN\n', proba2.xyz2flh())
    
    proba3 = Transformacje(model='kra', zapis=True, nazwa='output2')
    # proba3.wczytajplik('test.txt', 'XYZ')
    proba3.wczytajplik('test.txt', 'flh', nr = 3)
    proba3.wczytajplik('test.txt', 'saz', nr = 6)

    # print('\nflh2xyz\n', proba3.flh2xyz())
    # print('\nPL1992\n', proba3.fl2PL1992())
    # print('\nPL2000\n', proba3.fl2PL2000())
    print('\nNEU\n', proba3.xyz2neu())
    # print('\nHIRVONEN\n', proba3.xyz2flh())
   