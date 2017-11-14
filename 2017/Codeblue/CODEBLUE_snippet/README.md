# [MISC] Codeblue CTF 2017 - CODE BLUE Snippet

# Description

We developed the awesome snippet service. Have a try!
[http://cbs.tasks.ctf.codeblue.jp](http://cbs.tasks.ctf.codeblue.jp/)

Source Code(Old): [src.zip](https://static.score.ctf.codeblue.jp/attachments/src.zip-eb72057a135bb91ea9788a244f3980d6d23b2ce2d3126f32300ac31d7210723f)

Updated on 11/10 at 6:30(UTC+0900): 
This problem had an extremely easier unintended way.
We decided to fix it and open the previous flag in order to do justice to all of the teams:
CBCTF{plz fix PHP Bug #72374} ( this is not a valid flag now )

Source Code (Updated): [src-updated.zip](https://static.score.ctf.codeblue.jp/attachments/src-updated.zip-b61e2a1d4bc1af1b2cf7892d4dbd8eaf03fa563e8a3f30926f313f12c6d42467)

# Analysis

페이지의 기능은 3가지이다.

1. 파일 생성
2. 파일 Export
3. 파일 Import

소스코드를 보면 플래그를 얻는 조건은 다음과 같다.

```php
if (file_exists($USER_DIR . '/is_admin')) {
  exit($FLAG);
}
?>
```

업로드 폴더에 is_admin이 들어가면 플래그를 얻을 수 있다.

우선 is_admin을 업로드 시도해보았지만 소스코드상 is_admin파일은 생성이 불가능하였다.

```php
$filename = basename(strtolower($_POST['filename']));
if ($filename == 'is_admin' || preg_match('/\./', $filename)) {
  die('Hello hacker :)');
}
```

그래서 이번 문제는 export와 import를 이용한 문제라 확신하였다.

파일 Export를 담당하는 파일인 export.php을 보자.

```php
<?php
include('config.php');

$tmpfile = tempnam('/tmp', 'cbs');

if (preg_match('/\.|\\\\|^\//', $_GET['dir']) === 1) {
  die('hello hacker :(');
}

$zip = new ZipArchive();
$zip->open($tmpfile, ZipArchive::CREATE);
$options = array('remove_path' => $_GET['dir']);

$dir = trim($_GET['dirname(path)'], '/');
$zip->addGlob($dir . '/*', 0, $options);

$zip->close();

$hmac = hash_hmac('sha256', file_get_contents($tmpfile), $MY_SECRET);
header("Content-Disposition: attachment; filename='${hmac}.zip'");
readfile($tmpfile);

unlink($tmpfile);
```

dir 파라미터로 받은 파일을 통채로 압축하고 이름은 압축파일에 따른 sha256-hmac으로 해쉬화한다.

이번엔 Import를 담당하는 import.php를 보자.

```php
<?php
include('config.php');

$tmpfile = $_FILES['file']['tmp_name'];
$hmac = hash_hmac('sha256', file_get_contents($tmpfile), $MY_SECRET);
if ($_FILES['file']['name'] !== "${hmac}.zip") {
  die('hello hacker :)');
}

$zip = new ZipArchive();
$zip->open($tmpfile);
$zip->extractTo($USER_DIR);

$zip->close();

header('Location: /');
```

업로드한 파일의 sha256-hmac과 파일이름이 같아야 성공적으로 import한다.

어딜봐도 취약점은 없어보이지만 취약점이 나올만한 부분은 export.php의 코드이다.

```php
$options = array('remove_path' => $_GET['dir']);
$zip->addGlob($dir . '/*', 0, $options);
```

빠르게 remove_path에 대한 취약점이 존재하나 찾아보았고, https://bugs.php.net/bug.php?id=72374 사이트를 발견하였다.

addGlob의 옵션 중 add_path와 remove_path에 발생하며, 파일이름의 첫 번째 문자가 제거되는 버그가 존재한다.

# Exploit 

첫번째 자리를 더미값으로 주고 그 뒤에 is_admin을 이름으로 파일을 생성한다.

`ais_admin`

그후 export할때 dir의 경로 뒤에 /을 하나 더 추가한다.

`export.php?dir=89e9794cc3f67dfb012729fb35481a54/`

그러면 압축 파일이 하나 다운로드 되는데 열어보면 `ais_admin`에서 첫번째 자리가 짤린 `is_admin`이 압축되어 있음을 알 수있다.

그러니 다운받은 파일을 그대로 업로드하면 디렉토리에 is_admin이 생성되게 되어 Flag를 얻을 수 있다.



**CBCTF{sorry-we-had-a-pitty-bug;;}**

