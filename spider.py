#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import config
from nexusphp_spider import nexusphp_spider

import sys
sys.path.append("115API")

from u115_api import u115_api
from nyaa_spider import nyaa_spider

my_115account = ['13000000000', '123456']

def task_nyaase():
    #这是一个实例用于抓取nyaa丢入115,最好还是用个mysql,sqlite存一下已经下载过的种子信息什么的,避免重复工作
    nyaa = nyaa_spider()
    #115
    u115 = u115_api()
    u115.login(my_115account[0], my_115account[1])
    #首页循环
    auto_next = False
    page = 1
    torrents_id_falid = {}
    while True:
        index = 0
        resp, torrents_id = nyaa.ret_page_torrents_tid(page)
        if resp == False:
            continue
        if auto_next == True and len(torrents_id) == 0:
            print '所有工作都已经做完'
            break
        while index < len(torrents_id):
            while u115.ret_current_bt_task_count() < config.DL115_DLMAX:
                if index == len(torrents_id):
                    #没有需要添加的队列
                    break
                print '任务总数:%d 当前:%d id=%s' % (len(torrents_id), index, torrents_id[index])
                if nyaa.download_torrent(torrents_id[index]) == True:
                    #种子下载成功
                    torrent_path = config.TORRENT_DIR + torrents_id[index] + '.torrent'
                    if os.path.getsize(torrent_path) > 2 * 1024 * 1024:
                        print '种子文件超过2M限制'
                        index += 1
                        continue
                    flag = True
                    while u115.upload_torrent(torrent_path) == False:
                        #种子文件上传失败
                        if torrents_id_falid.has_key(torrents_id[index]):
                            #标记尝试三次后放弃
                            torrents_id_falid[torrents_id[index]] += 1
                            if torrents_id_falid[torrents_id[index]] > 2:
                                index += 1
                                flag = False
                                break
                        else:
                            torrents_id_falid[torrents_id[index]] = 1
                    if flag == True:
                        print '上传并添加任务 id=%s 成功' % torrents_id[index]
                        index += 1
                else:
                    #种子下载失败
                    #延时2秒后往死里下,不可能下不成功的
                    time.sleep(2)
            #制作分享礼包并从任务中删除
            u115.auto_make_share_link()
            #打印状态
            u115.print_bt_task_info()
            time.sleep(15)
        print 'page=%d 所有工作都已经做完' % page
        if auto_next == True:
            page += 1
        else:
            break
    print '所有工作都已经做完'

def task_i():
    #这是一个实例用于抓取u2某米帝的seed丢入115,最好还是用个mysql,sqlite存一下已经下载过的种子信息什么的,避免重复工作
    nexusphp = nexusphp_spider(cookie = config.NEXUSCOOKIE)
    #只找BDMV合集并且seeder小于8
    torrents_id = nexusphp.ret_user_page_torrents_id('23487', refresh = False, seedermax = 7, include = [['Fin', 'BDMV'], ['Fin','BDISO']])
    #115
    u115 = u115_api()
    u115.login(my_115account[0], my_115account[1])
    #122
    index = 0
    torrents_id_falid = {}

    while index < len(torrents_id):
        while u115.ret_current_bt_task_count() < config.DL115_DLMAX:
            if index == len(torrents_id):
                #没有需要添加的队列
                break
            print '任务总数:%d 当前:%d id=%s' % (len(torrents_id), index, torrents_id[index])
            if nexusphp.download_torrent(torrents_id[index]) == True:
                #种子下载成功
                torrent_path = config.TORRENT_DIR + torrents_id[index] + '.torrent'
                if os.path.getsize(torrent_path) > 2 * 1024 * 1024:
                    print '种子文件超过2M限制'
                    nexusphp.mv_faild_torrent(torrents_id[index])
                    index += 1
                    continue
                flag = True
                while u115.upload_torrent(torrent_path) == False:
                    #种子文件上传失败
                    if torrents_id_falid.has_key(torrents_id[index]):
                        #标记尝试三次后放弃
                        torrents_id_falid[torrents_id[index]] += 1
                        if torrents_id_falid[torrents_id[index]] > 2:
                            nexusphp.mv_faild_torrent(torrents_id[index])
                            index += 1
                            flag = False
                            break
                    else:
                        torrents_id_falid[torrents_id[index]] = 1
                if flag == True:
                    print '上传并添加任务 id=%s 成功' % torrents_id[index]
                    index += 1
            else:
                #种子下载失败
                #延时2秒后往死里下,不可能下不成功的
                time.sleep(2)
        #制作分享礼包并从任务中删除
        u115.auto_make_share_link()
        #打印状态
        u115.print_bt_task_info()
        time.sleep(15)
    print '所有工作都已经做完'

if __name__ == "__main__":
    print '专业作死一百年'
    task_nyaase()