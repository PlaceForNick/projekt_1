# Transformacje Współrzędncyh

# Spis Treści:
- [Infomacje o programie](#informacje-o-programie)
- [Obsługa programu](#obsługa-programu)
  - [Wprowadznie danych](#wprowadznie-danych)
    - [Za pośrednictem pythona](#za-pośrednictem-pythona)
    - [Za pośrednictem pliku tekstowego](#za-pośrednictem-pliku-tekstowego)
    - [Za pośrednistwem konsoli](#za-pośrednistwem-konsoli)
  - [Przykładowe wywołania](#przykładowe-wywołania)
    - [xyz2flh(), flh2xyz()](#xyz2flh-flh2xyz)
    - [fl2PL1992(), fl2PL2000()](#fl2pl1992-fl2pl2000)
    - [xyz2neu()](#xyz2neu)
- [Znane błędy](#znane-błędy)
  - [Wprowadzenie wszystkich możliwych danych jednocześnie](#wprowadzenie-wszystkich-możliwych-danych-jednocześnie)
  - [Nie wprowadzenie żadnych danych](#nie-wprowadzenie-żadnych-danych)
  - [Błędy przy próbie odkodowania znaków specjalnych](#błędy-przy-próbie-odkodowania-znaków-specjalnych)
  - [Błędy przy próbie przeliczenia ze stopni](#błędy-przy-próbie-przeliczenia-ze-stopni)
  - [błędy przy podaniu wartości poza zasięgiem stef odwzorowaczych układu PL2000](#błędy-przy-podaniu-wartości-poza-zasięgiem-stef-odwzorowaczych-układu-pl2000)

## Informacje o programie:
Program został napisany aby w szybki i łatwy sposób transformować oraz manipulować współrzędnymi. Skrypt oferuję takie transformacje jak:
  - XYZ (geocentryczne) -> BLH (elipsoidalne fi, lambda, h) 
  - BLH  (elipsoidalne fi, lambda, h)  -> XYZ (geocentryczne)
  - XYZ (geocentryczne) -> NEUp (topocentryczne northing, easting, up)
  - BL (elipsoidalne fi, lambda, h)  -> PL2000 
  - BL (elipsoidalne fi, lambda, h)  -> PL1992 
  - obsługuje elipsoidy ( GR80, WGS84, Krasowskiego)
  - do obsługi kodu wystarczy nam program python w wersji 3.9 wraz z zainstalowaną biblioteką 'numpy' i' math' oraz 'argparse'  jest możlwość także skorzystane z funkcji z konsoli Linuxowych np. GitBush. 
  - system operacyjny Windows 11 
  
# Obsługa programu:
## Wprowadznie danych:
### Za pośrednictem pythona:
```
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
```


### Za pośrednictem pliku tekstowego:

  Naszym plikiem wejściowym jest plik txt o nazwie 'wsp', w pliku znajdują sie podane współrzędne
  ![image](https://user-images.githubusercontent.com/129080867/234604463-bbb852d6-9fcd-4cbc-84d8-7b1b482f379f.png)


### Za pośrednistwem konsoli:
```
 python skrypt.py -h
usage: skrypt.py [-h] [-X X] [-Y Y] [-Z Z] [-X2 X2] [-Y2 Y2] [-Z2 Z2] [-s S]
                 [-alfa ALFA] [-z Z] [-f F] [-l L] [-H H]
                 [--model {grs80,wgs84,kra}]
                 [--metoda {xyz2flh,neu,flh2xyz,pl2000,pl1992}]
                 [--zapis {True,False}] [--nazwa NAZWA]

Transformacje wspolrzednych

options:
  -h, --help            show this help message and exit
  -X X                  wartosc wspolrzednej pierwszegi punktu X [m]
  -Y Y                  wartosc wspolrzednej pierwszego punktu Y [m]
  -Z Z                  wartosc wspolrzednej pierwszego punktu Z [m]
  -X2 X2                wartosc wspolrzednej drugiego punktu X [m]
  -Y2 Y2                wartosc wspolrzednej drugiego punktu Y [m]
  -Z2 Z2                wartosc wspolrzednej drugiego punktu Z [m]
  -s S                  wartosc dlugosci miedzy dwoma punktami [m]
  -alfa ALFA            wartosc kat poziomego [° ' '']
  -z Z                  wartosc kat zenitalnego [° ' '']
  -f F                  wartosc wspolrzednej f [° ' '']
  -l L                  wartosc wspolrzednej l [° ' '']
  -H H                  wartosc wspolrzednej H [m]
  --model {grs80,wgs84,kra}
                        model elipsoidy
  --metoda {xyz2flh,neu,flh2xyz,pl2000,pl1992}
                        metoda transformacji
  --zapis {True,False}  zapis do pliku tekstowego (.txt)
  --nazwa NAZWA         nazwa pliku wyjsciowego (.txt)


```
## Przykładowe wywołania:
### xyz2flh(), flh2xyz():
  Jako użytkownik chciałbym przeliczyć podane współrzędne we wszystkie metody transformacji jakie są dostępne w programie. Na początku pobieramy skrypt z zdalnego respozytorium https://github.com/PlaceForNick/projekt_1.git, odpalamy program python w wersji 3.9 importujemy wymienione biblioteki powyżej ( numpy oraz math).
   ```
 import numpy as np
from math import *
import argparse
from skrypt import *
   
  ```
  
  Aby przystąpić do obliczeń należy nazwać obiekt - na zdjęciu 'test1', a nastepnie wywołać funkcje 'Transformacje', w nawiasie określamy argumenty.
  - 'model' jest to brany model elipsoidy, do wyboru mamy ( 'grs80','kra', 'wgs84' )
  - 'zapis' ( True , False) program pyta się nas czy chcemy aby nasze wyniki końcowe zostały zestawione w pliku txt.
  - 'nazwa' - wybieramy dowolna nazwe naszego pliku tekstowego z wynikami 
```
  test1 = Transformacje(model='kra', zapis=True, nazwa='wynik')
```
  W naszym przykładzie użyliśmy modelu elipsoidy Krasowskiego , właczyliśmy zapis pliku końcowego w txt o nazwie 'wynik'. 
  Przed rozpoczęciem transformormacji musimy wczytać plik do programu na pomoc przychodzi nam funckja, która jest dostępna w naszym programie. 
  ```
  test1.wczytajplik('wsp.txt' , 'XYZ')
 ```
 Argumentami jakie ta funkcja przyjmuje są :
   - 'wsp.txt' - nazwa pliku odczytywanego przez program 
   - 'XYZ' - tutaj mamy parę możliwości , jeśli nasz plik txt składa się z współrzędnych XYZ -> 'XYZ', flh -> 'flh' , saz -> 'saz'.
 W naszym przypadku korzystamy z 'XYZ'.
 Nadszedł czas aby wykorzystać pierwsza definicje z programu. Przy okazji aby wywołać wyniki w pythonie uzywamy 'print'. Aby przeliczyć nasze współrzedne XYZ na współrzędne fi lambda i h używamy funkcje 'xyz2flh'. Składnia powinna wyglądać tak : ```print('\nHIRVONEN\n', test1.xyz2flh())```

  Wynik jaki powinniśmy uzyskać to pojawienie się nowego pliku txt ( w naszym przypadku 'wynik').
  ![image](https://user-images.githubusercontent.com/129080867/234590080-0590e520-4fd6-4335-aa07-068d8632b04c.png)
W pliku 'wynik' pojawiła się tabelka ze współzednymi podanymi w stopniach minuatch i sekundach a wysokość w metrach. 
Teraz spróbujmy odwrócić proces, użyjmy funkcji 'flh2xyz' . Składna funkcji jest taka sama jak wyżej.
```
import numpy as np
from math import *
import argparse
from skrypt import *

test1 = Transformacje(model='kra', zapis=True, nazwa='wynik')
test1.wczytajplik('wsp.txt' , 'XYZ')
print('\nHIRVONEN\n', test1.xyz2flh())
print('\nflh2xyz\n', test1.flh2xyz())
```
Otwieramy ponownie plik wyjściowy 'wynik' i mamy taką sytuacje: 
![image](https://user-images.githubusercontent.com/129080867/234591882-869ef439-bc2a-4cbe-b44a-98751cb76839.png)

### fl2PL1992(), fl2PL2000():
Porównując współrzędne z pliku wejściowego 'wsp' a plikiem wyjściowym 'wynik' możemy śmiało powiedzieć że obie funkcje działają bez problemowo. 
W podobny sposoób działają funkcje :
```
print('\nPL1992\n', test1.fl2PL1992()) # przeliczenie f,l na x,y w układzie PL1992
print('\nPL2000\n', test1.fl2PL2000()) # przeliczenie f,l na x,y w układzie PL2000
```

### xyz2neu()
Metoda xyz2neu() jest natomiast nieco bardziej zawiła. Do jej wykorzystania potrzebujemy bowiem dwoch zestawow danych. Jednym z nich są współrzędne miejsca obserwacji (flh lub XYZ) natomiast drugim współrzędne celu (XYZ2) lub odległość oraz kąty pionowy i zenitalny do tego celu (saz). Po wprowadzeniu tych danych możemy wywołać tę metodę w sposób następujący:
```
print('\nNEU\n', proba3.xyz2neu())
```

# Znane błędy

## Wprowadzenie wszystkich możliwych danych jednocześnie

Jedną z funkcjonalności tego programu jest automatyczne wykonywanie obliczeń, o które użytkownik bezpośrednio nie prosił. Na przykład chcąc przeliczyć współrzędne do układu PL1992 możemy podać współrzędne XYZ. Program samodzielnie przeliczy je na flh, a następnie poda nam interesujące nas współrzędne w układzie PL2000.
Jednakże nie ma praktycznie żadnego ograniczenia w tym ile i jakie wartości przypiszemy dla naszego obiektu. Dlatego też możliwe jest jednoczesne podanie współrzędnych XYZ punktu A oraz współrzędnych flh punktu B dla tego samego obiektu. Jest to wysoce niezalecane gdyż w połączeniu z funkcjonalnością wykonywania obliczeń w sposób automatyczny, opisaną wyżej może skutkować w utraceniu kontroli nad wykonywanymi przez program obliczeniami! 

## Nie wprowadzenie żadnych danych

Nie ma praktycznie żadnego ograniczenia w tym ile i jakie wartości przypiszemy dla tworzonego przez nas obiektu. Możliwe jest niepodanie żadnej wartości, aczkolwiek będzie to skutkować błędem programu przy próbie wykonania jakiejkolwiek metody.

## Błędy przy próbie odkodowania znaków specjalnych

Geneza tego problemu nie jest dokładnie znana, prawdopodobnie pojawia się on przy wywołaniu programu za pośrednictwem konsoli. Skutkuje on zamianą wszsytkich znaków specjalnych w pliku (m.in. znaków polskich) na inne, bliżej nieokreślone znaki. Taka zamiana może w krytycznych przypadkach niemożnaością korzystania z programu. W celu zapobiegawczym znaki specjalne zostały usunięte z kodu, jednakże niektóre z nich mogły zostać przeoczone. W związku z tym istnieje ryzyko ponownego zaistnienia błędu.

## Błędy przy próbie przeliczenia ze stopni

Program (w szczególności metoda ```__fromdms()```, ukryta przed użytkownikiem) z bliżej nieokreślonych przyczyn może nieumieć prawidłowo odczytać wartości kątów podanych w określony sposób (Pomimo, że teoretycznie powinna. Problem prawdopodobnie polega na mnogości znaków specjalnych, podczas gdy metada ta rozpoznaje tylko ograniczoną ich ilość.) Z tego powodu zaleca się podawanie wartości kątów w następujących formatach:
- ```123 45 67.890 ``` [stopnie minuty sekundy]
- ```123.4567890``` [stopnie dziesiętne]
- ```123``` [stopnie]


## Błędy przy podaniu wartości poza zasięgiem stef odwzorowaczych układu PL2000

Przy wczytaniu serii wielu danych znajdujących się poza zakresem stef odwzorowaczych układu PL2000 oraz próbie wykonania metody ```fl2PL2000```, program nie może opuścić pętli, przy jednoczesnym zwracaniu na konsolę błędu ```NieprawidlowaWartosc```.
  
  
  

  

  
  
  
