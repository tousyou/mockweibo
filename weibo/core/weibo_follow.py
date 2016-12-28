import time
import bs4
import re
import json

from logger import logger


class WeiboFollow(object):
    def __init__(self, session, uid):
        super(WeiboFollow, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid
    def follow(self,uid):
        return self.__follow(uid,"followed")
    def unfollow(self,uid):
        return self.__follow(uid,"unfollow")
    def __follow(self,uid,followtype):
        ret = 0
        data = {
                "uid": str(uid),
                "objectid": "",
                "f": "1",
                "extra": "",
                "refer_sort": "",
                "refer_flag": "",
                "location": "",
                "oid": "",
                "wforce": "1",
                "nogroup": "false",
                "fnick": "",
                "refer_lflag": "",
                "_t": "0",
                }
        self.session.headers["Referer"] = self.Referer
        #print "data: ",data
        try:
            resp = self.session.post(
                    "http://weibo.com/aj/f/%s?ajwvr=6&__rnd=%d" % (followtype,int( time.time() * 1000)),
                    data=data
            )
            #print "resp.text: ",resp.text
            hjson = json.loads(resp.text)
            #print "code: ",hjson['code']
            if hjson['code'] == "100000":
                ret = 1
                logger.info("weibo %s [%s] success" % (followtype,str(uid)))
        except Exception as e:
            logger.debug(e)
            logger.info( "weibo %s [%s] failed" % (followtype,str(uid)))
        return ret

    def myfollow(self):
        url = "http://weibo.com/p/100505%s/myfollow#place" % self.uid
        (midlist,pages) = self.__getfollow(url,"pl.relation.myFollow.index")
        count = int(pages)
        for i in range(2,count+1):
            next = "http://weibo.com/p/100505%s/myfollow?t=1&cfs=&Pl_Official_RelationMyfollow__96_page=%d#Pl_Official_RelationMyfollow__96" % (self.uid,i)
            (nextlist,index) = self.__getfollow(next,"pl.relation.myFollow.index")
            midlist.extend(nextlist)
        return midlist

    def followme(self):
        url = "http://weibo.com/p/100505%s/myfollow?relate=fans&pids=plc_main&ajaxpagelet=1&ajaxpagelet_v6=1" % (self.uid)
        (uidlist,pages) = self.__getfollow(url,"pl.relation.fans.index")
        count = int(pages)
        for i in range(2,count+1):
            next = "http://weibo.com/p/100505%s/myfollow?pids=Pl_Official_RelationFans__91&cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__91_page=%d&ajaxpagelet=1&ajaxpagelet_v6=1" % (self.uid,i)
            (nextlist, index) = self.__getfollow(next,"pl.relation.fans.index")
            uidlist.extend(nextlist)
        return uidlist

    def __getfollow(self,url,follow):
        midlist = []
        count = 0
        try:
            resp = self.session.get(url)
            #print "resp.content: ", resp.content
            #print "resp.code: ", resp.status_code
            html_script = r'<script>(.*?)</script>'  
            m_script = re.findall(html_script,resp.content,re.S|re.M)
            
            for script in m_script:
                if follow in script:
                    a = script.replace('\\"','"')
                    b = a.replace('\\/','/')
                    soup = bs4.BeautifulSoup( b, "html.parser" )
                    tags = soup.find_all(attrs={"action-type": "webim.conversation"})
                    #print "tag: ",len(tags)
                    for tag in tags:
                        mid = tag.get("action-data")
                        col = re.split('=|&',mid)
                        midlist.append(col[1])

                    pages = soup.find_all("a",class_="page S_txt1")
                    #print "pages: ",len(pages)
                    for page in pages:
                        count = page.text.strip()
        except Exception as e:
            logger.debug(e)
        return (midlist,count)
