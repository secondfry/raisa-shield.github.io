#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
from pprint import pprint

pprint(os.environ)

TYPES_BY_ID = json.load(open('types_by_id.json'))
TYPES_BY_NAME = json.load(open('types_by_name.json'))


def dna2eft(name, dna):
    ship = TYPES_BY_ID[dna.split(':')[0]]['name']

    modules = [i.split(';') for i in dna.split(':')[1:] if i]

    modules = [(TYPES_BY_ID[t], int(q)) for t, q in modules]

    modules_by_slot = {}

    for t, q in modules:
        for i in range(q):
            modules_by_slot.setdefault(t['slot'], []).append(
                t['name']
            )

    groups = ['low', 'med', 'high', 'rig', 'subsystem', 'drone']

    if 'subsystem' not in modules_by_slot:
        groups.remove('subsystem')

    return u'[%s, %s]\n\n%s\n' % (
        ship, name, '\n\n'.join([
                                    '\n'.join(modules_by_slot.get(group, [])) for group in groups
                                    ]),
    )


def eft2dna(eft):
    lines = eft.split('\n')
    ship, fitname = map(lambda x: x.strip(), lines[0].strip('[ ]').split(','))
    return text2dna(ship, lines[1:])


MODULE_RE = re.compile('((?P<q>[0-9 ]+)x )?(?P<name>.*)')


def text2dna(ship, lines):
    assert TYPES_BY_NAME[ship]['slot'] == 'ship'

    modules = {}

    for line in lines:
        m = MODULE_RE.match(line)
        if m is not None:
            if m.group('name') in TYPES_BY_NAME:
                if m.group('name') not in modules:
                    modules[m.group('name')] = 0
                q = 0
                if m.group('q') is not None:
                    q = int(m.group('q'))
                modules[m.group('name')] += q

    return '%d:%s::' % (TYPES_BY_NAME[ship]['id'], ':'.join(
        '%d;%d' % (TYPES_BY_NAME[name]['id'], int(q))
        for name, q in modules.items()
    ))
