#-*- coding: utf-8 -*-

import json
import getpass

class RepoInfo(object):

    def __init__(self):
        self.url = ''
        self.last_rev = 0
        self.username = ''
        self.password = ''

    @staticmethod
    def fromDict(dict_):
        ri = RepoInfo()
        ri.url = dict_['url']
        ri.last_rev = dict_['last_rev']
        ri.username = dict_['username']
        ri.password = dict_['password']
        return ri

    @staticmethod
    def toDict(repoInfo):
        return {
            'url': repoInfo.url,
            'username': repoInfo.username,
            'password': repoInfo.password,
            'last_rev': repoInfo.last_rev,
        }

    def __str__(self):
        return str(RepoInfo.toDict(self))

class RepoMonitorConfig(object):

    def __init__(self):
        self.repositories = []

    def load(self, path):
        self.path = path
        try:
            with open(path) as fp:
                config = json.loads(fp.read())
            repos = config['repositories']
            repos = map(RepoInfo.fromDict, repos)
        except (IOError, ValueError):
            repos = []

        self.repositories = repos

    def save(self):
        config = {
            'repositories': [RepoInfo.toDict(r) for r in self.repositories],
        }
        with open(self.path, 'w') as fp:
            fp.write(json.dumps(config))

    def updateLastRevision(self, path, lastRevisionNumber):
        pass # TODO

