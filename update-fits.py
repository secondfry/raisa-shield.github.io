#!/usr/bin/env python2
# coding: utf-8

## Импорты
import logging
import os
import re
import json

## Инициализация
starList = {
    "Basilisk": 5,
    "Scimitar": 5,
    "Machariel": 5,
    "Nightmare": 5,
    "Vindicator": 5,
    "Apocalypse Navy Issue": 1,
    "Drake": 1,
    "Raven": 1,
    "Scorpion Navy Issue": 1,
    "Typhoon": 1,
    "Abaddon": 2,
    "Armageddon Navy Issue": 2,
    "Dominix Navy Issue": 2,
    "Rattlesnake": 2,
    "Raven Navy Issue": 2,
    "Tempest": 2,
    "Tengu": 2,
    "Golem": 3,
    "Hyperion": 3,
    "Maelstrom": 3,
    "Rokh": 3,
    "Tempest Fleet Issue": 3,
    "Bhaalgorn": 4,
    "Loki": 4,
    "Megathron Navy Issue": 4,
    "Vargur": 4
}

fits = {"VG": [], "HQ": []}
fits_data = {"VG": '', "HQ": ''}
fits_file = {"VG": "fits/shield-vg.rst", "HQ": "fits/shield-hq.rst"}

SHIP_IMAGE_URL_FMT = 'http://image.eveonline.com/Render/%d_512.png'

_types_by_name = json.load(open('types_by_name.json')).items()

TYPES = dict((k, v['id']) for k, v in _types_by_name)


## Функции
def update_fit(eft_filename, rst_filename):
    logging.info('Updating file %s -> %s', eft_filename, rst_filename)

    eft = open(eft_filename).read().strip()
    ship_name, fit_name = eft.splitlines()[0].strip()[1:-1].split(',')
    ship_name = ship_name.strip()
    fit_name = fit_name.strip()
    complex_type = fit_name.split('-')[1].strip()

    modules = {}
    for item in eft.splitlines()[2:]:
        if not item:
            continue
        elif item.lower() in [
            '[empty high slot]',
            '[empty low slot]',
            '[empty med slot]',
        ]:
            continue
        elif item in TYPES:
            modules[TYPES[item]] = modules.get(TYPES[item], 0) + 1
        elif re.match('x\d+', item.split()[-1]) is not None and item.rsplit(' ', 1)[0] in TYPES:
            modules[TYPES[item.rsplit(' ', 1)[0]]] = modules.get(TYPES[item.rsplit(' ', 1)[0]], 0) + int(item.split()[-1][1:])

    dna = '%d:%s::' % (
        TYPES[ship_name],
        ':'.join('%d;%d' % (type_id, quantity)
                 for type_id, quantity in modules.items())
    )

    with open(rst_filename, 'w') as f:
        f.write('.. This file is autogenerated by update-fits.py script\n')
        f.write('.. Use https://github.com/RAISA-Shield/raisa-shield.github.io/edit/source/%s\n' % eft_filename)
        f.write('.. to edit it.\n\n')

        starcount = int(starList[ship_name])
        if 0 < starcount < 5:
            rst_link = '/' + rst_filename.split('.')[0].replace(os.path.sep, '/')
            fits[complex_type].append([starcount, ship_name, rst_link])

        s = "`%s <javascript:CCPEVE.showFitting('%s');>`_" % (fit_name, dna)
        f.write('%s\n%s\n\n' % (s, '=' * len(s)))

        f.write('*(кликните по заголовку чтобы открыть фит в Eve)*\n\n')

        eft_iter = iter(eft.splitlines()[2:])

        low_slots = list(iter(eft_iter.next, ''))
        med_slots = list(iter(eft_iter.next, ''))
        high_slots = list(iter(eft_iter.next, ''))
        rigs = list(iter(eft_iter.next, ''))
        ammo = list(iter(eft_iter.next, ''))
        drones = list(iter(eft_iter.next, ''))

        f.write('High slots\n----------\n\n')
        for line in high_slots:
            f.write('- %s\n' % get_type_link(line.strip()))
        f.write('\n')

        f.write('Med slots\n---------\n\n')
        for line in med_slots:
            f.write('- %s\n' % get_type_link(line.strip()))
        f.write('\n')

        f.write('Low slots\n---------\n\n')
        for line in low_slots:
            f.write('- %s\n' % get_type_link(line.strip()))
        f.write('\n')

        if rigs:
            f.write('Rigs\n----\n\n')
            for line in rigs:
                f.write('- %s\n' % get_type_link(line.strip()))
            f.write('\n')

        if ammo:
            f.write('Ammo\n----\n\n')
            for line in ammo:
                f.write('- %s\n' % get_type_link(line.strip()))
            f.write('\n')

        if drones:
            f.write('Drones\n------\n\n')
            for line in drones:
                f.write('- %s\n' % get_type_link(line.strip()))
            f.write('\n')


def get_type_link(t):
    if t.lower() in ['[empty high slot]',
                     '[empty low slot]',
                     '[empty med slot]']:
        return t
    elif re.match('x\d+', t.split()[-1]) is not None and t.rsplit(' ', 1)[0] in TYPES:
        return '`%s <javascript:CCPEVE.showInfo(%d)>`_' % (t, TYPES[t.rsplit(' ', 1)[0]])
    elif t in TYPES:
        return '`%s <javascript:CCPEVE.showInfo(%d)>`_' % (t, TYPES[t])
    return t

## Поехали!
if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    for root, subdirs, files in list(os.walk('fit'))[::-1]:
        for i in files:
            logging.info('Removing %s', i)
            os.unlink(os.path.join(root, i))
        for i in subdirs:
            logging.info('Removing directory %s', i)
            os.rmdir(os.path.join(root, i))
    for root, subdirs, files in os.walk('eft'):
        if os.path.sep in root:
            dirname = os.path.join('fit', root.split(os.path.sep, 1)[1])
        else:
            dirname = 'fit'
        for fname in files:
            m = re.match(r'^(?P<name>.*)\.eft$', fname)
            if m is not None:
                name = m.group('name')
                try:
                    update_fit(os.path.join(root, '%s.eft' % name),
                               os.path.join(dirname, '%s.rst' % name))
                except:
                    logging.error('Problem with fit: %s', name, exc_info=True)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        for subdir in subdirs:
            os.mkdir(os.path.join(dirname, subdir))

    for complexType in fits:
        fits[complexType].sort(key=lambda single_ship: single_ship[0], reverse=True)

        for ship in fits[complexType]:
            fits_data[complexType] += '%s :doc:`%s <%s>`\n\n' % (ship[0] * '\*', ship[1], ship[2])

        template = open(fits_file[complexType] + '.tpl').read().decode('utf-8')
        data = template.format(**{"data": fits_data[complexType]}).encode('utf-8')
        with open(fits_file[complexType], 'w') as f:
            f.write(data)
