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
for x in hash_str:
    result.append(format(ord(x), '08b'))
a = ''.join(result)
orig_len = len(a)# % (2**64)
if orig_len % 512 != 448:
    a = a+'1'
    while len(a) % 512 != 448:
        a = a + '0'

a = bitarray(a) + bitarray(format(orig_len, '064b'))

print('everything padded')

# These words are the basis of the main loop
wordA = bitarray(format(0x67452301, '032b'))
#wordA.frombytes(bytes.fromhex('67452301'))
wordB = bitarray(format(0xefcdab89, '032b'))
#wordB.frombytes(bytes.fromhex('efcdab89'))
wordC = bitarray(format(0x98badcfe, '032b'))
#wordC.frombytes(bytes.fromhex('98badcfe'))
wordD = bitarray(format(0x10325476, '032b'))
#wordD.frombytes(bytes.fromhex('10325476'))

# Used in the main loop
K = [math.floor(abs(math.sin(i + 1)) * 2**32) for i in range(64)] # checked
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

def remover(bitstr, tolen=32):
    return bitstr[len(bitstr)-tolen:]

print('before loops', a.length())

# Breaking everything up into words
for bigbyte in range(int(a.length() / 512)):
    prechunk = a[bigbyte*512: (bigbyte+1)*512]
    chunk = []
    for tzt in range(16):
        chunk.append(prechunk[tzt*32: (tzt+1)*32])
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
        topad = [cycler.length(), tmpA.length()]
        cycler = bitarray(remover(format(struct.unpack("<L", cycler.tobytes())[0] + struct.unpack("<L", tmpA.tobytes())[0] + K[round] + struct.unpack("<L", chunk[sp_round].tobytes())[0], '0'+str(max(topad))+'b')))
        tmpA = tmpD
        tmpD = tmpC
        tmpC = tmpB
        current = struct.unpack("<L", cycler.tobytes())[0]
        toadd = (current << s[round]) | (current >> ((len(bin(current)[2:])*8) - s[round]))
        tmpB = bitarray(remover(format(struct.unpack("<L", tmpB.tobytes())[0] + toadd, '0'+str(max([tmpB.length(), cycler.length()]))+'b')))
        final = tmpA+tmpB+tmpC+tmpD
        print(final.tobytes().hex())
    topad = [wordA.length(), tmpA.length()]
    wordA = bitarray(remover(format(struct.unpack("<L", wordA.tobytes())[0] + struct.unpack("<L", tmpA.tobytes())[0], '0'+str(max(topad))+'b')))
    topad = [wordB.length(), tmpB.length()]
    wordB = bitarray(remover(format(struct.unpack("<L", wordB.tobytes())[0] + struct.unpack("<L", tmpB.tobytes())[0], '0'+str(max(topad))+'b')))
    topad = [wordC.length(), tmpC.length()]
    wordC = bitarray(remover(format(struct.unpack("<L", wordC.tobytes())[0] + struct.unpack("<L", tmpC.tobytes())[0], '0'+str(max(topad))+'b')))
    topad = [wordD.length(), tmpD.length()]
    wordD = bitarray(remover(format(struct.unpack("<L", wordD.tobytes())[0] + struct.unpack("<L", tmpD.tobytes())[0], '0'+str(max(topad))+'b')))

final = wordA+wordB+wordC+wordD
print(final.tobytes().hex())

#struct.unpack("<L", d)[0]
