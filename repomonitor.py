#!/usr/bin/python

import pysvn
import pynotify
import getpass
import os

from guicontroller import GuiController

pynotify.init('RepoMonitor')


def get_login( realm, username, may_save ):
    return True, raw_input('Username: '), getpass.getpass(), False

def notif_X(str_, mess):
    pynotify.Notification(str_, mess).show()

def showLogsFromChanges(log):
    map(lambda e: notif_X('Rev.{}  Author: {}'.format(e.revision.number, e.author), e.message), log[:5])


class RepoMonitor(object):
    def __init__(self, config):
        self.config = config

        self.client = pysvn.Client()
        self.client.callback_get_login = get_login
        self.last_rev = self.config.repositories[0].last_rev
        self.repo = self.config.repositories[0].url

    def checkRepoForChanges(self, repoInfo):
        print 'Using repository {}'.format(repoInfo.url)
        head_revision = pysvn.Revision(pysvn.opt_revision_kind.head)
        current_rev = self.client.info2(self.repo, head_revision, recurse=False)[0][1].rev

        from_revision = pysvn.Revision(pysvn.opt_revision_kind.number, self.last_rev)

        print 'Checking range {0}:{1}'.format(from_revision.number, current_rev.number)

        if current_rev.number > repoInfo.last_rev:
            log = self.client.log(self.repo, head_revision, from_revision, limit=5, discover_changed_paths=True)
            if len(log) > 0:
                pynotify.Notification('New commits', '{} new commits in repository'.format(len(log))).show()
                showLogsFromChanges(log)

    def checkRepositoryOnline(self):
        try:
            self.client.info2(self.repo, pysvn.Revision(pysvn.opt_revision_kind.head), recurse=False)
            return True
        except pysvn.ClientError:
            return False

    def run(self):
        if self.client.is_url(self.repo) and self.checkRepositoryOnline():
            self.checkRepoForChanges(self.config.repositories[0])
        else:
            GuiController(self.config).showConfigurationWindow()
            print 'Could not connect to SVN {}'.format(self.repo)

