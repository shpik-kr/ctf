# [PWN] Codeblue CTF 2017 - Secret Mailer Service

# Description

nc sms.tasks.ctf.codeblue.jp 6029

# Analysis

해당 문제는 3가지의 기능을 가지고 있다.

1. Add Letter
   *  Letter을 추가하는 기능
   *  최대 Letter 5개까지 추가 가능
   *  Letter의 문자열 최대 길이 256
2. Delete Letter
   *  인덱스 제한 0~4
   *  삭제 대상은 전부 0으로 초기화
3. Post Letter
   *  인덱스 제한 0~4
   *  필터 적용 메뉴에서 음수 체크 안함 ( **취약점 발생** )

우선 취약점이 발생하는 부분인 Post의 어셈 코드를 보자.

```
.text:08048B79                 mov     eax, [ebp+var_10]
.text:08048B7C                 mov     edx, off_804B048[eax*4]
.text:08048B83                 mov     eax, [ebp+var_C]
.text:08048B86                 shl     eax, 3
.text:08048B89                 mov     ecx, eax
.text:08048B8B                 shl     ecx, 5
.text:08048B8E                 add     ecx, eax
.text:08048B90                 mov     eax, [ebp+arg_0]
.text:08048B93                 add     eax, ecx
.text:08048B95                 mov     ecx, [eax+4]
.text:08048B98                 mov     eax, [ebp+var_C]
.text:08048B9B                 shl     eax, 3
.text:08048B9E                 mov     ebx, eax
.text:08048BA0                 shl     ebx, 5
.text:08048BA3                 add     ebx, eax
.text:08048BA5                 mov     eax, [ebp+arg_0]
.text:08048BA8                 add     eax, ebx
.text:08048BAA                 add     eax, 8
.text:08048BAD                 sub     esp, 4
.text:08048BB0                 push    ecx             ; n
.text:08048BB1                 push    eax             ; ptr
.text:08048BB2                 push    [ebp+s]         ; s
.text:08048BB5                 call    edx ; sub_8048742
```

필터 적용 메뉴에서 입력 받은 값만큼 + 또는 -하여 `call ebx`를 통해 실행한다.

여기서 주의할 점은 더블 포인터여야 실행이 가능하다는 것이다.

즉, 이를 이용해 해당 바이너리에 있는 .got.plt를 마음대로 사용이 가능하다.

공격 순서는 다음과 같다.

1. printf를 이용해 stack주소 Leak
2. memset을 이용해 파일 스트림을 덮고 printf을 통해 libc주소 Leak
3. gets함수를 통해 파일 스트림에 /bin/sh 삽입
4. system을 통해 /bin/sh실행

# Exploit

