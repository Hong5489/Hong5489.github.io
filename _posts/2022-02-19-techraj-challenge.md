---
layout: post
title: Tech Raj 100$ Challenge
subtitle: Writeups for Tech Raj 100$ Challenge
tags: [writeups, steg, youtube]
comments: true
---

I saw Tech Raj publish an interesting challenge 4 days ago: [https://www.youtube.com/watch?v=Ua7C1v4Yquo](https://www.youtube.com/watch?v=Ua7C1v4Yquo)

Basically we need to find the hidden message in the video in order to claim the 100$

Saw the comments already have some spoiler like `spectogram` and `LSB`, so can confirm that this challenge is about [steganography](https://en.wikipedia.org/wiki/Steganography) 

Steganography is about hiding messages in digital content like image and video, those who play CTF should be familiar 

## Spectogram
Firstly I download the thumbnail and video from the [mega link](https://mega.nz/folder/J4VxiCzR#Zbw78pIMJiiDosDiFVpu-g)

Then I open the `Video.avi` in `Sonic Visualizer` https://sonicvisualiser.org/download.html

Then add spectogram layer:

![image1](/uploads/techraj/image1.png)

Then saw something like hash in the last part:

![image2](/uploads/techraj/image2.png)

The total length is 64 character so I guess should be SHA256 hash? But I didn't find any matches on the internet

If seperate into 32 character (MD5 hash) also didn't find any matches

After awhile, I think it maybe is a ciphertext and key for AES because both are 256bits which is valid for AES decrypt but it return some gibberish

## LSB

Then I started to look at the `thumbnail.png`, running `strings` on it found an interesting string at bottom:

```
oh, I can edit hex? Cool.
LSB{156,267,78,1100,321}
```

LSB is stand for **Least Significant Bit** which is a common technique to hide a message in steganography

But what does the 5 numbers means? Clearly not in ASCII range

At first I thought it was number of bits used in LSB steg, but it was 0-8 so definitely not

Whatever just tried running `zsteg` (Popular stego tool for PNG image)

```
zsteg -a thumbnail.png
[?] 51 bytes of extra data after image end (IEND), offset = 0xacab
extradata:0         .. text: "oh, I can edit hex? Cool. \nLSB{156,267,78,1100,321}"
imagedata           .. text: "EEE111)))"
```
But nothing return 🙁, the image data is not LSB

After that, I stucked for awhile.. tried many stego tools but didn't find anything.. The numbers must be something important

## Hints

Then I looked for hints in the Tech Raj discord channel, found that someone was discussing about this challenge

Then eventually, Tech Raj release the first hint:

![hint1](/uploads/techraj/hint1.png)

Then I thought it is SHA256 hash so I brute force it using `hashcat` but nothing also 🙁

Next I saw in discord, he gave hints in his instragram story:

![hint2](/uploads/techraj/hint2.png)

Then I suddently understand what the LSB string means! 

We need to extract each frames in the video and **extract the LSB value from the specific frame number!**

## Extract frame

We can extract all frame from the video using `ffmpeg` command 

```bash
# Extract all frame named by frame number
ffmpeg -i Video.avi %d.png
```
The string given was `LSB{156,267,78,1100,321}` so we need to extract `156.png` first

Then run `zsteg 156.png` and fingers crossed..

```
zsteg 156.png
imagedata           .. text: "Ej~Ej~Ej~Ej~Ej~Ej~Ej~Di}Bg}Af|?g|?g|@h}@h}@h}?g|AfzAfzBgyBgyAdwAdw>at?bu?bw?bw=bv6[o1Vj2Wk2Wi1Vh-Uf-Uf-Uf-Uf-Uf-Uf-Uf/Wh/Tf/Tf/Tf1Vh1Vh1Vh1Vh1Vh/Tf/Tf/Tf/Tf1Vh1Vh2Uh2Uh0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf0Sf2Uh2Vf2Vf2Vd3We3We3We3Yf4Zg5[j5[j8`qGo"
b2,r,lsb,xy         .. text: ["U" repeated 10 times]
b2,r,msb,xy         .. text: ["U" repeated 12 times]
b2,g,lsb,xy         .. file: VISX image file
b2,g,msb,xy         .. file: SoftQuad DESC or font file binary - version 27306
b2,b,lsb,xy         .. file: SoftQuad DESC or font file binary
b2,b,msb,xy         .. file: VISX image file
b4,r,lsb,xy         .. file: AIX core file fulldump
b4,r,msb,xy         .. text: ["D" repeated 8 times]
b4,g,lsb,xy         .. text: "ffffwwfffffffffffUTDDDDDDDDDDDDD33333333\"\"\""
b4,g,msb,xy         .. text: ["U" repeated 8 times]
b4,b,lsb,xy         .. file: 5View capture file
b4,b,msb,xy         .. file: VISX image file
b4,bgr,msb,xy       .. file: PGP Secret Key -
```
Nothing really interesting.. Even tried with `-a` but nothing also

After that, I was stucked for awhile again.. Then Tech Raj release a hint again:

![hint3](/uploads/techraj/hint3.png)

Looked at the code can see the usage:
```
Usage: 
python aesutil.py <encrypt/decrypt> <message/cipher> <key> <keytype> 
Encrypt a message: 
python aesutil.py encrypt "Hello world" "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05" "hex"
or
python aesutil.py encrypt "Hello world" "testpassword" "ascii"
Decrypt a message:
python aesutil.py decrypt "KnJxqDY0D5zWgycuvxZdTKm2520qI2DRCItSMyJtdxA=" "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05" "hex"
or
python aesutil.py decrypt "KnJxqDY0D5zWgycuvxZdTKm2520qI2DRCItSMyJtdxA=" "testpassword" "ascii"
```
This is the biggest hint! 

**Remember the hash we got from the spectrogram, is the key for this script! And now we just left finding the ciphertext to decrypt!**

Where is the ciphertext? No other place must be the LSB data from the specific frames!

The ciphertext should be in base64 form if not mistaken

After that, I tried many other [stego tools from gtihub](https://github.com/DominicBreuker/stego-toolkit) to extract the data but no luck..

Then Tech Raj release a hint again:

![hint4](/uploads/techraj/hint4.png)

Then I checked the youtube metadata [from here](https://mattw.io/youtube-metadata/)

Then from the video metadata got some interesting tags:
```json
{
    ...
    ...
    ...
    "channelTitle": "Tech Raj",
    "tags": [
        "stegano",
        "strings",
        "tech raj",
        "challenge",
        "100$"
    ],
    "categoryId": "28",
    "liveBroadcastContent": "none",
    "localized": {
        "title": "This video has 100$ hidden inside..",
        "description": "Hurry up! Find the 100$ and you get to keep it :)\nAlso, if you want to have a clearer look at the video in its original quality, without compression (youtube compresses the video file when uploaded), check this link: https://drive.google.com/drive/folders/16a15WZ_ERH4geKG0du2BJbJBM4Or0KAF?usp=sharing\nAlternate Link: https://mega.nz/folder/J4VxiCzR#Zbw78pIMJiiDosDiFVpu-g\n\nAnd, keep checking the pinned comment under this video. It will display the status of this challenge, that is, whether anyone has solved it.\n\nJoin my Discord: https://discord.gg/6TjBzgt\nFollow me on Instagram: https://instagram.com/teja.techraj\nWebsite: https://techraj156.com​​​​​\nBlog: https://blog.techraj156.com​\nGitHub: https://github.com/teja156\n\nThanks for watching!\nSUBSCRIBE for more videos"
    },
    "defaultAudioLanguage": "en"
}
```
The `stegano` tag reminds me about this tools in github: [https://github.com/cedricbonhomme/Stegano](https://github.com/cedricbonhomme/Stegano)

Then I tried to install and use it to extract LSB from `156.png` using command `stegano-lsb reveal -i 156.png`

But nothing is extracted.. What could possibly go wrong???

## Solving

Lastly, I realised the number is an index value (count from zero) after I tried to extract the number next to it:
```bash
stegano-lsb reveal -i 157.png
# MI4NLO+eBjkp67OyUvBeVPWc+gAwHNJwSkfkfqVaSeyj1
```
Alternatively, I found can use `zsteg` to extract also:
```
zsteg 157.png
imagedata           .. text: "Ej~Ej~Ej~Ej~Ej~Ej~Ej~Ej~Ej~Ej~Di}Di}Ch|Bg{Di}Ch|CfyCfyCfyCfyBexBexBex?bu?bu?bu=`s9\\o4Yk3Xj2Wi2Wi2Uh2Uh2Vf0Td/Ud/Ud/Ud/Ud1Vh1Vh1Vh1Vh1Vh1Vh1Vh1Vh1Vh1Vh2Uh2Uh0Sf0Sf0Sf0Sf0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td0Td2Vf2Vf5We5We4Vd4Vd3We3We4Xh-Qa3XjIn"
b1,r,lsb,xy         .. text: "94>eW5V4y425"
b1,rgb,lsb,xy       .. text: "45:MI4NLO+eBjkp67OyUvBeVPWc+gAwHNJwSkfkfqVaSeyj1"
...
...
...
```

So all numbers we have to plus one to extract, I wrote a python script to extract all value and decrypt the ciphertext:

```py
# Import stegano library
from stegano import lsb
index = [156,267,78,1100,321]
data = ""

for i in index:
	# concatenate all data together
	data += lsb.reveal(f"images_png/{i+1}.png")
print(data)

from Crypto.Cipher import AES
import base64
key = bytes.fromhex("92786491b4015404961822c6734475154ecd896215b35f3a3baf3f854b550d37")
# First 16 bytes is IV else is ciphertext
IV = base64.b64decode(data)[:16]
ciphertext = base64.b64decode(data)[16:]

cipher = AES.new(key,AES.MODE_CBC,IV)
print(cipher.decrypt(ciphertext))
# Output:
# MI4NLO+eBjkp67OyUvBeVPWc+gAwHNJwSkfkfqVaSeyj1LlKUGffUah27n7iesmQ/AD1DOd2yJ80HLVh09Fglve63Oh7LDXUEUpxJGULxWhx0caVI+BpdJL9lEgDyPkHOVw0k6Q38e7mAoltD2tnZcduEJx1jH+P/q5s8lKhiW9O1feyAfoJZedRv67As6/x26mXVCujVkG5CM0bk83vYQ==
# b'Well done! Now get your 100$ before someone else claims it https://www.techraj156.com/qkazggrkf96qq4y (password:5nTfzhehLagigjx)\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
```
Finally got the link! Yeah!! Solved after 3 days of struggling! 

## Decrypted Message
```
Well done! Now get your 100$ before someone else claims it https://www.techraj156.com/qkazggrkf96qq4y (password:5nTfzhehLagigjx)
```

## Conclusion

It was a fun challenge but I think its abit guessy, if without the hints I think maybe I will not able to solve it. Anyway thanks again to Tech Raj for the building the challenge and the gift!