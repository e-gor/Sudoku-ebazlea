# -*- coding: utf-8 -*-
"""
Sudoku ebazlea

Programa honek sudokuak ebazten ditu.

Copyright (C) 2020 e-gor (Igor Leturia)

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

Egilea: e-gor (Igor Leturia), <https://github.com/e-gor>

Iturburu-kode osoa, jarraibideak eta lizentzia: <https://github.com/e-gor/Sudoku-ebazlea>
"""

import re
from copy import deepcopy
import argparse

import termcolor
import boxea


# Garantiarik ezaren mezua (GNU GPL v3.0)
warranty_message = """  Bermea-ukatzea.

  PROGRAMAK EZ DU BERMERIK, LEGE APLIKAGARRIAK ONARTZEN DUEN NEURRIAN. IDATZIZ
AURKAKORIK ADIERAZTEN EZ BADA, EGILE-ESKUBIDEEN JABEEK ETA/EDO BESTE ALDERDI
BATZUEK PROGRAMA «BERE HORRETAN» EMATEN DUTE INOLAKO BERMERIK GABE, EZ
ESPRESUKI ADIERAZITAKORIK EZ INPLIZITURIK, BARNE HARTUZ, BAINA HORRETARA MUGATU
GABE, KOMERTZIALIZAGARRITASUNAREN EDO XEDE JAKIN BATERAKO EGOKITASUNAREN
BERMEAK. PROGRAMAREN KALITATEARI ETA ERRENDIMENDUARI DAGOKIONEZ, ZURE GAIN DAGO
ARRISKU GUZTIA. PROGRAMAK AKATSIK IZANGO BALU, ZURE GAIN HARTU BEHARKO DUZU
BEHAR DIREN ZERBITZUEN, KONPONKETEN EDO ZUZENKETEN KOSTUA.

  Erantzukizun-mugatzea.

  EZ BADA LEGE APLIKAGARRIAK EDO IDATZIZKO KONTRATU BATEK HALA ESKATZEN
DUELAKO, EGILE-ESKUBIDEEN EDOZEIN JABERI EDO GOIAN BAIMENTZEN DEN BEZALA
PROGRAMA HELARAZTEN EDO BERTAN ALDAKETAK EGITEN DITUEN BESTE ALDERDI BATI,
EZINGO DIOZU ERANTZUKIZUNIK ESKATU KALTEENGATIK, EZTA PROGRAMA ERABILTZETIK EDO
ERABILI EZINETIK SOR LITEZKEEN EDOZEIN ERATAKO KALTE OROKORRAK, BEREZIAK,
EZUSTEKOAK EDO ONDORIOZKOAK IZANDA ERE (BESTEAK BESTE, INFORMAZIOA GALTZEA,
DATU OKERRAK EMATEA, EDO ZUK EDO HIRUGARRENEK JASANDAKO GALERAK, EDO PROGRAMA
GAI EZ IZATEA BESTE PROGRAMA BATZUEKIN LAN EGITEKO), NAHIZ ETA ESKUBIDEEN
JABEAK EDO BESTE ALDERDI BATEK HALAKO KALTEAK SORTZEKO AUKERAREN BERRI IZAN.

  Aurreko atalen interpretazioa.

  Goian zehaztutako berme-ukatzeari eta erantzukizun-mugatzeari, ezartzen
dituzten baldintzak direla-eta, ezin bazaie legezko baliorik eman
jurisdikzioren batean, kasua aztertzen duten auzitegiek tokiko legeak aplikatu
beharko dituzte, Programari lotutako edozein erantzukizun zibilen uko-egite
absolutuari ahalik eta gehien hurbiltzeko moduan, salbu eta Programaren kopia
batekin batera, kuota bat ordainduta, berme bat edo erantzukizun-hartze bat
eskaintzen bada."""

