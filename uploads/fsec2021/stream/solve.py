import random
import binascii
enc = binascii.unhexlify(open("flag.enc",'rb').read())

def decrypt(s, k):
	n1 = k[0]
	n2 = k[1]

	encrypted = []
	for c in s:
		encrypted.append(c ^ n1)
		random.seed(n1)
		n1 = n2
		n2 = random.randint(0, 255)

	return bytes(encrypted)

for k1 in range(256):
	for k2 in range(256):
		flag = decrypt(enc,[k1,k2])
		if flag.startswith(b"fs") and flag.endswith(b"cyber"):
			print(k1,k2)
			print(flag)
