import re
import string

# for i in range(26):
# 	print(f"""{string.ascii_lowercase[i]}(open('flag','rb').read()[{i+26+26+26}])""",end='+')

text = open("output",'r').read()
result = bytearray([int(r) for r in re.findall("left\(([0-9]+) ",text)])
print(result.decode())