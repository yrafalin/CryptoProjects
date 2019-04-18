import random
import json
import string

def makeJSON(big, tx_len=20, adder='t'):
    fake_dict = {}
    for num in range(big):
        fake_dict[adder+str(num)] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random.randrange(big, tx_len)))
    return fake_dict

with open('./transactions1.json', 'w') as open_file:
    json.dump(fake_dict, open_file)
