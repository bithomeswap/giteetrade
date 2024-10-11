import wx#pip install wxPython

# # 创建应用程序对象
# app = wx.App()
# # 创建主窗口
# frame = wx.Frame(None, title="My First wxPython App", size=(800, 600))
# # 显示窗口
# frame.Show()
# # 进入应用程序主循环
# app.MainLoop()

#记事本
class Notepad(wx.Frame):
    def __init__(self, *args, **kw):
        super(Notepad, self).__init__(*args, **kw)

        # 创建文本区域
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # 创建菜单栏
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        newItem = fileMenu.Append(wx.ID_NEW, '&New')
        openItem = fileMenu.Append(wx.ID_OPEN, '&Open')
        saveItem = fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT, 'E&xit')

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # 绑定事件
        self.Bind(wx.EVT_MENU, self.on_new, newItem)
        self.Bind(wx.EVT_MENU, self.on_open, openItem)
        self.Bind(wx.EVT_MENU, self.on_save, saveItem)
        self.Bind(wx.EVT_MENU, self.on_exit, exitItem)

        # 设置窗口属性
        self.SetSize((800, 600))
        self.SetTitle('Simple Notepad')
        self.Centre()

    def on_new(self, event):
        self.text.Clear()

    def on_open(self, event):
        with wx.FileDialog(self, "Open Text file", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, 'r') as file:
                    self.text.SetValue(file.read())
            except IOError:
                wx.LogError("Cannot open file '%s'." % path)

    def on_save(self, event):
        with wx.FileDialog(self, "Save Text file", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, 'w') as file:
                    file.write(self.text.GetValue())
            except IOError:
                wx.LogError("Cannot save current contents in file '%s'." % path)

    def on_exit(self, event):
        self.Close(True)

app = wx.App()
notepad = Notepad(None)
notepad.Show()
app.MainLoop()