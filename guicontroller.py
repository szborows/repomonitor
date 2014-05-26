# -*- coding: utf-8

import wx

from config import RepoInfo

class AddRepositoryDialog(wx.Dialog):

    def __init__(self, repoInfo, *args, **kw):
        super(AddRepositoryDialog, self).__init__(*args, **kw) 
        self.repoInfo = repoInfo

        self.InitUI()
        self.SetSize((350, 180))
        self.SetTitle('Add a repository')

    def addField(self, label, fieldName, value, password=False):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label=label)
        if not password:
            edit = wx.TextCtrl(self)
        else:
            edit = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        edit.SetValue(value)
        setattr(self, fieldName, edit)
        hbox.Add(text, proportion=1, flag=wx.LEFT, border=8)
        hbox.Add(edit, proportion=1, flag=wx.RIGHT, border=8)
        return hbox

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hboxUrl = self.addField('URL', 'urlEditBox', self.repoInfo.url if self.repoInfo is not None else '')
        hboxUsername = self.addField('Username', 'usernameEditBox', self.repoInfo.username if self.repoInfo is not None else '')
        hboxPassword = self.addField('Password', 'passwordEditBox', self.repoInfo.password if self.repoInfo is not None else '', password=True)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hboxUrl, flag=wx.ALIGN_LEFT|wx.TOP|wx.EXPAND, border=10)
        vbox.Add(hboxUsername, flag=wx.ALIGN_LEFT|wx.TOP|wx.EXPAND, border=10)
        vbox.Add(hboxPassword, flag=wx.ALIGN_LEFT|wx.TOP|wx.EXPAND, border=10)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnSave)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def GetUrl(self):
        return self.urlEdit.text

    def OnSave(self, e):
        setattr(self, 'url', self.urlEditBox.GetValue())
        setattr(self, 'username', self.usernameEditBox.GetValue())
        setattr(self, 'password', self.passwordEditBox.GetValue())
        self.Destroy()
        self.EndModal(wx.ID_OK)

    def OnClose(self, e):
        self.Destroy()

class RepoMonitorConfigurationWindow(wx.Frame):

    def __init__(self, parent, title, config, showMessage):
        super(RepoMonitorConfigurationWindow, self).__init__(parent, title=title, size=(390, 250))
        self.config = config

        if showMessage:
            wx.MessageBox(
                'There are no configured repositories. Please add at least one.',
                'No repositories',
                wx.OK | wx.ICON_INFORMATION)

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Repositories')
        st1.SetFont(font)
        hbox1.Add(st1, proportion=1, flag=wx.RIGHT, border=8)
        bmAdd = wx.ArtProvider.GetBitmap(id=wx.ART_NEW, client=wx.ART_NEW)
        bmEdit = wx.Image('edit.png', wx.BITMAP_TYPE_PNG).Scale(22, 22, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        bmRemove = wx.ArtProvider.GetBitmap(id=wx.ART_DELETE, client=wx.ART_DELETE)
        ID_ADD, ID_EDIT, ID_REMOVE = wx.NewId(), wx.NewId(), wx.NewId()
        btAdd = wx.BitmapButton(panel, ID_ADD, bitmap=bmAdd)
        self.Bind(wx.EVT_BUTTON, self.OnAddRepository, id=ID_ADD)
        hbox1.Add(btAdd, flag=wx.LEFT)
        self.btnEdit = wx.BitmapButton(panel, ID_EDIT, bitmap=bmEdit)
        self.btnEdit.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnEditRepository, id=ID_EDIT)
        hbox1.Add(self.btnEdit, flag=wx.LEFT)
        self.btnRemove = wx.BitmapButton(panel, ID_REMOVE, bitmap=bmRemove)
        self.btnRemove.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnRemoveRepository, id=ID_REMOVE)
        hbox1.Add(self.btnRemove, flag=wx.LEFT)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        ID_CHECK_LIST_BOX = wx.NewId()
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.chkListBox = wx.CheckListBox(panel, id=ID_CHECK_LIST_BOX)

        self.refreshList()

        hbox3.Add(self.chkListBox, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)

        vbox.Add((-1, 15))
        panel.SetSizer(vbox)

        self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=ID_CHECK_LIST_BOX)

    def OnSelect(self, e):
        self.btnEdit.Enable()
        self.btnRemove.Enable()

    def refreshList(self):
        self.chkListBox.Clear()
        for repository in self.config.repositories:
            self.chkListBox.Append(repository.url)

    def OnAddRepository(self, e):
        dlg = AddRepositoryDialog(None, None)
        result = dlg.ShowModal()
        if wx.ID_OK == result:
            ri = RepoInfo()
            ri.url = dlg.url
            ri.username = dlg.username
            ri.password = dlg.password
            self.config.repositories.append(ri)
            self.config.save()
            self.refreshList()
        dlg.Destroy()

    def OnEditRepository(self, e):
        url = self.chkListBox.GetStrings()[self.chkListBox.GetSelections()[0]]
        for repoInfo in self.config.repositories:
            if repoInfo.url == url:
                repo = repoInfo
                break
        dlg = AddRepositoryDialog(repo, None)
        result = dlg.ShowModal()
        if wx.ID_OK == result:
            ri = RepoInfo()
            ri.url = dlg.url
            ri.username = dlg.username
            ri.password = dlg.password
            self.config.repositories.append(ri)
            self.config.save()
            self.refreshList()
        dlg.Destroy()

    def OnRemoveRepository(self, e):
        url = self.chkListBox.GetStrings()[self.chkListBox.GetSelections()[0]]
        for repoInfo in self.config.repositories:
            if repoInfo.url == url:
                self.config.repositories.remove(repoInfo)
                break
        self.chkListBox.Delete(self.chkListBox.GetSelections()[0])
        self.config.save()

class GuiController(object):

    def __init__(self, config):
        self.config = config

    def showConfigurationWindow(self, showMessage=False):
        app = wx.App()
        RepoMonitorConfigurationWindow(None, title='RepoMonitor configuration', config=self.config, showMessage=showMessage)
        app.MainLoop()
