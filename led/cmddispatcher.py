import threading
import subprocess


class CmdDispatcher(threading.Thread):

    def __init__(self):
        super().__init__()
        self.cmd_lock = threading.Semaphore(value=0)
        self.thread = None
        self.thread_stop = False
        self.cmd_list = []
        self.cmd_list_lock = threading.Lock()
        self.setDaemon(True)

    def run(self):

        # main loop
        while True:

            # wait for lock
            self.cmd_lock.acquire()

            # check for stop
            if self.thread_stop:
                break

            cmd = None
            with self.cmd_list_lock:
                if len(self.cmd_list):
                    cmd = self.cmd_list[-1]
                    self.cmd_list.clear()
            if cmd:
                proc = subprocess.Popen([*cmd.strip().split(" ")])
                proc.wait()

    def stop(self):
        self.thread_stop = True
        self.cmd_lock.release()
        self.join()

    def dispatch_cmd(self, cmd):
        with self.cmd_list_lock:
            if not len(self.cmd_list) or self.cmd_list[-1] != cmd:
                self.cmd_list.append(cmd)
                self.cmd_lock.release()
