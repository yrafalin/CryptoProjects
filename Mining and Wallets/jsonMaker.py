import random
import json
import string

def makeJSON(big, tx_len=20, adder='t'):
    fake_dict = {}
    for num in range(big):
        fake_dict[adder+str(num)] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random.randrange(4, tx_len)))
    return fake_dict

if __name__ == '__main__':
    with open('./transactions1.json', 'w') as open_file:
        json.dump(makeJSON(20), open_file)
