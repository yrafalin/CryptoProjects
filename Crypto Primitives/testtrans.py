#!/usr/bin/env python3
from hashlib import sha256
import json

with open('./transactions1.json') as open_file:
    transactions = json.load(open_file)

hash_object = sha256(transactions['t0'].encode())
t0 = hash_object.digest()
hash_object = sha256(transactions['t1'].encode())
t1 = hash_object.digest()
hash_object = sha256(transactions['t2'].encode())
t2 = hash_object.digest()
hash_object = sha256(transactions['t3'].encode())
t3 = hash_object.digest()
hash_object = sha256(t0)
hash_object.update(t1)
x1 = hash_object.digest()
hash_object = sha256(t2)
hash_object.update(t3)
x2 = hash_object.digest()
hash_object = sha256(x1)
hash_object.update(x2)
final = hash_object.digest()
print(final)
print(final.hex())
