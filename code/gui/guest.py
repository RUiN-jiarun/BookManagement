# -*- coding: utf-8 -*-

import wx
import wx.grid
import win32api
import sys, os
from db.insert import insert
from db.select import select
from db.delete import delete
import time

APP_TITLE = u'图书管理系统'
APP_ICON = 'res/python.ico'


class guestFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    id_login = wx.NewId()
    id_account = wx.NewId()
    id_quit = wx.NewId()
    id_info = wx.NewId()

    id_help = wx.NewId()
    id_about = wx.NewId()

    id_search = wx.NewId()


    def __init__(self, parent, id=-1, UpdateUI=None):
        '''构造函数'''

        wx.Frame.__init__(self, parent, id, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()
        self.UpdateUI = UpdateUI

        if hasattr(sys, "frozen") and getattr(sys, "frozen") == "windows_exe":
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.Maximize()
        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)

        self._CreateMenuBar()  # 菜单栏
        self._CreateToolBar()  # 工具栏
        self._CreateStatusBar()  # 状态栏
        self._CreateGrid()     # 工作区表格

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self._CreateSearchGrid()
        self._DestroySearchGrid()

    def _CreateMenuBar(self):
        '''创建菜单栏'''

        self.mb = wx.MenuBar()

        # 文件菜单
        m = wx.Menu()
        m.Append(self.id_info, u"账户信息")
        m.Append(self.id_login, u"切换账户")
        m.AppendSeparator()
        m.Append(self.id_quit, u"退出系统")
        self.mb.Append(m, u"系统")

        # 帮助菜单
        m = wx.Menu()
        m.Append(self.id_help, u"帮助主题")
        m.Append(self.id_about, u"关于...")
        self.mb.Append(m, u"帮助")

        self.Bind(wx.EVT_MENU, self.OnInfo, id=self.id_info)
        self.Bind(wx.EVT_MENU, self.OnLogin, id=self.id_login)
        self.Bind(wx.EVT_MENU, self.OnClose, id=self.id_quit)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=self.id_help)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.id_about)

        self.SetMenuBar(self.mb)

    def OnInfo(self, evt):
        '''显示账户信息'''
        dlg = wx.MessageDialog(None, u'登录信息：guest身份\n您当前只能进行查询事务', u'帮助', wx.OK)
        if (dlg.ShowModal() == wx.OK):
            dlg.Destroy()

    def OnHelp(self, evt):
        '''显示帮助'''
        with open('../Help.txt','rb') as g:
            help_info = g.read()
            g.close()
        dlg = wx.MessageDialog(None, help_info, u'帮助', wx.OK)
        if (dlg.ShowModal() == wx.OK):
            dlg.Destroy()

    def OnAbout(self, evt):
        '''显示关于'''
        about_info = """
                    图书管理系统1.0
                    作者：刘佳润
                    开发环境：Python 3.6
                    数据库系统：Microsoft SQL Server 2019
                    """
        dlg = wx.MessageDialog(None, about_info, u'关于', wx.OK)
        if (dlg.ShowModal() == wx.OK):
            dlg.Destroy()

    def _CreateToolBar(self):
        '''创建工具栏'''

        ico_search = wx.Bitmap('res/search.ico', wx.BITMAP_TYPE_ANY)


        self.tb = wx.ToolBar(self)
        self.tb.SetToolBitmapSize((16, 16))

        self.tb.AddLabelTool(self.id_search, u'图书查询', ico_search, shortHelp=u'查询', longHelp=u'查找图书相关信息')

        self.Bind(wx.EVT_MENU, self.OnSearch, id=self.id_search)
        self.tb.Realize()

    def _CreateStatusBar(self):
        '''创建状态栏'''

        self.sb = self.CreateStatusBar()
        self.sb.SetFieldsCount(3)
        self.sb.SetStatusWidths([-2, -1, -1])
        self.sb.SetStatusStyles([wx.SB_RAISED, wx.SB_RAISED, wx.SB_RAISED])

        self.sb.SetStatusText(u'', 0)
        self.sb.SetStatusText(u'', 1)
        self.sb.SetStatusText(u'正常', 2)

    def _CreateGrid(self):
        '''创建图书总表'''

        self.grid = wx.grid.Grid(self, -1, pos=(25, 170), size=(1200, 370))
        self.grid.CreateGrid(80, 9)
        self.grid.SetDefaultColSize(120, resizeExistingCols=True)
        self.grid.SetDefaultCellOverflow(False)
        GridLabelToDBLabel = [(0, '书号'), (1, '类别'), (2, '书名'), (3, '出版社'), (4, '年份'), (5, '作者'), (6, '价格'),
                              (7, '总藏书量'),
                              (8, '库存')]
        for i, tup in enumerate(GridLabelToDBLabel):
            self.grid.SetColLabelValue(i, tup[1])
        self.grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        s = select()
        data = s.select_all()
        for row, ele in enumerate(data):
            l_ShowRow = row
            for col, value in enumerate(ele):
                l_ShowCol = col
                if l_ShowCol >= 0:
                    if type(value) is not str:
                        value = str(value)
                    self.grid.SetCellValue(l_ShowRow, l_ShowCol, value)

        self.grid.EnableEditing(False)

    def OnLogin(self, evt):
        '''切换账户，退出到登录界面'''
        self.UpdateUI(0)

    def OnSearch(self, evt):
        '''图书查询'''
        self._CreateSearchGrid()
        self.sb.SetStatusText(u'图书查询', 1)

    def _CreateSearchGrid(self):
        self.gridb = wx.grid.Grid(self, -1, pos=(25, 600), size=(1200, 100))
        self.gridb.CreateGrid(20, 9)
        self.gridb.SetDefaultColSize(120, resizeExistingCols=True)
        self.gridb.SetDefaultCellOverflow(False)
        GridLabelToDBLabel = [(0,'书号'),(1,'类别'),(2,'书名'),(3,'出版社'),(4,'年份'),(5,'作者'),(6,'价格'),(7,'总藏书量'),(8,'库存')]
        for i, tup in enumerate(GridLabelToDBLabel):
            self.gridb.SetColLabelValue(i, tup[1])
        self.gridb.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.ShowSerial = []
        for i in range(20):
            self.ShowSerial.append([i,"str"])
        self.ShowCols = []
        for i in range(9):
            self.ShowCols.append(i)

        #self.gridb.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

        self.tc1 = wx.StaticText(self, -1, u'书名：', pos=(1250, 200), size=(50, -1), style=wx.ALIGN_RIGHT)
        self.tx1 = wx.TextCtrl(self, -1, '', pos=(1300, 200), size=(150, -1), name='TX01')
        self.tc2 = wx.StaticText(self, -1, u'类别：', pos=(1250, 230), size=(50, -1), style=wx.ALIGN_RIGHT)
        self.tx2 = wx.TextCtrl(self, -1, '', pos=(1300, 230), size=(150, -1), name='TX02')
        self.tc3 = wx.StaticText(self, -1, u'出版社：', pos=(1250, 260), size=(50, -1), style=wx.ALIGN_RIGHT)
        self.tx3 = wx.TextCtrl(self, -1, '', pos=(1300, 260), size=(150, -1), name='TX03')
        self.tc4 = wx.StaticText(self, -1, u'作者：', pos=(1250, 290), size=(50, -1), style=wx.ALIGN_RIGHT)
        self.tx4 = wx.TextCtrl(self, -1, '', pos=(1300, 290), size=(150, -1), name='TX04')
        self.tc5 = wx.StaticText(self, -1, u'起始年份：', pos=(1230, 320), size=(60, -1), style=wx.ALIGN_RIGHT)
        self.tx5 = wx.TextCtrl(self, -1, '1800', pos=(1300, 320), size=(150, -1), name='TX05')
        self.tc6 = wx.StaticText(self, -1, u'终止年份：', pos=(1230, 350), size=(60, -1), style=wx.ALIGN_RIGHT)
        self.tx6 = wx.TextCtrl(self, -1, '2020', pos=(1300, 350), size=(150, -1), name='TX06')
        self.tc7 = wx.StaticText(self, -1, u'最低价格：', pos=(1230, 380), size=(60, -1), style=wx.ALIGN_RIGHT)
        self.tx7 = wx.TextCtrl(self, -1, '0.00', pos=(1300, 380), size=(150, -1), name='TX07')
        self.tc8 = wx.StaticText(self, -1, u'最高价格：', pos=(1230, 410), size=(60, -1), style=wx.ALIGN_RIGHT)
        self.tx8 = wx.TextCtrl(self, -1, '999.99', pos=(1300, 410), size=(150, -1), name='TX08')
        self.tc9 = wx.StaticText(self, -1, u'排序属性：', pos=(1230, 450), size=(60, -1), style=wx.ALIGN_RIGHT)
        self.choice = ['书名','类别','作者','年份','价格','库存']
        self.choose_attr = wx.Choice(self, -1, choices=self.choice, pos=(1300, 450), size=(100, 25))
        self.choose_attr.SetSelection(0)
        self.method = ['升序', '降序']
        self.choose_method = wx.Choice(self, -1, choices=self.method, pos=(1300, 480), size=(100, 25))
        self.choose_method.SetSelection(0)
        self.btn_se = wx.Button(self, -1, u'查询', pos=(1280, 550), size=(100, 25))

        self.Bind(wx.EVT_BUTTON, self.OnSe, self.btn_se)

    def OnSe(self, evt):
        '''条件查询事件函数'''
        title = self.tx1.GetValue()
        category = self.tx2.GetValue()
        press = self.tx3.GetValue()
        author = self.tx4.GetValue()
        year_s = int(self.tx5.GetValue())
        year_e = int(self.tx6.GetValue())
        price_s = float(self.tx7.GetValue())
        price_e = float(self.tx8.GetValue())
        attr = self.choose_attr.GetString(self.choose_attr.GetSelection())
        method = self.choose_method.GetString(self.choose_method.GetSelection())
        #print(title,category,press,author,year_s,year_e,price_s,price_e)
        dbm = select()
        data = dbm.select_attr(title,category,press,author,year_s,year_e,price_s,price_e,attr,method)
        #print(data)
        self.gridb.ClearGrid()
        for row, ele in enumerate(data):
            l_ShowRow = row
            for col,value in enumerate(ele):
                l_ShowCol = col
                if l_ShowCol>=0:
                    if type(value) is not str:
                        value = str(value)
                    self.gridb.SetCellValue(l_ShowRow,l_ShowCol,value)
        self.gridb.ForceRefresh()
        self.gridb.EnableEditing(False)

    def _DestroySearchGrid(self):
        self.gridb.Destroy()
        self.tc1.Destroy()
        self.tx1.Destroy()
        self.tc2.Destroy()
        self.tx2.Destroy()
        self.tc3.Destroy()
        self.tx3.Destroy()
        self.tc4.Destroy()
        self.tx4.Destroy()
        self.tc5.Destroy()
        self.tx5.Destroy()
        self.tc6.Destroy()
        self.tx6.Destroy()
        self.tc7.Destroy()
        self.tx7.Destroy()
        self.tc8.Destroy()
        self.tx8.Destroy()
        self.tc9.Destroy()
        self.choose_attr.Destroy()
        self.choose_method.Destroy()
        self.btn_se.Destroy()

    def OnClose(self, evt):
        '''关闭窗口事件函数'''

        dlg = wx.MessageDialog(None, u'确定要退出系统？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
        if (dlg.ShowModal() == wx.ID_YES):
            exit(0)