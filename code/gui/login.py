# -*- coding: utf-8 -*-

import wx
import win32api
import sys, os
from db.select import select

APP_TITLE = u'管理员登录'
APP_ICON = 'res/python.ico'

class loginFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    def __init__(self, parent, id=-1, UpdateUI=None):
        '''构造函数'''

        wx.Frame.__init__(self, parent, id, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((520, 220))
        self.Center()
        self.UpdateUI = UpdateUI

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        wx.StaticText(self, -1, u'管理员id：', pos=(40, 50), size=(100, -1), style=wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, u'管理员密码：', pos=(40, 80), size=(100, -1), style=wx.ALIGN_RIGHT)
        self.tip = wx.StaticText(self, -1, u'', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)

        self.tc1 = wx.TextCtrl(self, -1, '', pos=(145, 50), size=(150, -1), name='TC01', style=wx.TE_CENTER)
        self.tc2 = wx.TextCtrl(self, -1, '', pos=(145, 80), size=(150, -1), name='TC02',
                               style=wx.TE_PASSWORD | wx.ALIGN_RIGHT)

        btn_mea = wx.Button(self, -1, u'管理员登录', pos=(350, 50), size=(100, 25))
        btn_guest = wx.Button(self, -1, u'游客登录', pos=(350, 80), size=(100, 25))
        btn_close = wx.Button(self, -1, u'关闭窗口', pos=(350, 110), size=(100, 25))

        # 控件事件
        self.Bind(wx.EVT_BUTTON, self.OnClose, btn_close)
        self.Bind(wx.EVT_BUTTON, self.OnGuest, btn_guest)
        self.Bind(wx.EVT_BUTTON, self.OnLogin, btn_mea)

        # 系统事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # self.Bind(wx.EVT_PAINT, self.On_paint)
        # self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)


    def OnClose(self, evt):
        '''关闭窗口事件函数'''

        dlg = wx.MessageDialog(None, u'确定要关闭本窗口？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
        if (dlg.ShowModal() == wx.ID_YES):
            self.Destroy()
            exit(0)

    def OnGuest(self, evt):
        '''游客登录事件函数'''
        dlg = wx.MessageDialog(None, u'欢迎你，guest！', u'操作提示', wx.OK)
        if (dlg.ShowModal() == wx.OK):
            dlg.Destroy()
        self.UpdateUI(2)

    def OnLogin(self, evt):
        '''管理员登录事件函数'''
        MNO = self.tc1.GetValue()
        with open('mno.txt','w',encoding='utf-8') as f:
            f.write(MNO)
        pw = self.tc2.GetValue()
        dbm = select()
        data = dbm.check_manager(MNO)[0][0]
        name = dbm.get_manager_name(MNO)[0][0]
        if (data == pw):
            dlg = wx.MessageDialog(None, u'欢迎你，{}！'.format(name), u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
            self.UpdateUI(1)
        else:
            dlg = wx.MessageDialog(None, u'密码错误！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()



class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = loginFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
