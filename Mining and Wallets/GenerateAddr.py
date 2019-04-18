#!/usr/bin/env python3
import ecdsa
from hashlib import sha256, new
import codecs
# https://github.com/warner/python-ecdsa this is the ecdsa library, since pycrypto doesn't have it
# helpful https://medium.freecodecamp.org/how-to-create-a-bitcoin-wallet-address-from-a-private-key-eca3ddd9c05f

# I have tested the following program and guarantee that it works

alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
balphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# from https://github.com/Destiner/blocksmith/blob/master/blocksmith/bitcoin.py
def base58encode(address_hex):
    b58_string = ''
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    address_int = int(address_hex, 16)
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    # Adding '1' for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string

# next 3 from https://github.com/keis/base58/blob/master/base58.py
def scrub_input(v):
    if isinstance(v, str) and not isinstance(v, bytes):
        v = v.encode('ascii')

    return v

def b58decode_int(v):
    v = v.rstrip()
    v = scrub_input(v)

    decimal = 0
    for char in v:
        decimal = decimal * 58 + balphabet.index(char)
    return decimal

def base58decode(v):
    v = v.rstrip()
    v = scrub_input(v)

    origlen = len(v)
    v = v.lstrip(balphabet[0:1])
    newlen = len(v)

    acc = b58decode_int(v)

    result = []
    while acc > 0:
        acc, mod = divmod(acc, 256)
        result.append(mod)
    return (b'\0' * (origlen - newlen) + bytes(reversed(result)))

# If you want to import a private key
# WIF decoding for private keys from electrum https://en.bitcoin.it/wiki/Wallet_import_format
#priv = 'KwuR6yB47CCfXhXPtuUWd6FYxWJizptG5XzGRdbjJQWzzj2VLToT'
#key = codecs.encode(base58decode(priv), 'hex')[2:-10]
#key = ecdsa.SigningKey.from_string(codecs.decode(key, 'hex'), curve=ecdsa.SECP256k1)

# If you want to generate a new key pair
# SECP256k1 is the Bitcoin elliptic curve
key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

# And get its private key in WIF
priv = b'80' + codecs.encode(key.to_string(), 'hex') + b'01'
priv += codecs.encode(sha256(sha256(codecs.decode(priv, 'hex')).digest()).digest(), 'hex')[:8]
print('Private WIF:', base58encode(priv.decode('utf-8')))

# Compressing the private keys and converting them to public keys
key = key.get_verifying_key()
key = codecs.encode(key.to_string(), 'hex')
key_string = key.decode('utf-8')
key_h_len = len(key) // 2
key_half = key[:key_h_len]
# Bitcoin byte, 0x02 if last digit is even, 0x03 if last digit is odd
last_byte = int(key_string[-1], 16)
bitcoin_byte = b'02' if last_byte % 2 == 0 else b'03'
key = bitcoin_byte + key_half
key = bytearray.fromhex(key.decode('utf-8'))

# If you already have a compressed public key:
#key = bytearray.fromhex('02f273a2050dce3b71b406a096b2ac33827eeb0663082ad920102eb006149716fe')

ripe_fruit = new('ripemd160', sha256(key).digest())

ripe_fruit = b'00' + codecs.encode(ripe_fruit.digest(), 'hex')
ripe_fruit += codecs.encode(sha256(sha256(codecs.decode(ripe_fruit, 'hex')).digest()).digest(), 'hex')[:8]
print('Address:', base58encode(ripe_fruit.decode('utf-8')))
# It actually works!!! Finally!
