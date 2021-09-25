import random
from secret import flag, key

def generate_key(s):
    assert len(s) == 16, "The key must be 16 bytes long"

    k = [0, 0]
    for i in range(len(s)):
        if i == 0:
            k[0] = k[0] ^ s[i]
            k[1] = (k[1] + s[i]) & 0xFF
        else:
            k[0] = (k[0] ^ (s[i] - s[i - 1])) & 0xFF
            k[1] = (k[1] + s[i] ^ s[i - 1]) & 0xFF

    return k

def encrypt(s, k):
    n1 = k[0]
    n2 = k[1]

    encrypted = []
    for c in s:
        encrypted.append(c ^ n1)
        random.seed(n1)
        n1 = n2
        n2 = random.randint(0, 255)

    return bytes(encrypted).hex()

e = encrypt(flag, generate_key(key))

with open('flag.enc', 'w') as f:
    f.write(e)
