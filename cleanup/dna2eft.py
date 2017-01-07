#!/usr/bin/env python2
# coding: utf-8
#
# Скрипт генерит EFT из DNA с указанного .rst-файла.
#

import logging
import os
import re
import sys

from eve_sphinx.utils import dna2eft, TYPES_BY_ID

FIT_LINK_RE = re.compile(r"`(?P<name>[^<`]+) <javascript:CCPEVE.showFitting\('(?P<dna>\d+:(\d+;\d+:)+:)'\);>`_")

if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    text = open(sys.argv[1]).read().decode('utf-8')
    fits = list(
        (i.group('name'), i.group('dna'))
        for i in FIT_LINK_RE.finditer(text)
    )

    for name, dna in fits:
        names = {
            u'бюджет': 'basic',
            u'средний': 'standard',
            u'ветеран': 'advanced',
            u'снайпер': 'snipe',
            u'активный': 'active',
            u'пассивный': 'passive',
            u'бластерный': 'blaster',
        }

        ship_id = int(dna.split(':')[0])
        assert TYPES_BY_ID[ship_id] == 'ship'
        ship = TYPES_BY_ID[ship_id]['name']

        if ship.lower() != name.lower():
            if name.lower() in names:
                t = names[name.lower()]
                name = u'%s - %s' % (ship, name)
            else:
                logging.warning(u'Bad name: %s', name)
                t = name.lower()
            fname = u'%s-%s.eft' % (ship.lower(), t.lower())
        else:
            fname = u'%s.eft' % ship.lower()

        fname = '-'.join(fname.split())
        eft = dna2eft(name, dna)

        with open(os.path.join(sys.argv[2], fname), 'w') as f:
            f.write((u'[%s, %s]\n\n' % (ship, name)).encode('utf-8'))
            f.write(eft)
            f.write('\n')
