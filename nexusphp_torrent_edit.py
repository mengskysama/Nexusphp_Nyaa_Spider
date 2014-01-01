#coding:utf-8
import config
import os

def torrent_announce_change(torrent_file_path):
    file = open(torrent_file_path, 'rb')
    torrent_ct = file.read()
    tracker = config.MY_TRACKER
    pos = torrent_ct.find('announce')
    leng = int(torrent_ct[pos + 8:torrent_ct.find(':', pos)])
    mod = '%s%d:%s%s' % (torrent_ct[:pos+8], len(tracker), tracker, torrent_ct[pos+11+leng:])
    file.close()
    os.remove(torrent_file_path)
    file = open(torrent_file_path, 'wb')
    file.write(mod)
    file.close()