import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from core.weibo_login import wblogin
from core.weibo_follow import WeiboFollow
from core.weibo_like import WeiboLike
from core.weibo_post import WeiboPost
from core.weibo_repost import WeiboRepost
from core.weibo_comment import WeiboComment
from core.logger import logger

def index(request):
    return HttpResponse("Hello,Weibo!")
def login(uid):
    (session,login_uid) = wblogin(uid)
    if login_uid == uid:
        logger.info('uid [%s] login success!' % uid)
        return (session,True)
    else:
        logger.info('uid [%s] login failed!' % uid)
        return (session,False)
def getdict(request):
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return request.POST
    
def follow(request,uid,custid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    wbfollow = WeiboFollow(session,uid)
    if wbfollow.follow(custid) == 1:
        return HttpResponse("uid [%s] follow custid[%s] success" % (uid,custid))
    else:
        return HttpResponse("uid [%s] follow custid[%s] failed" % (uid,custid))

def unfollow(request,uid,custid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    wbfollow = WeiboFollow(session,uid)
    if wbfollow.unfollow(custid) == 1:
        return HttpResponse("uid [%s] unfollow custid[%s] success" % (uid,custid))
    else:
        return HttpResponse("uid [%s] unfollow custid[%s] failed" % (uid,custid))

def followlist(request,uid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    wbfollow = WeiboFollow(session,uid)
    uidlist = wbfollow.myfollow()
    return HttpResponse(json.dumps(uidlist))

def followme(request,uid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    wbfollow = WeiboFollow(session,uid)
    uidlist = wbfollow.followme()
    return HttpResponse(json.dumps(uidlist))

def comment(request,uid,mid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    dic = getdict(request)
    if dic.has_key('text'):
        text = dic['text']
        wbcomment = WeiboComment(session,uid)
        commentid = wbcomment.comment(mid,text)
        return HttpResponse(commentid)
    else:
        return HttpResponse('no text parameter')

def like(request,uid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    dic = getdict(request)
    wblike = WeiboLike(session,uid)
    rsp = ''
    if dic.has_key('mid'):
        mid = dic['mid']
        if mid != '':
            rsp = rsp + 'like mid [%s]' % mid 
            if wblike.like_weibo(mid) == 1:
                rsp = rsp + 'success \r\n'
            else:
                rsp = rsp + 'failed \r\n'
    if dic.has_key('obj'):
        obj = dic['obj']
        if obj != '':
            rsp = rsp + 'like obj [%s]' % obj
            if wblike.like_object(obj) == 1:
                rsp = rsp + 'success \r\n'
            else:
                rsp = rsp + 'failed \r\n'
    if rsp != '':
        return HttpResponse(rsp)
    else:
        return HttpResponse("please set mid or obj")
def post(request,uid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    dic = getdict(request)
    if dic.has_key('text'):
        text = dic['text']
        print "text,",text
        wbpost = WeiboPost(session,uid)
        mid = wbpost.post_weibo(text)
        return HttpResponse(mid)
    else:
        return HttpResponse('no text parameter')

def repost(request,uid):
    (session,ok) = login(uid)
    if ok == False:
        return HttpResponse('not login')
    dic = getdict(request)
    if dic.has_key('mid'):
        mid = dic['mid']
    text = ''
    if dic.has_key('text'):
        text = dic['text']
    wbRepost = WeiboRepost(session,uid)
    if mid != '':
        postid = wbRepost.repost_weibo(mid,text)
        return HttpResponse(postid)
    else:
        return HttpResponse('no mid parameter')
