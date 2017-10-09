import urllib
import urllib2

e_b64 = lambda x:x.encode('base64').replace('\n','')
d_b64 = lambda x:x.decode('base64')

url = 'http://95.85.51.183/'
ciphertext = d_b64('laohzfIjJ0KMBkuTU4VUph5LAW6n9I5siXZeqC42febijJUkD3+VUtcLq0nVr/tVBjmQgppbinbAnz2H5zgl5A==')
plaintext = '{"name": "1", "show_flag": false}'
mal_plain = '{"name": "1", "show_flag": true }'
bs = 16

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

# plain ^ malformed_plain ^ iv = malformed_iv [ block 1 ]
mal_tmp = ''
for j in range(16):
    mal_tmp += chr(ord(plaintext[bs+j])^ord(mal_plain[bs+j])^ord(ciphertext[bs+j]))

cipher = ciphertext[:16]+mal_tmp+ciphertext[32:]

# [ block 0 : IV ]
cookie = ''
for idx in range(0x00,0x10):
    for k in range(0x00,0x100):
        mal_cipher = cookie + chr(k) + cipher[idx+1:]
        d = r(mal_cipher, idx)
        if d > -1:
            cookie += chr(d^k^ord(plaintext[idx]))
            print '[+] %d(%s): %s '%(idx,(chr(d^k^ord(plaintext[idx])).encode('hex')),cookie)
            break
        else:
            continue

cookie += cipher[16:]

print '[*] Cookie : %s'%(cookie)
print '[*] Cookie base64 : %s'%(e_b64(cookie))
