with open('japanese.txt','rb') as f:
	p = f.read()

with open('flag.txt','rb') as f:
	q = f.read()

wl = p.split('\n')

en = []
for i in q.split('\n'):
	for j in range(len(wl)):
		if i==wl[j]:
			en.append(j+1)
			break
res = ''
for i in en:
	res += bin(i).replace('0b','').rjust(11,'0')

rr = ''
for i in range(256/4):
	rr += hex(int(res[:256][4*i:4*i+4],2)).replace('0x','')

print rr

import hashlib

d = hashlib.md5()
d.update(rr)
print 'flag is :',d.hexdigest()
