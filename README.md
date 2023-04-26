# Transformacje Współrzędncyh

Program został napisany aby w szybki i łatwy sposób transformować oraz manipulować współrzędnymi. Skrypt oferuję takie transformacje jak:
  - XYZ (geocentryczne) -> BLH (elipsoidalne fi, lambda, h) 
  - BLH  (elipsoidalne fi, lambda, h)  -> XYZ (geocentryczne)
  - XYZ (geocentryczne) -> NEUp (topocentryczne northing, easting, up)
  - BL (elipsoidalne fi, lambda, h)  -> PL2000 
  - BL (elipsoidalne fi, lambda, h)  -> PL1992 
  - obsługuje elipsoidy ( GR80, WGS84, Krasowskiego)
  - do obsługi kodu wystarczy nam program python w wersji 3.9 wraz z zainstalowaną biblioteką 'numpy' i' math' oraz 'argparse'  jest możlwość także skorzystane z funkcji z konsoli Linuxowych np. GitBush. 
  - system operacyjny Windows 11 
  
Obsługa programu :
  Naszym plikiem wejściowym jest plik txt o nazwie 'wsp', w pliku znajdują sie podane współrzędne
   ![image](https://user-images.githubusercontent.com/129080867/234579943-3dea2586-7834-4930-8a5f-b9993b1069b4.png)
  
  Jako użytkownik chciałbym przeliczyć podane współrzędne we wszystkie metody transformacji jakie są dostępne w programie. Na początku pobieramy skrypt z zdalnego respozytorium https://github.com/PlaceForNick/projekt_1.git, odpalamy program python w wersji 3.9 importujemy wymienione biblioteki powyżej ( numpy oraz math).
  ![image](https://user-images.githubusercontent.com/129080867/234581247-6ec2991f-2336-489d-9617-41a1c19145f1.png)
  
  Aby przystąpić do obliczeń należy nazwać obiekt - na zdjęciu 'test1', a nastepnie wywołać funkcje 'Transformacje', w nawiasie określamy argumenty.
  - 'model' jest to brany model elipsoidy, do wyboru mamy ( 'grs80','kra', 'wgs84' )
  - 'zapis' ( True , False) program pyta się nas czy chcemy aby nasze wyniki końcowe zostały zestawione w pliku txt.
  - 'nazwa' - wybieramy dowolna nazwe naszego pliku tekstowego z wynikami 
  ![image](https://user-images.githubusercontent.com/129080867/234584514-de212cdd-d66e-420e-94d1-34fd5a05be75.png)

  W naszym przykładzie użyliśmy modelu elipsoidy Krasowskiego , właczyliśmy zapis pliku końcowego w txt o nazwie 'wynik'. 
  Przed rozpoczęciem transformormacji musimy wczytać plik do programu na pomoc przychodzi nam funckja, która jest dostępna w naszym programie. 
  ![image](https://user-images.githubusercontent.com/129080867/234585375-02521963-66d9-4df3-bd78-5db56fcacc11.png)
 
 Argumentami jakie ta funkcja przyjmuje są :
   - 'wsp.txt' - nazwa pliku odczytywanego przez program 
   - 'XYZ' - tutaj mamy parę możliwości , jeśli nasz plik txt składa się z współrzędnych XYZ -> 'XYZ', flh -> 'flh' , saz -> 'saz'.
 W naszym przypadku korzystamy z 'XYZ'.
 Nadszedł czas aby wykorzystać pierwsza definicje z programu. Przy okazji aby wywołać wyniki w pythonie uzywamy 'print'. Aby przeliczyć nasze współrzedne XYZ na współrzędne fi lambda i h używamy funkcje 'xyz2flh'. Składnia powinna wyglądać tak :
 ![image](https://user-images.githubusercontent.com/129080867/234589809-006356f0-148d-406e-a662-be638f3ad2ad.png)

 
 
  Wynik jaki powinniśmy uzyskać to pojawienie się nowego pliku txt ( w naszym przypadku 'wynik').
  ![image](https://user-images.githubusercontent.com/129080867/234590080-0590e520-4fd6-4335-aa07-068d8632b04c.png)
W pliku 'wynik' pojawiła się tabelka ze współzednymi podanymi w stopniach minuatch i sekundach a wysokość w metrach. 
Teraz spróbujmy odwrócić proces, użyjmy funkcji 'flh2xyz' . Składna funkcji jest taka sama jak wyżej.
![image](https://user-images.githubusercontent.com/129080867/234591499-2b7535be-c318-4967-bef7-cee05e2774b3.png)
Otwieramy ponownie plik wyjściowy 'wynik' i mamy taką sytuacje: 
![image](https://user-images.githubusercontent.com/129080867/234591882-869ef439-bc2a-4cbe-b44a-98751cb76839.png)

Porównując współrzędne z pliku wejściowego 'wsp' a plikiem wyjściowym 'wynik' możemy śmiało powiedzieć że obie funkcje działają bez problemowo. 

 
  
  
  

  

  
  
  
