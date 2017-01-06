#!/usr/bin/env python2
# coding: utf-8

import json
import time
from ConfigParser import RawConfigParser
from urllib import urlopen, urlencode
from xml.etree.ElementTree import fromstring

API_URL = 'https://api.eveonline.com'


def get_api_key_info(key_id, v_code):
    return urlopen(API_URL + '/account/APIKeyInfo.xml.aspx?' + urlencode({
        'keyID': key_id,
        'vCode': v_code,
    })).read()


def get_character_id(key_id, v_code):
    api_key_info = get_api_key_info(key_id, v_code)
    row = fromstring(api_key_info).find('.//row')
    if (row is None):
        return None
    return row.get('characterID')


def get_account_balance(key_id, character_id, v_code):
    return urlopen(API_URL + '/corp/AccountBalance.xml.aspx?' + urlencode({
        'keyID': key_id,
        'characterID': character_id,
        'vCode': v_code,
    })).read()


def get_wallet_journal(key_id, character_id, v_code):
    return urlopen(API_URL + '/corp/WalletJournal.xml.aspx?' + urlencode({
        'keyID': key_id,
        'characterID': character_id,
        'vCode': v_code,
        'rowCount': 2560,
    })).read()


if __name__ == "__main__":
    parser = RawConfigParser()
    parser.read('api.ini')
    key_id = parser.get('RAISA SRP', 'keyID')
    v_code = parser.get('RAISA SRP', 'vCode')

    character_id = get_character_id(key_id, v_code)

    if character_id is not None:
        balance_data = get_account_balance(key_id, character_id, v_code)
        balance_xml = fromstring(balance_data)
        balance = sum(float(row.get('balance'))
                      for row in balance_xml.findall('.//row'))
        balance = '{:,.2f} ISK'.format(balance).replace(',', ' ')

        journal_data = get_wallet_journal(key_id, character_id, v_code)
        journal_xml = fromstring(journal_data)
        journal = [i.attrib for i in journal_xml.findall('.//row')]
        journal.sort(key=lambda x: -int(x['refID']))

        date = journal_xml.find('.//currentTime').text

        compens_lines = [', '.join([
            i['date'],
            i['ownerName2'],
            '{:,.2f}'.format(-float(i['amount'])).replace(',', ' '),
            i['reason'].strip()[6:].decode('raw_unicode_escape')
        ]) for i in journal if float(i['amount']) < 0]

        compens_table = '\n    '.join(compens_lines)

        srp_json = json.dumps([
                                  (int(time.strftime('%s', time.strptime(
                                      i['date'], "%Y-%m-%d %H:%M:%S"
                                  ))) * 1000, float(i['balance']))
                                  for i in journal
                                  ]).replace('], ', '],\n ')
        with open('srp.json', 'w') as f:
            f.write(srp_json)
    else:
        balance = '??? ISK'
        journal = '???'
        date = '???'
        compens_table = '???'

    # API is closed
    # template = open('srp_info.rst.tpl').read().decode('utf-8')
    # data = template.format(**locals()).encode('utf-8')
    #
    # with open('srp_info.rst', 'w') as f:
    #    f.write(data)
