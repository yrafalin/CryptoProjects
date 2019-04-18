#!/usr/bin/env python3
#https://www.quora.com/How-does-the-MD5-algorithm-work
#http://infohost.nmt.edu/~sfs/Students/HarleyKozushko/Presentations/MD5.pdf
#https://www.iusmentis.com/technology/hashfunctions/md5/
#http://www.faqs.org/rfcs/rfc1321.html

from bitarray import bitarray
import math
import struct

with open('./hash_str.txt', 'r') as open_file:
    hash_str = open_file

#  The following stuff is preprocessing padding
a = bitarray()
a.frombytes(hash_str.encode())
orig_len = a.length() % (2**64)
padded = False
if orig_len % 512 != 448:
    padded = True
    a.append(True)
    while a.length() % 512 != 448:
        a.append(False)

b = bitarray(bin(orig_len)[2:])
while b.length() != 64:
    a.insert(0, False)

a += b

# These words are the basis of the main loop
wordA = bitarray().frombytes(bytearray.fromhex('01234567'))
wordB = bitarray().frombytes(bytearray.fromhex('89abcdef'))
wordC = bitarray().frombytes(bytearray.fromhex('fedcba98'))
wordD = bitarray().frombytes(bytearray.fromhex('76543210'))

# Used in the main loop
K = [bitarray(bin(math.floor(abs(math.sin(i + 1)) * (2^32)))[2:]) for i in range(64)]
M = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
     5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
     4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
     6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

# These are the important functions which take 3 inputs
# and give one output (for condensing and obfuscating the input)
def F(B, C, D):
    return (B & C) | (~B & D)

def G(B, C, D):
    return (B & D) | (C & ~D)

def H(B, C, D):
    return B ^ C ^ D

def I(B, C, D):
    return C ^ (B | ~D)

# Breaking everything up into words
for bigbyte in range(a.length() / 512):
    chunk = a[bigbyte*512: (bigbyte+1)*512]
    for tzt in range(16):
        word = chunk[tzt*32: (tzt+1)*32]
        # In the following 40 or so lines, the program iterates
        # over every word, and runs a different operation on it.
        # It then adds them to the previous steps.
        tmpA = wordA
        tmpB = wordB
        tmpC = wordC
        tmpD = wordD
        # Main Loop
        for round in range(64):
            if round >= 0 and round <= 15:
                cycler = F(tmpB, tmpC, tmpD)
                sp_round = round
            elif round >= 16 and round <= 31:
                cycler = G(tmpB, tmpC, tmpD)
                sp_round = (5*round + 1) % 16
            elif round >= 32 and round <= 47:
                cycler = H(tmpB, tmpC, tmpD)
                sp_round = (3*round + 5) % 16
            elif round >= 48 and round <= 63:
                cycler = I(tmpB, tmpC, tmpD)
                sp_round = (7*round) % 16
            cycler += A + K[round] + M[sp_round]
            tmpA = tmpD
            tmpD = tmpC
            tmpC = tmpB
            tmpB +=
        wordA


struct.unpack("<L", d)[0]
