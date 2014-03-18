#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
from daemon import runner

from repomonitor import RepoMonitor

class RepoMonitorDaemon(object):

    INTERVAL = 20

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/repomonitor.pid'
        self.pidfile_timeout = 5

    def run(self):
        monitor = RepoMonitor()
        while True:
          monitor.run()
          time.sleep(self.INTERVAL)


if __name__ == "__main__":
    repoMonitorDaemon = RepoMonitorDaemon()
    daemon_runner = runner.DaemonRunner(repoMonitorDaemon)
    daemon_runner.do_action()
