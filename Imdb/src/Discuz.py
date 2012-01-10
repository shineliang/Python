#-*-coding:utf-8-*-
'''
Created on Jan 9, 2012

@author: shineliang
'''

from urllib import urlencode
import cookielib, urllib2, urllib
import os, sys
import re
from xml.dom.minidom import parse, parseString
import getpass
import time
from Queue import Queue
import threading

class Discuz:
    def __init__(self, uid, pwd, **param):
        self.username = uid
        self.password = pwd
        self.para = param
        self.regex = {
            'loginreg':'<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'postreg':'<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>'
        }
        self.opener = None
        self.request = None
        self.islogin = False
        self.donecount = 0
        self.__login()
        self.threadcount = 1    #总线程数
        self.count = 0
        self.totalcount = 1   #发帖量
    def __login(self):
        try:
#            formhash = re.search(self.regex['loginreg'], loginPage)
#            formhash = formhash.group(1)
#            print formhash
            print 'start login......'
            cookiejar = cookielib.CookieJar()
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
            self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7')]
            urllib2.install_opener(self.opener)
            values = {
                         'username':self.username,
                         'password':self.password,
                         'loginsubmit':'true'
                     }
            data = urllib.urlencode(values)
            self.request = urllib2.Request(self.para['loginsubmiturl'], data)
            rq = self.opener.open(self.request)
 
            print rq.read().decode('gb2312')
            print 'login success......'
            self.islogin = True
 
        except Exception , e:
            print 'Loggin Error:%s' % e
            
    def Post(self, subject, wysiwyg, content):
        threads = []
        for i in range(self.threadcount):
            t = threading.Thread(target=self.__postTopic, kwargs={'_subject':subject, '_wysiwyg':wysiwyg, '_body':content})
            threads.append(t)
        for i in range(self.threadcount):
            threads[i].start()
        lst = threading.enumerate()
        for i in range(self.threadcount):
            threads[i].join()
        print 'done'
    def __postTopic(self, **para):
        if not self.islogin:
            print 'please login......'
            return
        while self.count < self.totalcount:
            try:
                print 'current count %d:' % self.count
                print 'current thread name %s' % (threading.currentThread().getName())
                self.request = urllib2.Request(self.para['posturl'])
                rq = self.opener.open(self.request)
                data = rq.read()
                formhash = re.search(self.regex['postreg'], data)
                formhash = formhash.group(1)
                postdata = {
#                    'addtags':'+可用标签',
#                    'checkbox':'0',
                    'formhash':formhash,
#                    'iconid':'',
                    'message':para['_body'],
                    'subject':para['_subject'],
#                    'tags':'',
#                    'updateswfattach' : '0',
                    'wysiwyg' : para['_wysiwyg']
                }
                self.request = urllib2.Request(self.para['postsubmiturl'], urllib.urlencode(postdata))
                self.opener.open(self.request)
                self.donecount += 1
                print '%d done.....' % self.donecount
            except Exception, e:
                print e
            if para.has_key('sleep'):
                time.sleep(float(para['sleep']))
            self.count += 1
 
if __name__ == '__main__':
    name = raw_input('username:').strip()
    password = getpass.getpass('password:').strip()
    
    dz = Discuz(name, password,
    loginsubmiturl='http://www.5d5d.com/member.php?mod=logging&action=login',
    posturl='http://www.5d5d.com/forum.php?mod=post&action=newthread&fid=4&extra=&topicsubmit=yes',
    postsubmiturl='http://www.5d5d.com/forum.php?mod=post&action=newthread&fid=4&extra=&topicsubmit=yes',
    sleep='1'
    )
    subject = u'''网友提供Firefox+扩展 15秒网上快速预定火车票教程'''.encode('gb2312')
    content = u'''http://www.cnbeta.com/articles/168179.htm'''.encode('gb2312')
 
    dz.Post(subject, '1', content)
