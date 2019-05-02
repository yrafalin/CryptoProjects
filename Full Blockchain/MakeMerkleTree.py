#!/usr/bin/env python3
from hashlib import sha256
import json

def clean_it(data):  # credit goes to https://stackoverflow.com/questions/33137741/fastest-way-to-convert-a-dicts-keys-values-from-bytes-to-str-in-python3/33137796
    if isinstance(data, bytes):      return data.decode('utf-8', errors='replace')#decode('unicode_escape').encode().decode('utf-8')
    if isinstance(data, (str, int)): return str(data)
    if isinstance(data, dict):       return dict(map(clean_it, data.items()))
    if isinstance(data, tuple):      return tuple(map(clean_it, data))
    if isinstance(data, list):       return list(map(clean_it, data))
    if isinstance(data, set):        return set(map(clean_it, data))

def merkle(txs):
    first_layer = []
    if type(txs) == dict:
        for tx in txs:
            hash_object = sha256(txs[tx].encode())
            first_layer.append(hash_object.digest())
    if type(txs) == list:
        txs = clean_it(txs)
        for tx in txs:
            hash_object = sha256(json.dumps(tx).encode())
            first_layer.append(hash_object.digest())

    #print('first_layer', first_layer, txs)

    old_layer = []
    new_layer = first_layer
    while len(new_layer) != 1:
        old_layer = new_layer
        new_layer = []
        first = 1
        cycle = 1
        for h in old_layer:
            if first:
                hash_object = sha256(h)
                first = 0
                if cycle == len(old_layer): # in case the length is odd
                    new_layer.append(hash_object.digest())
            else:
                hash_object.update(h)
                new_layer.append(hash_object.digest())
                first = 1
            cycle += 1
    return new_layer[0].hex()

if __name__ == "__main__":
    with open('./transactions.json') as open_file:
        transactions = json.load(open_file)
    print('\n', merkle(transactions))
