# [WEB] Hackcon 2018 - Web5

## Description

Add host entry as "34.201.73.166 mypictureblog"



## Analysis&Exploit

/etc/hosts에 `34.201.73.166 mypictureblog`를 추가한다.

페이지를 요청하면 div.js파일을 로드하는 것을 확인할 수 있다.

div.js는 상당히 코드가 더러운데, 이 코드는 다음과 같은 수행을 한다.

```Js
(function() {
document.getElementById('divimage').innerHTML ='<img src="images/pic02.jpg" alt="" />';var backup="uggcf://f3.nznmbanjf.pbz/unpxvz18jroyriry2/onpxhc/uvqqra.gkg";
})
```

"uggcf://f3.nznmbanjf.pbz/unpxvz18jroyriry2/onpxhc/uvqqra.gkg"의 값 뭔가 이상한데 시저암호일거같은 느낌이 굉장히 많이 들어서 돌려보니 주소를 얻을 수 있었다.

https://s3.amazonaws.com/hackim18weblevel2/backup/hidden.txt의 값이 나오며 들어가보면 base64가 나오며 풀어주게되면 한번더 base64로 암호화된 값이 나오게 되고, 다시 풀어주면 주소를 하나 더 얻을 수 있다.

```
osehun:~/writeup/tools$ echo "aHR0cHM6Ly9zMTBlMGF6NTNmLmV4ZWN1dGUtYXBpLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tL3Byb2QvaGFja2ltZmxhZ3dlYmxldmVsMg==" | base64 -D
https://s10e0az53f.execute-api.us-east-1.amazonaws.com/prod/hackimflagweblevel2
```

해당 사이트에 요청하면 auth값이 없다고 한다.

```
osehun:~/writeup/tools$ curl https://s10e0az53f.execute-api.us-east-1.amazonaws.com/prod/hackimflagweblevel2
"{'msg':'[Missing param in querystring: auth]'}"
```

이 값은 mypictureblog 사이트 메인에 존재한다.

```
auth:bf0e14593e3e9c9392a4fe360326ab6f
```

이를 인자로써 페이지를 요청하게되면 플래그를 얻을 수 있다.

```
osehun:~/writeup/tools$ curl https://s10e0az53f.execute-api.us-east-1.amazonaws.com/prod/hackimflagweblevel2?auth=bf0e14593e3e9c9392a4fe360326ab6f
"{'flag':'LaMBda-oR-NoT-tO-LAmBdA'}"
```



**'LaMBda-oR-NoT-tO-LAmBdA'**