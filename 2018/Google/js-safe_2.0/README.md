# Google CTF 2018 Quals - js safe 2

## Introduce

이 문제는 javascript로 구성된 anti debugging가 걸려있는 문제였다.

개인적으로 최근에 풀어본 문제중에 가장 재밌었고, 또한 신비한 문제였다. (구글의 기술력은 세계 최고다..)

문제를 풀면서 느낀건  Javascript를 구현해 Anti Debugging적용이 가능하며, 사람의 눈으로 보이기에 같은 문자라도 컴퓨터가 보기엔 다른 문자들을 조심해야 한다는 것이다.

사실 후자의 상황 때문에 약간 삽질을 많이 했었으며, 이보다는 이 문제에서 Anti Debugging이 어떻게 작동하며 이를 어떻게 우회하는지에 대한 설명을 중점으로 할 것이다.

서문이 너무 길었으니 바로 문제 분석으로 들어가보자.

## Description

### 초기 분석

문제는 html페이지 하나가 주어졌다.

이를 실행해면 가운데 정육각형이 뱅글뱅글 돌며 위에 열쇠 모양의 Input칸이 있다.

이 칸에 우리는 FLAG를 넣고, 이를 javascript를 통해 정상적인 값이 맞는지 확인을 하는 문제이다.

Chrome + Text Editor(e.g. sublime text)를 이용해 분석을 시작한다.

입력 칸에 Flag를 넣으면 작동하는 코드는 다음과 같다.

```js
function open_safe() {
  keyhole.disabled = true;
  password = /^CTF{([0-9a-zA-Z_@!?-]+)}$/.exec(keyhole.value);
  if (!password || !x(password[1])) return document.body.className = 'denied';
  document.body.className = 'granted';
  password = Array.from(password[1]).map(c => c.charCodeAt());
  encrypted = JSON.parse(localStorage.content || '');
  content.value = encrypted.map((c,i) => c ^ password[i % password.length]).map(String.fromCharCode).join('')
}
function save() {
  plaintext = Array.from(content.value).map(c => c.charCodeAt());
  localStorage.content = JSON.stringify(plaintext.map((c,i) => c ^ password[i % password.length]));
}
```

위의 password 정규식에 의해 `CTF{~~~~}`의 형태를 입력해야 한다.

그 후에 `x(password[1])` 에 의해 아래의 함수가 실행될 것이다.

```javascript
function x(х){ord=Function.prototype.call.bind(''.charCodeAt);chr=String.fromCharCode;str=String;function h(s){for(i=0;i!=s.length;i++){a=((typeof a=='undefined'?1:a)+ord(str(s[i])))%65521;b=((typeof b=='undefined'?0:b)+a)%65521}return chr(b>>8)+chr(b&0xFF)+chr(a>>8)+chr(a&0xFF)}function c(a,b,c){for(i=0;i!=a.length;i++)c=(c||'')+chr(ord(str(a[i]))^ord(str(b[i%b.length])));return c}for(a=0;a!=1000;a++)debugger;x=h(str(x));source=/Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;source.toString=function(){return c(source,x)};try{console.log('debug',source);with(source)return eval('eval(c(source,x))')}catch(e){}}
```

이제 간단하게 흐름을 알았으니 개발자 도구를 살포시 킨 후 CTF{shpik}을 넣어주자.

그러면 우리의 개발자 도구는 해당 코드에서 멈출 것이다.

```javascript
for(a=0;a!=1000;a++)debugger;
```

1000번을 다음을 눌러줘야 할 것 같으니, console창에 `a=999`를 입력해줘서 넘어가주자.

for문을 넘어가면 바로 `x=h(str(x));` 코드를 만날 것인데, h 함수는 간단하므로 한번 보고 넘어가자.

```javascript
function h(s) {
    for (i = 0; i != s.length; i++) {
        a = ((typeof a == 'undefined' ? 1 : a) + ord(str(s[i]))) % 65521;
        b = ((typeof b == 'undefined' ? 0 : b) + a) % 65521
    }
    return chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
}
```

입력값에 대하여 4byte의 문자열을 리턴해준다.

### 삽질 (1st edition)

뭔가 코드가 이상하다는걸 느꼇다.

코드를 수정하지 않고 디버깅을 하다보면 `x=h(str(x));` 를 수행하는데 우리가 입력한 입력 값 `shpik` 이 아니라 `x()` 함수의 코드가 들어가는 걸 볼 수있다.

이게 뭔 상황이냐...

sublime text에서 `function x(х)` 함수 이름 `x` 를 클릭했을 때 아차 싶었다.

함수이름의 x와 인자 х는 다른 값이다.

> x :  https://en.wikipedia.org/wiki/X
>
> х :  https://en.wiktionary.org/wiki/%D1%85

함수 이름은 알파벳 x, 변수는 키릴(?)문자 х이다.

이 둘을 주의하며 다시 분석을 재개하자.

### 다시 분석 시작

