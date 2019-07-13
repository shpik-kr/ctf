
# Stage2

import ctypes
import string

def uint32_to_int32(i):
    return ctypes.c_int32(i).value

def int32_to_uint32(i):
    return ctypes.c_uint32(i).value

def str2hex(s):
	h = []
	for i in range(len(s)/4):
		t = (ord(s[i*4]) + (ord(s[i*4+1])<<8) + (ord(s[i*4+2])<<16) + (ord(s[i*4+3])<<24))

		h.append(uint32_to_int32(t))
	return h

def hex2str(h):
	s = ''
	for i in h:
		t = hex(int32_to_uint32(i)).replace('L','')[2:].rjust(8,'0').decode('hex')[::-1]
		s += t
	return s

def d1(a,b):
	c = 0
	d = 0
	e = 0
	f = len(a)
	g = a[f-1]
	h = a[0]
	i = 2654435769
	j = 7
	k = 18581050383
	for iii in range(7):
		d = 3 & (k>>2)
		for e in range(f-1,-1,-1):
			if e > 0:
				g = a[e-1]
			else:
				g = a[f-1]
			tmp1 = ((int32_to_uint32(g)>>5) ^ (int32_to_uint32(h)<<2))
			tmp2 = ((int32_to_uint32(h)>>3) ^ (int32_to_uint32(g)<<4))
			tmp3 = k^h
			tmp4 = (int32_to_uint32(b[3&e^d]) ^ g)
			c = (tmp1+tmp2)^(tmp3+tmp4)
			c = uint32_to_int32(c)
			a[e] = (a[e]-c)
			h = a[e]
		k -= i
	return a


encrypt = 'A2xcVTrDuF+EqdD8VibVZIWY2k334hwWPsIzgPgmHSapj+zeDlPqH/RHlpVCitdlxQQfzOjO01xCW/6TNqkciPRbOZsizdYNf5eEOgghG0YhmIplCBLhGdxmnvsIT/69I08I/ZvIxkWyufhLayTDzFeGZlPQfjqtY8Wr59Lkw/JggztpJYPWng=='.decode('base64')
c = str2hex(encrypt)

