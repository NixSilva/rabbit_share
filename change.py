import socket
import sync
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    """Handle events for file changed"""

    def request_hashes(self, event):
        if event.event_type == 'moved':
            metadata = "{0} {1} {2} {3}".format(
                event.event_type, event.is_directory,
                event.src_path, event.dest_path)
        else:
            metadata = "{0} {1} {2}".format(
                event.event_type, event.is_directory,
                event.src_path)
        host = '::1'
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.connect((host, 1129))
        s.send(metadata)
        s.recv(1024)
        s.close()

    def on_moved(self, event):
        super(ChangeHandler, self).on_moved(event)
        self.request_hashes(event)

    def on_created(self, event):
        super(ChangeHandler, self).on_created(event)
        self.request_hashes(event)

    def on_deleted(self, event):
        super(ChangeHandler, self).on_deleted(event)
        self.request_hashes(event)

    def on_modified(self, event):
        super(ChangeHandler, self).on_modified(event)
        self.request_hashes(event)
