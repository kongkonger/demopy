print('cmc')


import  _thread
import  time

def print_time( threadName,delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        # print "%s: %s" %( threadName,time.ctime(time.time()) )
#
# try:
#     _thread.start_new_thread(pri)