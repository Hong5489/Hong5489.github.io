from Crypto.Util.number import *
from z3 import *

# AND gate
def f1(a, b):
	return a & b

# OR Gate
def f2(a, b):
	return a | b

# NOT gate
def f3(a):
	return ~a

def f4(a, b):
	return f2(f1(a, f3(b)), f1(f3(a), b))

def f5(x, y, z):
	s = f4(f4(x, y), z)
	c = f2(f1(x, y), f1(z, f2(x, y)))
	return (s, c)

def f6(a, b):
	ans = 0
	z = 0
	# Reverse bit string twise so nothing will change
	for i in range(32):
		ans |= f5((a & (1 << i))>>i,(b & (1 << i))>>i, z)[0] << i
		z = f5((a & (1 << i))>>i,(b & (1 << i))>>i, z)[1]

	return ans

# Shift Left
def f7(a, n):
	return a << n 

# Shift Right
def f8(a, n):
	return a >> n

def f9(a, b):
	ans = 0
	for i in range(32):
		ans |= f4((a & (1 << i))>>i,(b & (1 << i))>>i) << i

	return ans

def f10(v0, v1, k0, k1, k2, k3):
	s = 0
	d = 2654435769
	for i in range(32):
		s = f6(s, d)
		v0 = f6(v0, f9(f9(f6(f7(v1, 4), k0), f6(v1, s)), f6(f8(v1, 5), k1)))
		v1 = f6(v1, f9(f9(f6(f7(v0, 4), k2), f6(v0, s)), f6(f8(v0, 5), k3)))

	return (v0 << 32)+ v1

k0 = 0b100010001000101
k1 = 0b100000101000100
k2 = 0b100001001000101
k3 = 0b100010101000110
res = 0b001111101000100101000111110010111100110010010100010001100011100100110001001101011000001110001000001110110000101101101000100100111101101001100010011100110110000100111011001011100110010000100111
# Declare 2 BitVector 64bit for the input
v0 = BitVec('v0',64)
v1 = BitVec('v1',64)
for i in range(3):
	s = Solver()
	# Add both condition > 0 and < 0xffffffff
	s.add(v0 > 0)
	s.add(v0 < 0xffffffff)
	s.add(v1 > 0)
	s.add(v1 < 0xffffffff)
	# Add condition to equal the bit string
	s.add(f10(v0, v1, k0, k1, k2, k3) == res & 0xffffffffffffffff)
	s.check()
	model = s.model()
	print(long_to_bytes(model[v0].as_long()))
	print(long_to_bytes(model[v1].as_long()))
	res >>= 64