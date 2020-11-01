# Sudoku ebazlea

Programa honek sudokuak ebazten ditu.

## Instalazioa

Programa honek Python 3-rekin funtzionatzen du.

Behar dituen liburutegiak instalatzeko, egin:

```shell script
pip install -r requirements.txt
```

## Exekuzioa

```shell script
python sudoku.py
```

Horrela exekutatuz gero, ebatzi nahi dugun sudokua eskuz sartuko diogu, elementu bakoitza banan-banan. Ebazpena arterainoko aukera eta pauso guztiak erakutsiko dizkigu, bakoitzaren ondoren `<enter>` tekla sakatu arte pausatuz.

Aukerako parametroak:

* `-h, --help`: erabilera eta parmetorei buruzko laguntza
* `-b, --ez_bistaratu`: ez erakutsi aukera eta pauso guztiak, baizki eta azken emaitza soilik
* `-g, --ez_gelditu`: ez gelditu pauso bakoitza erakutsi ostean
* `-a, --aurrez_definitua <AURREDEFINITUA>`: aurrez definitutako sudoku bat erabili adibide gisa, hauen artetik:
  * `hutsa`
  * `erraza1`
  * `erraza2`
  * `ertaina1`
  * `ertaina2`
  * `zaila1`
  * `zaila2`
  * `osozaila1`
  * `osozaila2`
  * `ebatziezina`
  * `ebazpenanitz`

## Lizentzia

Programa hau software librea da: birbanatu dezakezu, eta/edo aldatu,
Software Librearen Fundazioak argitaratutako GNU Lizentzia Publiko
Orokorraren baldintzen arabera, dela Lizentziaren 3. bertsioaren arabera
edo dela (nahi baduzu) bertsio berriagoren baten arabera.

Erabilgarria izango delakoan banatzen da programa hau, baina INOLAKO
BERMERIK GABE; ez du KOMERTZIALIZAGARRITASUNAREN EDO XEDE JAKIN BATERAKO
EGOKITASUNAREN berme inpliziturik ere. Xehetasun gehiagorako ikusi GNU
Lizentzia Publiko Orokorra.

Programa honekin batera GNU Lizentzia Publiko Orokorraren kopia bat jaso
eharko zenuke. Ez baduzu halakorik jaso, ikusi
<http://www.gnu.org/licenses/>.

## Egilea

Egilea: e-gor (Igor Leturia), <https://github.com/e-gor>