lang = ['af', 'hr', 'el', 'Greek', 'pl', 'sx', 'Sutu', 'sq', 'cs', 'Czech', 'gu', 'pt', 'sw', 'ar', 'da', 'ht', 'pt-br', 'sv', 'ar-dz', 'nl', 'he', 'pa', 'sv-fi', 'ar-bh', 'nl-be', 'hi', 'Hindi', 'pa-in', 'sv-sv', 'ar-eg', 'en', 'hu', 'pa-pk', 'ta', 'Tamil', 'ar-iq', 'en-au', 'is', 'qu', 'tt', 'Tatar', 'ar-jo', 'en-bz', 'id', 'rm', 'te', 'ar-kw', 'en-ca', 'iu', 'ro', 'th', 'Thai', 'ar-lb', 'en-ie', 'ga', 'Irish', 'ro-mo', 'tig', 'Tigre', 'ar-ly', 'en-jm', 'it', 'ru', 'ts', 'ar-ma', 'en-nz', 'it-ch', 'ru-mo', 'tn', 'ar-om', 'en-ph', 'ja', 'sz', 'tr', 'ar-qa', 'en-za', 'kn', 'sg', 'Sango', 'tk', 'ar-sa', 'en-tt', 'ks', 'sa', 'uk', 'ar-sy', 'en-gb', 'kk', 'sc', 'hsb', 'ar-tn', 'en-us', 'km', 'Khmer', 'gd', 'ur', 'Urdu', 'ar-ae', 'en-zw', 'ky', 'sd', 've', 'Venda', 'ar-ye', 'eo', 'tlh', 'si', 'vi', 'ar', 'et', 'ko', 'sr', 'vo', 'hy', 'fo', 'ko-kp', 'sk', 'wa', 'as', 'fa', 'Farsi', 'ko-kr', 'sl', 'cy', 'Welsh', 'ast', 'fj', 'la', 'Latin', 'so', 'xh', 'Xhosa', 'az', 'fi', 'lv', 'sb', 'ji', 'eu', 'fr', 'lt', 'es', 'zu', 'Zulu', 'bg', 'fr-be', 'lb', 'es-ar', 'be', 'fr-ca', 'mk', 'es-bo', 'bn', 'fr-fr', 'ms', 'Malay', 'es-cl', 'bs', 'fr-lu', 'ml', 'es-co', 'br', 'fr-mc', 'mt', 'es-cr', 'bg', 'fr-ch', 'mi', 'Maori', 'es-do', 'my', 'fy', 'mr', 'es-ec', 'ca', 'fur', 'mo', 'es-sv', 'ch', 'gd', 'nv', 'es-gt', 'ce', 'gd-ie', 'ng', 'es-hn', 'zh', 'gl', 'ne', 'es-mx', 'zh-hk', 'ka', 'no', 'es-ni', 'zh-cn', 'de', 'nb', 'es-pa', 'zh-sg', 'de-at', 'nn', 'es-py', 'zh-tw', 'de-de', 'oc', 'es-pe', 'cv', 'de-li', 'or', 'Oriya', 'es-pr', 'co', 'de-lu', 'om', 'Oromo', 'es-es', 'cr', 'Cree', 'de-ch', 'fa', 'es-uy', 'fa-ir', 'es-ve']
platform = ['linux']
for i in range(len(platform)):
	for ll in range(128):
		for ll2 in lang:
			encrypt = 'A2xcVTrDuF+EqdD8VibVZIWY2k334hwWPsIzgPgmHSapj+zeDlPqH/RHlpVCitdlxQQfzOjO01xCW/6TNqkciPRbOZsizdYNf5eEOgghG0YhmIplCBLhGdxmnvsIT/69I08I/ZvIxkWyufhLayTDzFeGZlPQfjqtY8Wr59Lkw/JggztpJYPWng=='.decode('base64')
			c = str2hex(encrypt)
			tt = bin(ll).replace('0b','').rjust(7,'0')
			key = platform[i][:5].upper()+'1'+tt[:4]+ll2[:2].upper()+tt[4:]+'0' + '011MOZILLA'
			k = str2hex(key)
			qq = hex2str(d1(c,k))
			cnt = 0
			for asdf in qq:
				if asdf in string.printable:
					cnt += 1
			if cnt > 90:
				print key, qq
'''
LINUX10000FR1000000MOZILLA
var dJs = document.createElement('script'); 
dJs.setAttribute('src','./src/npoTHyBXnpZWgLorNrYc.js'); 
document.head.appendChild(dJs);
'''

# Stage 3
with open('rev2.js','rb') as f:
	q = f.read()
res =  ''
for i in q.split('_0x5877'):
	qq = i[:30]
	if "')" in qq:
		res += '"\\n'+'_0x5877'+qq.split("')")[0]+"') : \""'+'+'_0x5877'+qq.split("')")[0]+"')+"

print res

'''
_0x5877('0x0', 'fYVo') : csEBi
_0x5877('0x1', 'cw[y') : apply
_0x5877('0x2', 'R2OT') : NvaHu
_0x5877('0x3', 'WlSm') : NvaHu
_0x5877('0x4', 'adOx') : function *\( *\)
_0x5877('0x5', 'R2OT') : \+\+ *(?:_0x(?:[a-f0-9]){4,6}|(?:\b|\d)[a-z0-9]{1,4}(?:\b|\d))
_0x5877('0x6', '5&eh') : init
... ... 
_0x5877('0x86', '^9I*') : ./src/WFmJWvYBQmZnedwpdQBU.js
_0x5877('0x87', 'w(zO') : appendChild
_0x5877('0x88', 'jEx@') : PYyVn
_0x5877('0x89', 'E7O$') : XVaYV

_0x5877('0x86', '^9I*') : ./src/WFmJWvYBQmZnedwpdQBU.js
https://malvertising.web.ctfcompetition.com/ads/src/WFmJWvYBQmZnedwpdQBU.js
alert("CTF{I-LOVE-MALVERTISING-wkJsuw}")
'''