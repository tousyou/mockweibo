import time
import re
import json

from logger import logger

class WeiboRepost(object):
    def __init__(self, session, uid):
        super(WeiboRepost, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid

    def repost_weibo(self,mid,comment=""):
        repost_id = ""
        data = {
            "pic_src": "",
            "pic_id": "",
            "appkey": "",
            "mid": str(mid),
            "style_type": "1",
            "mark": "",
            "reason": comment,
            "location": "v6_content_home",
            "pdetail": "",
            "module": "",
            "page_module_id": "",
            "refer_sort": "",
            "rank": "0",
            "rankid": "",
            "group_source": "group_all",
            "rid": "",
            "_t": 0,
        }
        self.session.headers["Referer"] = self.Referer
        #print "data: ",data
        try:
            resp = self.session.post(
                    "http://www.weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=%s&__rnd=%d"
                    % (self.uid,int( time.time() * 1000)),
                    data=data
            )
            #print "resp.text: ",resp.text
            hjson = json.loads(resp.text)
            #print "code: ",hjson['code']
            if hjson['code'] == "100000":
                a = resp.text.replace('\\"','"')
                pattern = re.compile("mid=\"(\d*)\" isForward=")
                res = pattern.search(a).groups()
                repost_id = res[0]
                logger.info("weibo [%s] repost success, repost_id [%s]" %
                    (str(mid),repost_id))
        except Exception as e:
            logger.debug(e)
            logger.info( "weibo [%s] repost failed" % str(mid) )
        return repost_id