# Birbanaketa baldintzen mezua (GNU GPL v3.0)
conditions_message = """  Hitzez hitzeko kopiak helaraztea.

  Programaren iturburu-kodearen hitzez hitzeko kopiak helaraz ditzakezu, jaso
bezala, edozein euskarritan, baina, horretarako, kopia bakoitzean egile-
eskubideen ohar bat argitaratu beharko duzu modu ikusgarri eta egoki batean;
oso-osorik mantendu beharko dituzu bai Lizentzia hau eta bai 7. atalaren
arabera gehitzen den edozein baldintza murriztaile kodeari aplikatzen zaizkiola
zehazten duten ohar guztiak; oso-osorik mantendu beharko dituzu bermerik ezaren
inguruko ohar guztiak; eta Lizentzia honen kopia bat eman beharko diezu
hartzaile guztiei Programarekin batera.

  Kopiak prezio baten truke edo dohainik helaraz ditzakezu, eta laguntza-
zerbitzua edo berme-babesa eskain dezakezu kuota baten truke.

  Iturburu-kodearen bertsio aldatuak helaraztea.

  Programan oinarritutako lan bat helaraz dezakezu, edo Programatik abiatuta
lan hori sortzeko egin behar diren aldaketak, iturburu-kodearen forman, 4.
ataleko baldintzak betez, eta, gainera, beste baldintza hauek guztiak ere
betez:

    a) Lana aldatu duzula adierazi behar duzu ohar nabarmenen bidez, eta data
    adierazgarri bat eman.

    b) Adierazi behar duzu lana Lizentzia honen arabera eta 7. atalean jasotzen
    den edozein baldintzaren arabera argitaratu dela ohar nabarmenen bidez.
    Eskakizun honek 4. ataleko eskakizun bat aldatzen du: «ohar guztiak
    oso-osorik mantentzea».

    c) Lana bere osotasunean hartzen duen Lizentzia bat eman behar diozu kopia
    bat eskuratzen duen edonori. Ondorioz, Lizentzia hau, 7. ataleko edozein
    baldintza osagarri aplikagarrirekin batera, lan osoari aplikatuko zaio, eta
    lanaren atal guztiei, nola paketatu diren kontuan hartu gabe. Lizentzia
    honek ez du baimenik ematen lanaren lizentziak beste edozein modutara
    emateko, baina ez du halako baimenik baliogabetzen bereizita jaso baldin
    baduzu.

    d) Lanak erabiltzaile-interfaze interaktiboak baldin baditu, horietako
    bakoitzak Lege-ohar Egokiak erakutsi behar ditu. Hala ere, Programak
    Lege-ohar Egokiak erakusten ez dituzten interfaze interaktiboak baldin
    baditu, ez dituzu gehitu beharko zure lanean.

  Babestutako lan batek beste lan bereizi eta independente batzuekin batera
bilduma bat osatzen duenean, baldin eta lanok babestutako lanaren luzapenak ez
badira eta babestutako lanarekin programa handiago bat osatzeko konbinatzen ez
badira, biltegiratze-bolumen edo banaketa-euskarri batean, bilduma horri
«agregatu» esaten zaio, baldin eta bilduma eta haren egile-eskubideak ez badira
erabiltzen bildumaren erabiltzaileen sarbidea edo legezko eskubideak mugatzeko,
lan bakoitzak baimentzen duenetik harago. Babestutako lan bat agregatu batean
sartzeak ez du behartuko Lizentzia hau agregatuaren gainerako atalei
aplikatzera.

  Iturburu-kode ez diren formetan helaraztea.

  Babestutako lanak objektu-kodean helaraz ditzakezu, 4. eta 5. ataletako
baldintzen arabera, baldin eta horrekin batera Dagokion Iturburua, makina bidez
irakurgarria, ere helarazten baduzu Lizentzia honen baldintzen arabera, modu
hauetako batean:

    a) Objektu-kodea produktu fisiko batean, edo horren barruan, (banaketarako
    euskarri fisikoetan barne) helarazi, Dagokion Iturburuarekin batera
    normalean softwareak trukatzeko erabiltzen den euskarri fisiko iraunkor
    batean.

    b) Objektu-kodea produktu fisiko batean, edo horren barruan, (banaketarako
    euskarri fisikoetan barne) helarazi, idatzizko eskaintza batekin batera,
    objektu-kodea daukan edozeini eskaintzeko: (1) Dagokion Iturburuaren kopia
    bat Lizentzia honek babesten duen produktu barneko software guztiarentzat,
    normalean softwareak trukatzeko erabiltzen den euskarri fisiko iraunkor
    batean, eta iturburua fisikoki helaraztea kostatu zaizun zentzuzko prezioa
    baino gehiago kobratu gabe, edo (2) Dagokion Iturburua kopiatzeko sarbidea,
    kosturik gabeko sareko zerbitzari batetik. Eskaintza hori baliagarria
    izango da gutxienez hiru urterako eta produktu-modelo horrentzako ordezko
    piezak edo bezeroarentzako zerbitzua eskaintzen dituzun bitartean.

    c) Objektu-kodearen banakako kopiak helarazi, Dagokion Iturburua emateko
    idatzizko eskaintzaren kopia batekin batera. Aukera hau kasu batzuetan
    baino ez dago baimenduta eta modu ez komertzialean, eta zuk ere objektu-
    kodea halako eskaintza batekin jaso baduzu soilik, 6b azpiatalean zehazten
    den bezala.

    d) Objektu-kodea helarazi izendatutako leku batetik sarbidea eskainiz
    (dohainik edo kostu baten truke), eta Dagokion Iturbururako sarbide berdina
    eskainiz, modu berean eta leku beretik eta kostu gehigarririk gabe.
    Hartzaileei ez daukazu eskatu beharrik Dagokion Iturburua objektu-
    kodearekin batera kopiatzeko. Objektu-kodea kopiatzeko lekua sareko
    zerbitzari bat baldin bada, Dagokion Iturburua beste zerbitzari batean egon
    daiteke (zuk edo hirugarren batek kudeatzen duzuen batean), baina
    zerbitzari horrek kopiatzeko erraztasun baliokideak eskaini beharko ditu,
    eta objektu-kodearen ondoan jarraibide argiak eman beharko dituzu, Dagokion
    Iturburua non aurkitu adieraziz. Dagokion Iturburua edozein zerbitzaritan
    egonda ere, eskuragarri dagoela segurtatu behar duzu, baldintza hauek
    betetzeko behar den denbora guztian zehar.

    e) Objektu-kodea helarazi parekoen arteko (peer-to-peer) transmisioaren
    bidez, beste parekoei jakinaraziz publiko orokorrak non eskura ditzakeen
    lanaren objektu-kodea eta Dagokion Iturburua, inolako kosturik gabe, 6d
    azpiatalak ezartzen duen bezala.

  Lanaren objektu-kodea helaraztean, ez dago zertan sartu objektu-kodearen zati
banangarririk, zati horren iturburu-kodea Dagokion Iturburutik kanpo geratzen
bada Sistema Liburutegi gisa.

  «Erabiltzaile Produktu» bat da (1) «kontsumitzaile-produktu» bat, hau da,
edozein ondasun pertsonal ukigarri, normalean norberaren gauzetarako, edo
familiako edo etxeko kontuetarako erabiltzen dena, edo (2) etxebizitza batean
erabiltzeko diseinatzen edo saltzen den edozer. Produktu bat kontsumitzaile-
produktu bat den zehazteko, zalantza dagoen kasuetan babesaren alde egin behar
da. Erabiltzaile batek jasotzen duen produktu jakin bati buruz, «normalean
erabiltzen dela» aipatzen denean esan nahi da hori dela produktu mota horren
erabilera ohikoa edo arrunta, alde batera utzita erabiltzaile jakin baten
estatusa edo horrek ematen dion, edo ematea espero dion, erabilera. Produktu
bat kontsumitzaile-produktutzat joko da, funtsean erabilera komertzialak,
industrialak edo kontsumotik kanpokoak dituen kontuan hartu gabe, erabilera
horiek produktua erabiltzeko modu adierazgarri bakarra direnean izan ezik.

  Erabiltzaile Produktu baten «Instalazio Informazio» gisa jotzen da edozein
metodo, prozedura, baimen-gako edo bestelako informazio, babestutako lan baten
bertsio aldatuak Erabiltzaile Produktu horretan instalatzeko eta exekutatzeko
beharrezko dena, Dagokion Iturburuaren bertsio aldatutik abiatuta. Informazioak
nahikoa izan behar du segurtatzeko aldatutako objektu-kodearen funtzionamendu
etengabea ez dela eragotziko edo oztopatuko aldaketa egin izanagatik bakarrik.

  Atal honen arabera Lan baten objektu-kodea helarazten baduzu Erabiltzaile
Produktu batean, edo batekin batera, edo berariaz Produktu horretan
erabiltzeko, eta transakzio baten baitan helarazten baduzu, zeinaren bidez
produktuaren edukitza- eta erabilera-eskubideak hartzaileari transferitzen
baitzaizkio epe mugatu baterako edo betiko (transakzioaren ezaugarriak kontuan
hartu gabe), atal honen arabera helarazitako Dagokion Iturburua Instalazio
Informazioarekin batera helarazi beharko duzu. Hala ere, betekizun hori hau ez
da aplikatuko, baldin eta zuk edo hirugarren batek ez baduzue aldatutako
objektu-kodea Erabiltzaile Produktuan instalatzeko gaitasuna atxikitzen
(adibidez, lana ROM memorian instalatu bada).

  Instalazio Informazioa eman beharrak ez du esan nahi laguntza-zerbitzua,
bermea edo eguneratzeak helarazten jarraitu behar denik lana hartzaileak aldatu
edo instalatu duen kasuetan edo lana instalatua edo aldatua izan den
Erabiltzaile Produktuaren kasuan. Sare baterako sarbidea uka daiteke aldaketak
berak sarearen funtzionamenduari eragiten dionean modu material eta
kaltegarrian edo sarearen bidezko komunikazio-arau edo -protokoloak hausten
dituenean.

  Atal honen arabera helarazitako Dagokion Iturburua eta emandako Instalazio
Informazioa, publikoki dokumentatutako formatu batean eman beharko dira
(publikoarentzat iturburu-kodean eskuragarri dagoen inplementazio batekin),
inolako pasahitz edo gako berezirik eskatu gabe paketea irekitzeko, irakurtzeko
edo kopiatzeko.

  Baldintza osagarriak.

  «Baimen osagarriak» dira Lizentzia honen baldintzak osatzen dituzten
baldintzak, Lizentziako baldintza bat edo gehiago salbuetsiz. Programa osoari
aplikatzekoak diren baimen osagarriak Lizentzia honen zati balira bezala
tratatu beharko dira, baldin eta lege aplikagarrien arabera baliozkoak badira.
Baimen osagarriak Programaren zati bati soilik aplikatzen bazaizkio, zati hori
bereizirik erabili ahal izango da baimen horien arabera, baina Programak, bere
osotasunean, Lizentzia honen mende jarraituko du baimen osagarriak aintzat
hartu gabe.

  Babestutako lan baten kopia helarazten duzunean, edozein baimen osagarri
ezabatu dezakezu, nahi izanez gero, kopia horretatik edo kopiaren edozein
zatitatik. (Zenbait kasutan, lana aldatzen duzunean, baimen osagarriak idatz
daitezke baimen horiek ezaba daitezen eskatzeko). Materialari baimen osagarriak
gehi diezazkiokezu, babestutako lan bati gehitu diozun materialaren kasuan,
baldin eta egile-eskubideen baimen egokia baldin baduzu edo eman baldin
badezakezu.

  Lizentzia honen beste edozein xedapen alde batera utzita, babestutako lan
bati gehitzen diozun materialari dagokionez, Lizentzia honen baldintzak beste
baldintza hauekin osa ditzakezu (material horren egile-eskubideen jabeek hala
baimentzen badute):

    a) Bermeak ukatzea edo erantzukizunak mugatzea Lizentzia honen 15. eta 16.
ataletako baldintzetatik harago, edo

    b) Zentzuzko lege-ohar espezifikoak edo egiletasun-aitortzeak mantentzera
behartzea, aipatutako materialean edo material hori jasotzen duten lanetan
erakusten diren Lege-ohar Egokietan, edo

    c) Materialaren jatorriaren desitxuratzea debekatzea, edo aldatutako
bertsioak jatorrizko bertsiotik desberdintzen direla zentzuz adierazi behar
izatea, edo

    d) Materialaren lizentzia-emaileen edo egileen izenak publizitate asmoekin
erabiltzea mugatzea, edo

    e) Izen komertzialak, markak edo zerbitzu-markak erabiltzeko marka-legearen
araberako eskubideak emateari uko egitea, edo

    f) Material horren lizentzia-emaileen eta egileen kalte-ordaina exijitzea,
materiala (edo materialaren bertsio aldatua) hartzailearekiko erantzukizunak
kontratu bidez hartuta helarazten duen orori, kontratu bidez hartutako
erantzukizun horiek lizentzia-emaileei eta egileei zuzenean inposatzen dieten
erantzukizun orotarako.

  Bestelako baldintza osagarri murriztaile guztiak «bestelako murrizketa» gisa
jasotzen dira 10. atalean. Programak, jaso bezala, edo programaren edozein
zatik, ohar bat baldin badu, Programari, Lizentzia honez gain, bestelako
murrizketa bat ezartzen dion baldintza batekin, baldintza hori ezaba dezakezu.
Lizentzia-dokumentu batek, bestelako murrizketa bat eduki arren, baimena ematen
badu birlizentziatzeko edo helarazteko Lizentzia honen baldintzapean,
babestutako lanari edozein material gehi diezaiokezu lizentzia-dokumentu horren
baldintzen arabera, baldin eta bestelako murrizketa ez bada mantentzen
birlizentziatu edo helarazi ondoren.

  Babestutako lan bati atal honen arabera baldintzak gehitzen badizkiozu,
dagozkion iturburu-fitxategietan deklarazio bat gehitu beharko duzu fitxategi
horiei aplikatzen zaizkien baldintza osagarriekin, edo, bestela, baldintza
horiek non aurkitu adierazten duen ohar bat.

  Baldintza osagarriak (permisiboak edo murriztaileak) idatzizko lizentzia
bereizi batean zehaztu daitezke, edo salbuespen modura; nolanahi ere, goian
aipatutako baldintzak aplikatuko dira."""


