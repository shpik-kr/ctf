flag  = "FE7588A95AAA10529C6A67F482BE2156590B9732214693AE400D2E1F83434000".decode("hex")
rnd = "1DAB1B0FA7D91AB0617EB648A456CF7E4905FD059CF95445FA24C61D68F246CEC1ADAB0824869CF8586562884922821129146374AE28CE8C792DAB07BB75259D".decode("hex")

def xor64(x=88172645463325252):
	x = (x ^ (x << 13))&((1 << 64)-1)
	x = (x ^ (x >> 7))&((1 << 64)-1)
	x = (x ^ (x << 17))&((1 << 64)-1)
	return x & ((1 << 64)-1)

x = 0x139408dcbbf7a44
res = ""

for j in range(0, len(flag)):
	x = xor64(x)

	res += chr( ord(flag[j]) ^ (x & 0xff) ^ ord(rnd[j]) )
print(res)
