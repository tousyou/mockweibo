import time
import re
import json

from logger import logger


class WeiboLike(object):
    def __init__(self, session, uid):
        super(WeiboLike, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid

    def like_weibo(self,mid):
        ret = 0
        data = {
            "location": "page_100505_single_weibo",
            "version": "mini",
            "qid": "heart",
            "mid": str(mid),
            "loc": "profile",
        }
        self.session.headers["Referer"] = self.Referer
        #print "data: ",data
        try:
            resp = self.session.post(
                    "http://weibo.com/aj/v6/like/add?ajwvr=6",
                    data=data
            )
            #print "resp.text: ",resp.text
            hjson = json.loads(resp.text)
            #print "code: ",hjson['code']
            if hjson['code'] == "100000":
                logger.info("weibo [%s] like success" % str(mid))
                ret = 1
        except Exception as e:
            logger.debug(e)
            logger.info("weibo [%s] like failed" % str(mid))
        return ret

    def like_object(self,mid):
        ret = 0
        data = {
            "location": "page_100206_single_weibo",
            "object_id": str(mid),
            "object_type": "comment",
        }
        self.session.headers["Referer"] = self.Referer
        #print "data: ",data
        try:
            resp = self.session.post(
                    "http://weibo.com/aj/v6/like/objectlike?ajwvr=6",
                    data=data
            )
            #print "resp.text: ",resp.text
            hjson = json.loads(resp.text)
            #print "code: ",hjson['code']
            if hjson['code'] == "100000":
                logger.info("weibo [%s] like success" % str(mid))
                ret = 1
        except Exception as e:
            logger.debug(e)
            logger.info("weibo [%s] like failed" % str(mid))
        return ret

