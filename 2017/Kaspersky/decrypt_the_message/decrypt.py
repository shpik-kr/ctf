import urllib
import urllib2

e_b64 = lambda x:x.encode('base64').replace('\n','')
d_b64 = lambda x:x.decode('base64')

url = 'http://95.85.51.183/'
#ciphertext = d_b64('sF6qYP/KDXDo4A8hnqukxv5V1Pw2mLJN/yJ57KeMxOn4f0YW87tbwp7MT//KgtezhJcqqQXzDqFP8EA9j5abmQ==')
ciphertext = d_b64('laohzfIjJ0KMBkuTU4VUph5LAW6n9I5siXZeqC42febijJUkD3+VUtcLq0nVr/tVBjmQgppbinbAnz2H5zgl5A==')
bs = 16
plain = ''
def r(cookie, idx):
    global url
    try:
        req = urllib2.Request(url)
        req.add_header('Cookie','user_info= %s'%(e_b64(cookie)))
        res = urllib2.urlopen(req)
        data = res.read()
    except urllib2.HTTPError, e:
        if e.getcode() == 500:
            data = e.read()
            if 'UnicodeDecodeError: \'ascii\'' in data:
                tmp = data.split('codec can\'t decode byte ')[1]
                d = tmp.split(' in')[0][2:]
                p = int(tmp.split('position ')[1].split(':')[0])
                if idx == p:
                    return int(d,16)
                return -1

for i in range(len(ciphertext)/bs):
    cipher = ciphertext[i*bs:]
    for idx in range(0x00,0x10):
        for k in range(0x00,0x100):
            mal_cipher = cipher[:idx] + chr(k) + cipher[idx+1:]
            d = r(mal_cipher, idx)
            if d > -1:
                plain += chr(d^ord(cipher[idx])^k)
                print '[+] %d(%s): %s '%(idx,(chr(d^ord(cipher[idx])^k)),plain)
                break
            else:
                continue

print '[*] Plain : %s'%(plain)

'''
[+] 0({): {
[+] 1("): {"
[+] 2(n): {"n
[+] 3(a): {"na
[+] 4(m): {"nam
[+] 5(e): {"name
[+] 6("): {"name"
[+] 7(:): {"name":
[+] 8( ): {"name":
[+] 9("): {"name": "
[+] 10(1): {"name": "1
[+] 11("): {"name": "1"
[+] 12(,): {"name": "1",
[+] 13( ): {"name": "1",
[+] 14("): {"name": "1", "
[+] 15(s): {"name": "1", "s
[+] 0(h): {"name": "1", "sh
[+] 1(o): {"name": "1", "sho
[+] 2(w): {"name": "1", "show
[+] 3(_): {"name": "1", "show_
[+] 4(f): {"name": "1", "show_f
[+] 5(l): {"name": "1", "show_fl
[+] 6(a): {"name": "1", "show_fla
[+] 7(g): {"name": "1", "show_flag
[+] 8("): {"name": "1", "show_flag"
[+] 9(:): {"name": "1", "show_flag":
[+] 10( ): {"name": "1", "show_flag":
[+] 11(f): {"name": "1", "show_flag": f
[+] 12(a): {"name": "1", "show_flag": fa
[+] 13(l): {"name": "1", "show_flag": fal
[+] 14(s): {"name": "1", "show_flag": fals
[+] 15(e): {"name": "1", "show_flag": false
[+] 0(}): {"name": "1", "show_flag": false}
'''
