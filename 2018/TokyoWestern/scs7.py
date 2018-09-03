from pwn import *
import string
r = remote('crypto.chal.ctf.westerns.tokyo',14791)

r.recvuntil(': ')
flag = r.recvuntil('\n')[:-1]	
print flag

prev = ['a','b','c','d','e']
prev = []
FFF = '67ced5346146c105075443add26fd7efd72763dd'
if prev != []:
	for p in prev:
		tmp_flag = FFF+str(p)
		print 'Now : %s'%(tmp_flag)
		for i in '0123456789abcdef':
			r.recvuntil('message:')
			r.sendline('TWCTF{'+tmp_flag+i+'A'*(39-len(tmp_flag))+'}')
			r.recvuntil('ciphertext: ')
			res = r.recvuntil('\n')[:-1]
			#print len(res),res
			cnt = 0
			for j in range(64):
				if flag[j] == res[j]:
					cnt += 1
				else:
					break
			print cnt,i
else:
	tmp_flag = FFF
	print 'Now : %s'%(tmp_flag)
	for i in '0123456789abcdef':
		r.recvuntil('message:')
		r.sendline('TWCTF{'+tmp_flag+i+'A'*(39-len(tmp_flag))+'}')
		r.recvuntil('ciphertext: ')
		res = r.recvuntil('\n')[:-1]
		#print len(res),res
		cnt = 0
		for j in range(64):
			if flag[j] == res[j]:
				cnt += 1
			else:
				break
		print cnt,i

'''
TWCTF{67ced5346146c105075443add26fd7efd72763dd}
'''