import random
from MakeMerkleTree import merkle
import json
from hashlib import sha256
from flask import Flask, jsonify, request
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

PRIVATE_KEY = RSA.generate(1024)
LOCAL_ADDRESS = PRIVATE_KEY.publickey()
DIFF = 3
DISC = 'Do NOT read the following too closely. You will get a headache. This is solely for demonstration purposes.\n'

def clean_it(data):  # credit goes to https://stackoverflow.com/questions/33137741/fastest-way-to-convert-a-dicts-keys-values-from-bytes-to-str-in-python3/33137796
    if isinstance(data, bytes):      return data.decode()
    if isinstance(data, (str, int)): return str(data)
    if isinstance(data, dict):       return dict(map(clean_it, data.items()))
    if isinstance(data, tuple):      return tuple(map(clean_it, data))
    if isinstance(data, list):       return list(map(clean_it, data))
    if isinstance(data, set):        return set(map(clean_it, data))

class Blockchain:
    def __init__(self, genesis_block=None, reward=1000, genesis_dict=None, genesis_json=None, addr=LOCAL_ADDRESS, diffic=DIFF):
        self.blocks = []
        self.reward = reward
        self.txs = []
        self.pay_to = addr.export_key('PEM')
        self.diff = diffic
        if genesis_block == None and genesis_dict == None and genesis_json == None:  # this option is none of the parameters
            the_block = Block(in_ph=0, in_reward=1000, diff=self.diff)
            the_block.build_from_dict({'txs': [self.create_pay_to()], 'h': {'ph': 0}})
            self.add_full_block(the_block)
        elif genesis_dict == None and genesis_json == None:
            self.add_full_block(genesis_block)
        elif genesis_json == None:
            the_block = Block(in_reward=1000, diff=self.diff)
            the_block.build_from_dict(genesis_dict)
            self.add_full_block(the_block)
        else:
            the_block = Block(in_reward=1000, diff=self.diff)
            the_block.build_from_json(genesis_json)
            self.add_full_block(the_block)
        self.announce()

    def add_block(self):
        self.add_tx(self.create_pay_to())
        #print(self.txs)
        #print(self.blocks)
        #print(block_data)

        block_dict = {'txs': self.txs, 'h': {'ph': sha256(json.dumps(self.blocks[-1].header).encode()).digest().hex()}}
        new = Block(in_reward=1000, diff=self.diff)
        new.build_from_dict(block_dict)
        self.add_full_block(new)
        self.txs = []

    def add_full_block(self, new_block):
        self.blocks.append(new_block)
        self.announce()

    def validate_chain(self, chain=None):
        if chain == None:
            chain = self.blocks

        for block in chain:
            last_block = chain[0] # Genesis block
            for block in chain[1:]:
                if(block.prev_hash != sha256(json.dumps(last_block.header).encode()).digest().hex()):
                    return False
                if sha256(json.dumps(block.header).encode()).digest().hex()[:self.diff] != '0'*self.diff:
                    return False
                last_block = block
            return True

    def validate_txs(self, txs, blockchn=None):
        for txer in txs:
            if 'src' in txer and self.value_key(txer['src'], blockchn) >= txer['val']:
                h = SHA256.new(txer['src'])
                h.update(txer['dest'])
                h.update(txer['val'])
                try:
                    pkcs1_15.new(RSA.import_key(txer['src'])).verify(h, txer['sig'])
                except:
                    return False

    def validate_block(self, s_block):
        if sha256(json.dumps(s_block.header).encode()).digest().hex()[:s_block.diff] != '0'*s_block.diff:
            return False
        if self.validate_txs(s_block.data) == False:
            return False
        return True

    def create_pay_to(self):
        to_add = {'dest': self.pay_to, 'val': self.reward}
        return to_add

    def announce(self):
        known_addr = ['alice', 'bob', 'carl']
        print('New Block Added')
        for address in known_addr:
            # announce longer blockchain to address
            pass

    def add_tx(self, tx):
        # contains {'src': public key, 'dest': public key, 'val': 0, 'sig': signature}
        if 'src' in tx and self.value_key(tx['src']) >= tx['val']:
            if type(tx['val']) is not bytes:
                tx['val'] = str(tx['val']).encode()
            h = SHA256.new(tx['src'])
            h.update(tx['dest'])
            h.update(tx['val'])
            try:
                pkcs1_15.new(RSA.import_key(tx['src'])).verify(h, tx['sig'])
                self.txs.append(tx)
                print('Transaction Added')
            except Exception as e:
                print('Transaction Failed', e)
        elif tx['dest'] == self.pay_to:
            self.txs.append(tx)
            print('Self Transaction Added')
        else:
            print('Transaction Failed')

    def value_key(self, pub_key, blocks=None):
        if blocks == None:
            blocks = self.blocks

        running_total = 0
        for block in blocks:
            for transaction in block.data:
                if transaction['dest'] == pub_key:
                    running_total += int(transaction['val'].decode('utf-8') if type(transaction['val']) == bytes else transaction['val'])
                if 'src' in transaction and transaction['src'] == pub_key:
                    running_total -= int(transaction['val'].decode('utf-8') if type(transaction['val']) == bytes else transaction['val'])
        return running_total

    def get_known_addr(self):
        addrs = []
        for block in self.blocks:
            for transaction in block.data:
                if transaction['dest'] not in addrs:
                    addrs.append(transaction['dest'])
                if 'src' in transaction and transaction['src'] not in addrs:
                    addrs.append(transaction['src'])
        return addrs

    def get_balances(self):
        balance_dict = {}
        for addr in self.get_known_addr():
            balance_dict[addr] = self.value_key(addr)
        return balance_dict

    def dump(self):
        blocks = []
        for block in self.blocks:
            blocks.append(block.dump())
        return '\n'.join(blocks)

