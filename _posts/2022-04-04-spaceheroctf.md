---
layout: post
title: Space Heroes CTF 2022
subtitle: Writeups for Space Heroes CTF 2022
tags: [writeups,rev,crypto, global, ctf]
comments: true
---

I play this CTF last weekend, and we manage to get 46th place!

![score](/uploads/spacehero/score.png)

Here are some of my writeups

# Challenges
- [An Unknown Disassembly](#unknown)
- [Easy Crypto Challenge](#ecc)
- [Shai-Hulud](#worm)

# An Unknown Disassembly {#unknown}
## Description
![unknown](/uploads/spacehero/unknown.png)

## Attachment
- [Dis.txt](/uploads/spacehero/Dis.txt)

We got a text file, looks like python bytes code:
```
  5           0 LOAD_GLOBAL              0 (input)
              2 LOAD_CONST               1 ('Enter the super secret password:')
              4 CALL_FUNCTION            1
              6 STORE_FAST               0 (a)

  6           8 LOAD_CONST               2 ('')
             10 STORE_FAST               1 (b)

  7          12 LOAD_CONST               3 (0)
             14 STORE_FAST               2 (c)

  8          16 LOAD_FAST                0 (a)
             18 GET_ITER
        >>   20 FOR_ITER               136 (to 158)
             22 STORE_FAST               3 (x)
             ...
             ...
             ...
 30         182 LOAD_GLOBAL              1 (print)
            184 LOAD_CONST              14 ('You got the flag!')
            186 CALL_FUNCTION            1
            188 POP_TOP

 31         190 LOAD_GLOBAL              2 (exit)
            192 CALL_FUNCTION            0
            194 POP_TOP

 33     >>  196 LOAD_GLOBAL              1 (print)
            198 LOAD_CONST              15 ('Oops, try again.')
            200 CALL_FUNCTION            1
            202 POP_TOP
            204 LOAD_CONST               0 (None)
            206 RETURN_VALUE
```
## Analyse

After analyse the code, it just replace our input from:
- `3` to `e` or `e` to `3`
- `a` to `@` or `@` to `a`
- `o` to `0` or `0` to `o`

After that it compare the result to `S0th3combination1sonetw0thr3efourf1ve`, if equals then it will print the flag! (when connect to the netcat port)

Then I wrote a python script to reverse the convertion:
```py
text = "S0th3combination1sonetw0thr3efourf1ve"
password = ""
for t in text:
	if t == 'a':
		password += '@'
	elif t == '@':
		password += 'a'
	elif t == '0':
		password += 'o'
	elif t == 'o':
		password += '0'
	elif t == 'e':
		password += '3'
	elif t == '3':
		password += 'e'
	else:
		password += t
print(password)
# Sothec0mbin@ti0n1s0n3twothre3f0urf1v3
```
But when I type the password in netcat, it is incorrect!

```
nc 0.cloud.chals.io 27178
Enter the super secret password:Sothec0mbin@ti0n1s0n3twothre3f0urf1v3
Oops, try again.
```

## Solving

Looks like I missed an important part of the code:
```
 25     >>  148 LOAD_FAST                2 (c)
            150 LOAD_CONST              11 (1)
            152 INPLACE_ADD
            154 STORE_FAST               2 (c)
            156 JUMP_ABSOLUTE           20

 27     >>  158 LOAD_CONST              12 ('S0th3combination1sonetw0thr3efourf1ve')
            160 STORE_FAST               4 (d)

 28         162 LOAD_FAST                2 (c)
            164 LOAD_CONST              13 (4)
            166 BINARY_MODULO
            168 LOAD_CONST               3 (0)
            170 COMPARE_OP               2 (==)
            172 POP_JUMP_IF_FALSE      196

 29         174 LOAD_FAST                1 (b)
            176 LOAD_FAST                4 (d)
            178 COMPARE_OP               2 (==)
            180 POP_JUMP_IF_FALSE      196
```
**The variable `c` must be divisible by 4 then it only compare our input to the string**, and we can control `c` by adding letter `l`

Because it doesn't add `l` to the compare variable `b` and will add variable `c` so we can add `l` to control `c`:

```
 21     >>  130 LOAD_FAST                3 (x)
            132 LOAD_CONST              10 ('l')
            134 COMPARE_OP               2 (==)
            136 POP_JUMP_IF_FALSE      140

 22         138 JUMP_FORWARD             8 (to 148)

 24     >>  140 LOAD_FAST                1 (b)
            142 LOAD_FAST                3 (x)
            144 INPLACE_ADD
            146 STORE_FAST               1 (b)

 25     >>  148 LOAD_FAST                2 (c)
            150 LOAD_CONST              11 (1)
            152 INPLACE_ADD
            154 STORE_FAST               2 (c)
            156 JUMP_ABSOLUTE           20
```

Our input length is `37`, so we need to add three `l` to our input to let `c` = 40:

```
nc 0.cloud.chals.io 27178
Enter the super secret password:Sothec0mbin@ti0n1s0n3twothre3f0urf1v3lll
You got the flag! shctf{1m_jUst_a_p14in_y0gurt_ch4l1eng3}
```
That's it! Simple reverse challenge

## Flag
```
shctf{1m_jUst_a_p14in_y0gurt_ch4l1eng3}
```
---
# Easy Crypto Challenge {#ecc}
## Description
![ecc](/uploads/spacehero/ecc.png)

## Attachment
- [ecc.txt](/uploads/spacehero/ecc.txt)

Got a text file, open it:
```
y^2 = x^3 + ax + b
a = 3820149076078175358
b = 1296618846080155687
modulus = 11648516937377897327
G = (4612592634107804164, 6359529245154327104)
PubKey = (9140537108692473465, 10130615023776320406)
k*G = (7657281011886994152, 10408646581210897023)
C = (5414448462522866853, 5822639685215517063)


What's the message?
```

As stated in the title, it is [Elliptic Curve Cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)

More specific it is using [Elliptic-curve Diffie–Hellman](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)

## Solving

After some researching, found [a wiki page explaining ECC](https://ctf-wiki.mahaloz.re/crypto/asymmetric/discrete-log/ecc/)

Also got python sage code for brute forcing private key:
```py
a = 1234577

b = 3213242

n = 7654319



E = EllipticCurve(GF(n), [0, 0, 0, a, b])



base = E ([5234568, 2287747])
pub = E ([2366653, 1424308])


c1 = E ([5081741, 6744615])
c2 = E ([610619, 6218])


X = base



for i in range(1, n):

    if X == pub:

        secret = i

        print "[+] secret:", i

        break

    else:

        X = X + base

        print i



m = c2 - (c1 * secret)



print "[+] x:", m[0]

print &quot;[+] y:&quot;, m [1]
print "[+] x+y:", m[0] + m[1]
```

Remember the challenge description? 

> I was trying to tell him the importance of setting **a large, random private key**, but he wouldn't listen.

Therefore, the private key should be brute forcable!

Then I modify the sage code to this:
```py
a = 3820149076078175358
b = 1296618846080155687
n = 11648516937377897327
E = EllipticCurve(GF(n), [0, 0, 0, a, b])
G = E([4612592634107804164, 6359529245154327104])
PubKey = E([9140537108692473465, 10130615023776320406])
kG = E([7657281011886994152, 10408646581210897023])
C = E([5414448462522866853, 5822639685215517063])

X = G
for i in range(1,100000):
	if X == PubKey:
		secret = i
		print(i)
		break
	else:
		X = X + G

m = C-(kG*secret)
print(m)
```
If no Sage installed can use the [online shell](https://sagecell.sagemath.org/)

![ecc2](/uploads/spacehero/ecc2.png)

As you can see, found the key is `32901` and decrypted message is `8042846929834025144 : 11238981380437369357`!!

## Flag
So the flag is `shctf{8042846929834025144_11238981380437369357}`

---
# Shai-Hulud {#worm}
## Description
![worm](/uploads/spacehero/worm.png)

## Attachment
- [worm](/uploads/spacehero/worm)

We got an ELF file
```
file worm
worm: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=fa172228425ced68ff045064e58e7a55618ab7b0, not stripped
```
Try to run it:

![worm2](/uploads/spacehero/worm2.png)

It is a snake game... We can use WASD to control the snake

But I played awhile still no idea how to win this game, lets open it with Ghidra!

## Static Analysis

main function:
```c
undefined8 main(void)
{
  int iVar1;
  
  srand(0x2454);
  SHA256_Init((SHA256_CTX *)buf);
  clear();
  wormsign();
  vibration();
  while( true ) {
    if (worm._0_4_ == 0x295) {
      print_flag();
      return 0;
    }
    input_thread();
    wriggle();
    iVar1 = frame();
    if (iVar1 == 0) break;
    printf("\x1b[H\x1b[J");
    draw();
    usleep(100000);
  }
  return 0;
}
```
Can see the `print_flag` function, so when the worm size equals 0x295 then it will print the flag, I guess...

`print_flag` function:
```c
void print_flag(void)
{
  int local_c;
  
  printf("shctf{");
  local_c = 0;
  while (local_c < 0x20) {
    buf2[local_c] = buf2[local_c] ^ magic_bytes[local_c];
    local_c = local_c + 1;
  }
  printf("%.32s}\n",buf2);
  return;
}
```
As you can see, the flag just `buf2` XOR with `magic_bytes`!! 

`magic_bytes` is hard coded in the binary, but `buf2` is not

After some analyzing, notice `buf2` is displaying in the console, can see in the `draw` function
```c
printf("  POW: ");
local_c = 0;
while (local_c < 0x20) {
	printf("%02x",(ulong)(byte)buf2[local_c]);
	local_c = local_c + 1;
}
```

And notice everytime I eat the asterik, the value will change, and every time restart the value is the same!!

Then saw `vibration` is the function to generate the coordinates of the asterik:
```c
void vibration(void)
{
  int iVar1;
  int iVar2;
  
  iVar1 = rand();
  iVar2 = rand();
  *(undefined4 *)(arrakis + ((long)(iVar1 % 0x21) * 0x14 + (long)(iVar2 % 0x14)) * 4) = 0xfffffffe;
  return;
}
```
Can see it generate two random values then calculate the array index of `arrakis` to equal `fffffffe` (-2)

We can guess those values are coordinates x and y

In the `frame` function can see what happen when we eat the asterik:
```c
if (*(int *)(arrakis + ((long)worm._8_4_ * 0x14 + (long)worm._12_4_) * 4) == -2) {
	local_20 = (long)(worm._12_4_ + worm._8_4_ * 0x10);
	SHA256_Update((SHA256_CTX *)buf,&local_20,8);
	SHA256_Final(buf2,(SHA256_CTX *)buf);
	vibration();
	worm._0_4_ = worm._0_4_ + 1;
}
```
It will calculate SHA256 hash based on our coordinates (`worm._8_4_`, `worm._12_4_`)

So it calculate `y + x * 0x10` and store in 8 bytes, then pass to generate the SHA256 hash

After that, it call vibration to generate a new asterik

## First Attempt 

In the `main` function, we can see the random seed number is hardcoded:
```c
srand(0x2454);
```
Remember the coordinates of asterik is generate using `rand()`?

Therefore, we can predict the coordinates of all asterik, then calculate the hash, decrypt the flag!

I used python ctypes libary to generate the random numbers

```py
from ctypes import CDLL
import hashlib
import struct
libc = CDLL("libc.so.6")
libc.srand(0x2454)
x = libc.rand() % 33;
y = libc.rand() % 20;
p = y + x * 16
p = struct.pack("q",p)
print(hashlib.sha256(p).hexdigest())
# 633fcc3c724a53d2dac9328292349c92a17486acdb634f7d33f8f40db7928677
```
Yes! The first hash is the same!

Now check the second hash in case:
```py
from ctypes import CDLL
import hashlib
import struct
libc = CDLL("libc.so.6")
libc.srand(0x2454)
for i in range(2):
	x = libc.rand() % 33;
	y = libc.rand() % 20;
	p = y + x * 16
	p = struct.pack("q",p)
	print(hashlib.sha256(p).hexdigest())
# 633fcc3c724a53d2dac9328292349c92a17486acdb634f7d33f8f40db7928677
# 3fe9233e7ee137c9f87037868a46ccf691b6a0fab013b94cc8aaf2089b4aa019
```
But it not matches.. the second hash should be `ad484ca2df9b973f6c7047aef57580f59440b651d7d6b29bda63301e418b7280`

Then I changed to update instead, but still not matches

```py
from ctypes import CDLL
import hashlib
import struct
libc = CDLL("libc.so.6")
libc.srand(0x2454)
h = hashlib.sha256()
for i in range(2):
	x = libc.rand() % 33;
	y = libc.rand() % 20;
	p = y + x * 16
	p = struct.pack("q",p)
	h.update(p)
	print(h.hexdigest())
# 633fcc3c724a53d2dac9328292349c92a17486acdb634f7d33f8f40db7928677
# 538999d91c309b0edaa40e1a628c16f4d700b3f5ab629a6d3950432c234980b4
```

Then I stuck for awhile to debug the binary

Notice the SHA256 in C and Python got some differences, in C got something called `SHA256_CTX` is a variable in openssl SHA256 library

Everytime I debug the CTX value was not erased, but the [documentation](https://nxmnpg.lemoda.net/3/SHA256_Init) stated after called `SHA256_Final` it will erased

I guess will not work in python, no choice I have to code in C

## Second Attempt

Then coded in C using the openssl library refer to [stackoverflow](https://stackoverflow.com/questions/2262386/generate-sha256-with-openssl-and-c)

```c
#include <openssl/sha.h>
#include <stdio.h>

int main(int argc, char const *argv[])
{
	SHA256_CTX ctx;
	srand(0x2454);
	unsigned char output[256];
	__int64_t buffer;
	int x,y;
	SHA256_Init(&ctx);
	for (int i = 0; i < 2; ++i)
	{
		x = rand() % 33;
		y = rand() % 20;
		buffer = 16 * x + y;
		SHA256_Update(&ctx, &buffer, 8);
		SHA256_Final(output, &ctx);
	}
	fwrite(output,32,1,stdout);
	return 0;
}
```
Compile by `gcc -o test test.c -I/opt/ssl/include/ -L/opt/ssl/lib/ -lcrypto`

Then run it:
```
./test | xxd
00000000: ad48 4ca2 df9b 973f 6c70 47ae f575 80f5  .HL....?lpG..u..
00000010: 9440 b651 d7d6 b29b da63 301e 418b 7280  .@.Q.....c0.A.r.
```
Yes! Looks like is the correct hash!!

Now we just need to change the loop number to `0x294` then get the hash to decrypt the flag!

```
./test | xxd
00000000: c298 d18e c8bf 9975 5041 545d 3c39 a805  .......uPAT]<9..
00000010: 737b deea a3be 4c40 2be2 4890 807f 7b8d  s{....L@+.H...{.
```
Copy the hash and the magic_bytes to decrypt the flag:
```py
magic_bytes = bytes.fromhex("b2eae5bfbb8cc60138720b2f0f549c6e4024ea84c7e17d3458bd2ee2b41248fe")
key = bytes.fromhex("c298d18ec8bf99755041545d3c39a805737bdeeaa3be4c402be24890807f7b8d")
for a,b in zip(magic_bytes,key):
	print(chr(a^b),end='')
# pr41s3_th3_r3m4k3_4nd_1ts_fr4m3s
```
Thats it! That is the flag!

## Flag
```
shctf{pr41s3_th3_r3m4k3_4nd_1ts_fr4m3s}
```

## Conclusion

I think it was good are beginners to play. Some challenge was quite easy but was harder than I expected but it was quite fun 🙂