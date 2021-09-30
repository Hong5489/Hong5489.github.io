flag = bytearray("fs0bfusc????????4rtcyber",encoding="ascii")
f1 = flag[0:2] + flag[0x14:0x16]
verify = [0x52, 0x7, 0x4a, 0x6, 0x4, 0xa, 0x0, 0x12]

for i in range(8):
    flag[i+8] = verify[i] ^ f1[i%4]
print(flag)