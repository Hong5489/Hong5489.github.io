---
layout: post
title: The 6th “Qiangwang” International Elite Challenge on Cyber Mimic Defense
subtitle: The 6th “Qiangwang” International Elite Challenge on Cyber Mimic Defense (第六届“强网”拟态防御国际精英挑战赛)
tags: [crypto,misc,pwn]
katex: yes
comment: no
---

At 6th December, we were invited to participate the cybermimic elite challenge at Nanjing!!

We got 20++th place for networking racetrack and internet of vehicle racetrack. *No capture the final score.* But we got a trophy for international friendship prize!

![](/uploads/cybermimic2023/competition.jpg)
*Competition title*

![](/uploads/cybermimic2023/competition2.jpg)
*Teams that participated in the competition*

![](/uploads/cybermimic2023/competition3.jpg)
*The car we need to hack during the competition (we didn't managed to hack it..)*

![](/uploads/cybermimic2023/jeopardy.png)
*Jeopardy challenges*

![](/uploads/cybermimic2023/trophy.jpg)
*国际友谊奖 (international friendship prize)*

Here is the writeups for the jeopardy challenges (White-Box Qualification)

# Challenges
- [Bad_rsa](#rsa)
- [Classical](#classical)
- [Git gud](#gitgud)
- [fmt](#fmt)

## Bad_rsa {#rsa}
```py
from Crypto.Util.number import *

f = open('flag.txt','rb')
m = bytes_to_long(f.readline().strip())

p = getPrime(512)
q = getPrime(512)
e = getPrime(8)
n = p*q
phi = (p-1)*(q-1)
d = inverse(e,phi)
leak = d & ((1<<265) - 1)

print(f'e = {e}')
print(f'leak = {leak}')
print(f'n = {n}')
c = pow(m,e,n)
print(f'c = {c}')

'''
e = 149
leak = 6001958312144157007304943931113872134090201010357773442954181100786589106572169
n = 88436063749749362190546240596734626745594171540325086418270903156390958817492063940459108934841028734921718351342152598224670602551497995639921650979296052943953491639892805985538785565357751736799561653032725751622522198746331856539251721033316195306373318196300612386897339425222615697620795751869751705629
c = 58064034919290611425318979044251233043307367338592434271520705142630256695300292742557470989514758812829578637705322075108849184034214079815168950909257727593842696875265180239425397887757956078862042802996557884275633264196055546402068708323290198423684939624230328528498527478735524752152887413794806886338
'''
```
As you can see, it is a RSA question and it leaked the lower 265 bits of the private key `d`. We can use the Boneh Durfee attack to recover the prime factors given part of private key!!

I used this github script to solve this challenge https://github.com/jvdsn/crypto-attacks/blob/master/attacks/rsa/partial_key_exposure.py

Added this few lines at the code below:
```py
from Crypto.Util.number import *
e = 149
leak = 6001958312144157007304943931113872134090201010357773442954181100786589106572169
n = 88436063749749362190546240596734626745594171540325086418270903156390958817492063940459108934841028734921718351342152598224670602551497995639921650979296052943953491639892805985538785565357751736799561653032725751622522198746331856539251721033316195306373318196300612386897339425222615697620795751869751705629
c = 58064034919290611425318979044251233043307367338592434271520705142630256695300292742557470989514758812829578637705322075108849184034214079815168950909257727593842696875265180239425397887757956078862042802996557884275633264196055546402068708323290198423684939624230328528498527478735524752152887413794806886338

p,q,d = attack(n, e, PartialInteger.lsb_of(leak, 1024, 265),m=20, t=20)
print(long_to_bytes(pow(c,d,n)))
```
Then it output the flag!!
```
b'flag{202cb962ac59075b964b07152d234b70}'
```
## Flag
```
flag{202cb962ac59075b964b07152d234b70}
```
---

## Classical {#classical}
- [task.pdf](/uploads/cybermimic2023/classical//task.pdf)

As the PDF stated we need to crack the encryption of [Hill cipher](https://en.wikipedia.org/wiki/Hill_cipher) combine with Vernam cipher

We can combine the two encryption togther into single equation:

\\[c_1 = (k_{1,1}p_1 + k_{1,2}p_2 + ... + k_{1,m}p_m + K_1) \mod 29 \\]
\\[c_2 = (k_{2,1}p_1 + k_{2,2}p_2 + ... + k_{2,m}p_m + K_2) \mod 29 \\]
\\[... \\]
\\[c_m = (k_{m,1}p_1 + k_{m,2}p_2 + ... + k_{m,m}p_m + K_m) \mod 29 \\]

But how we recover both keys?

### Recover keys

We can use the leak given in the PDF to recover both keys!

There are six unknows for the first block of ciphertext $$k_{1,1}$$ $$k_{1,2}$$ $$k_{1,3}$$ $$k_{1,4}$$ $$k_{1,5}$$ and $$K_1$$

Then we need to find the same unknows but different block of ciphertext, which is the 6th block of ciphertext! Because it has block size of 5 means it will reuse the same key in the 6th block of ciphertext

So technically we will 6 different block of ciphertext to solve 6 unknows equation, so we will need gather 6 different ciphertext with 6 different equations

I using matrix method in sage to solve the unknows:
```py
from sage import *
p = "ZQIUOMCEFZGVRGTBAAAAAJRTKENSNQ"
c = "WUJQYGCAHAAAAAGDPQXUXHIDTDLIRG"
# Mod 29
R = IntegerModRing(29)
# Construct plaintext in 6x6 matrix
P = []
for plain in p:
    P.append(ord(plain)-0x41)
P2 = []
for i in range(6):
    P2.append([P[i*5],P[i*5+1],P[i*5+2],P[i*5+3],P[i*5+4],1])
P = Matrix(R,P2)

# Loop 5 times for 6 diff ciphertext
for j in range(5):
    C = []
    for i in range(j,30,5):
        C.append(ord(c[i])-0x41)
    C = vector(R,C)
    # Print the result
    print(P.solve_right(C))
# Output:
# (21, 3, 11, 24, 27, 11)
# (25, 19, 20, 17, 14, 19)
# (2, 9, 1, 26, 4, 14)
# (22, 7, 9, 24, 20, 1)
# (4, 5, 7, 25, 6, 16)
```
Yeah! We recovered the key! Now we just need to decrypt the ciphertext given in the PDF

### Decrypt

```py
import string
# Hill cipher key
k = [[21, 3, 11, 24, 27],
[25, 19, 20, 17, 14],
[2, 9, 1, 26, 4],
[22, 7, 9, 24, 20],
[4, 5, 7, 25, 6]]
# Vername cipher key
K = [11,19,14,1,16]
R = IntegerModRing(29)
ciphertext = "OKCZKNCSQ_ULYOKPKW,PL.UXIWX,YCLXZFGBM_SUJLSCOXZT.AIGFZRDCIX,"
key_matrix = Matrix(R,k)
flag = ""

# Decrypt the ciphertext in block size of 5
for j in range(0,len(ciphertext),5):
	C = ciphertext[j:j+5]
	p = []
	# Decrypt vername cipher (just minus the key)
	for i in range(5):
		p.append((list(string.ascii_uppercase+"_,.").index(C[i]) - K[i%5]) %29)
	p = vector(R,p)
	# Decrypt hill cipher
	result = key_matrix.solve_right(p)
	for r in result:
		flag += (string.ascii_uppercase+"_,.")[r]

print(flag)
# Output:
# QUANTUM_CRYPTOGRAPHY_IS_AN_UNBREAKABLE_SYSTEM_OF_ENCRYPTION.
```
Yes! we solve it! (Solve it at 3am in hotel 😂)

### Flag
```
flag{QUANTUM_CRYPTOGRAPHY_IS_AN_UNBREAKABLE_SYSTEM_OF_ENCRYPTION.}
```
---
## Git gud {#gitgud}

We are given an image:

![](/uploads/cybermimic2023/gitgud/attachment.png)

We solved it after the competition, ask the solution from other teams

## Solution

We you run `zsteg -a` to it, it will show a long text with `Vegetable` `Then` `Many` `Practice`
```bash
zsteg -a attachment.png
imagedata           .. file: executable (RISC System/6000 V3.1) or obj module not stripped
b1,a,lsb,xy         .. text: "nZDDZZDZF"
b1,a,msb,xy         .. text: "KvZ\"\"ZZ\"Zb"
b2,rgb,lsb,xy       .. file: MPEG ADTS, AAC, v4 LTP, surround + LFE
b2,bgr,lsb,xy       .. file: MPEG ADTS, layer II, v1,  32 kbps, 44.1 kHz, 2x Monaural
b4,r,msb,xy         .. text: "E?$(rz&\n"
b4,g,lsb,xy         .. text: "EfUTDUfx"
b4,a,lsb,xy         .. text: "I5H^euA,T"
b4,rgba,lsb,xy      .. text: "*d\t)\\c9%"
b5,r,msb,xy         .. text: "xcwG)Z#(F"
b5,rgba,msb,xy      .. text: ">%Tb4J\n\n$-"
b5,abgr,msb,xy      .. text: "(%ob,THU"
b7,rgba,msb,xy      .. text: "7*eb*PF+x"
b8,r,lsb,xy         .. text: "}]STND>;</,-;WbRQMLHECB<A62\"/_"
b8,g,lsb,xy         .. text: "D21))'7Zt"
b8,b,lsb,xy         .. text: "`RQHE>Ji"
b8,a,lsb,xy         .. text: "VegetableThenManyPracticeThenThenThenManyThenManyThenThenThenManyThenPracticeThenManyThenThenThenPracticeThenVegetableThenManyVegetableThenThenManyVegetableManyThenManyPracticeVegetableThenManyThenThenThenThenThenVegetableThenManyManyVegetableThenManyThenT"
```
When you look closely the text order is not consistent, so it may contains information in it

So we need to convert the long text to base4:
- `Vegetable` replace with `0`
- `Then` replace with `1`
- `Many` replace with `2`
- `Practice` replace with `3`

I wrote a python script to solve this:
```py
from Crypto.Util.number import *
# Ignore the last few words
text = open("text","r").read()[:-36]
text = text.replace("Vegetable", "0").replace("Then", "1").replace("Many","2").replace("Practice","3")
print(long_to_bytes(int(text,4)))
```
it outputs this, means we need to decrypt it again:
```
b"\x1bVegetableThenManyPracticeThenManyThenManyThenManyPracticeVegetableThenManyVegetableThenThenManyThenPracticeThenPracticeManyPracticeThenManyThenVegetableVegetablePracticeThenPracticeVegetablePracticeThenPracticeThenManyThenThenThenManyThenVegetableVegetablePracticeThenThenVegetablePracticeManyThenVegetablePracticeManyVegetableVegetablePracticeThenManyThenManyVegetablePracticeVegetablePracticeVegetablePracticeVegetablePracticeVegetableVegetableThenManyVegetableManyVegetablePracticeThenVegetableThenManyThenThenThenManyThenManyVegetablePracticeManyVegetableVegetablePracticeVegetableManyVegetablePracticeVegetableThenVegetablePracticeManyThenVegetablePracticeThenVegetableVegetablePracticeVegetableManyVegetablePracticeVegetablePracticeVegetablePracticeVegetablePracticeVegetablePracticeThenVegetableVegetablePracticeThenManyThenManyThenThenVegetablePracticeThenPracticeVegetablePracticeVegetableThenVegetablePracticeThenVegetableThenManyThenVegetableVegetablePracticeVegetableVegetableThenPracticePracticeThenIfYouCan'tAffordToLoseThenDon'tPlay"
```
Final script, and we get the flag!!:
```py
from Crypto.Util.number import *
text = open("text","r").read()[:-36]
text = text.replace("Vegetable", "0").replace("Then", "1").replace("Many","2").replace("Practice","3")
text = long_to_bytes(int(text,4))[1:-35].decode()
text = text.replace("Vegetable", "0").replace("Then", "1").replace("Many","2").replace("Practice","3")
text = long_to_bytes(int(text,4))
print(text[1:])
# b'flag{d77ed5986c30b4ef8219423346e714d0}'
```
## Flag
```
flag{d77ed5986c30b4ef8219423346e714d0}
```
---
## fmt {#fmt}
- [fmt](/uploads/cybermimic2023/fmt/fmt)

We are given a linux executable binary file, we need to exploit the format string vulnerability and get the shell, but I cannot solve it during the competition

The binary protection got full relro so we cannot overwrite the GOT and got NX enabled cannot run shellcode, and it calls `exit(0)` after the `printf` so I have no idea how to exploit it

```
[*] '/home/hong/ctf/XCTF/fmt/fmt'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

After the competition, lukily someone from WreckTheLine gave me the [solution script](/uploads/cybermimic2023/fmt/x.py), just run it with `./x.py LOCAL` and it works!! I havent investigate how it works yet, but I guess the solution is related to stack pivot?

# Other challenges (no writeup)
Here are some challenges that we cannot solve during the competition, feel free to try it
- [easy_firmware](/uploads/cybermimic2023/easy_firmware/attachment.zip)
- [cyberpic](/uploads/cybermimic2023/cyberpic/flag.png)
- [ezJava](/uploads/cybermimic2023/ezJava/attachment.zip)
- [funweb](/uploads/cybermimic2023/fun_web/src.zip)
- [keygen](/uploads/cybermimic2023/keygen/keygen1.apk)
- [qi](/uploads/cybermimic2023/qi/attachments.zip)

## Conclusion
I think is great experience to join this onsite competition, finally understood the rules of whitebox and blackbox after the staff explained to us, which is quite complicated lol.. But we still cannot understand how the mimic defense works and how to bypass the executor etc. Maybe we need to study next year before joining the competition. Hope we can join again next year!