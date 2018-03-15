# [Crypto] Nu1lCTF - baby_N1ES

## Description

N/A

## Analysis

문제의 파일에서 암호화 하는 루틴을 보면 다음과 같다.

```Python
def encrypt(self, plaintext):
        if (len(plaintext) % 16 != 0 or isinstance(plaintext, bytes) == False):
            raise Exception("plaintext must be a multiple of 16 in length")
        res = ''
        for i in range(len(plaintext) / 16):
            block = plaintext[i * 16:(i + 1) * 16]
            L = block[:8]
            R = block[8:]
            for round_cnt in range(32):
                L, R = R, (round_add(L, self.Kn[round_cnt]))
            L, R = R, L
            res += L + R
        return res
```

**L,R = R,L**의 로직을 보면 **<u>Feistel 구조</u>**인 것을 확인할 수 있다.([Wiki](https://en.wikipedia.org/wiki/Feistel_cipher))

Feistel 구조는 decrypt할 때 Key의 값을 거꾸로 넣어주기만 하여 encrypt 로직에 넣으면 복호화가 된다.

또한 문제에서 아래와 같이 암호화 로직을 사용하여 얻은 플래그 값이 주어졌다.

```python
from N1ES import N1ES
import base64
key = "wxy191iss00000000000cute"
n1es = N1ES(key)
flag = "N1CTF{*****************************************}"
cipher = n1es.encrypt(flag)
print base64.b64encode(cipher)  # HRlgC2ReHW1/WRk2DikfNBo1dl1XZBJrRR9qECMNOjNHDktBJSxcI1hZIz07YjVx
```

## Exploit

```python
def decrypt(self, plaintext):
        if (len(plaintext) % 16 != 0 or isinstance(plaintext, bytes) == False):
            raise Exception("plaintext must be a multiple of 16 in length")
        res = ''
        for i in range(len(plaintext) / 16):
            block = plaintext[i * 16:(i + 1) * 16]
            L = block[:8]
            R = block[8:]
            for round_cnt in range(31,-1,-1):
                L, R = R, (round_add(L, self.Kn[round_cnt]))
            L, R = R, L
            res += L + R
        return res
```

Key만 거꾸로 변경해주면 decrypt함수를 만들어 줄 수 있다.

이를 주어진 문제의 N1ES 클래스에 넣어주고 아래의 코드를 실행하면 플래그를 얻을 수 있다.

```python
from N1ES import N1ES
cipher = 'HRlgC2ReHW1/WRk2DikfNBo1dl1XZBJrRR9qECMNOjNHDktBJSxcI1hZIz07YjVx'.decode('base64')
key = "wxy191iss00000000000cute"
n1es = N1ES(key)
print n1es.decrypt(cipher)

# N1CTF{F3istel_n3tw0rk_c4n_b3_ea5i1y_s0lv3d_/--/}
```



**N1CTF{F3istel_n3tw0rk_c4n_b3_ea5i1y_s0lv3d_/--/}**