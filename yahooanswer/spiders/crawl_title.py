
import re
import sys
import threading
import requests
import Queue

qid_reg = re.compile(r'/question\\/index\?qid=([\d\w]+)\\')

mutex = threading.Lock()


class DownloadThread(threading.Thread):
    def __init__(self, in_queue, fout):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.fout = fout

    def run(self):
        while True:
            url = self.in_queue.get()
            qid_list = []
            print url
            qid_list = crawl_page(url)
            for i in range(5):
                # try 5 times at most
                try:
                    qid_list = crawl_page(url)
                    break
                except:
                    continue
            if qid_list:
                mutex.acquire()
                for qid in qid_list:
                    self.fout.write('%s\n' % qid)
                mutex.release()
            self.in_queue.task_done()


def crawl_page(url):
    global qid_reg
    r = requests.get(url)
    qid_list = qid_reg.findall(r.text)
    return qid_list



def main():
    in_queue = Queue.Queue()
    outpath = 'qid.out'
    sid_list = [u'396545367', u'396545301', u'396545327', u'396546046', u'396545443', u'396545444', u'396545394', u'396545018', u'396545019', u'396545014', u'396545015', u'396545016', u'396545469', u'396545401', u'396545013', u'396545213', u'396545311', u'396545454', u'396545144', u'396545451', u'396545439', u'396545012', u'396545660', u'396545433', u'396546089', u'396545122']
    for i in range(3, 1000):
        bpos = i
        cpos = (i - 1) * 20
        for sid in sid_list:
            url = 'https://answers.yahoo.com/_module?name=YANewDiscoverTabModule&after=pc%s~p%%3A0&sid=%s&disableLoadMore=false&bpos=%s&cpos=%s' % (cpos, sid, bpos, cpos)
            in_queue.put(url)

    fout = open(outpath, 'wb')
    for i in range(5):
        dt = DownloadThread(in_queue, fout)
        dt.setDaemon(True)
        dt.start()
    in_queue.join()
    fout.close()
    print 'Done!'


if __name__ == '__main__':
    main()