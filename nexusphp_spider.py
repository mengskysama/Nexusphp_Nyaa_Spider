#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from BeautifulSoup import BeautifulSoup

import config
from http_request import http_request

class nexusphp_spider:

    def __init__(self, cookie = config.NEXUSCOOKIE, nexus_url = config.NEXUS_URL, nexus_page_url = config.NEXUS_PAGE_URL,  nexus_download_url = config.NEXUS_DOWNLOAD_URL):
        self.http = http_request(cookie)
        self.nexus_url = nexus_url
        self.nexus_page_url = nexus_url + nexus_page_url
        self.nexus_download_url = nexus_url + nexus_download_url
        self.current_page = 0

    def login(self, user, passwd):
        '''
        Toooooo much trouble
        '''

    def download_torrent(self, id) :
        get_url = self.nexus_download_url % id
        resp, ret = self.http.get(get_url)
        if not resp['status'] == 200:
            print '下载种子文件 id=%s 失败:请求失败' % id
            return False
        else:
            print '下载种子文件 id=%s 成功' % id
        f = file(config.TORRENT_DIR + id + '.torrent', 'wb')
        f.write(ret)
        f.close()
        return True

    def mv_faild_torrent(self, id):
        old_file = config.TORRENT_DIR + id + '.torrent'
        new_file = config.TORRENT_DIR + id + '_faild.torrent'
        try:
            os.rename(old_file, new_file)
        except:
            return

    def ret_page_torrents_id(self, page = 0):
        #获取页面种子id
        torrents = []
        get_url = self.nexus_page_url % str(page)
        print get_url
        #get_url = 'http://u2.dmhy.org/torrents.php'
        resp, ret = self.http.get(get_url)
        if not resp['status'] == 200:
            print '获取种子列表 page=%d 失败:请求失败' % page
            return torrents
        else:
            print '获取种子列表 page=%d 成功' % page
        soup = BeautifulSoup(ret)
        torrenttbale = soup.find(attrs={'class':'torrents'})
        soup = BeautifulSoup(str(torrenttbale))
        row = soup.table.findAll('tr', recursive=False)
        for i in range(1, len(row)):
            soup = BeautifulSoup(str(row[i]))
            #for i in range(0, len(soup.contents[0])):
            #    print str(i) + '  '+ str(soup.contents[0].contents[i])
            #break
            #得到种子id
            #u2引号没有正确进行转义,包含双引号就完了,不过download?id=都是有的
            #details = soup.contents[0].contents[3].a['href'].encode('utf-8')
            details = str(soup.contents[0].contents[3].find(href = re.compile('id=')))
            reg = re.compile('id=(\d+)')
            ids = re.findall(reg, details)
            id = str(ids[0])

            #得到做种数
            #print soup.contents[0].contents[7]
            if soup.contents[0].contents[7].string == '0':
                seeder = 0
            elif not soup.contents[0].contents[7].b.a.font == None:
                #U2蛋疼的红字
                seeder = int(soup.contents[0].contents[7].b.a.font.string)
            else:
                seeder = int(soup.contents[0].contents[7].b.a.string)

            #得到种子下载数
            if soup.contents[0].contents[9].string == '0':
                leecher = 0
            elif not soup.contents[0].contents[9].b.a.font == None:
                #U2蛋疼的红字
                leecher = int(soup.contents[0].contents[9].b.a.font.string)
            else:
                leecher = int(soup.contents[0].contents[9].b.a.string)

            #if seeder>0:
            torrents.append(id)
            #print '%s %d %d' % (id, seeder, leecher)

        return torrents

    def ret_user_page_torrents_id(self, uid, type = 'seeding', filter = [], include = [], refresh = True, seedermin = 0, seedermax = 999999):
        #获取某个用户做种列表
        if refresh:
            get_url = self.nexus_url + '/getusertorrentlistajax.php?userid=%s&type=%s' % (uid, type)
            resp, ret = self.http.get(get_url)
            if not resp['status'] == 200:
                print '获取用户 id=%s 数据失败:请求失败' % uid
                return
            f = file(config.USER_TORRENT_DIR + '%s.txt' % uid, 'w')
            f.write(ret)
            f.close()

        if os.path.exists(config.USER_TORRENT_DIR + '%s.txt' % uid) == False:
            print '获取用户 id=%s 数据失败:找不到本地用户数据,请尝试 refresh = True' % uid
            return
        f = file(config.USER_TORRENT_DIR + '%s.txt' % uid, 'r')
        ret = f.read()
        f.close()

        torrents = []
        soup = BeautifulSoup(ret)
        row = soup.table.findAll('tr', recursive = False)
        for i in range(1, len(row)):
            soup = BeautifulSoup(str(row[i]))
            #for i in range(0, len(soup.contents[0])):
            #    print str(i) + '  '+ str(soup.contents[0].contents[i])
            #break
            #得到种子id
            details = soup.contents[0].contents[2].a['href'].encode('utf-8')
            reg = re.compile('id=(\d+)')
            ids = re.findall(reg, details)
            id = str(ids[0])

            title = soup.contents[0].contents[2].a['title'].encode('utf-8')
            #得到做种数
            if soup.contents[0].contents[4].string == '0':
                seeder = 0
            else:
                seeder = int(soup.contents[0].contents[4].b.a.string)
            #得到种子下载数
            if soup.contents[0].contents[5].string == '0':
                leecher = 0
            else:
                leecher = int(soup.contents[0].contents[5].b.a.string)

            #种子数不足条件
            if seeder < seedermin or seeder > seedermax:
                continue

            #过滤条件
            flag = 0
            for item in filter:
                if title.find(item) > -1:
                    flag = 1
                    break
            if flag == 1:
                continue

            #包含条件
            flag = 0
            for item in include:
                flag = 0
                for subitem in item:
                    if title.find(subitem) == -1:
                        flag = 1
                        break
                if flag == 0:
                    break
            if flag == 1:
                continue

            torrents.append(id)
            print 'id=%s title=%s seeder=%d leecher=%d' % (id, title, seeder, leecher)
        return torrents

if __name__ == "__main__":
    nexusphp = nexusphp_spider('your cookie')
    #nexusphp.download_torrent('15683')
    #print nexusphp.ret_page_torrents_id(1)
    #nexusphp.ret_user_page_torrents_id('23487', refresh = False, include = [['Fin', 'BDMV'], ['Fin','BDISO']], filter = ['U2娘@Share'])
    #nexusphp.mv_faild_torrent('1')