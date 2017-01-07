#!/usr/bin/env python2

import json
import os
from collections import OrderedDict

from reverence import blue


def get_slot(t):
    category = t.Group().Category().name
    if category == 'Module':
        effects = [CFG.dgmeffects.Get(i.effectID).effectName
                   for i in CFG.dgmtypeeffects[t.typeID]]
        if 'rigSlot' in effects:
            return 'rig'
        elif 'hiPower' in effects:
            return 'high'
        elif 'medPower' in effects:
            return 'med'
        elif 'loPower' in effects:
            return 'low'
    elif category == 'Drone':
        return 'drone'
    elif category == 'Charge':
        return 'charge'
    elif category == 'Ship':
        return 'ship'
    elif category == 'Subsystem':
        return 'subsystem'


def get_json(*args, **kwargs):
    with_slots = [(t, get_slot(t)) for t in CFG.invtypes]
    with_slots = [i for i in with_slots if i[1] is not None]
    types_by_name = json.dumps(OrderedDict((t.name, {
        'id': t.typeID,
        'slot': slot,
    }) for t, slot in sorted(with_slots, key=lambda x: x[0].name)
                                           ), *args, **kwargs)
    types_by_id = json.dumps(OrderedDict((t.typeID, {
        'name': t.name,
        'slot': slot,
    }) for t, slot in sorted(with_slots, key=lambda x: x[0].typeID)
                                         ), *args, **kwargs)
    return types_by_name, types_by_id


if __name__ == "__main__":
    EVE = blue.EVE(os.path.expanduser(
        '~/.wine/drive_c/Program Files (x86)/CCP/EVE'
    ))
    CFG = EVE.getconfigmgr()
    types_by_name, types_by_id = get_json(indent=4)
    with open('types_by_name.json', 'w') as f:
        f.write(types_by_name)
    with open('types_by_id.json', 'w') as f:
        f.write(types_by_id)
