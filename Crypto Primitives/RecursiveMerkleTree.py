#!/usr/bin/env python3
from hashlib import sha256
import json

with open('./transactions.json') as open_file:
    transactions = json.load(open_file)

first_layer = []
for tx in transactions:
    hash_object = sha256(transactions[tx].encode())
    first_layer.append(hash_object.digest())

def mesh_layer(old_layer):
    if len(old_layer) == 1:
        return old_layer
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
    return mesh_layer(new_layer)

print('\n', mesh_layer(first_layer)[0].hex())
