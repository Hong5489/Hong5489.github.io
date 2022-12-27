from Crypto.Util.number import *
from Crypto.PublicKey import RSA
n = int("b48404b9ad050a1b0ea8689e3e3d40c9aeae77ed202db8836aba1a19bb5ec678b26130fc51bd57d8a32ed256a7adaa0134642a71cb3f833a1edf5f478b549072a0c0c1e258d5e22a633f8b4dfa908c3add594e2db19a0cd5d5f9e553b71817eb3d0b549acc33c07737554501b1306b0a5f963d9d6a8b7b7ed48eeeb1d9b38e1f",16)
p_low = int("177b788ae518aca1e26d81d3971e9d3eea80becdb6f2ce94b83facf4f39da5",16)
q_high = int("e73c9e22a5b47418d95bf7d13f7f99859e81a23594e340c243281c657936bdc181",16)

q_low = n * inverse(p_low, 2**246) % 2**246

for i in range(4):
	q = q_high<<248 | i<<246 | q_low
	if n%q==0:
		p = n//q
		e = 65537
		phi = (p-1)*(q-1)
		d = inverse(e, phi)
		key = RSA.construct((n,e,d,p,q))
		pem = key.export_key('PEM')
		print(pem.decode())