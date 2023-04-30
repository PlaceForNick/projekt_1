import numpy as np
from math import *
import argparse
  
class NieprawidlowaWartosc(Exception):
    pass
    '''
    Blad oznaczajacy podanie niepoprawnej lub/i nieobslugiwanej przez program wartosci.
    '''
        
class Transformacje():
        
    def __init__(self, model='grs80', zapis=False, nazwa='', X='', Y='', Z='', f='', l='', h='', X2='', Y2='', Z2='', s='', alfa='', z =''):
        
        self.__elipsoida(model) #wybor elipsoidy
        self.__zapiszplik(zapis, nazwa) #wybor zapisu do pliku txt     

        #zamiana podanych danych na liste
        dane = [X, Y, Z, f, l, h, X2, Y2, Z2, s, alfa, z]
        dane_ost = []
        for wartosc in dane:
            if type(wartosc) == list:
                wartosc_lista = wartosc
            else:
                wartosc_lista = []
                wartosc_lista.append(wartosc)
            dane_ost.append(wartosc_lista)
        self.X = dane_ost[0]
        self.Y = dane_ost[1]
        self.Z = dane_ost[2]
        self.f = dane_ost[3]
        self.l = dane_ost[4]
        self.h = dane_ost[5]
        self.X2 = dane_ost[6]
        self.Y2 = dane_ost[7]
        self.Z2 = dane_ost[8]
        self.s = dane_ost[9]
        self.alfa = dane_ost[10]
        self.z = dane_ost[11]
        
        #zamiana stopni na radiany           
        dane_kat = [self.f, self.l, self.alfa, self.z]
        dane_kat_ost = []
        for wartosc_lista in dane_kat:
            wartosc_ost = []
            i = 0  
            while True:
                try:
                    wartosc = wartosc_lista[i]
                    if wartosc =='':
                        wartosc = wartosc
                    elif type(wartosc) == str:
                        wartosc = self.__fromdms(wartosc)
                    else:
                        wartosc = radians(wartosc)
                    wartosc_ost.append(wartosc)
                    i += 1
                except IndexError:
                    break
            dane_kat_ost.append(wartosc_ost)
        self.f = dane_kat_ost[0]
        self.l = dane_kat_ost[1]
        self.alfa = dane_kat_ost[2]
        self.z = dane_kat_ost[3]
        
        try:
            self.__wykonajmetode(self.metoda) #wybor metody dla argparse
        except AttributeError:
            pass  
            
    
    def __elipsoida(self, model):
        #wybor elipsoidy
        if    model  == 'kra':
            self.a= 6378245
            self.b= 6356863.01877
        elif  model == "wgs84":
            self.a = 6378137.0 
            self.b = 6356752.31424518 
        elif  model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        else:
            raise NieprawidlowaWartosc(f"{model} ten model elipsoidy nie jest obslugiwany")
        self.splasz = (self.a - self.b) / self.a
        self.e2 = (2 * self.splasz - self.splasz ** 2)
        
    def __zapiszplik(self, zapis, nazwa):
        #wybor zapisu do pliku txt
        if zapis == True:
            self.zapis = zapis
            self.nazwa = nazwa
            self.plik = open(self.nazwa, 'w')
            self.plik.close()
        elif zapis == False:
            self.zapis = zapis
        else:
            raise NieprawidlowaWartosc(f'Podana przez Ciebie wartosc zapis "{zapis}" jest nieprawidlowa. Wybierz jedna z podanych ponizej wartosci:\n'
                                      '- False\n'
                                      '- True')
    
    def __wykonajmetode(self, metoda):
        #wybor metody dla argparse
        # try:
            if self.metoda == 'xyz2flh':
                print(self.xyz2flh())
            elif self.metoda == 'flh2xyz':
                print(self.flh2xyz())
            elif self.metoda == 'pl2000':
                print(self.fl2PL2000())
            elif self.metoda == 'pl1992':
                print(self.fl2PL1992())
            elif self.metoda == 'neu':
                print(self.xyz2neu())
            elif self.metoda == '':
                pass
            else:
                raise NieprawidlowaWartosc(f"{self.metoda} ta metoda transformacji wspolrzednych nie jest obslugiwana")
        # except AttributeError:
            # pass  
        
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
        
    def xyz2flh(self): #HIRVONEN
        '''
        Funkcja sluzacaca do transformacji wspolrzednych ortokartezjanskich (prostokatnych) x, y, z 
        na wspolrzedne geodezyjne B, L, h.
        
        Argumenty:
        ----------
        X : TYPE: [FLOAT/ LIST OF FLOAT]
            Wspolrzedna X w ukladzie ortokartezjanskim [metry]
            
        Y : TYPE: FLOAT
            Wspolrzedna Y w ukladzie ortokartezjanskim [metry]
            
        Z : TYPE: [FLOAT/ LIST OF FLOAT]
            Wspolrzedna Z w ukladzie ortokartezjanskim [metry]
            
        Wynik:
        ----------
        
        f : TYPE: [FLOAT/ LIST OF FLOAT]
            Szerokokosc geodezyjna [stopnie]
            
        l: TYPE: [FLOAT/ LIST OF FLOAT]
            Dlugosc geodezyjna [stopnie]
            
        h : TYPE: [FLOAT/ LIST OF FLOAT]
            Wysokosc elipsoidalna [metry]
        
        '''
        try:
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
        
        except TypeError:
            raise NieprawidlowaWartosc('Podane dane są nieprawidłowe do skorzystnia z metody xyz2flh(). Podane przez Ciebie wartosci to:\n'
                                       f'- X = {self.X}\n'
                                       f'- Y = {self.Y}\n'
                                       f'- Z = {self.Z}\n'
                                       'Metoda ta mogła zostać wykonana automatycznie przez program, jeśli do wykonania innej metody podano niepoprawne wartości flh lub nie podano ich wcale. Podane przez Ciebie wartosci to:\n'
                                       f'- f = {self.f}\n'
                                       f'- l = {self.l}\n'
                                       f'- h = {self.h}')
     
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
        Funkcja przelicza wspolrzedne geodezyjne na wspolrzedne prostokatne ukladu 2000.

        Parameters
        ----------
        f : TYPE : [FLOAT/ LIST OF FLOAT] 
            Szerokosc geodezyjna [stopnie]
            
        l : TYPE : [FLOAT/ LIST OF FLOAT]
            Dlugosc geodezyjna [stopnie]
        
        m0 : TYPE, optional
            DESCRIPTION. The default is 0.999923.

        Raises
        ------
        NieprawidlowaWartosc
            DESCRIPTION.

        Returns
        -------
        x2000 : TYPE : [FLOAT/ LIST OF FLOAT] 
            Wspolrzedna X w ukladzie 2000 [metry]
            
        y2000 : TYPE : [FLOAT/ LIST OF FLOAT] 
            Wspolrzedna Y w ukladzie 2000 [metry]

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
                raise NieprawidlowaWartosc(f'podana wartosc l znajduje sie poza zakresem stref odwzorowawcych ukladu wspolrzednych PL2000. '
                                           f'Obslugiwany zakres to {13.5}° - {25.5}° '
                                           f'Podana przez Ciebie wartosc to {self.__dms(l)}')
           
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
        Funkcja przelicza wspolrzedne geodezyjne na wspolrzedne prostokatne ukladu 1992.

        Parameters
        ----------
        f : TYPE : [FLOAT/ LIST OF FLOAT]
            Szerokosc geodezyjna [stopnie]
            
        l : TYPE : [FLOAT/ LIST OF FLOAT]
            Dlugosc geodezyjna [stopnie]
        
        l0 : TYPE, optional
            DESCRIPTION. The default is radians(19).
            
        m0 : TYPE, optional
            DESCRIPTION. The default is 0.9993.

        Returns
        -------
        x1992 : TYPE : [FLOAT/ LIST OF FLOAT]
            Wspolrzedna X w ukladzie 1992 [metry]
        
        y1992 : TYPE : [FLOAT/ LIST OF FLOAT]
            Wspolrzedne Y w ukladzie 1992 [metry]

        '''
        a=self.a
        e2=self.e2
        x_ost = []
        y_ost = []
        i = 0
        
        while i < (len(self.f) or len(self.X)):
            if self.f[i] =='' or self.l[i] =='':
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
        Funckja obliczajaca wektor w ukladzie NEU
        
        Parameters:
        -----------
        X: TYPE : [FLOAT/ LIST OF FLOAT]
            Wspolrzedna X prostokatna [metry]
            
        Y: TYPE : [FLOAT/ LIST OF FLOAT]
            Wspolrzedna Y prostokatna [metry]
            
        Z: TYPE : [FLOAT/ LIST OF FLOAT]
            Wspolrzedna Z prostokatna [metry]

        Returns
        -------
        NEU: TYPE : LIST OF FLOAT
            Wspolrzedne topocentryczne (North , East (E), Up (U))
            
        '''
        try:
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
        
        except TypeError:
            raise NieprawidlowaWartosc('Podane dane są nieprawidłowe do skorzystnia z metody xyz2neu(). Podane przez Ciebie wartosci to:\n'
                                       f'- s = {self.s}\n'
                                       f'- alfa = {self.alfa}\n'
                                       f'- z = {self.z}\n'
                                       'Ewentualnie można też wykożystać XYZ2 zamiast saz. Podane przez Ciebie wartosci to:\n'
                                       f'- X2 = {self.X2}\n'
                                       f'- Y2 = {self.Y2}\n'
                                       f'- Z2 = {self.Z2}\n'
                                       'Oprócz tego potrzebne są też XYZ lub fl, ale te są podane poprawne.')
            
    def flh2xyz(self):
        '''
        Funkcja przelicza ze wspolrzednych krzywoliniowych na wspolrzedne prostokatne.
        
        Parameters:
        ----------
        
        f : TYPE:  [FLOAT/ LIST OF FLOAT]
            Szerokosc geodezyjna punktu 
            
        l : TYPE: [FLOAT/ LIST OF FLOAT]
            Dlugosc geograficzna punktu   
            
        h : TYPE: [FLOAT/ LIST OF FLOAT]
            Wysokosc punktu               

        Returns
        -------
        X :  TYPE : [FLOAT/ LIST OF FLOAT] 
            Wspolrzedna prostokatna X punktu [metry] 
            
        Y : TYPE : [FLOAT/ LIST OF FLOAT] 
            Wspolrzedna prostokatna Y punktu [metry]
            
        Z :  TYPE : [FLOAT/ LIST OF FLOAT]
            Wspolrzedna prostokatna Z punktu [metry] 

        '''
        try:
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
        
        except TypeError:
            raise NieprawidlowaWartosc('Podane dane są nieprawidłowe do skorzystnia z tej metody. Podane przez Ciebie wartosci to:\n'
                                       f'- f = {self.f}\n'
                                       f'- l = {self.l}\n'
                                       f'- h = {self.h}')
    
    def wczytajplik(self, plik, typ, nr = 0):
        
        if typ == 'XYZ':
            dane = np.genfromtxt(plik, delimiter=',', skip_header = 4)
            self.X = []
            self.Y = []
            self.Z = []
            for i, j in enumerate(dane):
                (self.X).append(j[nr + 0])
                (self.Y).append(j[nr + 1])
                (self.Z).append(j[nr + 2])
                
        elif typ == 'XYZ2':
            dane = np.genfromtxt(plik, delimiter=',', skip_header = 4)
            self.X2 = []
            self.Y2 = []
            self.Z2 = []
            for i, j in enumerate(dane):
                (self.X2).append(j[nr + 0])
                (self.Y2).append(j[nr + 1])
                (self.Z2).append(j[nr + 2])
            
                
        elif typ == 'flh':
            dane = np.genfromtxt(plik, delimiter=',', dtype=str, skip_header = 4)
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
            dane = np.genfromtxt(plik, delimiter=',', dtype=str, skip_header = 4)
            self.s = []
            self.alfa = []
            self.z = []
            for i, j in enumerate(dane):
                i = 0
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
            raise NieprawidlowaWartosc(f'Podany przez Ciebie typ danych "{typ}" jest nieporawny. Wybierz jedna z podanych ponizej wartosci:\n'
                                      '- XYZ\n'
                                      '- XYZ2\n'
                                      '- flh\n'
                                      '- saz\n')

    def wczytajzargparse(self):
        
        parser = argparse.ArgumentParser(description='Transformacje wspolrzednych')
        
        parser.add_argument('-X', help='wartosc wspolrzednej pierwszegi punktu X [m]', required=False, default='')
        parser.add_argument('-Y', help='wartosc wspolrzednej pierwszego punktu Y [m]', required=False, default='')
        parser.add_argument('-Z', help='wartosc wspolrzednej pierwszego punktu Z [m]', required=False, default='')
        
        parser.add_argument('-X2', help='wartosc wspolrzednej drugiego punktu X [m]', required=False, default='')
        parser.add_argument('-Y2', help='wartosc wspolrzednej drugiego punktu Y [m]', required=False, default='')
        parser.add_argument('-Z2', help='wartosc wspolrzednej drugiego punktu Z [m]', required=False, default='')
        
        parser.add_argument('-s', help='wartosc dlugosci miedzy dwoma punktami [m]', required=False, default='')
        parser.add_argument('-alfa', help="wartosc kat poziomego [Â° ' '']", required=False, default='')
        parser.add_argument('-z', help="wartosc kat zenitalnego [Â° ' '']", required=False, default='')
           
        parser.add_argument('-f', help="wartosc wspolrzednej f [Â° ' '']", required=False, default='')
        parser.add_argument('-l', help="wartosc wspolrzednej l [Â° ' '']", required=False, default='')
        parser.add_argument('-H', help='wartosc wspolrzednej H [m]', required=False, default='')
        
        parser.add_argument('--model', help='model elipsoidy', choices=['grs80','wgs84', 'kra'], required=False, type=str, default='grs80')
        parser.add_argument('--metoda', help='metoda transformacji', choices=['xyz2flh','neu', 'flh2xyz','pl2000','pl1992'], required=False, type=str, default='')
        parser.add_argument('--zapis', help='zapis do pliku tekstowego (.txt)', choices=[True, False], required=False, type=bool, default=False)
        parser.add_argument('--output', help='nazwa pliku wyjsciowego (.txt)', required=False, type=str, default='output')
        parser.add_argument('--input', help='nazwa pliku wejsciowego (.txt)', required=False, type=str, default='input')
        parser.add_argument('--odczyt', help='odczyt z pliku tekstowego (.txt)', choices=[True, False], required=False, type=bool, default=False)
        parser.add_argument('--typ', help='typ danych zawartych we wczytywanym pliku', choices=['XYZ','XYZ2','flh','saz'], required=False, type=str, default='')
        
        args = parser.parse_args()
        
        #zamiana podanych argumentow na float o ile to mozliwe
        dane = [args.X, args.Y, args.Z, args.f, args.l, args.H, args.X2, args.Y2, args.Z2, args.s, args.alfa, args.z]
        dane_ost = []
        for wartosc in dane:
            try:
                wartosc = float(wartosc)
            except ValueError:
                wartosc = wartosc
            dane_ost.append(wartosc)
            
        self.metoda = args.metoda
        
        if args.odczyt == True:
            self.wczytajplik(args.input, args.typ)
            self.__elipsoida(args.model)
            self.__zapiszplik(args.zapis, args.output)
            self.__wykonajmetode(self.metoda)
        else:  
            nazwa = args.output
            zapis = args.zapis
            model = args.model
            self.__init__(model=model, zapis=zapis, nazwa=nazwa, X=dane_ost[0], Y=dane_ost[1], Z=dane_ost[2], f=dane_ost[3], l=dane_ost[4], h=dane_ost[5], X2=dane_ost[6], Y2=dane_ost[7], Z2=dane_ost[8], s=dane_ost[9], alfa=dane_ost[10], z=dane_ost[11])    
    