# Sudoku adibideak
hasierako_sudokua_hutsa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

hasierako_sudokua_erraza_1 = [
    [2, 4, 0, 9, 0, 0, 0, 7, 3],
    [6, 0, 0, 0, 4, 2, 9, 0, 8],
    [0, 1, 0, 0, 7, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 6],
    [0, 6, 4, 0, 0, 0, 8, 5, 0],
    [3, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 2, 0, 0, 8, 0],
    [4, 0, 2, 6, 1, 0, 0, 0, 5],
    [5, 7, 0, 0, 0, 9, 0, 2, 4],
]

hasierako_sudokua_erraza_2 = [
    [0, 1, 8, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 4, 0, 0, 2, 6],
    [0, 0, 0, 1, 0, 9, 0, 0, 4],
    [0, 0, 4, 6, 0, 2, 3, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 5, 4, 0, 7, 8, 0, 0],
    [2, 0, 0, 5, 0, 3, 0, 0, 0],
    [8, 5, 0, 0, 9, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 2, 7, 0],
]

hasierako_sudokua_ertaina_1 = [
    [5, 0, 0, 0, 4, 0, 0, 0, 0],
    [3, 0, 0, 7, 0, 0, 2, 0, 0],
    [0, 6, 0, 2, 0, 0, 0, 5, 0],
    [0, 4, 7, 0, 0, 5, 0, 0, 0],
    [0, 9, 1, 0, 0, 0, 4, 6, 0],
    [0, 0, 0, 6, 0, 0, 9, 1, 0],
    [0, 5, 0, 0, 0, 3, 0, 9, 0],
    [0, 0, 8, 0, 0, 7, 0, 0, 3],
    [0, 0, 0, 0, 1, 0, 0, 0, 6],
]

