# PHP Vulnerability

###### Author : shpik (@TenDollar)

## Introduce

이 문서는 취약한 함수 및 PHP Trick에 대한 연구 및 자료 수집입니다.

>  PHP Trick : 코드를 간결하게 만들고 성능을 향상시키는 방법중 하나이며 다른뜻으로는 Trick뜻 그대로 속임수이다.

하지만 여기서는 해킹 관점에서의 취약함 함수와 PHP Trick을 주로 다룰 것이다.

해당 내용은 지속적으로 추가될 예정이다.



## Vulnerable Function

#### int strpos ( string $haystack, mixed $needle [, int $offset ] )

* haystack 문자열에서 needle이 처음 나타나는 인덱스를 반환하고, needle을 발견하지 못할경우 False를 반환한다.
* 취약점을 설명하기 위한 예제를 보자.

>  ```php
>  # This is vulnerable function strpos's example code.
>  # author : shpik.korea@gmail.com
>  $filename = $_GET['f'];
>  if(strpos($filename,'../')!=false){
>    die('Do not hacking.');
>  }
>  include_once($filename);
>  ```
>
>  위 소스는 f 파라미터에서 ../을 발견하면 include_once를 수행하지 않고 die하는 코드이다.
>
>  딱보면 LFI를 방지하기 위해 만든거 같은데 strpos는 찾은 문자열의 `index`를 리턴한다.
>
>  즉, 찾는 문자열이 맨 처음에 나오면 strpos의 리턴값이 0이 되고 ==(loose comparison)에 의해 false와의 비교값이 false가 되어 die하지 않고 include_once를 수행하게 된다.



#### string system ( string $command [, int &$return_var ] )

* shell에서 command의 명령어를 수행한다.
* 해당 함수에서는 주로 `command injection`, `remote code execution` 이 발생하게 된다.
* 또한 `command injection` 을 이용하여 해당함수를 사용해 `remote code execution`을 발생시킬 수 있다.
* 다만 해당 함수는 워낙 많이 사용되어 필터링 되는 경우가 많다.
* 다음의 함수들로 우회해보자.
  * ``
  * passthru()
  * exec()
  * shell_exec()




#### mixed parse_url ( string $url [, int $component ] )

*  간단하게 URL을 파싱해준다.
*  반환 값 : schema, host, port, user, pass, path, query, fragment
*  해당 함수는 파싱 과정에서 취약점이 존재한다. ( SSRF 유발 가능 )





## Trick

#### == (Loose Comparison), === (Strict Comparison)

* PHP 코딩 중에 가장 흔히 일어날 수 있는 취약점 중 하나이다.
* ===의 경우 타입까지 정확히 일치해야 True를 반환한다.
  * e.g. var_dump(False===0) = False
* ==의 경우 타입은 중요하게 생각하지 않는다.
  * e.g. var_dump(False==0) = True
* ==와 ===의 Comparison Table을 한번 참고해보는 것이 좋다.




#### Parameter underscore(_) bypass

*  parameter이름에 _가 들어가고 필터링 된다면 이를 우회할 수 있다.

>  ```php
>  if(preg_match('_',$_SERVER['QUERY_STRING'])){
>    die('Do not hacking!');
>  }
>  if(isset($_GET['__flag__'])){
>    echo $flag;
>  }
>  ```
>
>  위 소스는 \_\_flag\_\_파라미터가 존재하면 flag를 주는 간단한 소스인데, $_SERVER['QUERY_STRING']을 통해 파라미터 부분에 _(underscore)가 들어가면 die를 통해 프로그램을 죽인다.

*  파라미터의 이름에 한해서 underscore는 다음의 문자로 우회가 가능하다.
   *  . (dot)
   *  [ (open square bracket) - 현재 미작동 ( > php7.0)
   *  %20 (space)
   *  %80 ~ %9F - 현재 미작동 ( > php7.0 )




#### Type casting

*  PHP에서 Integer 타입 캐스팅 부분을 이용한 Trick이 존재한다.

>  ```php
>  if((int)$_GET['number']>100 && $_GET['number']<1){
>    echo $flag;
>  }
>  ```
>
>  위의 if 조건문을 보면 말도 안된다.
>
>  하지만 Integer 타입 캐스팅이 되면 index 0번부터 string이 존재하기 전까지의 integer만 가져온다.
>
>  ( e.g. (int)'153B19' = 153 )
>
>  이를 이용하여 number에 101e-1을 넣을 경우 (int)'101e-1'이 되어 101이 리턴되어 참이되고 두번째는 101e-1이 연산되어 참이 나와 flag를 출력하게 된다.

*  하지만 캐스팅 관련 부분은 보기도 드물 뿐더러 코딩 상의 실수이기 때문에 찾기는 힘들겠지만, 가끔 Wargame이나 CTF에서 나오기도 한다.




#### MD5, SHA1 and other hash algorithm

*  PHP에서 Hash비교 시 Loose Comaprison을 사용하면 발생할 수 있는 Trick and Vulnerability이다.

>  ```php
>  if( md5($_GET['h1'])==md5($_GET['h2']) && h1 != h2 ){
>    echo $flag;
>  }
>  ```
>
>  md5한 값이 같으면서 스트링의 값이 다른 2개의 값을 구하면 flag를 출력해준다.

*  해당 취약점은 php의 loose comparison에 의해 발생하는 취약점으로 0e[0-9]+의 형태를 지닌 값을 php은 0으로 취급해 버린다.
*  즉 `00e0 = 0e0 = 000e0 …` 과 같이 같은 값으로 처리가 된다.

>  ```php
>  var_dump('0e462097431906509019562988736854'=='0'); # true
>  var_dump('0e462097431906509019562988736854'=='0eabcdef'); # false
>  var_dump('00e46209743190650901956298873685'=='0e462097431906509019562988736854'); # true
>  ```
>
>  위와 같이 간략하게 설명이 가능하다.

