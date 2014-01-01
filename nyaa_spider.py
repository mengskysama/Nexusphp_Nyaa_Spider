#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from BeautifulSoup import BeautifulSoup

import config
from http_request import http_request

class nyaa_spider:

    def __init__(self):
        self.current_page = 0
        self.http = http_request()

    def download_torrent(self, tid) :
        get_url = 'http://www.nyaa.se/?page=download&tid=%s' % tid
        resp, ret = self.http.get(get_url)
        if not resp['status'] == 200:
            print '下载种子文件 tid=%s 失败:请求失败' % tid
            return False
        else:
            print '下载种子文件 tid=%s 成功' % tid
        f = file(config.TORRENT_DIR + tid + '.torrent', 'wb')
        f.write(ret)
        f.close()
        return True

    def ret_page_torrents_tid(self, page = 1):
        torrents = []
        get_url = 'http://www.nyaa.se/?page=search&term=BDMV&offset=%d' % page
        resp, ret = self.http.get(get_url)
        if not resp['status'] == 200:
            print '获取种子列表 page=%d 失败:请求失败' % page
            return False, torrents
        else:
            print '获取种子列表 page=%d 成功' % page
        soup = BeautifulSoup(ret)
        torrentshref = soup.findAll(attrs={'title':'Download', 'rel':'nofollow'})
        for i in range(1, len(torrentshref)):
            ret = BeautifulSoup(str(torrentshref[i]))
            ret = ret.a['href'].encode('utf-8')
            reg = re.compile('tid=(\d+)')
            ids = re.findall(reg, ret)
            id = str(ids[0])
            torrents.append(id)
        return True, torrents

if __name__ == "__main__":
    nyaa = nyaa_spider()
    resp, torrents_tid =  nyaa.ret_page_torrents_tid(1)
    nyaa.download_torrent(torrents_tid[0])