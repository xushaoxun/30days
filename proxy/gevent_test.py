# coding:utf-8
from gevent import monkey
from gevent.queue import Queue, Empty
from gevent.pool import Pool
from time import sleep

monkey.patch_all()

def use_gevent_with_queue():
    queue = Queue()
    pool = Pool(10)

    for i in range(1,10):
        queue.put(i)

    while pool.free_count():
        sleep(0.1)
        pool.spawn(fun_with_queue, queue)

    pool.join()

def fun_with_queue(queue):
    while True:
        try:
            i = queue.get(timeout=0)
        except Empty:
            break

        fun(i, queue)
    print 'stop'

def fun(i, queue):
    print i, 'a'
    sleep(1)
    print i

    if i==5:
        queue.put(i+10)

if __name__ == '__main__':
    use_gevent_with_queue()