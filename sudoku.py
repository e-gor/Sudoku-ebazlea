# -*- coding: utf-8 -*-
"""
Sudoku ebazlea

Programa honek sudokuak ebazten ditu.
"""

import re
from copy import copy, deepcopy
import argparse

import termcolor
import boxea


def bistaratu_taula(sudoku_arraya, kolore_zerrendak=[], zabalera=None):
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
        taula = taula.replace (' ─ ', ' - ')
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
    
    elementuaren_aukerak = ''.join([i for i in elementuaren_aukerak if i not in ''.join(map(lambda x: x.replace('-',''), sudoku_arraya[lerro_indizea]))])
    elementuaren_aukerak = ''.join(
        [i for i in elementuaren_aukerak if i not in ''.join(map(lambda x: x.replace('-',''), [lerroa[zutabe_indizea] for lerroa in sudoku_arraya]))])
    elementuaren_aukerak = ''.join([i for i in elementuaren_aukerak if i not in ''.join(map(lambda x: x.replace('-',''), [elementua for lerroa in [
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
            aukeren_arraya[lerro_indizea][zutabe_indizea] = ezabatu_aukerak_elementutik(elementua, lerro_indizea, zutabe_indizea,
                                                                                 sudoku_arraya)
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
    if len(errepikatuak)>0:
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

hasierako_sudokuak = {}
hasierako_sudokuak["hutsa"] = hasierako_sudokua_hutsa
hasierako_sudokuak["erraza1"] = hasierako_sudokua_erraza_1
hasierako_sudokuak["erraza2"] = hasierako_sudokua_erraza_2
hasierako_sudokuak["ertaina1"] = hasierako_sudokua_ertaina_1
hasierako_sudokuak["ertaina2"] = hasierako_sudokua_ertaina_2
hasierako_sudokuak["zaila1"] = hasierako_sudokua_zaila_1
hasierako_sudokuak["zaila2"] = hasierako_sudokua_zaila_2
hasierako_sudokuak["osozaila1"] = hasierako_sudokua_osozaila_1
hasierako_sudokuak["osozaila2"] = hasierako_sudokua_osozaila_2
hasierako_sudokuak["ebatziezina"] = hasierako_sudokua_ebatziezina
hasierako_sudokuak["ebazpenanitz"] = hasierako_sudokua_ebazpenanitz

# Argumentuak irakurri
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--ez_bistaratu", help="ez erakutsi pausoak", action="store_true")
parser.add_argument("-g", "--ez_gelditu", help="ez gelditu pauso bakoitza erakutsi ostean", action="store_true")
parser.add_argument("-a", "--aurrez_definitua", type=str, help="aurrez defintutako sudoku bat erabili", choices=[
    "hutsa", "erraza1", "erraza2", "ertaina1", "ertaina2", "zaila1", "zaila2", "osozaila1", "osozaila2", "ebatziezina", "ebazpenanitz"
])
args = parser.parse_args()
bistaratu = not args.ez_bistaratu
gelditu = not args.ez_gelditu

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
            print(bistaratu_taula(sudokua,[[lerro_indizea, zutabe_indizea, '-', 'blue']]))
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
        aukera_bakarrak = [(ix, iy, i) for ix, lerroa in enumerate(sudokuaren_aukerak) for iy, i in enumerate(lerroa) if
                                i != '-' and i != '*' and len(i) == 1]

        # Begiratu lerroren batean zenbaki batek aukera toki bakarrean duen
        aukera_bakarrak.extend(aukerak_lerroetan(sudokuaren_aukerak, luzera=1))

        # Begiratu zutaberen batean zenbaki batek aukera toki bakarrean duen
        aukera_bakarrak.extend(aukerak_zutabeetan(sudokuaren_aukerak, luzera=1))

        # Begiratu koadroren batean zenbaki batek aukera toki bakarrean duen
        aukera_bakarrak.extend(aukerak_koadroetan(sudokuaren_aukerak, luzera=1))

        #Aukera bakarrik badago
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
