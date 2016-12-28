import time
import re
import json

from weibo_message import WeiboMessage
from config import add_watermark, watermark_url, watermark_nike
from config import max_images
from logger import logger

if max_images < 0 or max_images > 9:
    max_images = 9

class WeiboPost(object):
    def __init__(self, session, uid):
        super(WeiboPost, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid

    def post_weibo(self,content):
        msg = WeiboMessage(content)
        return self.send_weibo(msg)

    def send_weibo(self, weibo):
        mid = ""
        if not isinstance(weibo, WeiboMessage):
            #raise ValueError( 'weibo must WeiboMessage class type' )
            logger.debug( 'weibo must WeiboMessage class type' )
            return mid
        if weibo.is_empty:
            return mid

        pids = ''
        if weibo.has_image:
            pids = self.upload_images(images)
        data = weibo.get_send_data(pids)
        self.session.headers["Referer"] = self.Referer
        
        try:
            resp = self.session.post(
                "http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d" % int( time.time() * 1000),
                data=data
            )
            #print "resp.text: ",resp.text
            hjson = json.loads(resp.text)
            #print "code: ",hjson['code']
            if hjson['code'] == "100000":
                a = resp.text.replace('\\"','"')
                pattern = re.compile("mid=\"(\d*)\"  action-type=")
                res = pattern.search(a).groups()
                mid = res[0]
                logger.info("weibo [%s] send success, mid [%s]" %
                        (str(weibo),mid))
        except Exception as e:
            logger.debug(e)
            logger.info( "weibo [%s] send failed" % str(weibo) )
        return mid        
        
    def upload_images(self, images):
        pids = ""
        if len(images) > max_images:
            images = images[0: max_images]
        for image in images:
            pid = self.upload_image_stream(image)
            if pid:
                pids += " " + pid
            time.sleep(10)
        return pids.strip()


    def upload_image_stream(self, image_url):
        if add_watermark:
            url = "http://picupload.service.weibo.com/interface/pic_upload.php?app=miniblog&data=1&url=" \
                + watermark_url + "&markpos=1&logo=1&nick="\
                + watermark_nike + \
                "&marks=1&mime=image/jpeg&ct=0.5079312645830214"

        else:
            url = "http://picupload.service.weibo.com/interface/pic_upload.php?rotate=0&app=miniblog&s=json&mime=image/jpeg&data=1&wm="

        # self.http.headers["Content-Type"] = "application/octet-stream"
        image_name = image_url
        try:
            f = self.http.get( image_name, timeout=30 )
            img = f.content
            resp = self.session.post( url, data=img )
            upload_json = re.search( '{.*}}', resp.text ).group(0)
            result = json.loads( upload_json )
            code = result["code"]
            if code == "A00006":
                pid = result["data"]["pics"]["pic_1"]["pid"]
                return pid
        except Exception as e:
            logger.info("image upload failed: %s" % image_name)
        return None
    
