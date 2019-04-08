# Midnight Sun Quals

I participated in the competition with the Harekaze.

Then, we finished 23rd with 3217 pts.

And I got 1094 pts.

I really enjoyed being with Harekaze. (Thanks to, @st98)

## Solved Problem

- marcodowno - web / xss
- marcozuckerbergo - web / xss
- EZDSA - crypto / Euler's theorem / DSA
- gissa2 - pwn / seccomp bypass

## Writeup

### marcodowno

It is reflected xss problem on markdown environment.

So, i use image tag's description in markdown.

It is possible html injeciton, so i can alert(1).

Here is my payload :

```
Payload : ![d" onerror="alert(1);](http://shpik.kr)
```

**FLAG :** midnight{wh0_n33ds_libs_wh3n_U_g0t_reg3x?}

### marcozuckerbergo (First Blood)

It is reflected xss problem on markdown environment, too.

This problem is allow drawing graph.

So, i used grath's LR, then i can alert. (Thanks to, @Safflower)

```
Payload : graph LR\na(Stop<img src=x% onerror=alert`1`>)
```

**FLAG :** midnight{1_gu3zz_7rust1ng_l1bs_d1dnt_w0rk_3ither:(}

### EZDSA

Here is problem source :

```python
from hashlib import sha1
from Crypto import Random
from flag import FLAG


class PrivateSigningKey:

    def __init__(self):
        self.gen = 0x44120dc98545c6d3d81bfc7898983e7b7f6ac8e08d3943af0be7f5d52264abb3775a905e003151ed0631376165b65c8ef72d0b6880da7e4b5e7b833377bb50fde65846426a5bfdc182673b6b2504ebfe0d6bca36338b3a3be334689c1afb17869baeb2b0380351b61555df31f0cda3445bba4023be72a494588d640a9da7bd16L
        self.q = 0x926c99d24bd4d5b47adb75bd9933de8be5932f4bL
        self.p = 0x80000000000001cda6f403d8a752a4e7976173ebfcd2acf69a29f4bada1ca3178b56131c2c1f00cf7875a2e7c497b10fea66b26436e40b7b73952081319e26603810a558f871d6d256fddbec5933b77fa7d1d0d75267dcae1f24ea7cc57b3a30f8ea09310772440f016c13e08b56b1196a687d6a5e5de864068f3fd936a361c5L
        self.key = int(FLAG.encode("hex"), 16)

    def sign(self, m):

        def bytes_to_long(b):
            return long(b.encode("hex"), 16)

        h = bytes_to_long(sha1(m).digest())
        u = bytes_to_long(Random.new().read(20))
        assert(bytes_to_long(m) % (self.q - 1) != 0)

        k = pow(self.gen, u * bytes_to_long(m), self.q)
        r = pow(self.gen, k, self.p) % self.q  
        s = pow(k, self.q - 2, self.q) * (h + self.key * r) % self.q
        assert(s != 0)

        return r, s
```

`assert(bytes_to_long(m) % (self.q - 1) != 0)` is not allow euler's theorem.

But, It is not secure.
$$
gen^{u*m} =  k \bmod q\\
if\ u=0\bmod 2\ and\ m = (q-1)/2,\ then,\\
k = gen^{(u/2)(q-1)} = (gen^{(q-1)})^{(u/2)} = 1^{(u/2)} = 1 \bmod q
$$
So, we make k set 1.

In conclusion k is 1,  then we can calculate key.

```python

from hashlib import sha1
# m = (p-1)/2 = 417967266380781845811177255381354966430691989413
gen = 0x44120dc98545c6d3d81bfc7898983e7b7f6ac8e08d3943af0be7f5d52264abb3775a905e003151ed0631376165b65c8ef72d0b6880da7e4b5e7b833377bb50fde65846426a5bfdc182673b6b2504ebfe0d6bca36338b3a3be334689c1afb17869baeb2b0380351b61555df31f0cda3445bba4023be72a494588d640a9da7bd16L
q = 0x926c99d24bd4d5b47adb75bd9933de8be5932f4bL
p = 0x80000000000001cda6f403d8a752a4e7976173ebfcd2acf69a29f4bada1ca3178b56131c2c1f00cf7875a2e7c497b10fea66b26436e40b7b73952081319e26603810a558f871d6d256fddbec5933b77fa7d1d0d75267dcae1f24ea7cc57b3a30f8ea09310772440f016c13e08b56b1196a687d6a5e5de864068f3fd936a361c5L
k = 1
def bytes_to_long(b):
    return long(b.encode("hex"), 16)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
'''
s = pow(k, self.q - 2, self.q) * (h + self.key * r) % self.q
'''
s = 629758878500372559472644038362239654961033814558L
m = 'I6L\xe9%\xeaj\xda=m\xba\xde\xcc\x99\xefE\xf2\xc9\x97\xa5'
h = bytes_to_long(sha1(m).digest())
r = 698847418084580852997663919979623019513778951409L

mi= modinv(r,q)
key = ((s-h)*mi)%q
print hex(key)[2:-1].decode('hex')
```

**FLAG :** midnight{th4t_w4s_e4sy_eh?}