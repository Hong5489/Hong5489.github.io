from sage.all import *
from hashlib import sha256
from Crypto.Cipher import AES


def recurrent(s0, a, b, n):
    s = s0
    for i in range(1, n + 1):
        s = s + a * i + b
    return s


def pad(plaintext, b_size):
    pad_size = b_size - (len(plaintext) % b_size)
    return plaintext + pad_size.to_bytes(1, 'big') * pad_size


if __name__ == '__main__':
    p = random_prime(2 ** 512 - 1, False, 2 ** 511)
    F = GF(p)
    
    a = IntegerMod(F, randint(1, p))
    b = IntegerMod(F, randint(1, p))
    s0 = IntegerMod(F, randint(1, p))
    
    n_a = IntegerMod(F, randint(1, p))
    n_b = IntegerMod(F, randint(1, p))
    
    print("p =", p)
    print("a =", a)
    print("b =", b)
    print("s0 =", s0)
    
    A = recurrent(s0, a, b, n_a)
    B = recurrent(s0, a, b, n_b)
    
    print("A =", A)
    print("B =", B)
    
    master_secret = int(recurrent(A, a, b, n_b))

    flag = open("flag.txt", "rb").read()
    key = sha256(master_secret.to_bytes(64, 'big')).digest()[:16]
    iv = sha256(key).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    print("Encrypted:", iv + cipher.encrypt(pad(flag, 16)))
