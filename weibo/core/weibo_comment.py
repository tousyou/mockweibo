import time
import re
import json

from logger import logger


class WeiboComment(object):
    def __init__(self, session, uid):
        super(WeiboComment, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid

    def comment(self,mid,comment=""):
        comment_id = ""
        data = {
            "act": "post",
            "mid": str(mid),
            "uid": str(self.uid),
            "forward": "0",
            "isroot": "0",
            "content": comment,
            "location": "page_100505_single_weibo",
            "module": "bcommlist",
            "page_module_id": "",
            "tranandcomm": "1",
            "pdetail": "0",
            "_t": 0,
        }
        self.session.headers["Referer"] = self.Referer
        #print "data: ",data
        try:
            resp = self.session.post( "http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=%d" % int(time.time() * 1000),data=data)
            #print "resp.text: ",resp.text
            hjson = json.loads(resp.text)
            #print "code: ",hjson['code']
            if hjson['code'] == "100000":
                a = resp.text.replace('\\"','"')
                pattern = re.compile("comment_id=\"(\d*)\" class=")
                res = pattern.search(a).groups()
                comment_id = res[0]
                logger.info("weibo [%s] comment success, comment_id [%s]" %
                    (str(mid),comment_id))
        except Exception as e:
            logger.debug(e)
            logger.info("weibo [%s] comment failed")
        return comment_id

