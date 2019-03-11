# UTCTF 2019

Problem is good, but Server is ... :)

I attend ctf as '**Mashiro**'.

**Mashiro** #23 7000pts

And, I wrote writeups about interesting things.

## Solved Problem

- [basics] re - Rev/strings
- Super Secure Authentication - Rev/Java/Crackme
- HabbyDabby's Secret Stash - Web/LFI/Guessing
- Premium Flag Checker - Web/Wasm/Crackme
- Baby Pwn - Pwn/Shellcode/Stack Overflow
- BabyEcho - Pwn/FSB
- Jendy's - Pwn/FastbinDup/UAF/FSB
- [basics] crypto - Crypto/Decoding
- Jacobi's Chance Encryption - Crypto/Jacobi Symbols
- [basics] forensics - Forensics/Strings
- Low Sodium Bagel - Forensics/Stegano


## writeup

### Premium Flag Checker (1400) - Solver 8

##### Description

```
Are you feeling lucky? Type a wild guess into this website, and it will tell you whether or not you guessed the flag correctly. Be careful though, the website knows when something fishy is going on.

http://web.overflow.fail
```

##### Exploit

페이지에 접속하면 전형적인 Web Crackme의 형태를 띄고있습니다.

페이지에 존재하는 js파일을 읽어보면 Wasm관련 javascript인 것을 알 수 있고, 페이지 접속 시 Wasm파일(`verifyFlag.wasm`)이 로드되는 것을 볼 수 있습니다.

wabt를 build하여 wasm2c 바이너리를 이용해 wasm파일을 디컴파일하였습니다.

그 중 \_verify\_flag함수의 일부분입니다.

```c
...
static u32 _verify_flag(u32 p0) {
  u32 l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0, 
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0, 
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0, 
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0, 
      l33 = 0, l34 = 0, l35 = 0, l36 = 0, l37 = 0, l38 = 0, l39 = 0, l40 = 0, 
      l41 = 0, l42 = 0, l43 = 0, l44 = 0, l45 = 0, l46 = 0, l47 = 0, l48 = 0, 
      l49 = 0, l50 = 0, l51 = 0, l52 = 0, l53 = 0, l54 = 0, l55 = 0, l56 = 0, 
      l57 = 0, l58 = 0, l59 = 0, l60 = 0, l61 = 0, l62 = 0, l63 = 0, l64 = 0, 
      l65 = 0, l66 = 0, l67 = 0, l68 = 0, l69 = 0, l70 = 0, l71 = 0, l72 = 0, 
      l73 = 0, l74 = 0, l75 = 0, l76 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1, i2;
  u64 j1;
  i0 = g14;
  l76 = i0;
  i0 = g14;
  i1 = 160u;
  i0 += i1;
  g14 = i0;
  i0 = g14;
  i1 = g15;
  i0 = (u32)((s32)i0 >= (s32)i1);
  if (i0) {
    i0 = 160u;
    (*Z_envZ_abortStackOverflowZ_vi)(i0);
  }
  ...
  i0 = f29(i0);
  ...
}
...
```

쭉 보다보면 f29함수를 호출하는데,  다음은 f29함수의 일부분입니다.

