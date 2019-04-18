#!/usr/bin/env python3
from hashlib import sha256
import json

def merkle(txs):
    first_layer = []
    for tx in txs:
        hash_object = sha256(txs[tx].encode())
        first_layer.append(hash_object.digest())

    #print(first_layer)

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
