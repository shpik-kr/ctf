p = ''
with open('filtered.pcap') as f:
    for line in f.readlines():
        p += line

f = open('flag.jpg','w')
from pwn import *

hdr = '\x00\x0c\x29\xac\x31\xb8\x00\x0c\x29\xf4\xb2\xef\x08\x00\x45\x00\x00\xe8'
#print len(p.split(hdr))*0x18
for i in p.split(hdr)[1:]:
	#print i[62:66]
	k = i.split('\x01\x01\x08\x0a\x00\x2b')
	if len(k)==2:
		if k[1][6]=='1':
			f.write(i[67:67+u32(i[63:67])])
	else:
		for j in k:
			if j[6] == '1':
				f.write(i[67:67+u32(i[63:67])])


f.close()
'''
SCTF{H3llo_Cov3rt_S5L}
'''