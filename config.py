#!/usr/bin/python
#encoding=utf-8

PRINT = False
VER = 1.0

#种子页面
NEXUS_URL = 'http://u2.dmhy.org/'
#参数&page=%s
#BDMV活种
NEXUS_PAGE_URL = 'torrents.php?inclbookmarked=0&incldead=1&spstate=0&cat9=1&cat10=1&cat11=1&cat12=1&cat13=1&cat14=1&cat15=1&cat16=1&cat17=1&cat21=1&cat22=1&cat23=1&cat30=1&cat40=1&search_area=0&search=BDMV&search_mode=0&page=%s'
NEXUS_DOWNLOAD_URL = 'download.php?id=%s'

NEXUSCOOKIE = ''
#种子存储目录
TORRENT_DIR = 'D:\\code\\python\\NexusPHPSpider\\torrents\\'
#用户做种信息存储目录
USER_TORRENT_DIR =  'D:\\code\\python\\NexusPHPSpider\\usertorrents\\'

#115帐号并发数
DL115_DLMAX = 15

#115不需要(Transmission2.82
#除了chd之外应该都不需要的.
USE_MY_TRACKER = False

#自己的转发Tracker
#尽量使用独立IP,不应该让别人知道
MY_TRACKER = 'http://www.zuosi.com:18888/announce'