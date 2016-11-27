# coding:utf-8
import threading, multiprocessing, time
from multiprocessing.dummy import Pool
from Queue import Empty

# using thread pool
def fun():
    print threading.current_thread().getName(), 'do work1'
    time.sleep(3)
    print threading.current_thread().getName(), 'do work2'

    print '*'* 20

def use_pool():
    pool = Pool(5)

    # pool.map(fun, [])
    for _ in range(13):
        pool.apply_async(fun)
    pool.close()
    pool.join()

# using process & queue
def do_work(data, in_queue):
    print multiprocessing.current_process().name, 'do work with data', data
    time.sleep(2)
    return data+10

def do_work_with_queue(in_queue, out_queue):
    while True:
        try:
            print multiprocessing.current_process().name, 222
            data = in_queue.get(timeout=1)
            print 'get data', data
        except Empty:
            print 'in queue empty'
            break
        rv = do_work(data, in_queue)
        out_queue.put(rv)
        in_queue.task_done()

def process():
    in_queue = multiprocessing.JoinableQueue()
    num = multiprocessing.cpu_count() * 2
    out_queue = multiprocessing.Queue()

    for i in range(2):
        in_queue.put(i)

    for _ in range(2):
        p = multiprocessing.Process(target=do_work_with_queue, args=(in_queue, out_queue))
        p.start()

    in_queue.join()

    results = []
    while True:
        try:
            results.append(out_queue.get(timeout=1))
        except Empty:
            break
    print results


if __name__ == '__main__':
    # use_pool()
    process()
    print multiprocessing.cpu_count()


