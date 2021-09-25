import random
import binascii
enc = binascii.unhexlify(open("flag.enc",'rb').read())

def decrypt(s,k):
	n1 = k[0]
	n2 = k[1]

	encrypted = []
	for c in s:
		encrypted.append(c ^ n1)
		random.seed(n1)
		n1 = n2
		n2 = random.randint(0, 255)

	return bytes(encrypted)

k = [ord('f') ^ enc[0], ord('s') ^ enc[1]]
print(k)
print(decrypt(enc,k))
			