```c
static u32 f29(u32 p0) {
  u32 l1 = 0, l2 = 0, l3 = 0, l4 = 0, l5 = 0, l6 = 0, l7 = 0, l8 = 0, 
      l9 = 0, l10 = 0, l11 = 0, l12 = 0, l13 = 0, l14 = 0, l15 = 0, l16 = 0, 
      l17 = 0, l18 = 0, l19 = 0, l20 = 0, l21 = 0, l22 = 0, l23 = 0, l24 = 0, 
      l25 = 0, l26 = 0, l27 = 0, l28 = 0, l29 = 0, l30 = 0, l31 = 0, l32 = 0;
  FUNC_PROLOGUE;
  u32 i0, i1;
  i0 = g14;
  l32 = i0;
  i0 = p0;
  l9 = i0;
  i0 = l9;
  i1 = 3u; 
  i0 &= i1;
  l20 = i0;
  i0 = l20;
  ...
  if (i0) {
    i0 = l3;  
    l1 = i0;  
    L7: 
      i0 = l1;
      i0 = i32_load(Z_envZ_memory, (u64)(i0)); 
      l10 = i0;
      i0 = l10;
      i1 = 4278124287u; 
      i0 += i1; 
      l11 = i0; 
      i0 = l10;
      i1 = 2155905152u;
      i0 &= i1; 
      l12 = i0; 
      i0 = l12;
      i1 = 2155905152u;
      i0 ^= i1;
      ...
  }
  ...
}
```

분석하다 보니 **0xfefefeff**와 **0x80808080**를 보고 f29는 strlen함수라고 예측하였습니다.

다시 \_verify\_flag로 돌아와 이어서 보면 아래와 같이 입력받은 길의 검증하는 로직이 보입니다.

```c
i0 = f29(i0);
l8 = i0;
i0 = l8;
l56 = i0;
i0 = l56;
l9 = i0;
i0 = l9;
i1 = 1u;  
i0 <<= (i1 & 31);
l10 = i0;
i0 = l56;
l11 = i0;
i0 = l56;
l13 = i0;
i0 = l11;
i1 = l13;
i0 *= i1;
l14 = i0;
i0 = l10;  
i1 = l14;
i0 += i1;
l15 = i0;
i0 = l15;
i1 = 1443u;
i0 = i0 != i1;
```

위 로직은 간단히 아래와 같이 나타낼 수 있으며, 이는 입력 받은 문자열이 37이어야 한다는 것을 보여줍니다.

```python
l = strlen(input)
if (l**2) + (l<<1) != 1443:
	exit(1)
```

다음의 코드를 보면, 이번에는 입력 값의 0~6째 자리를 확인하는 부분입니다.

우리는 플래그 양식이 utflag{blahblah}임 을 알고 있으니, 간단하게 패스해줍니다.

~~(Wasm2c로 생성된 코드 뭔가 더럽다.)~~

```c
i0 = 1324u;
l67 = i0; 
i0 = 0u;
l73 = i0; 
L2:   
  i0 = l73; 
  l17 = i0;
  i0 = l17;
  i1 = 7u;  
  i0 = (u32)((s32)i0 < (s32)i1);  
  l18 = i0;
  i0 = l18;
  i0 = !(i0); 
  if (i0) { 
    goto B3;  // break
  }
  i0 = l67;
  l19 = i0; 
  i0 = l73;
  l20 = i0; 
  i0 = l19;
  i1 = l20;
  i0 += i1; 
  l21 = i0;
  i0 = l21;
  i0 = i32_load8_s(Z_envZ_memory, (u64)(i0));	// 'utflag{'
  l22 = i0;
  i0 = l22; 
  i1 = 24u;
  i0 <<= (i1 & 31);
  i1 = 24u;
  i0 = (u32)((s32)i0 >> (i1 & 31));
  l24 = i0;
  i0 = l12;
  l25 = i0;
  i0 = l73;
  l26 = i0;
  i0 = l25;
  i1 = l26;
  i0 += i1;
  l27 = i0;
  i0 = l27;
  i0 = i32_load8_s(Z_envZ_memory, (u64)(i0));
  l28 = i0;
  i0 = l28;
  i1 = 24u;
  i0 <<= (i1 & 31);
  i1 = 24u;
  i0 = (u32)((s32)i0 >> (i1 & 31));
  l29 = i0;
  i0 = l24;
  i1 = l29;
  i0 = i0 != i1;
  l30 = i0;
  i0 = l30;
  if (i0) {
    i0 = 6u;
    l75 = i0;
    goto B3;
  }
  i0 = l73;
  l31 = i0;
  i0 = l31;
  i1 = 1u;
  i0 += i1;
  l32 = i0;
  i0 = l32;
  l73 = i0;
  goto L2;
  B3:;
i0 = l75;
i1 = 6u;
i0 = i0 == i1;	// current index check
```

