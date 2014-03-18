#!/usr/bin/python

import pysvn
import pynotify
import getpass
import os

pynotify.init('RepoMonitor')


def get_login( realm, username, may_save ):
    return True, raw_input('Username: '), getpass.getpass(), True 


def showLogsFromChanges(log):
    map(lambda e: pynotify.Notification('Rev.{}  Author: {}'.format(e.revision.number, e.author), e.message).show(), log[:5])


def readRepo():
    if os.path.isfile(RepoMonitor.repo_file):
        with open(RepoMonitor.repo_file) as fp:
            repo = fp.readline().strip()
        return repo
    else:
        open(RepoMonitor.repo_file, 'w').close()
        return 'No repository defined'


class RepoMonitor(object):
    last_rev_file = '/tmp/RepoMonitor/LAST_REV'
    repo_file = '/tmp/RepoMonitor/REPO'

    def __init__(self):
        self.client = pysvn.Client()
        self.client.callback_get_login = get_login
        self.last_rev = self.readLastRev()
        self.repo = readRepo()

    def initLastRevFile(self):
        open(RepoMonitor.last_rev_file, 'w').close()

    def saveLastRev(self, currentRev):
        self.last_rev = currentRev
        with open(RepoMonitor.last_rev_file, 'w') as fp:
            fp.write(str(self.last_rev))

    def readLastRev(self):
        if os.path.isfile(RepoMonitor.last_rev_file):
            with open(RepoMonitor.last_rev_file) as fp:
                last_rev = int(fp.read().strip().split()[0])
        else:
            last_rev = 0
        return last_rev


def checkRepoForChanges(self):
    repo = readRepo()
    head_revision = pysvn.Revision(pysvn.opt_revision_kind.head)
    from_revision = pysvn.Revision(pysvn.opt_revision_kind.number, self.last_rev)
    self.client.info2(repo, head_revision, recurse=False)
    current_rev = self.client.info2(repo, head_revision, recurse=False)[0][1].rev
    if current_rev.number > self.last_rev:
        log = self.client.log(repo, head_revision, from_revision, discover_changed_paths=True)
        if len(log) > 0:
            pynotify.Notification('New commits', '{} new commits in repository'.format(len(log))).show()
            showLogsFromChanges(log)
            self.saveLastRev(current_rev.number)

def run(self):
    self.checkRepoForChanges()

