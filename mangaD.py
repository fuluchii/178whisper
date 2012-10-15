#coding=utf-8

#At first the script is using gevent to create a multithread downloader.But I don't think it will be so efficient ,also the installation of gevent is too hateful so I changed it to original threadpoll.Amount of workers is 8,change it if you like.Make sure you have beautifulsoup4 installed, it is the only external module this script used.Any problem,use '-h' command.

#import gevent
#from gevent import monkey;monkey.patch_all()  
#from gevent.pool import Pool
#from gevent.queue import JoinableQueue
import Queue
import threading
import BeautifulSoup
import re
import time
import os
import socket
from optparse import OptionParser
import urllib
ROOT_URL = "http://imgfast.manhua.178.com/"

class WorkGreenlet(threading.Thread):
    def __init__(self,tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks

    def run(self):
        t = self.tasks.get()
        t()
        self.tasks.task_done()

class Spider:
    def __init__(self,max_worker):
        self.tasks = Queue.Queue()


    def add_tasks(self,url,path):
        def crawl():
            print url
            while True:
                try:
                    page = urllib.urlopen(url)
                    content = re.findall("var pages.*?;",page.read())
                    print len(content)
                    if len(content) > 0:
                        break
                except Exception,e:
                    print url+"raise an error"
                    print e[0]
                    continue
            content = re.findall("\[.*?\]",content[0])[0]
            img_list = re.split(",",content[1:-1])
            for index,img in enumerate(img_list):
                decode_url = img[1:-1].decode('unicode_escape').replace("\/","/")
                while True:
                    try:
                        image  = urllib.urlopen(ROOT_URL+decode_url.encode('utf-8'))
                        print(decode_url+"start")
                        suffix = re.split("\.",decode_url)
                        suffix = suffix[-1]
                        image_data = image.read()
                        with open(os.path.join(path,"img"+('%0*d' % (3, index))+"."+suffix),'wb') as f:
                            f.write(image_data)
                        break
                    except Exception,e:
                        print decode_url+" raise an error."
                        print e[0]
                        continue
            print path+" done"
        self.tasks.put(lambda:crawl())

class Manager:
    def __init__(self,num_thread):
        self.spider = Spider(10)
        self.num_thread = num_thread

    def get_chapter_list(self,url):
        while True:
            try:
                first_chapter = urllib.urlopen(url)
                soup = BeautifulSoup.BeautifulSoup(first_chapter,'lxml')
                break
            except Exception,e:
                continue
        if not soup('a',{'id':'next_chapter'}):
             next_chapter_url = soup('a',{'id':'next_chapter'})[0]['href']
        return nil

    def get_chapter_urls(self,root_url,first_chapter_url):
        url = root_url + first_chapter_url
        while True:
            try:
                print url
                chapter = urllib.urlopen(url)
                soup = BeautifulSoup.BeautifulSoup(chapter)
            except Exception,e:
                print chapter.read()
            next_chapter_link = soup('a',{'id':'next_chapter'})
            print next_chapter_link
            yield next_chapter_link
            url = root_url + next_chapter_link[0]['href']
    def set_url(self,root_url,first_url):
        self.root_url = root_url
        self.first_url = first_url

    def set_path(self,root_path):
        self.root_path = root_path



    def start(self,d_count=1):
        download_count = d_count
        count = 1
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)
        if not os.path.exists(os.path.join(self.root_path,self.first_url)):
            os.mkdir(os.path.join(self.root_path,self.first_url))
        self.spider.add_tasks(self.root_url+self.first_url,os.path.join(self.root_path,self.first_url))
        for index,url in enumerate(self.get_chapter_urls(self.root_url,self.first_url)):
            if(download_count>0 and count>=download_count):
                break
            if not url:
                print "empty"
                break
            if not os.path.exists(os.path.join(self.root_path,url[0].string)):
                os.mkdir(os.path.join(self.root_path,url[0].string))
            self.spider.add_tasks(self.root_url+url[0]['href'],os.path.join(self.root_path,url[0].string))
            count = count+1
        st = time.time()
        print st
        for i in range(self.num_thread):
            t = WorkGreenlet(self.spider.tasks)
    	    t.setDaemon(True)
    	    t.start()
        self.spider.tasks.join()
        print time.time()-st


def get_downloader(num):
    return Manager(num)

# usage = "usage: %prog [options] args.for example, you want to download 2 chapters from www.178.com/mh/sthqgmn/16001.shtml :the command will be like this: python xx.py -r http://178.com/mh/sthqgmn/ -c 16001.shtml -n 2 -p xxxxxx"
# parser = OptionParser(usage=usage)
# parser.add_option('-r','--rootURL',dest="root",
#         help="manga's root address.In fact, it will always be http://www.178.com/mh/xxxxx/")
# parser.add_option('-c','--chapter',dest="chapter",
#         help="start download from FIRST CHAPTER.for example,16001.shtml")
# parser.add_option('-n','--number',dest='count',
#         type='int',help="[option]count of manga.default=1")
# parser.add_option('-p','--path',dest='path',
#         help="store manga in FILEPATH")

# (opts,args) = parser.parse_args()
# if  opts.path is None or opts.root is None or opts.path is None:
#     parser.print_help()
#     exit()
# self.root_path = opts.path
# socket.setdefaulttimeout(10)
# try:
#     urllib.urlopen(opts.root+opts.chapter)
# except Exception,e:
#     print 'Wrong url!!!!'
#     exit()
# manager = get_downloader(7)

# if opts.count:
# manager.start("http://178.manhua.com/test","1.shtml")
# else:
    # manager.start(opts.root,opts.chapter)