다음의 코드를 보면 뭔가 load하고 store하는 것을 볼 수 있습니다.

```c
i0 = l74;
i1 = 1024u;
j1 = i64_load(Z_envZ_memory, (u64)(i1));
i64_store(Z_envZ_memory, (u64)(i0), j1);
...
i0 = l74;
i1 = 112u;
i0 += i1;
i1 = 1024u;
i2 = 112u;
i1 += i2;
i1 = i32_load(Z_envZ_memory, (u64)(i1));
i32_store(Z_envZ_memory, (u64)(i0), i1);
```

이 코드는 data segment의 값을 i0에 옮기는 코드이며, 총 120byte를 옮깁니다.

```c
static const u8 data_segment_data_0[] = {
  0x63, 0x00, 0x00, 0x00, 0x71, 0x00, 0x00, 0x00, 0x6e, 0x00, 0x00, 0x00, 
  0x67, 0x00, 0x00, 0x00, 0x72, 0x00, 0x00, 0x00, 0x7f, 0x00, 0x00, 0x00, 
  0x74, 0x00, 0x00, 0x00, 0x73, 0x00, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 
  0x6b, 0x00, 0x00, 0x00, 0x72, 0x00, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 
  0x61, 0x00, 0x00, 0x00, 0x41, 0x00, 0x00, 0x00, 0x6a, 0x00, 0x00, 0x00, 
  0x73, 0x00, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 0x70, 0x00, 0x00, 0x00, 
  0x69, 0x00, 0x00, 0x00, 0x6e, 0x00, 0x00, 0x00, 0x6a, 0x00, 0x00, 0x00, 
  0x7f, 0x00, 0x00, 0x00, 0x5f, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 
  0x38, 0x00, 0x00, 0x00, 0x2d, 0x00, 0x00, 0x00, 0x34, 0x00, 0x00, 0x00, 
  0x6a, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 
  0x03, 0x00, 0x00, 0x00, 0x48, 0x05, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 
  0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x80, 0x04, 0x00, 0x00, 0x7b, 0x20, 0x72, 0x65, 0x74, 0x75, 0x72, 0x6e, 
  0x20, 0x77, 0x69, 0x6e, 0x64, 0x6f, 0x77, 0x5b, 0x53, 0x74, 0x72, 0x69, 
  0x6e, 0x67, 0x2e, 0x66, 0x72, 0x6f, 0x6d, 0x43, 0x68, 0x61, 0x72, 0x43, 
  0x6f, 0x64, 0x65, 0x28, 0x24, 0x30, 0x29, 0x5d, 0x3b, 0x20, 0x7d, 0x00, 
  0x75, 0x74, 0x66, 0x6c, 0x61, 0x67, 0x7b, 
};
```

data segment를 옮긴 다음에 진행되는 코드는 너무 길어서 여기에는 담지 않겠습니다. [Source](./verifyFlag.c#L695)를 참조해주세요!

L7의 코드를 간략하게 다음과 같이 표현할 수 있고, 플래그를 얻을 수 있습니다.

```python
l74 = [99, 113, 110, 103, 114, 127, 116, 115, 95, 107, 114, 95, 97, 65, 106, 115, 95, 112, 105, 110, 106, 127, 95, 100, 56, 45, 52, 106, 100]

l3 = 7
l1 = 4

q= []
for i in range(len(l74)):
	if (l3 + i)%4 == 0:
		tmp = l74[i] ^ 30
	else:
		tmp = l74[i]
	q.append(tmp&0xFF)

print 'utflag{'+bytearray(q)+'}'
```

**FLAG :** utflag{congrats_ur_a_js_ninja_d834jd}

