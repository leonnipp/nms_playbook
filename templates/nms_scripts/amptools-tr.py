#!/usr/bin/python2
#last Updated at 20180726-1944
import re
import sys
import traceconfig
import urllib2, json, Geohash
from subprocess import check_output
from time import sleep
import threading
import syslog

def systemOut(object):
    sys.stdout.write(object + "\n")

def main():
    for dest in traceconfig.dest:
        destip=dest.split(':')[0]
        try:
           destname=dest.split(':')[1]
        except:
           destname="NA"
        sleep(20)
        screenlock = threading.Semaphore(value=1)
        screenlock.acquire()
        thread = threading.Thread(target=trace, args=(destip,destname)).start()
        screenlock.release()
        syslog.syslog(syslog.LOG_INFO, dest)

def trace(dest,destname):
    result = check_output(["sudo", "/usr/bin/amp-trace", "--", dest])
    arOutput = result.rstrip().split("\n")[5:]
    c_us = 0
    for route in arOutput:
        rs = re.sub(r"(\(|\))", "", route.lstrip().replace('  ', ' ')).split(' ')
        hop = rs[0]
        ip = rs[1]
        us = int(rs[2][:-2].strip()) if len(rs) > 2 else 0

        try:
            url = urllib2.urlopen('http://ip-api.com/json/' + ip + '?fields=lat,lon,as')
            obj = json.load(url)
            as_num = obj["as"].replace(' ', '\ ').replace(',', '\,')
            if not as_num:
                        as_num = "NA"
            geohashresult=Geohash.encode(obj["lat"], obj["lon"])
        except:
            as_num = "NA"
            geohashresult = "NA"

        c_us += us
        systemOut('traceroute,dest=%s,destname=%s,hop=%s,ip=%s,as_num=%s,geohash=%s hopcount=%s,us=%d,c_us=%d' % (dest, destname, hop, ip, as_num, geohashresult, hop, us, c_us))

if __name__ == '__main__':
    main()