hasierako_sudokua_ertaina_2 = [
    [0, 7, 1, 0, 9, 0, 4, 0, 6],
    [0, 6, 2, 0, 0, 0, 7, 0, 0],
    [0, 4, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 6, 0, 0, 9, 2, 0, 3],
    [0, 0, 0, 1, 0, 3, 0, 0, 0],
    [4, 0, 7, 5, 0, 0, 1, 0, 0],
    [0, 0, 0, 9, 0, 0, 0, 5, 0],
    [0, 0, 5, 0, 0, 0, 3, 1, 0],
    [6, 0, 3, 0, 1, 0, 9, 4, 0],
]

hasierako_sudokua_zaila_1 = [
    [0, 0, 2, 4, 5, 6, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 8, 0, 0, 0, 6, 1, 0],
    [9, 0, 0, 5, 0, 1, 0, 0, 7],
    [7, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 5, 0, 0, 0, 0, 0, 3, 0],
    [0, 8, 0, 9, 0, 2, 0, 5, 0],
    [0, 1, 0, 0, 3, 0, 0, 4, 0],
    [0, 9, 0, 8, 1, 5, 0, 2, 0],
]

hasierako_sudokua_zaila_2 = [
    [0, 6, 0, 0, 0, 0, 0, 0, 5],
    [2, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 2, 0, 0, 6, 9],
    [0, 0, 9, 0, 0, 0, 5, 0, 1],
    [0, 0, 6, 7, 5, 3, 9, 0, 0],
    [0, 0, 3, 0, 0, 0, 7, 0, 6],
    [0, 8, 0, 0, 4, 0, 0, 5, 3],
    [3, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 0, 8],
]

hasierako_sudokua_osozaila_1 = [
    [5, 0, 6, 0, 0, 0, 0, 9, 7],
    [7, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 9, 7, 1, 0, 6, 0, 4],
    [0, 5, 0, 0, 8, 0, 4, 0, 0],
    [0, 0, 7, 6, 0, 3, 2, 0, 0],
    [0, 0, 2, 0, 7, 0, 0, 5, 0],
    [3, 0, 5, 0, 6, 8, 7, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 5],
    [9, 6, 0, 0, 0, 0, 8, 0, 2],
]

hasierako_sudokua_osozaila_2 = [
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 8, 3, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 9, 2, 7, 5, 0],
    [4, 0, 0, 0, 3, 0, 9, 0, 0],
    [1, 0, 2, 0, 0, 9, 0, 4, 7],
    [8, 0, 0, 0, 1, 0, 2, 0, 0],
    [0, 0, 0, 0, 2, 4, 5, 7, 0],
    [5, 0, 9, 6, 0, 1, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0],
]

hasierako_sudokua_ebatziezina = [
    [0, 6, 0, 0, 0, 0, 0, 1, 4],
    [0, 5, 0, 8, 0, 0, 6, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 7, 0, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 8],
    [0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 9, 0, 5, 4, 0],
    [0, 4, 0, 5, 0, 0, 0, 9, 0],
    [0, 3, 0, 0, 0, 2, 0, 0, 0],
]

hasierako_sudokua_ebazpenanitz = [
    [0, 6, 0, 0, 0, 0, 0, 1, 4],
    [0, 5, 0, 8, 0, 0, 6, 0, 0],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 7, 0, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 8],
    [0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 9, 0, 5, 4, 0],
    [0, 0, 0, 5, 0, 0, 0, 9, 0],
    [0, 3, 0, 0, 0, 2, 0, 0, 0],
]

hasierako_sudokuak = {
    "hutsa": hasierako_sudokua_hutsa,
    "erraza1": hasierako_sudokua_erraza_1,
    "erraza2": hasierako_sudokua_erraza_2,
    "ertaina1": hasierako_sudokua_ertaina_1,
    "ertaina2": hasierako_sudokua_ertaina_2,
    "zaila1": hasierako_sudokua_zaila_1,
    "zaila2": hasierako_sudokua_zaila_2,
    "osozaila1": hasierako_sudokua_osozaila_1,
    "osozaila2": hasierako_sudokua_osozaila_2,
    "ebatziezina": hasierako_sudokua_ebatziezina,
    "ebazpenanitz": hasierako_sudokua_ebazpenanitz
}