if __name__=='__main__':
    
    #PRZYKLADOWE WYWOLANIA
    
    proba1 = Transformacje(f='52 0 5.72012',
                           l='16 0 21.66234',
                           h=289.08952781930566,
                           s=43000.0,
                           alfa=230,
                           z=90,
                           X=3782450,
                           Y=1085030,
                           Z=5003140,
                           model='grs80',
                           zapis=True,
                           nazwa='output1')
    
    # print('\nflh2xyz\n', proba1.flh2xyz())
    # print('\nPL1992\n', proba1.fl2PL1992())
    # print('\nPL2000\n', proba1.fl2PL2000())
    # print('\nNEU\n', proba1.xyz2neu())
    print('\nHIRVONEN\n', proba1.xyz2flh())

    proba2 = Transformacje(f='52 0 5.72012',
                           l='16 0 21.66234',
                           h=289.08952781930566,
                           s=43000.0,
                           alfa=230,
                           z=90,
                           X=[3782450, 3782450],
                           Y=[1085030, 1085030],
                           Z=[5003140, 5003140],
                           model='grs80')
    
    # print('\nflh2xyz\n', proba2.flh2xyz())
    # print('\nPL1992\n', proba2.fl2PL1992())
    # print('\nPL2000\n', proba2.fl2PL2000())
    # print('\nNEU\n', proba2.xyz2neu())
    # print('\nHIRVONEN\n', proba2.xyz2flh())
    
    # proba3 = Transformacje(model='kra', zapis=True, nazwa='output2')
    # proba3.wczytajplik('test.txt', 'XYZ')
    # # proba3.wczytajplik('test.txt', 'flh', nr = 3)
    # proba3.wczytajplik('test.txt', 'saz', nr = 6)

    # # print('\nflh2xyz\n', proba3.flh2xyz())
    # print('\nPL1992\n', proba3.fl2PL1992())
    # # print('\nPL2000\n', proba3.fl2PL2000())
    # # print('\nNEU\n', proba3.xyz2neu())
    # # print('\nHIRVONEN\n', proba3.xyz2flh())
    
    # proba4 = Transformacje(model='grs80', zapis=True, nazwa='output3')
    # proba4.wczytajplik('wsp_inp.txt', 'XYZ')
    # proba4.fl2PL2000()
    
    proba4 = Transformacje(f = '52 5 50.18',
                           l = '21 1 53.52',
                           s = 31000,
                           alfa = 280,
                           z = 90)
    print(proba4.xyz2neu())
    proba5 = Transformacje()
    proba5.wczytajzargparse()