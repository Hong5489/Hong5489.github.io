from pwn import *
import hashlib
import string
import json
p = remote("121.36.197.254" ,9999)
# p = remote("127.0.0.1",23333)
p.recvuntil("sha256(XXXX+")
text = p.recvuntil(") == ")[:-5]
h = p.recvuntil("\n")[:-1]
# print(text,h)

key = pwnlib.util.iters.mbruteforce(lambda x: hashlib.sha256(x.encode()+text).hexdigest() == h.decode(), string.ascii_letters+string.digits, length = 4)
p.sendlineafter("Give me XXXX:",key)
sigs = []
p.recvuntil('(')
public_key = p.recvuntil(')')[:-1].split(b', ')

p.sendlineafter("Give me your message:",'a')
for i in range(100):
	result = p.recvuntil("Give me").split(b'\n')
	# print(result)
	r = int(result[1].split(b" = ")[1])
	s = int(result[2].split(b" = ")[1])
	kp = int(result[3].split(b" = ")[1])
	h = int(result[4].split(b" = ")[1])
	sigs.append({
		"r":r,
		"s":s,
		"kp":kp
	})
	if i != 99:
		p.sendline('a')

data = {
	"curve": "SECP256K1", 
	"public_key": [int(public_key[0]), int(public_key[1])], 
	"known_type": "LSB",
	"known_bits": 8,
	"signatures": sigs, 
	"message": [97]
}
with open("data.json", "w") as fout:
	json.dump(data, fout)
p.interactive()