def bistaratu_taula(sudoku_arraya, kolore_zerrendak=(), zabalera=None):
    """
    Sudoku bat modu politean eta ertzekin bistaratzen du pantailan, nahi izanez gero elementu batzuk kolore batelkin nabarmenduz.
     
    :param sudoku_arraya: sudokua bi dimentsiotako array gisa; aukeren array-a ere izan daiteke
    :param kolore_zerrendak: nabarmendu nahi diren elementuen zerrenda bat; elementu bakoitzarentzat koordenatuak, nabarmendu nahi den karakterea eta kolorea adierazten dira
    :param zabalera: elementuak zabalera jakin batekin justifikatu eta zentratzeko; ez bada pasatzen, elementu luzeenaren luzerarekin justifikatu eta zentratzen dira elementu guztiak
    :return: ez du ezer itzultzen
    """

    if zabalera is None:
        zabalera = max([len(str(elementua)) for lerroa in sudoku_arraya for elementua in lerroa])
    sudoku_arraya_zentratuta = [[str(e).center(zabalera) for e in lerroa] for lerroa in sudoku_arraya]
    zutabe_luzera_maximoak = [max(map(len, zutabea)) for zutabea in zip(*sudoku_arraya_zentratuta)]
    formatua = ''
    banatzeko_lerroa = ''
    for indizea, formatua_elementua in enumerate('{{:{}}}'.format(x) for x in zutabe_luzera_maximoak):
        if indizea % 3 == 0:
            if indizea // 3 == 0:
                banatzailea = '| '
                banatzeko_lerroa_banatzailea = '+-'
            else:
                banatzailea = ' | '
                banatzeko_lerroa_banatzailea = '-+-'
        else:
            banatzailea = ' '
            banatzeko_lerroa_banatzailea = '-'
        formatua = formatua + banatzailea + formatua_elementua
        banatzeko_lerroa = banatzeko_lerroa + banatzeko_lerroa_banatzailea + ('-' * len(formatua_elementua.format(*sudoku_arraya_zentratuta[0][0])))
    formatua = formatua + ' |'
    banatzeko_lerroa = banatzeko_lerroa + '-+'
    taula = []
    for indizea, lerroa in enumerate(sudoku_arraya_zentratuta):
        if indizea % 3 == 0:
            taula.append(banatzeko_lerroa)
        taula.append(formatua.format(*lerroa))
    taula.append(banatzeko_lerroa)
    taula = boxea.ascii_to_box('\n'.join(taula))
    for errepikapena in range(3):
        taula = taula.replace(' ─ ', ' - ')
    taula_zerrenda = taula.split('\n')
    for kolore_zerrenda in kolore_zerrendak:
        lerro_indizea = kolore_zerrenda[0]
        zutabe_indizea = kolore_zerrenda[1]
        lerro_indizea = lerro_indizea + 1 + (lerro_indizea // 3)
        lerroa = taula_zerrenda[lerro_indizea]
        lerroa_zerrenda = re.split(r'([│ ]+)', lerroa)
        zutabe_indizea = (zutabe_indizea + 1) * 2
        if kolore_zerrenda[3].startswith('on_'):
            lerroa_zerrenda[zutabe_indizea] = lerroa_zerrenda[zutabe_indizea].replace(kolore_zerrenda[2], termcolor.colored(kolore_zerrenda[2], on_color=kolore_zerrenda[3]))
        else:
            lerroa_zerrenda[zutabe_indizea] = lerroa_zerrenda[zutabe_indizea].replace(kolore_zerrenda[2], termcolor.colored(kolore_zerrenda[2], kolore_zerrenda[3]))
        taula_zerrenda[lerro_indizea] = ''.join(lerroa_zerrenda)
    taula = '\n'.join(taula_zerrenda)
    return taula


def ezabatu_aukerak_elementutik(elementuaren_aukerak, lerro_indizea, zutabe_indizea, sudoku_arraya):
    """
    Elementu batentzat dauden aukerak ezabatzen dira, sudokuko lerro, zutabe eta koadro bereko elementuak kontuan izanda. 
    
    :param elementuaren_aukerak: elementu batentzat dauden aukerak
    :param lerro_indizea: zein lerroko elementua den
    :param zutabe_indizea: zein zutabeko elementua den
    :param sudoku_arraya: sudokua bi dimentsiotako array gisa
    :return: elementuaren aukera berriak, sudokuko kointzidentziak kendu eta gero
    """
    
    elementuaren_aukerak = ''.join([i for i in elementuaren_aukerak if i not in ''.join(map(lambda x: x.replace('-', ''), sudoku_arraya[lerro_indizea]))])
    elementuaren_aukerak = ''.join(
        [i for i in elementuaren_aukerak if i not in ''.join(map(lambda x: x.replace('-', ''), [lerroa[zutabe_indizea] for lerroa in sudoku_arraya]))])
    elementuaren_aukerak = ''.join([i for i in elementuaren_aukerak if i not in ''.join(map(lambda x: x.replace('-', ''), [elementua for lerroa in [
        lerroa[(zutabe_indizea // 3) * 3:((zutabe_indizea // 3) + 1) * 3] for lerroa in
        sudoku_arraya[(lerro_indizea // 3) * 3:((lerro_indizea // 3) + 1) * 3]] for elementua in lerroa]))])
    if elementuaren_aukerak == '':
        elementuaren_aukerak = '#'
    return elementuaren_aukerak


def ezabatu_aukerak_aukeren_arraytik(aukeren_arraya, sudoku_arraya):
    """
    Aukeren arraytik aukerak ezabatzen dira, sudokuko lerro, zutabe eta koadro bereko elementuak kontuan izanda.
    
    :param aukeren_arraya: aukerak bi dimentsiotako array gisa, eta aukerak zenbakien kate gisa
    :param sudoku_arraya: sudokua bi dimentsiotako array gisa
    :return: arraya aukera berriekin, sudokuko kointzidentziak kendu eta gero
    """
    
    for lerro_indizea, lerroa in enumerate(aukeren_arraya):
        for zutabe_indizea, elementua in enumerate(lerroa):
            aukeren_arraya[lerro_indizea][zutabe_indizea] = ezabatu_aukerak_elementutik(elementua, lerro_indizea, zutabe_indizea, sudoku_arraya)
    return aukeren_arraya


def begiratu_amaituta(sudoku_arraya):
    """
    Sudoku bat amaituta dagoen begiratzen du.

    :param sudoku_arraya: sudokua bi dimentsiotako array gisa
    :return: sudokua amaituta dagoen
    """

    return '-' not in [elementua for lerroa in sudoku_arraya for elementua in lerroa]


def begiratu_zuzena_den(sudoku_arraya):
    """
    Sudoku bat zuzena den begiratzen du (errepikaturik ez lerro, zutabe eta koadroetan).
    
    :param sudoku_arraya: sudokua bi dimentsiotako array gisa
    :return: errepikatuem indizeen zerrenda
    """

    errepikatuak = []
    for lerro_indizea in range(9):
        lerroa = sudoku_arraya[lerro_indizea]
        lerroko_elementuak = list(filter(lambda x: x != '-', lerroa))
        lerroko_elementuak_kopuruekin = [[x, lerroa.count(x)] for x in set(lerroko_elementuak)]
        lerroko_elementu_errepikatuak = list(filter(lambda y: y[1] > 1, lerroko_elementuak_kopuruekin))
        if len(lerroko_elementu_errepikatuak) > 0:
            lerroko_errepikatuak = [[lerro_indizea, ind_x, str(s)] for ind_x, s in enumerate(lerroa) if lerroko_elementu_errepikatuak[0][0] == s]
            errepikatuak.extend(lerroko_errepikatuak)
    for zutabe_indizea in range(9):
        zutabea = [lerroa[zutabe_indizea] for lerroa in sudoku_arraya]
        zutabeko_elementuak = list(filter(lambda x: x != '-', zutabea))
        zutabeko_elementuak_kopuruekin = [[x, zutabea.count(x)] for x in set(zutabeko_elementuak)]
        zutabeko_elementu_errepikatuak = list(filter(lambda y: y[1] > 1, zutabeko_elementuak_kopuruekin))
        if len(zutabeko_elementu_errepikatuak) > 0:
            zutabeko_errepikatuak = [[ind_y, zutabe_indizea, str(s)] for ind_y, s in enumerate(zutabea) if zutabeko_elementu_errepikatuak[0][0] == s]
            errepikatuak.extend(zutabeko_errepikatuak)
    for lerro_indizea in range(0, 9, 3):
        for zutabe_indizea in range(0, 9, 3):
            aukerak_koadroetan_zerrenda = [elementua for lerroa in [
                lerroa[(zutabe_indizea // 3) * 3:((zutabe_indizea // 3) + 1) * 3] for lerroa in
                sudoku_arraya[(lerro_indizea // 3) * 3:((lerro_indizea // 3) + 1) * 3]] for elementua in lerroa]
            koadroko_elementuak = list(filter(lambda x: x != '-', aukerak_koadroetan_zerrenda))
            koadroko_elementuak_kopuruekin = [[x, aukerak_koadroetan_zerrenda.count(x)] for x in set(koadroko_elementuak)]
            koadroko_elementu_errepikatuak = list(filter(lambda y: y[1] > 1, koadroko_elementuak_kopuruekin))
            if len(koadroko_elementu_errepikatuak) > 0:
                koadroko_errepikatuak = [[lerro_indizea+(indizea//3), zutabe_indizea+(indizea % 3), str(s)] for indizea, s in enumerate(aukerak_koadroetan_zerrenda) if koadroko_elementu_errepikatuak[0][0] == s]
                errepikatuak.extend(koadroko_errepikatuak)
    if len(errepikatuak) > 0:
        return errepikatuak
    else:
        return True


def aukera_hutsik_ez(aukeren_arraya):
    """
    Aukeren arrayan begiratzen du ea elementuren bat hutsik dagoen (eta, beraz, aukerarik ez dagoen sudokuan posizio horrentzat).
    
    :param aukeren_arraya: aukerak bi dimentsiotako array gisa, eta aukerak zenbakien kate gisa
    :return: aukera hutsen indizeen zerrenda
    """

    hutsen_indizeak = [[ix, iy, '-'] for ix, lerroa in enumerate(aukeren_arraya) for iy, i in enumerate(lerroa) if i == '#']
    if len(hutsen_indizeak) == 0:
        return True
    return hutsen_indizeak


def aukerak_lerroetan(aukeren_arraya, luzera=None):
    """
    Lerroen aukerak itzultzen ditu koordenatuekin eta zenbatetan dagoen aukeran, beharrezkoa bada aukera kopuru jakin batekoak soilik filtratuz.

    :param aukeren_arraya: aukerak bi dimentsiotako array gisa, eta aukerak zenbakien kate gisa
    :param luzera: zein luzeratakoak nahi diren
    :return: lerroen aukerak koordenatuekin eta zenbatetan dagoen aukeran
    """

    aukerak_lerroetan_zerrenda = []
    for lerro_indizea in range(9):
        lerroa = aukeren_arraya[lerro_indizea]
        lerroko_elementu_ezberdinak = [elementua for lerroa in filter(lambda x: x != '-' and x != '*', lerroa) for elementua in lerroa]
        lerroko_elementuak_kopuruekin = [[x, lerroko_elementu_ezberdinak.count(x)] for x in set(lerroko_elementu_ezberdinak)]
        if luzera is not None:
            lerroko_elementuak_kopuruekin_luzeradunak = list(filter(lambda y: y[1] == luzera, lerroko_elementuak_kopuruekin))
            aukerak_lerroan = list(map(lambda x: [[lerro_indizea, ind_x, x[0]] for ind_x, s in enumerate(lerroa) if x[0] in s][0], lerroko_elementuak_kopuruekin_luzeradunak))
        else:
            lerroko_elementuak_kopuruekin_luzeradunak = lerroko_elementuak_kopuruekin
            aukerak_lerroan = list(map(lambda x: [[lerro_indizea, ind_x, x[0], x[1]] for ind_x, s in enumerate(lerroa) if x[0] in s][0], lerroko_elementuak_kopuruekin_luzeradunak))
        aukerak_lerroetan_zerrenda.extend(aukerak_lerroan)
    return aukerak_lerroetan_zerrenda


def aukerak_zutabeetan(aukeren_arraya, luzera=None):
    """
    Zutabeen aukerak itzultzen ditu koordenatuekin eta zenbatetan dagoen aukeran, beharrezkoa bada aukera kopuru jakin batekoak soilik filtratuz.

    :param aukeren_arraya: aukerak bi dimentsiotako array gisa, eta aukerak zenbakien kate gisa
    :param luzera: zein luzeratakoak nahi diren
    :return: zutabeen aukerak koordenatuekin eta zenbatetan dagoen aukeran
    """

    aukerak_zutabeetan_zerrenda = []
    for zutabe_indizea in range(9):
        zutabea = [lerroa[zutabe_indizea] for lerroa in aukeren_arraya]
        zutabeko_elementu_ezberdinak = [elementua for lerroa in filter(lambda x: x != '-' and x != '*', zutabea) for elementua in lerroa]
        zutabeko_elementuak_kopuruekin = [[x, zutabeko_elementu_ezberdinak.count(x)] for x in set(zutabeko_elementu_ezberdinak)]
        if luzera is not None:
            zutabeko_elementuak_kopuruekin_luzeradunak = list(filter(lambda y: y[1] == luzera, zutabeko_elementuak_kopuruekin))
            aukerak_zutabean = list(map(lambda x: [[ind_y, zutabe_indizea, x[0]] for ind_y, s in enumerate(zutabea) if x[0] in s][0], zutabeko_elementuak_kopuruekin_luzeradunak))
        else:
            zutabeko_elementuak_kopuruekin_luzeradunak = zutabeko_elementuak_kopuruekin
            aukerak_zutabean = list(map(lambda x: [[ind_y, zutabe_indizea, x[0], x[1]] for ind_y, s in enumerate(zutabea) if x[0] in s][0], zutabeko_elementuak_kopuruekin_luzeradunak))
        aukerak_zutabeetan_zerrenda.extend(aukerak_zutabean)
    return aukerak_zutabeetan_zerrenda


def aukerak_koadroetan(aukeren_arraya, luzera=None):
    """
    Koadroen aukerak itzultzen ditu koordenatuekin eta zenbatetan dagoen aukeran, beharrezkoa bada aukera kopuru jakin batekoak soilik filtratuz.

    :param aukeren_arraya: aukerak bi dimentsiotako array gisa, eta aukerak zenbakien kate gisa
    :param luzera: zein luzeratakoak nahi diren
    :return: koadroen aukerak koordenatuekin eta zenbatetan dagoen aukeran
    """

    aukerak_koadroetan_zerrenda = []
    for lerro_indizea in range(0, 9, 3):
        for zutabe_indizea in range(0, 9, 3):
            koadro = [elementua for lerroa in [
                lerroa[(zutabe_indizea // 3) * 3:((zutabe_indizea // 3) + 1) * 3] for lerroa in
                aukeren_arraya[(lerro_indizea // 3) * 3:((lerro_indizea // 3) + 1) * 3]] for elementua in lerroa]
            koadroko_elementu_ezberdinak = [elementua for lerroa in filter(lambda x: x != '-' and x != '*', koadro) for elementua in lerroa]
            koadroko_elementuak_kopuruekin = [[x, koadroko_elementu_ezberdinak.count(x)] for x in set(koadroko_elementu_ezberdinak)]
            if luzera is not None:
                koadroko_elementuak_kopuruekin_luzeradunak = list(filter(lambda y: y[1] == luzera, koadroko_elementuak_kopuruekin))
                aukerak_koadroan = list(map(lambda x: [[lerro_indizea+(indizea//3), zutabe_indizea+(indizea % 3), x[0]] for indizea, s in enumerate(koadro) if x[0] in s][0], koadroko_elementuak_kopuruekin_luzeradunak))
            else:
                koadroko_elementuak_kopuruekin_luzeradunak = koadroko_elementuak_kopuruekin
                aukerak_koadroan = list(map(lambda x: [[lerro_indizea+(indizea//3), zutabe_indizea+(indizea % 3), x[0], x[1]] for indizea, s in enumerate(koadro) if x[0] in s][0], koadroko_elementuak_kopuruekin_luzeradunak))
            aukerak_koadroetan_zerrenda.extend(aukerak_koadroan)
    return aukerak_koadroetan_zerrenda


# Copyright abisua erakutsi
print('Copyright (C) 2020 e-gor (Igor Leturia)')
print('Programa honek ez du INOLAKO BERMERIK; informazio gehiagorako erabili `-w` edo `--warranty` parametroa.\nHau software librea da, eta birbanatu dezakezu zenbait baldintzarekin; erabili `-c` edo `--conditions` parametroa xehetasunak ikusteko.')

# Argumentuak irakurri
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--warranty", help="bermerik ezaren ohar zehatza ikusi", action="store_true")
parser.add_argument("-c", "--conditions", help="birbanaketa baldintzak ikusi", action="store_true")
parser.add_argument("-b", "--ez_bistaratu", help="ez erakutsi pausoak", action="store_true")
parser.add_argument("-g", "--ez_gelditu", help="ez gelditu pauso bakoitza erakutsi ostean", action="store_true")
parser.add_argument("-a", "--aurrez_definitua", type=str, help="aurrez defintutako sudoku bat erabili", choices=[
    "hutsa", "erraza1", "erraza2", "ertaina1", "ertaina2", "zaila1", "zaila2", "osozaila1", "osozaila2", "ebatziezina", "ebazpenanitz"
])
args = parser.parse_args()
bistaratu = not args.ez_bistaratu
gelditu = not args.ez_gelditu

# Hala adierazi bada, erakutsi bermerik ezaren oharra eta atera
if args.warranty:
    print(warranty_message)
    exit(0)

# Hala adierazi bada, erakutsi birbanaketarako baldintzak eta atera
if args.conditions:
    print(conditions_message)
    exit(0)

# Adibideko sudokuetako bat aukeratu parametroetan hala adierazi bada
if args.aurrez_definitua:
    sudokua = hasierako_sudokuak[args.aurrez_definitua]

# Edo eskuz sartu sudokua
else:
    sudokua = hasierako_sudokuak["hutsa"]
    sudokua = list(map(lambda x: list(map(lambda y: str(y).replace('0', '-'), x)), sudokua))
    for lerro_indizea in range(9):
        for zutabe_indizea in range(9):
            print('')
            print(bistaratu_taula(sudokua, [[lerro_indizea, zutabe_indizea, '-', 'blue']]))
            balioa = 'k'
            mezua = "\nSartu hurrengo balioa:\n"
            while balioa != '' and balioa not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']:
                balioa = input(mezua)
                mezua = "\nOkerra, izan behar da 1-9 edo hutsa. Sartu hurrengo balioa:\n"
            if balioa in "0-" or balioa == '':
                balioa = '-'
            sudokua[lerro_indizea][zutabe_indizea] = balioa

# Hasieraketak
sudokua = list(map(lambda x: list(map(lambda y: str(y).replace('0', '-'), x)), sudokua))
sudokuaren_aukerak = [['-'] * 9 for i in range(9)]
for lerro_indizea, lerroa in enumerate(sudokuaren_aukerak):
    for zutabe_indizea, elementua in enumerate(lerroa):
        if sudokua[lerro_indizea][zutabe_indizea] == '-':
            sudokuaren_aukerak[lerro_indizea][zutabe_indizea] = "123456789"
sudokuaren_aukerak = ezabatu_aukerak_aukeren_arraytik(sudokuaren_aukerak, sudokua)
lehenagoko_aukerak = []
aukerak = True

# Bistaratu hasierako sudokua
print("\nHasierako sudokua:\n")
print(bistaratu_taula(sudokua))
if gelditu:
    input("\nSakatu <enter> jarraitzeko...")

# Sudokua amaitu ez den bitartean eta aukerak dauden bitartean
while not begiratu_amaituta(sudokua) and aukerak:

    # Begiratu sudokua okerra den, eta hala bada bistaratu okerrak gorriz markatuta
    okerra = False
    sudokua_zuzena = begiratu_zuzena_den(sudokua)
    if sudokua_zuzena != True:
        okerra = True
        if bistaratu:
            print("\nOkerra:\n")
            print(bistaratu_taula(sudokua, list(map(lambda x: x+['red'], sudokua_zuzena))))
            if gelditu:
                input("\nSakatu <enter> jarraitzeko...")

    # Begiratu aukerak dauden, eta hala ez bada bistaratu aukera gabekoaren fondoa gorriz markatuta
    aukerak_zuzena = aukera_hutsik_ez(sudokuaren_aukerak)
    if aukerak_zuzena != True:
        okerra = True
        if bistaratu:
            print("\nAukerarik ez:\n")
            print(bistaratu_taula(sudokua, list(map(lambda x: x+['red'], aukerak_zuzena))))
            if gelditu:
                input("\nSakatu <enter> jarraitzeko...")

    # Sudokua ez bada okerra eta aukerak badaude
    if not okerra:

        # Begiratu ea posizioren batean aukera bakarrik dagoen
        aukera_bakarrak = [(ix, iy, i) for ix, lerroa in enumerate(sudokuaren_aukerak) for iy, i in enumerate(lerroa) if i != '-' and i != '*' and len(i) == 1]

        # Begiratu lerroren batean zenbaki batek aukera toki bakarrean duen
        aukera_bakarrak.extend(aukerak_lerroetan(sudokuaren_aukerak, luzera=1))

        # Begiratu zutaberen batean zenbaki batek aukera toki bakarrean duen
        aukera_bakarrak.extend(aukerak_zutabeetan(sudokuaren_aukerak, luzera=1))

        # Begiratu koadroren batean zenbaki batek aukera toki bakarrean duen
        aukera_bakarrak.extend(aukerak_koadroetan(sudokuaren_aukerak, luzera=1))

        # Aukera bakarrik badago
        if len(aukera_bakarrak) > 0:

            # Hartu aukera bakarretatik lehenengoa
            lehen_aukera = aukera_bakarrak[0]

            # Aukera bakarra denez, kolore berdea erakutsi
            kolorea = 'green'

            # Bistaratu aukerak, hartuko dena berdez markatuz
            if bistaratu:
                print("\nAukerak:\n")
                print(bistaratu_taula(sudokuaren_aukerak, [
                    [lehen_aukera[0], lehen_aukera[1], lehen_aukera[2], kolorea]]))
                if gelditu:
                    input("\nSakatu <enter> jarraitzeko...")

            # Aplikatu aukera
            sudokua[lehen_aukera[0]][lehen_aukera[1]] = lehen_aukera[2]
            sudokuaren_aukerak[lehen_aukera[0]][lehen_aukera[1]] = '*'
            sudokuaren_aukerak = ezabatu_aukerak_aukeren_arraytik(sudokuaren_aukerak, sudokua)

            # Bistaratu sudokua, hartu dena berdez markatuz
            if bistaratu:
                print("\nTarteko sudokua:\n")
                print(bistaratu_taula(sudokua, [
                    [lehen_aukera[0], lehen_aukera[1], lehen_aukera[2], kolorea]]))
                if gelditu:
                    input("\nSakatu <enter> jarraitzeko...")

        # Aukera bakarrik ez badago
        else:

            # Hartu lerroetako, zutabeetako eta koadroetako aukerak eta ordenatu aukera kopuruen arabera
            aukera_guztiak = []
            aukera_guztiak.extend(aukerak_lerroetan(sudokuaren_aukerak))
            aukera_guztiak.extend(aukerak_zutabeetan(sudokuaren_aukerak))
            aukera_guztiak.extend(aukerak_koadroetan(sudokuaren_aukerak))
            aukera_guztiak.sort(key=lambda x: x[3])

            # Aukerarik ez badago
            if len(aukera_guztiak) == 0:

                # Amaitu
                aukerak = False

            # Aukerarik badago
            else:

                # Hartu aukeretatik lehenengoa
                lehen_aukera = aukera_guztiak.pop(0)

                # Besteak sartu lehenagoko aukeretan, atzera bueltatzeko biderik ez badago
                sudokuaren_aukerak_copy = deepcopy(sudokuaren_aukerak)
                sudokuaren_aukerak_copy[lehen_aukera[0]][lehen_aukera[1]] = sudokuaren_aukerak_copy[lehen_aukera[0]][lehen_aukera[1]].replace(lehen_aukera[2], '')
                lehenagoko_aukerak.append([deepcopy(sudokua), sudokuaren_aukerak_copy, deepcopy(aukera_guztiak)])

                # Aukera bakarra ez denez, kolore horia erakutsi
                kolorea = 'yellow'

                # Bistaratu aukerak, hartuko dena horiz markatuz
                if bistaratu:
                    print("\nAukerak:\n")
                    print(bistaratu_taula(sudokuaren_aukerak, [
                        [lehen_aukera[0], lehen_aukera[1], lehen_aukera[2], kolorea]]))
                    if gelditu:
                        input("\nSakatu <enter> jarraitzeko...")

                # Aplikatu aukera
                sudokua[lehen_aukera[0]][lehen_aukera[1]] = lehen_aukera[2]
                sudokuaren_aukerak[lehen_aukera[0]][lehen_aukera[1]] = '*'
                sudokuaren_aukerak = ezabatu_aukerak_aukeren_arraytik(sudokuaren_aukerak, sudokua)

                # Bistaratu sudokua, hartu dena horiz markatuz
                if bistaratu:
                    print("\nTarteko sudokua:\n")
                    print(bistaratu_taula(sudokua, [
                        [lehen_aukera[0], lehen_aukera[1], lehen_aukera[2], kolorea]]))
                    if gelditu:
                        input("\nSakatu <enter> jarraitzeko...")

    # Sudokua okerra bada edo aukerak ez badaude
    else:

        # Aukerarik ez dagoen artean, lehenagoko aukeretan begiratu
        aukera_guztiak = []
        while len(aukera_guztiak) == 0 and len(lehenagoko_aukerak) > 0:
            (sudokua, sudokuaren_aukerak, aukera_guztiak) = lehenagoko_aukerak.pop()

        # Aukerarik ez badago
        if len(aukera_guztiak) == 0:

            # Amaitu
            aukerak = False

        # Aukerarik badago
        else:

            # Hartu aukeretatik lehenengoa
            lehen_aukera = aukera_guztiak.pop(0)

            # Besteak sartu lehenagoko aukeretan, atzera bueltatzeko biderik ez badago
            sudokuaren_aukerak_copy = deepcopy(sudokuaren_aukerak)
            sudokuaren_aukerak_copy[lehen_aukera[0]][lehen_aukera[1]] = \
                sudokuaren_aukerak_copy[lehen_aukera[0]][lehen_aukera[1]].replace(lehen_aukera[2], '')
            lehenagoko_aukerak.append([deepcopy(sudokua), sudokuaren_aukerak_copy, deepcopy(aukera_guztiak)])

            # Aukera bakarra ez denez, kolore horia erakutsi
            kolorea = 'yellow'

            # Bistaratu aukerak, hartuko dena horiz markatuz
            if bistaratu:
                print("\nAukerak:\n")
                print(bistaratu_taula(sudokuaren_aukerak, [
                    [lehen_aukera[0], lehen_aukera[1], lehen_aukera[2], kolorea]]))
                if gelditu:
                    input("\nSakatu <enter> jarraitzeko...")

            # Aplikatu aukera
            sudokua[lehen_aukera[0]][lehen_aukera[1]] = lehen_aukera[2]
            sudokuaren_aukerak[lehen_aukera[0]][lehen_aukera[1]] = '*'
            sudokuaren_aukerak = ezabatu_aukerak_aukeren_arraytik(sudokuaren_aukerak, sudokua)

            # Bistaratu sudokua, hartu dena horiz markatuz
            if bistaratu:
                print("\nTarteko sudokua:\n")
                print(bistaratu_taula(sudokua, [
                    [lehen_aukera[0], lehen_aukera[1], lehen_aukera[2], kolorea]]))
                if gelditu:
                    input("\nSakatu <enter> jarraitzeko...")


# Ez badago amaituta, aukera guztiak agortu direlako da
if not begiratu_amaituta(sudokua):
    print("\nEbazpenik ez\n")

# Bestela
else:

    # Begiratu sudokua okerra den, eta hala bada bistaratu okerrak gorriz markatuta
    sudokua_zuzena = begiratu_zuzena_den(sudokua)
    if sudokua_zuzena != True:
        if bistaratu:
            print("\nOkerra:\n")
            print(bistaratu_taula(sudokua, list(map(lambda x: x+['red'], sudokua_zuzena))))
            if gelditu:
                input("\nSakatu <enter> jarraitzeko...")
        print("\nEbazpenik ez\n")

    # Sudokua zuzena eta amaituta
    else:
        print("\nSudoku ebatzia:\n")
        print(bistaratu_taula(sudokua))
        print('')
