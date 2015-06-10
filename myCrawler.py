import urllib2
import urllib
from HTMLParser import HTMLParser
import time
import pickle
import codecs
import os

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.urllist = list()

    def handle_starttag(self, tag, attrs):
        # Only parse the 'img' tag.
        #needed = False
        if tag == 'img':
            #print 'encounter an image!'
            attrs_dict = dict(attrs)
            if 'width' in attrs_dict and 'height' in attrs_dict:
                #print 'yes'
                if attrs_dict['width'] == '280' and attrs_dict['height'] == '280':
                    imgurl = attrs_dict['data-src']
                    self.urllist.append(imgurl)

class HTMLParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dishList = list()
        self.dishDict = dict()
        self.record = 0

    def handle_starttag(self, tag, attrs):
        # Only parse the 'a' tag.
        if tag == 'a':
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict:
                dish = attrs_dict['href']
                if dish.find('/recipe/') == 0:
                    dishId = dish[8:-1]
                    self.dishList.append(dishId)
                    self.record += 1

    def handle_endtag(self, tag):
        if tag == 'a' and self.record:
            self.record -= 1

    def handle_data(self, data):
        if self.record:
            #print data
            self.dishDict[self.dishList[-1]] = data

                
def writeImg(imgurl, cnt, dirname):
    try:
        urllib.urlretrieve(imgurl, dirname + '%s.jpg' % (cnt))
        print 'retrieved'
    except Exception:
        return

def setProxy(proxyIP, proxyPort):
    print 'using proxy: %s:%s' % (proxyIP, proxyPort)
    proxy_handler = urllib2.ProxyHandler({"http" : proxyIP + ':' + proxyPort})
    opener = urllib2.build_opener(proxy_handler)
    return opener

def downloadDish(dishId, proxyList, proxyIndStart):
    print dishId
    dic = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
    "referer": "http://www.xiachufang.com/recipe/"}
    
    opener = setProxy(proxyList[proxyIndStart][1], proxyList[proxyIndStart][2])
    proxyIndStart = (proxyIndStart + 1) % 50
    urllib2.install_opener(opener)
    i = 1
    imgUrlList = list()
    while (True):
        time.sleep(2)
        url = 'http://www.xiachufang.com/recipe/%s/dishes/?page=%s' % (dishId, i)
        while(True):
            try:
                request = urllib2.Request(url, None, dic)
                response = urllib2.urlopen(request, timeout = 10)
                html = response.read().decode('utf-8')
                break
            except Exception, e:
                print e
                opener = setProxy(proxyList[proxyIndStart][1], proxyList[proxyIndStart][2])
                proxyIndStart = (proxyIndStart + 1) % 50
                urllib2.install_opener(opener)
        parser = MyHTMLParser()
        parser.feed(html)
        imgUrlList += parser.urllist
        print len(imgUrlList)
        if len(parser.urllist) <= 0 or len(imgUrlList) > 500:
            break
        i += 1
    if len(imgUrlList) >= 500:
        dirname = ('./%s/' % (dishId)).encode('ascii')
        print 'downloading %s\n' % dirname
        try:
            os.makedirs(dirname)
        except WindowsError:
            return
        for i in range(500):
            if (i % 18 == 0):
                time.sleep(2)
            writeImg(imgUrlList[i], i, dirname)

def getDishList(proxyIP, proxyIndStart):
    dic = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',\
    "referer": "http://www.xiachufang.com/"}
    opener = setProxy(proxyList[proxyIndStart][1], proxyList[proxyIndStart][2])
    proxyIndStart = (proxyIndStart + 1) % 50
    urllib2.install_opener(opener)
    dishList = list()
    dishDict = dict()
    i = 1
    while(True):
        time.sleep(1)
        url = 'http://www.xiachufang.com/category/5263/?page=%s' % (i)
        while(True):
            try:
                request = urllib2.Request(url, None, dic)
                response = urllib2.urlopen(request, timeout = 10)
                html = response.read().decode('utf-8')
                break
            except Exception, e:
                print e
                opener = setProxy(proxyList[proxyIndStart][1], proxyList[proxyIndStart][2])
                proxyIndStart = (proxyIndStart + 1) % 50
                urllib2.install_opener(opener)
        parser = HTMLParser2()
        parser.feed(html)
        dishList += parser.dishList
        dishDict.update(parser.dishDict)
        i += 1
        print len(dishList)
        if i > 50:
            break
    with codecs.open('dishDict4.txt', 'w+', 'utf-8') as f:
        for key in dishDict:
            f.write('%s %s' % (key, dishDict[key]))
            f.write('\r\n')
    with open('dishDict4.dp', 'wb+') as f:
        pickle.dump(dishDict, f)

def main():
    with open('dishDict4.dp', 'rb') as f:
        dishDict = pickle.load(f)
    with open('proxy.dp', 'rb') as f:
        proxyList = pickle.load(f)
    dishIdList = dishDict.keys()
    for i in range(0, len(dishIdList)):
        print 'NO.', i
        proxyInd = i % 50
        downloadDish(dishIdList[i], proxyList, proxyInd)


if __name__ == '__main__':
    main()
    #with open('proxy.dp', 'rb') as f:
    #    proxyList = pickle.load(f)
    #getDishList(proxyList, 0)