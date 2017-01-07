#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


def writeln(file, string):
    file.write(string)
    file.write('\n')


def writelntab(file, string, tabcount):
    file.write(tabcount * '\t')
    file.write(string)
    file.write('\n')


propertiesList = {
    "point": {
        "weight": "0b10000",
        "icon": "http://image.eveonline.com/Type/3242_64.png",
        "text": "Поинт"
    },
    "neut": {
        "weight": "0b01000",
        "icon": "http://image.eveonline.com/Type/533_64.png",
        "text": "Нейтрят"
    },
    "jam": {
        "weight": "0b00100",
        "icon": "http://image.eveonline.com/Type/1957_64.png",
        "text": "Джам"
    },
    "dps": {
        "weight": "0b00010",
        "icon": "http://image.eveonline.com/Type/267_64.png",
        "text": "ДПС"
    },
    "web": {
        "weight": "0b00001",
        "icon": "http://image.eveonline.com/Type/526_64.png",
        "text": "Сетка"
    }
}

typeList = {
    "frigate": "Фригаты"
}

lasttype = ''


class Ship:
    def __init__(self, shipname, shiptype, shipweight, properties):
        self.name = shipname
        self.type = shiptype
        self.weight = shipweight
        self.properties = properties

    def __repr__(self):
        return repr((self.name, self.type, self.weight, self.properties))


ships = []

dirpath = 'npc'
filepath_source = os.path.join(dirpath, 'data.json')
filepath_destination = os.path.join(dirpath, 'index.rst')

header = "Описание NPC"

JSON = json.load(open(filepath_source))

for i, val in enumerate(JSON):
    weight = 0
    for v in val['properties']:
        weight += int(propertiesList[v]['weight'], 2)
    ships.append(Ship(val['name'], val['type'], weight, val['properties']))

ships.sort(key=lambda ship: ship.weight, reverse=True)

with open(filepath_destination, 'w') as f:
    writeln(f, '.. index:: ' + header)
    writeln(f, '')
    writeln(f, header)
    writeln(f, len(header.decode('utf-8')) * '=')

for val in ships:
    with open(filepath_destination, 'a') as f:
        if lasttype != val.type:
            writeln(f, typeList[val.type])
            signcount = len(typeList[val.type].decode('utf-8'))
            writeln(f, signcount * '-')
            writeln(f, '.. glossary::')
            lasttype = val.type

        writeln(f, '')
        writelntab(f, val.name, 1)

        for v in val.properties:
            writelntab(f, '.. figure:: ' + propertiesList[v]['icon'], 2)
            writelntab(f, ':figclass: prop-figure', 3)
            writelntab(f, ':class: prop-img', 3)
            writelntab(f, '', 3)
            writelntab(f, propertiesList[v]['text'], 3)
