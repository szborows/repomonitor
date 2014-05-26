#!/usr/bin/python
#-*- coding: utf-8 -*-

import signal
import daemon
import lockfile
import time

from repomonitor import RepoMonitor

if __name__ == "__main__":
    def cleanup():
        pass

    def reloadConfig():
        pass

    print daemon.__file__

    context = daemon.DaemonContext(
        working_directory='/tmp',
        umask=0o002,
        pidfile=lockfile.FileLock('/var/run/repomonitor.pid'),)

    context.signal_map = {
        signal.SIGTERM: cleanup,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reloadConfig,
    }

    with context:
        RepoMonitorDaemon().run()
