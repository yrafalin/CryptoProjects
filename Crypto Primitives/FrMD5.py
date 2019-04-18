#!/usr/bin/env python3
#https://www.quora.com/How-does-the-MD5-algorithm-work
#http://infohost.nmt.edu/~sfs/Students/HarleyKozushko/Presentations/MD5.pdf
#https://www.iusmentis.com/technology/hashfunctions/md5/
#http://www.faqs.org/rfcs/rfc1321.html
#http://cs.indstate.edu/~fsagar/doc/paper.pdf

from bitarray import bitarray
import math
import struct

with open('./hash_str.txt', 'r') as open_file:
    hash_str = open_file.read()

#  The following stuff is preprocessing padding
result = []
hash_str += '?'
for x in hash_str:
    result.append(format(ord(x), '08b'))
a = ''.join(result)
orig_len = len(a)# % (2**64)
if orig_len % 512 != 448:
    a = a+'1'
    while len(a) % 512 != 448:
        a = a + '0'

a = bitarray(a) + bitarray(format(orig_len, '064b'))

print(a.tolist())
print('everything padded')

# These words are the basis of the main loop
wordA = 0x67452301
wordB = 0xefcdab89
wordC = 0x98badcfe
wordD = 0x10325476

# Used in the main loop
K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)] # checked
s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
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

def old_remover(bitstr, tolen=32):
    return bitstr[len(bitstr)-tolen:]

def remover(bitstr):
    return bitstr & 0xFFFFFFFF

print('before loops', a.length())

# Breaking everything up into words
for bigbyte in range(int(a.length() / 512)):
    prechunk = a[bigbyte*512: (bigbyte+1)*512]
    chunk = []
    for tzt in range(16):
        chunk.append(int(prechunk[tzt*32: (tzt+1)*32].tobytes().hex(), 16))
    print('after chunking')
    # In the following 40 or so lines, the program iterates
    # over every word, and runs a different operation on it.
    # It then adds them to the previous steps.
    tmpA = wordA
    tmpB = wordB
    tmpC = wordC
    tmpD = wordD
    # Main Loop
    for round in range(64):
        print('round', round)
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
        cycler = remover(cycler + tmpA + K[round] + chunk[sp_round])
        tmpA = tmpD
        tmpD = tmpC
        tmpC = tmpB
        current = cycler
        toadd = (current << s[round]) | (current >> (32 - s[round]))
        tmpB = remover(tmpB + toadd)
        final = bytearray(tmpA).append(tmpB).append(tmpC).append(tmpD)
        #final = bitarray(format(tmpA, '032b'))+bitarray(format(tmpB, '032b'))+bitarray(format(tmpC, '032b'))+bitarray(format(tmpD, '032b'))
        print(int.from_bytes(final.to_bytes(16, byteorder='little'), byteorder='big'))
    wordA = remover(wordA + tmpA)
    wordB = remover(wordB + tmpB)
    wordC = remover(wordC + tmpC)
    wordD = remover(wordD + tmpD)

#final = bitarray(format(wordA, '032b'))+bitarray(format(wordB, '032b'))+bitarray(format(wordC, '032b'))+bitarray(format(wordD, '032b'))
#print(final.tobytes().hex())
final = bytearray(wordA).append(wordB).append(wordC).append(wordD)
#final = bitarray(format(tmpA, '032b'))+bitarray(format(tmpB, '032b'))+bitarray(format(tmpC, '032b'))+bitarray(format(tmpD, '032b'))
print(int.from_bytes(final.to_bytes(16, byteorder='little'), byteorder='big'))

#struct.unpack("<L", d)[0]