`x=h(str(x));` 의 값은 함수 x()에 대한 결과 값이므로 항상 같은 값이 나오는 구문이다.

이를 계산하면 x는 다음과 같은 값을 가진다.

```
\x82\x1e\x0a\x9a
```

이제 디버깅을 이어서 하다보면 브라우저가 죽는 괴현상을 발견할 것이다.

### 삽질 (2nd edition)

대체 왜 죽는지 원인을 몰라서 '이 문제 뭐야 !!!!!' 하고 하고있었으나, 이를 해결한 후  '좋은 문제네'라는 태세 변환이 일어난 살집이었다.

우선 코드를 보자.

```javascript
source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
source.toString = function() {
    return c(source, x)
}
;
try {
    console.log('debug', source);
    with (source)
        return eval('eval(c(source,x))')
} catch (e) {}
```

우선 첫번째 로 주의해야 할 점은 source는 `/Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/` 의 값으로 선언하는데, source의 Type은 string이 아니라 object이다.

```
> source = /Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/;
/Ӈ#7ùª9¨M¤À.áÔ¥6¦¨¹.ÿÓÂ.Ö£JºÓ¹WþÊmãÖÚG¤¢dÈ9&òªћ#³­1᧨/
> typeof source
'object'
```

그리고 source의 toString을 c() 함수로 정의하였다.

그 후 디버깅 모드, 즉 개발자 도구가 켜져 있으면 console.log를 실행하는데 source는 string이 아니다.

그래서 c 함수의 인자로 들어간 타입은 `(object, string)`이 된다.

c 함수를 보자.

```javascript
function c(a, b, c) {
	for (i=0;i!=a.length;i++){
    	c = (c || '') + chr(ord(str(a[i])) ^ ord(str(b[i % b.length])));
    }
    console.log(c); 
    return c
}
```

브라우저가 죽는 이유가 바로 이 함수에 있다.

for문에서 a의 length를 입력받는데 a는 object 타입이라서 length 속성이 없어 undefined가 되고 그로 인하여 무한루프를 돌게 되는 것이다!

이를 해결하기 위해 console.log를 없애거나 c함수의 a.length의 값 대신에 100과 같은 상수를 넣어주면 된다.

### 다시 분석

무한 루프를 해결 했다면 다음의 코드를 만날 것이다.

```javascript
with (source)
	return eval('eval(c(source,x))')
```

with문에 의해 eval안에 들어간 source는 string 타입을 가지고있다.

```
> with(source)
... typeof source
'string'
```

그로 인해 에러가 발생하지 않고 `c(source,x)` 가 실행되고 다음과 같은 값을 얻는다.

```
х==c('¢×&Ê´cÊ¯¬$¶³´}ÍÈ´T©Ð8Í³Í|Ô÷aÈÐÝ&¨þJ',h(х));
```

아 이제야 Anti Debugging을 우회하여 진짜 문제가 나온 것 같다.

이제부터는 h와 c의 함수를 구현하여 brute force공격을 하며 차분히 기다리면 될 것 같다.



## Exploit

h 함수의 경우 항상 4바이트가 나오고,  c함수는 이 4바이트를 기준으로 연산을 하기때문에 결국 4byte brute force 문제가 되는 것이다.

하지만 경우의 수가 너무 크므로 h 함수를 다시 보았고, 정규식 문자열 중 아스키 값이 가장 작은 !를 c에서 연산에 사용되는 문자열의 길이(68byte)만큼 넣어 h함수를 실행시키고, 이를 통해 알 수 있는 a,b의 값을 최소 값으로 설정하였다.

그리고 정규식 문자열 중 가장 큰 z를 같은 방식을 사용하여 a를 얻고 이 값을 최대로 설정하였다.(b의 경우 mod연산을 하므로, 무의미 한 것 같아 최대값을 65521로 설정)

```python
a_min = 2245
a_max = 8297
b_min = 11965

charset = string.ascii_letters+string.digits+'_@!?-'

def c(a,b):
	c = ''
	for i in range(len(a)):
		p = chr(ord(str(a[i])) ^ ord(str(b[i % len(b)])))
		if p not in charset:
			return False
		c = c + p
	return c

cipher = '\xa2\xd7&\x81\xca\xb4c\xca\xaf\xac$\xb6\xb3\xb4}\xcd\xc8\xb4T\x97\xa9\xd08\xcd\xb3\xcd|\xd4\x9c\xf7a\xc8\xd0\xdd&\x9b\xa8\xfeJ'

for a in range(a_min,a_max):
	for b in range(b_min,64930):
		h = chr(b >> 8) + chr(b & 0xFF) + chr(a >> 8) + chr(a & 0xFF)
		p = c(cipher,h)
		if p:
			print(a,b,p)
```

작성된 코드는 다음과 같으며, 이제 기다리면 문자열들이 후루룩 나오고, 그 중에서 플래그를 얻을 수 있었다.



FLAG : CTF{\_N3x7-v3R51ON-h45-AnTI-4NTi-ant1-D3bUg\_}