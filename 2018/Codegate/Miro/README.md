# [Crypto] Codegate 2018 Quals - Miro

## Description

Do you wanna play the game? :D



## Analysis

문제에서 pcap파일과 py파일이 주어졌다.

python의 파일의 내용은 다음과 같다.

```python
from socket import *
from ssl import *
import time

def recv_until(s, string):
    result = ''
    while string not in result:
        result += s.recv(1)
    return result

client_socket=socket(AF_INET, SOCK_STREAM)
tls_client = wrap_socket(client_socket, ssl_version=PROTOCOL_TLSv1_2, cert_reqs=CERT_NONE)

print "[+] Connecting with server.."

tls_client.connect(('ch41l3ng3s.codegate.kr',443))

print "[+] Connect OK"

while 1:
    data = recv_until(tls_client, "Input : ")
    print data
    #message
    user_input = raw_input()
    
    if user_input == "u":
        print "Sorry.. Not support function.."
        exit()
    elif user_input == "d": 
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        print "Sorry.. Not support function.."
        exit()
    else:
        print "Invalid input!"
        exit()    

client_socket.shutdown(SHUT_RDWR)
client_socket.close()
```

up과 left의 기능을 구현하면 되는 문제인 것 같다.

pcap파일을 열어 보면 Hello Server패킷에서 인증서(public)를 추출할 수 있다.

해당 데이터를 추출해서 openssl을 이용해 인증서 내용을 확인하자.

```
openssl x509 -inform DER -in ./miro_cert.bin -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 18149708421998587521 (0xfbe0b7a606242e81)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=KR, ST=Daejeon, L=Daejeon, O=Bpsec, OU=Bpsec, CN=codegate/emailAddress=codegate2018@bpsec.co.kr
        Validity
            Not Before: Jan 29 06:55:41 2018 GMT
            Not After : Jan 30 06:55:41 2028 GMT
        Subject: C=KR, ST=Daejeon, L=Daejeon, O=Bpsec, OU=Bpsec, CN=codegate/emailAddress=codegate2018@bpsec.co.kr
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (1025 bit)
                Modulus:
                    01:c2:0b:dc:01:7e:3c:aa:3c:57:9b:40:d4:39:e2:
                    ec:d7:0f:12:c4:d7:f2:76:47:84:c9:5a:3f:dd:ba:
                    00:98:1b:a9:ce:5b:22:7a:de:47:b0:a7:a0:a8:ac:
                    ab:a4:54:1a:b9:5c:52:f6:b6:de:3d:f9:ec:09:0c:
                    6c:35:64:45:b2:1b:e4:37:ab:e1:02:14:d0:b4:a3:
                    98:a9:67:43:bb:f7:0c:86:46:87:fb:2e:c9:29:f0:
                    1d:6e:da:b2:d9:87:fe:09:79:9a:d2:20:4a:27:04:
                    f3:30:61:db:f9:c2:e0:3b:33:2f:0b:a1:a4:46:64:
                    4c:86:4a:06:cd:58:6d:48:0b
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier:
                E8:F6:76:EA:72:5A:71:E6:50:47:D6:8F:0B:44:A4:9C:24:FB:C8:23
            X509v3 Authority Key Identifier:
                keyid:E8:F6:76:EA:72:5A:71:E6:50:47:D6:8F:0B:44:A4:9C:24:FB:C8:23

            X509v3 Basic Constraints:
                CA:TRUE
    Signature Algorithm: sha256WithRSAEncryption
         00:07:32:9a:43:79:ec:e6:c2:4e:52:df:8a:b9:2e:c5:78:cb:
         c1:1b:ff:fd:44:6c:8f:fa:96:36:a5:9e:b9:05:27:d3:65:39:
         3e:11:1b:19:b9:74:8c:ad:ab:a9:84:af:5b:f1:25:69:62:c0:
         1f:70:b3:3e:93:89:63:a0:bb:81:bb:83:46:28:22:ae:8e:bc:
         d3:36:1b:7f:d1:65:0c:dd:20:05:d0:3e:47:84:dc:2c:62:97:
         57:fc:f3:6a:0c:57:69:f9:2d:31:f9:d6:8d:97:ec:cf:b8:78:
         c9:5a:df:c1:2b:47:2f:27:fb:94:c4:ac:93:0a:c0:66:47:9b:
         6e:ad:6a
-----BEGIN CERTIFICATE-----
MIIC6zCCAlOgAwIBAgIJAPvgt6YGJC6BMA0GCSqGSIb3DQEBCwUAMIGNMQswCQYD
VQQGEwJLUjEQMA4GA1UECAwHRGFlamVvbjEQMA4GA1UEBwwHRGFlamVvbjEOMAwG
A1UECgwFQnBzZWMxDjAMBgNVBAsMBUJwc2VjMREwDwYDVQQDDAhjb2RlZ2F0ZTEn
MCUGCSqGSIb3DQEJARYYY29kZWdhdGUyMDE4QGJwc2VjLmNvLmtyMB4XDTE4MDEy
OTA2NTU0MVoXDTI4MDEzMDA2NTU0MVowgY0xCzAJBgNVBAYTAktSMRAwDgYDVQQI
DAdEYWVqZW9uMRAwDgYDVQQHDAdEYWVqZW9uMQ4wDAYDVQQKDAVCcHNlYzEOMAwG
A1UECwwFQnBzZWMxETAPBgNVBAMMCGNvZGVnYXRlMScwJQYJKoZIhvcNAQkBFhhj
b2RlZ2F0ZTIwMThAYnBzZWMuY28ua3IwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJ
AoGBAcIL3AF+PKo8V5tA1Dni7NcPEsTX8nZHhMlaP926AJgbqc5bInreR7CnoKis
q6RUGrlcUva23j357AkMbDVkRbIb5Der4QIU0LSjmKlnQ7v3DIZGh/suySnwHW7a
stmH/gl5mtIgSicE8zBh2/nC4DszLwuhpEZkTIZKBs1YbUgLAgMBAAGjUDBOMB0G
A1UdDgQWBBTo9nbqclpx5lBH1o8LRKScJPvIIzAfBgNVHSMEGDAWgBTo9nbqclpx
5lBH1o8LRKScJPvIIzAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBCwUAA4GCAAAH
MppDeezmwk5S34q5LsV4y8Eb//1EbI/6ljalnrkFJ9NlOT4RGxm5dIytq6mEr1vx
JWliwB9wsz6TiWOgu4G7g0YoIq6OvNM2G3/RZQzdIAXQPkeE3Cxil1f882oMV2n5
LTH51o2X7M+4eMla38ErRy8n+5TErJMKwGZHm26tag==
-----END CERTIFICATE-----
```

