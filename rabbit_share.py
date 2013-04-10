#!/usr/bin/env python2

import rsync
import socket
import time
import threading
from change import ChangeHandler
from watchdog.observers import Observer


def run_server(path):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 1129))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        try:
            conn.settimeout(5)
            buf = conn.recv(1024)
            conn.send(buf)
        except s.timeout:
            print 'time out'
        print addr, buf
        conn.close()

def run_client(path):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(
        event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    path = '/home/celeron/Dropbox'
    threading.Thread(target=run_server, args=(path,)).start()
    run_client(path)
