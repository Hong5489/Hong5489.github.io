transform_table = bytes.fromhex("c649139a6709de2b581e48534f9d35ae81d8c477ad96c1ee0c16321faa08e5ca8783fe45e01454ff5e107fd3202d2ea77b3e64a2846f91bfb441d6ef75aced5b3c50740f045d714b25ba9f3fe1608c33e7c7f41bc5bce2ecb3b143231a9c247ecdda826cd038707d0afd01114e7a97ce408826b7a086cb1799306e63988accd2025a56348ba4807c19429521b9c28e6690550d47b6e4d9d4a18d93db6d92361261f0e3f573f1c9c872c0f2aba885f8afd52ff90beb9e4cdc94bbd1a6298f374aa35122e939e6c31c0076523b65fb0344f305a95c46e857f74d3d0627cf153af65fddb8b2fc68d7bd629b0789592a6b31a51d0eb5282cfabe79186a7869eab0")
target = [i%256 for i in [-74, 56, -99, -111, 95, 98, -38, -116, -5, 76, -18, -84, -65, -112, 31, -81]]

b2 = 0
flag = bytearray(b'a'*16)
for i in range(0,len(target),2):
	b1 = transform_table[i]
	flag[i] = transform_table.index(target[i] ^ b1 ^ b2)
	b2 = transform_table[i+1] ^ b1 ^ b2
	flag[i+1] = transform_table.index(target[i+1] ^ b2)

print(flag)