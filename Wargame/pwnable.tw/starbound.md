# [pwnable.tw] starbound

# Description

>  Let's play starbound together!
>
>  *multi-player features are disabled.*
>
>  `nc chall.pwnable.tw 10202`
>
>  [starbound](https://pwnable.tw/static/chall/starbound)

# Analysis

```assembly
0x0804a605 <+0>:	push   ebp
0x0804a606 <+1>:	mov    ebp,esp
0x0804a608 <+3>:	push   ebx
0x0804a609 <+4>:	and    esp,0xfffffff0
0x0804a60c <+7>:	sub    esp,0x110
0x0804a612 <+13>:	call   0x80496e8 <init>
0x0804a617 <+18>:	lea    ebx,[esp+0x10]
0x0804a61b <+22>:	mov    DWORD PTR [esp],0x3c
0x0804a622 <+29>:	call   0x8048af0 <alarm@plt>
0x0804a627 <+34>:	call   DWORD PTR ds:0x805817c
0x0804a62d <+40>:	mov    DWORD PTR [esp+0x4],0x100
0x0804a635 <+48>:	mov    DWORD PTR [esp],ebx
0x0804a638 <+51>:	call   0x8049919 <readn>
0x0804a63d <+56>:	test   eax,eax
0x0804a63f <+58>:	je     0x804a666 <main+97>
0x0804a641 <+60>:	mov    DWORD PTR [esp+0x8],0xa
0x0804a649 <+68>:	mov    DWORD PTR [esp+0x4],0x0
0x0804a651 <+76>:	mov    DWORD PTR [esp],ebx
0x0804a654 <+79>:	call   0x8048a90 <strtol@plt>
0x0804a659 <+84>:	test   eax,eax
0x0804a65b <+86>:	je     0x804a666 <main+97>
0x0804a65d <+88>:	call   DWORD PTR [eax*4+0x8058154]
0x0804a664 <+95>:	jmp    0x804a61b <main+22>
0x0804a666 <+97>:	call   0x8049c03 <do_bye>
0x0804a66b <+102>:	mov    eax,0x0
0x0804a670 <+107>:	mov    ebx,DWORD PTR [ebp-0x4]
0x0804a673 <+110>:	leave
0x0804a674 <+111>:	ret
```

`call   DWORD PTR [eax*4+0x8058154]`을 통해 함수를 호출하는데, `readn`함수에서는 인덱스를 검사하지 않는다.

```c
ssize_t __cdecl readn(void *buf, size_t nbytes)
{
  ssize_t result; // eax

  result = read(0, buf, nbytes); // <-- Vulnerability
  if ( result <= 0 )	
    exit(0);
  return result;
}
```

즉 -의 함수를 실행시킬 수 있다.