class Block:
    def __init__(self, data=[{}], in_ph=0, in_nonce=0, in_reward=1000, diff=DIFF):
        self.data = data if type(data) == list else [{}]  # contains {'src': address, 'dest': address, 'value': 0}
        self.merkle = merkle(data)
        self.prev_hash = in_ph
        self.nonce = in_nonce
        self.reward = in_reward
        self.header = {'m': self.merkle, 'ph': self.prev_hash, 'n': self.nonce, 'r': self.reward}
        self.diff = diff

    def build_from_dict(self, block_dict):
        self.data = block_dict['txs']  # contains {'src': address, 'dest': address, 'value': 0}
        self.merkle = merkle(block_dict['txs'])
        self.prev_hash = block_dict['h']['ph']
        self.reward = block_dict['h']['r'] if 'r' in block_dict['h'] else self.reward
        self.header = {'m': self.merkle, 'ph': self.prev_hash, 'n': self.nonce, 'r': self.reward}
        if 'n' in block_dict['h']:
            test = sha256(json.dumps(block_dict['h']).encode())
            if test.digest().hex()[:self.diff] != '0'*self.diff:
                self.add_nonce()
        else:
            self.add_nonce()

    def build_from_json(self, block_json):
        undump = json.loads(block_json)
        self.data = undump['txs']  # contains {'src': address, 'dest': address, 'value': 0}
        self.merkle = merkle(undump['txs'])
        self.prev_hash = undump['h']['ph']
        self.header = {'m': self.merkle, 'ph': self.prev_hash, 'n': self.nonce, 'r': self.reward}
        if 'n' in undump['h']:
            test = sha256(json.dumps(undump['h']).encode())
            if test.digest().hex()[:self.diff] != '0'*self.diff:
                self.header['n'] = self.find_nonce()
        else:
            self.header['n'] = self.find_nonce()

    def add_nonce(self):
        nonce = self.find_nonce()
        self.nonce = nonce
        self.header['n'] = nonce
        return nonce

    def find_nonce(self):
        nonce = 0
        head = self.header
        # print(head, type(head))
        # print(json.dumps(head))
        head['n'] = nonce
        tester = sha256(json.dumps(head).encode())
        while tester.digest().hex()[:self.diff] != '0'*self.diff:
            nonce += 1
            head['n'] = nonce
            tester = sha256(json.dumps(head).encode())
        #print(nonce)
        #print(tester.digest().hex())
        return nonce

    def dump(self):
        return json.dumps(clean_it(self.get_dict()))

    #def __str__(self):
    #    return json.dumps(clean_it(self.get_dict()))

    def get_dict(self):
        return {'txs': self.data, 'h': {'m': self.merkle, 'ph': self.prev_hash, 'n': self.nonce, 'r': self.reward}}

if __name__ == "__main__":
    blocky = Blockchain()
    for num in range(10):
        blocky.add_block()
    # print('now sending money')
    for i in range(10):
        for num in range(10):
            prik = RSA.generate(1024)
            pubk = prik.publickey()

            h = SHA256.new(LOCAL_ADDRESS.export_key('PEM'))
            dest = RSA.generate(1024).publickey()
            h.update(dest.export_key('PEM'))
            h.update(b'200')
            signer = pkcs1_15.new(PRIVATE_KEY).sign(h)
            blocky.add_tx({'src': LOCAL_ADDRESS.export_key('PEM'), 'dest': dest.export_key('PEM'), 'val': 200, 'sig': signer})
        blocky.add_block()
    # print(blocky.dump())

    app = Flask(__name__)

    @app.route('/blockchain', methods=['GET'])
    def get_blockchain():
        return '<html><body><p>'+DISC +'</p><p>'+ blocky.dump()+'</p></body></html>'

    @app.route('/last_block', methods=['GET'])
    def get_last():
        return blocky.blocks[-1].dump()

    @app.route('/known_addr', methods=['GET'])
    def get_known():
        return ' '.join(clean_it(blocky.get_known_addr()))

    @app.route('/balances', methods=['GET'])
    def get_balan():
        return json.dumps(clean_it(blocky.get_balances()))

    if(__name__ == "__main__"):
        app.run(host='127.0.0.1', port=8080)