Modulus값을 [factorization](http://www.factordb.com)해보니 p와 q가 구해졌고, 이를 이용해 p와 q의 값을 구하였으며, e는 65537로 주어졌다.

p와 q를 구했으니 private 인증서를 만들어보자.

```
parallels@ubuntu:/media/psf/Home/writeup/tools/rsatool$ python ./rsatool.py -p 17777324810733646969488445787976391269105128850805128551409042425916175469483806303918279424710789334026260880628723893508382860291986009694703181381742497  -q 17777324810733646969488445787976391269105128850805128551409042425916175469168770593916088768472336728042727873643069063316671869732507795155086000807594027 -e 65537 -o miro_priv.pem
Using (p, q) to initialise RSA instance

n =
1c20bdc017e3caa3c579b40d439e2ecd70f12c4d7f2764784c95a3fddba00981ba9ce5b227ade47b
0a7a0a8acaba4541ab95c52f6b6de3df9ec090c6c356445b21be437abe10214d0b4a398a96743bbf
70c864687fb2ec929f01d6edab2d987fe09799ad2204a2704f33061dbf9c2e03b332f0ba1a446644
c864a06cd586d480b

e = 65537 (0x10001)

d =
1a5c9d3a21a9be4b8b52aaeb1b8a6f36e039485a4167bc03fb52ebe58a270d81e65211fcccaf6f49
d9e1d36b8ce0d2f3df4a790a1e575990458b18a51082138265f3b909c7155c173def686e4387b98a
9fe6ec917551d8095783b21eb98798ffb1324957b6dbf944ce591c8099a1e2f4787a28804c995964
c059d02749dfe5b81

p =
1536dc0ecfbdc740b242c755760f77f86cac9feb35190721687bd702f159c6a8184e3f75c6f3786c
0832d301372ad3165d600adf637cda4efbc99adb6185bafa1

q =
1536dc0ecfbdc740b242c755760f77f86cac9feb35190721687bd702f159c5fe0d14ef4f564011aa
270cd326b5dcc69fb2bd76673357a9fa1399581abc231c82b

Saving PEM as miro_priv.pem
```

이 인증서를 이용해 pcap파일의 SSL패킷을 복호화 해주자!

```
-- Labytinth Game --
You have to go to the [G]
Input List : u(go up), d(go down), r(go right), l(go left)
[O][O][O][O][O][O][*][O][O][O]
[O][O][O][O][O][O][ ][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][O]
[O][ ][ ][O][ ][ ][ ][ ][ ][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][*][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][O]
[O][ ][ ][O][ ][ ][ ][ ][ ][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][*][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][O]
[O][ ][ ][O][ ][ ][ ][ ][ ][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][*][O]
[O][O][ ][ ][ ][O][O][O][ ][O]
[O][ ][ ][O][ ][ ][ ][ ][ ][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][ ][O][O][O][*][O]
[O][ ][ ][O][ ][ ][ ][ ][ ][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][ ][O][O][O][V][O]
[O][ ][ ][O][ ][ ][ ][ ][*][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][ ][O][O][O][V][O]
[O][ ][ ][O][ ][ ][ ][*][V][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][ ][O][O][O][V][O]
[O][ ][ ][O][ ][ ][*][V][V][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][ ][O][O][O][V][O]
[O][ ][ ][O][ ][*][V][V][V][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][ ][O][O][O][V][O]
[O][ ][ ][O][*][V][V][V][V][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
9de133535f4a9fe7de66372047d49865d7cdea654909f63a193842f36038d362
[O][O][O][O][O][O][V][O][O][O]
[O][O][O][O][O][O][V][V][V][O]
[O][O][ ][ ][*][O][O][O][V][O]
[O][ ][ ][O][V][V][V][V][V][O]
[O][ ][O][O][O][O][O][O][O][O]
[ ][ ][O][O][ ][ ][ ][ ][O][O]
[ ][O][O][O][ ][O][O][ ][O][O]
[ ][ ][ ][O][ ][O][O][ ][ ][O]
[O][O][ ][ ][ ][O][O][O][ ][ ]
[O][O][O][O][O][O][O][O][O][G]
Input : 
```

u과 l의 해당하는 인풋 값을 구할 수 있으며,  이를 주어진 python파일에 넣어주므로써 미로를 탈출 할 수 있다.

최종적으로 완성된 python파일은 다음과 같으며 즐겁게 미로를 탈출하면 Flag를 얻을 수 있다.

```python
from socket import *
from ssl import *
import time

def recv_until(s, string):
    result = ''
    while string not in result:
        result += s.recv(1)
    return result

client_socket=socket(AF_INET, SOCK_STREAM)
tls_client = wrap_socket(client_socket, ssl_version=PROTOCOL_TLSv1_2, cert_reqs=CERT_NONE)

print "[+] Connecting with server.."

tls_client.connect(('ch41l3ng3s.codegate.kr',443))

print "[+] Connect OK"

while 1:
    data = recv_until(tls_client, "Input : ")
    print data
    #message
    user_input = raw_input()
    
    if user_input == "u":
        #print "Sorry.. Not support function.."
        #exit()
        tls_client.send("9de133535f4a9fe7de66372047d49865d7cdea654909f63a193842f36038d362\n")
    elif user_input == "d": 
        tls_client.send("6423e47152f145ee5bd1c014fc916e1746d66e8f5796606fd85b9b22ad333101\n")
    elif user_input == "r":
        tls_client.send("34660cfdd38bb91960d799d90e89abe49c1978bad73c16c6ce239bc6e3714796\n")
    elif user_input == "l":
        tls_client.send("27692894751dba96ab78121842b9c74b6191fd8c838669a395f65f3db45c03e2\n")
        #print "Sorry.. Not support function.."
        #exit()
    else:
        print "Invalid input!"
        exit()    

client_socket.shutdown(SHUT_RDWR)
client_socket.close()
```



**C4n_y0u_d3crypt_th3_P4ck3t?**