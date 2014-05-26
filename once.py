#!/usr/bin/env python

import optparse
import wx

import repomonitor
from config import RepoMonitorConfig
from guicontroller import GuiController

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-c', '--configuration', action='store_true', dest='configuration')
    options, _ = parser.parse_args()

    config = RepoMonitorConfig()
    config.load('config.json')

    guiController = GuiController(config)

    if not config.repositories:
        guiController.showConfigurationWindow(showMessage=True)

    if options.configuration:
        guiController.showConfigurationWindow()
    else:
        repomonitor.RepoMonitor(config).run()

