#!/usr/bin/env python3
from hashlib import sha256
import json
import copy
from MakeMerkleTree import merkle
from jsonMaker import makeJSON

DIFF = 6

# with open('./blockchain.json') as open_file:
#     blockchain = json.load(open_file)

blockchain = {}
blockchain['b0'] = {'txs': makeJSON(20), 'header': 0}  # genesis block
blockchain['b0']['header'] = merkle(blockchain['b0']['txs'])
prevHash = blockchain['b0']['header']
block_num = 1

def find_nonce(header):
    nonce = 0
    head = copy.copy(header)
    head['nonce'] = nonce
    tester = sha256(json.dumps(head).encode())
    while not tester.digest().hex()[:DIFF] == '0'*DIFF:
        nonce += 1
        head['nonce'] = nonce
        tester = sha256(json.dumps(head).encode())
    print(nonce)
    print(tester.digest().hex())
    return nonce


for _ in range(10):
    recTx = makeJSON(20)
    blockchain['b'+str(block_num)] = {'txs': recTx, 'header': {'m': merkle(recTx), 'ph': prevHash}}
    blockchain['b'+str(block_num)]['header']['nonce'] = find_nonce(blockchain['b'+str(block_num)]['header'])
    print(json.dumps(blockchain['b'+str(block_num)]))
    block_num += 1
