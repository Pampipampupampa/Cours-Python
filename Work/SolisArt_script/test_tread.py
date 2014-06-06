import sys
import time
import threading


class WorkerThread(threading.Thread):

    def run(self):
        while True:
            print('Working hard')
            time.sleep(0.5)


def main(args):
    use_daemon = False
    for arg in args:
        if arg == '--use_daemon':
            use_daemon = True
    worker = WorkerThread()
    worker.setDaemon(use_daemon)
    worker.start()
    time.sleep(10)
    sys.exit(0)

if __name__ == '__main__':
    main(('--use_daemon',))
