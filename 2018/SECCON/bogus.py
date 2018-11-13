with open('./flag.txt.encrypted','rb') as f:
	c = f.read()

v3 = 'cur10us4ndl0ngh0stn4m3'[::-1]*4

print ''.join( chr(ord(i)^ord(j)) for i,j in zip(c,v3) )