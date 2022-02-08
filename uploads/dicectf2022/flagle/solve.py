from z3 import *

p1 = "dice{"
p2 = "F!3lD"
print(p1+p2,end='')

s = Solver()
p3 = [BitVec('b%i'%i,16) for i in range(5)]

s.add(p3[0] * p3[1] == 4800)
s.add(p3[2] + p3[0] == 178)
s.add(p3[2] + p3[1] == 126)
s.add(p3[2] * p3[3] == 9126)
s.add(p3[3] - p3[4] == 62)
s.add(p3[2] * 4800 - p3[4] * p3[3] == 367965)
s.check()
model = s.model()
for p in p3:
	print(chr(model[p].as_long()),end='')

p4 = "cwrap"
print(p4,end='')
p5 = bytearray([121-12,68-4,126-6,35-2,77])
print(p5.decode(),end='')
s2 = Solver()
p6 = [BitVec('c%i'%i,16) for i in range(5)]
for i in range(5):
	s2.add(And(p6[i] <= 126,p6[i] >= 33))
s2.add((p6[1] + 2933) * (p6[0] + 1763) == 5483743)
s2.add(p6[4] == 125)
s2.add((p6[3] + 1546) * (p6[2] + 3913) == 6431119)
s2.check()
model = s2.model()
for p in p6:
	print(chr(model[p].as_long()),end='')