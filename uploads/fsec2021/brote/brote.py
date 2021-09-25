
import re
import hashlib

def md5_sha1(x):
        a = hashlib.sha1(x).hexdigest().encode('utf-8')
        return hashlib.md5(a)

def md5_md5_md5(x):
    a = hashlib.md5(x).hexdigest().encode('utf-8')
    a = hashlib.md5(a).hexdigest().encode('utf-8')
    return hashlib.md5(a)

x = [hashlib.sha224, hashlib.sha256, hashlib.sha384, hashlib.sha512, hashlib.md5, hashlib.sha1, md5_sha1, md5_md5_md5]
y = ['3770f06168c0137f3471ba682068ba1de460468d3f04a6412c23fa59', '1d853c1e3b909efceb14a4d92337589041372449d2edc83f890b5fde31d3644b', 'e85fb4a65bc3613d33910d9836cddad339e82a9c3f773c2b23d6bb9734431251ba3e9900e7e22dd5df0f575977549147', '9d7108c35983cf0f0789ed4b09bf44f5b089dc2b9c770336d71fe123908f782318c48c2849dc59c7ad3be9ade3f568bb1cf7e42c3dd9795de829565d46343ac6', '2fc2e03201e06a52b59cdf57075336d8', 'f5043ed6f522cd05f3a771d471ba82f4945feab5', '6ef11bc47eadba4c9c4c44f1e4aaa84f', '3850cda130224d889937e2c652bad56c'
]

def check_flag(flag):
    flag = flag.encode()
    chunks = [flag[i:i+4] for i in range(0, len(flag), 4)]
    for c,(f,o) in zip(chunks, zip(x,y)):
        if f(c).hexdigest() != o:
            return False
    return True

user_input = input("Enter flag for verification: ")

if user_input and \
   len(user_input) == 32 and \
   re.match(r'^[a-z0-9]+$', user_input) and \
   check_flag(user_input):
    print("Congratulations!")
else:
    print("Bad flag!")
