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


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    id_login = wx.NewId()
    id_account = wx.NewId()
    id_quit = wx.NewId()
    id_info = wx.NewId()

    id_help = wx.NewId()
    id_about = wx.NewId()

    id_insert = wx.NewId()
    id_borrow = wx.NewId()
    id_search = wx.NewId()
    id_delete = wx.NewId()


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

        self._CreateInsertGrid()
        self._DestroyInsertGrid()
        self._CreateSearchGrid()
        self._DestroySearchGrid()
        self._CreateBorrowGrid()
        self._DestroyBorrowGrid()
        self._CreateCardGrid()
        self._DestroyCardGrid()

    def _DestroyInsertGrid(self):
        self.grida.Destroy()
        self.btn_in.Destroy()
        self.btn_open.Destroy()
        self.btn_read.Destroy()
        self.FileName.Destroy()

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

    def _DestroyBorrowGrid(self):
        self.gridd.Destroy()
        self.tcc1.Destroy()
        self.txx1.Destroy()
        self.btn_sea.Destroy()
        self.tcc2.Destroy()
        self.txx2.Destroy()
        self.btn_bor.Destroy()
        self.btn_ret.Destroy()

    def _DestroyCardGrid(self):
        self.gridc.Destroy()
        self.btn_add.Destroy()
        self.tc.Destroy()
        self.tx.Destroy()
        self.btn_del.Destroy()

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
        with open('mno.txt','r') as f:
            mno = f.read()
            f.close()
        dbm = select()
        name = dbm.get_manager_name(mno)[0][0]
        dlg = wx.MessageDialog(None, u'用户：{}\n姓名：{}'.format(mno, name), u'信息', wx.OK)
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

        ico_insert = wx.Bitmap('res/insert.ico', wx.BITMAP_TYPE_ANY)
        ico_search = wx.Bitmap('res/search.ico', wx.BITMAP_TYPE_ANY)
        ico_borrow = wx.Bitmap('res/borrow.ico', wx.BITMAP_TYPE_ANY)
        ico_account = wx.Bitmap('res/account.ico', wx.BITMAP_TYPE_ANY)

        self.tb = wx.ToolBar(self)
        self.tb.SetToolBitmapSize((16, 16))

        self.tb.AddLabelTool(self.id_insert, u'图书入库', ico_insert, shortHelp=u'入库', longHelp=u'导入图书信息或批量导入')
        self.tb.AddLabelTool(self.id_search, u'图书查询', ico_search, shortHelp=u'查询', longHelp=u'查找图书相关信息')
        self.tb.AddSeparator()
        self.tb.AddLabelTool(self.id_borrow, u'借书与还书', ico_borrow, shortHelp=u'借书与还书', longHelp=u'借还书事务登记')
        self.tb.AddLabelTool(self.id_account, u'账户管理', ico_account, shortHelp=u'账户', longHelp=u'借书卡信息管理')

        # self.Bind(wx.EVT_TOOL_RCLICKED, self.OnOpen, id=self.id_open)

        self.Bind(wx.EVT_MENU, self.OnInsert, id=self.id_insert)
        self.Bind(wx.EVT_MENU, self.OnSearch, id=self.id_search)
        self.Bind(wx.EVT_MENU, self.OnBorrow, id=self.id_borrow)
        self.Bind(wx.EVT_MENU, self.OnAccount, id=self.id_account)

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

        self.grid = wx.grid.Grid(self, -1, pos=(25, 170), size=(1200,370))
        self.grid.CreateGrid(80, 9)
        self.grid.SetDefaultColSize(120, resizeExistingCols=True)
        self.grid.SetDefaultCellOverflow(False)
        GridLabelToDBLabel = [(0, '书号'), (1, '类别'), (2, '书名'), (3, '出版社'), (4, '年份'), (5, '作者'), (6, '价格'), (7, '总藏书量'),
                              (8, '库存')]
        for i, tup in enumerate(GridLabelToDBLabel):
            self.grid.SetColLabelValue(i, tup[1])
        self.grid.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        s = select()
        data = s.select_all()
        for row, ele in enumerate(data):
            l_ShowRow = row
            for col,value in enumerate(ele):
                l_ShowCol = col
                if l_ShowCol>=0:
                    if type(value) is not str:
                        value = str(value)
                    self.grid.SetCellValue(l_ShowRow,l_ShowCol,value)

        self.grid.EnableEditing(False)

    def OnLogin(self, evt):
        '''切换账户，退出到登录界面'''
        self.UpdateUI(0)
        #self.Destroy()

    def OnInsert(self, evt):
        '''图书入库'''
        if self.grida:
            return
        if self.gridb:
            self._DestroySearchGrid()
        if self.gridc:
            self._DestroyCardGrid()
        if self.gridd:
            self._DestroyBorrowGrid()
        self._CreateInsertGrid()
        self.sb.SetStatusText(u'图书入库', 1)

    def OnSearch(self, evt):
        '''图书查询'''
        if self.grida:
            self._DestroyInsertGrid()
        if self.gridb:
            return
        if self.gridc:
            self._DestroyCardGrid()
        if self.gridd:
            self._DestroyBorrowGrid()
        self._CreateSearchGrid()
        self.sb.SetStatusText(u'图书查询', 1)

    def OnBorrow(self, evt):
        '''借还书处理'''
        if self.grida:
            self._DestroyInsertGrid()
        if self.gridb:
            self._DestroySearchGrid()
        if self.gridc:
            self._DestroyCardGrid()
        if self.gridd:
            return
        self._CreateBorrowGrid()
        self.sb.SetStatusText(u'借还书处理', 1)

    def OnAccount(self, evt):
        '''账户管理'''
        if self.grida:
            self._DestroyInsertGrid()
        if self.gridb:
            self._DestroySearchGrid()
        if self.gridc:
            return
        if self.gridd:
            self._DestroyBorrowGrid()
        self._CreateCardGrid()
        self.sb.SetStatusText(u'账户管理', 1)

    def _CreateInsertGrid(self):
        '''显示插入操作表格'''
        self.grida = wx.grid.Grid(self, -1, pos=(25, 600), size=(1200, 100))
        self.grida.CreateGrid(1, 8)
        self.grida.SetDefaultColSize(120, resizeExistingCols=True)
        self.grida.SetDefaultCellOverflow(False)
        GridLabelToDBLabel = [(0, '书号'), (1, '类别'), (2, '书名'), (3, '出版社'), (4, '年份'), (5, '作者'), (6, '价格'), (7, '总藏书量')]
        for i, tup in enumerate(GridLabelToDBLabel):
            self.grida.SetColLabelValue(i, tup[1])
        self.grida.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.grida.SetCellEditor(0, 4, wx.grid.GridCellNumberEditor(1900, 2019))
        self.grida.SetCellEditor(0, 6, wx.grid.GridCellFloatEditor(precision=2))
        self.grida.SetCellEditor(0, 7, wx.grid.GridCellNumberEditor(1, 500))

        self.btn_in = wx.Button(self, -1, u'入库', pos=(1300, 300), size=(100, 25))
        self.Bind(wx.EVT_BUTTON, self.OnIn, self.btn_in)
        self.btn_open = wx.Button(self, -1, '>>', pos=(1270, 450), size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnOp, self.btn_open)
        self.FileName = wx.TextCtrl(self, pos=(1300, 450), size=(230, 25))
        self.btn_read = wx.Button(self, -1, u'批量入库', pos=(1300, 600), size=(100, 25))
        self.Bind(wx.EVT_BUTTON, self.OnRe, self.btn_read)

    def OnIn(self, evt):
        '''单本入库事件函数'''
        bno = self.grida.GetCellValue(0, 0)
        category = self.grida.GetCellValue(0,1)
        title = self.grida.GetCellValue(0,2)
        press = self.grida.GetCellValue(0,3)
        year = self.grida.GetCellValue(0,4)
        author = self.grida.GetCellValue(0,5)
        price = self.grida.GetCellValue(0,6)
        num = self.grida.GetCellValue(0,7)
        if bno=='' or category=='' or title=='' or \
            press=='' or year=='' or author=='' or \
            price=='' or num=='':
            self.sb.SetStatusText(u'异常', 2)
            dlg = wx.MessageDialog(None, u'信息有误，入库失败！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            dbm = insert()
            dbm.insert_single(bno,category,title,press,year,author,price,num)
            status = dbm._out
            if status == 'SUCCESSED':
                self.sb.SetStatusText(u'正常', 2)
                dlg = wx.MessageDialog(None, u'入库成功', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
                self.grid.Destroy()
                self._CreateGrid()
                self.grida.DeleteRows(pos=0, numRows=1)
                self.grida.InsertRows(pos=0, numRows=1)
                self.grida.SetCellEditor(0, 4, wx.grid.GridCellNumberEditor(1900, 2019))
                self.grida.SetCellEditor(0, 6, wx.grid.GridCellFloatEditor(precision=2))
                self.grida.SetCellEditor(0, 7, wx.grid.GridCellNumberEditor(1, 500))
            else:
                self.sb.SetStatusText(u'异常', 2)
                dlg = wx.MessageDialog(None, u'信息有误，入库失败！', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()

    def OnOp(self, evt):
        '''选择文件事件函数'''
        wildcard = 'TXT files(*.txt)|*.txt'
        dlg = wx.FileDialog(None, u'选择', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.FileName.SetValue(dlg.GetPath())
            dlg.Destroy

    def OnRe(self, evt):
        '''批量入库事件函数'''
        if self.FileName.GetValue()=='':
            self.sb.SetStatusText(u'异常', 2)
            dlg = wx.MessageDialog(None, u'信息有误，入库失败！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            file = open(self.FileName.GetValue())
            info = file.readlines()
            print(info)
            file.close()
            dbm = insert()
            dbm.insert_multi(info)
            status = dbm._out
            if 'FAILED' not in status:
                self.sb.SetStatusText(u'正常', 2)
                dlg = wx.MessageDialog(None, u'成功入库{}本，失败0本'.format(len(info)), u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            else:
                self.sb.SetStatusText(u'异常', 2)
                su = status.count('SUCCESSED')
                fa = status.count('FAILED')
                dlg = wx.MessageDialog(None, u'成功入库{}本，失败{}本'.format(su, fa), u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            self.grid.Destroy()
            self._CreateGrid()

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

    def _CreateCardGrid(self):
        '''显示借书卡表格'''
        self.gridc = wx.grid.Grid(self, -1, pos=(25, 550), size=(700, 200))
        self.gridc.CreateGrid(20, 4)
        self.gridc.SetDefaultColSize(120, resizeExistingCols=True)
        self.gridc.SetDefaultCellOverflow(False)
        GridLabelToDBLabel = [(0, '卡号'), (1, '姓名'), (2, '单位'), (3, '身份类别')]
        for i, tup in enumerate(GridLabelToDBLabel):
            self.gridc.SetColLabelValue(i, tup[1])
        self.gridc.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        s = select()
        data = s.select_card()
        for row, ele in enumerate(data):
            l_ShowRow = row
            for col, value in enumerate(ele):
                l_ShowCol = col
                if l_ShowCol >= 0:
                    if type(value) is not str:
                        value = str(value)
                    self.gridc.SetCellValue(l_ShowRow, l_ShowCol, value)
                    self.gridc.SetReadOnly(l_ShowRow, l_ShowCol)
        self.add_row = len(data)

        self.btn_add = wx.Button(self, -1, u'添加', pos=(1300, 270), size=(100, 25))
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.btn_add)
        self.tc = wx.StaticText(self, -1, u'要删除的卡号：', pos=(1250, 350), size=(100, -1), style=wx.ALIGN_RIGHT)
        self.tx = wx.TextCtrl(self, -1, '', pos=(1350, 350), size=(150, -1), name='TX')
        self.btn_del = wx.Button(self, -1, u'删除', pos=(1300, 400), size=(100, 25))
        self.Bind(wx.EVT_BUTTON, self.OnDel, self.btn_del)

    def OnAdd(self, evt):
        '''添加借书卡'''
        #print(self.add_row)
        if self.gridc.GetCellValue(self.add_row, 0) == '' or self.gridc.GetCellValue(self.add_row, 1) == '' or \
            self.gridc.GetCellValue(self.add_row,2) == '' or self.gridc.GetCellValue(self.add_row, 3) == '':
            self.sb.SetStatusText(u'异常', 2)
            dlg = wx.MessageDialog(None, u'信息有误，添加失败！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            info = (self.gridc.GetCellValue(self.add_row, 0),self.gridc.GetCellValue(self.add_row, 1),
                self.gridc.GetCellValue(self.add_row, 2),self.gridc.GetCellValue(self.add_row, 3))
            dbm = insert()
            dbm.insert_card(info)
            status = dbm._out
            if status == 'SUCCESSED':
                dlg = wx.MessageDialog(None, u'添加成功', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
                self.sb.SetStatusText(u'正常', 2)
                self._DestroyCardGrid()
                self._CreateCardGrid()
            else:
                self.sb.SetStatusText(u'异常', 2)
                dlg = wx.MessageDialog(None, u'信息有误，添加失败！', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()

    def OnDel(self, evt):
        '''删除借书卡'''
        delcno = self.tx.GetValue()
        if delcno == '':
            self.sb.SetStatusText(u'异常', 2)
            dlg = wx.MessageDialog(None, u'信息有误，删除失败！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            dlg = wx.MessageDialog(None, u'确定要删除这个借书卡吗？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
            if (dlg.ShowModal() == wx.ID_YES):
                dbm = delete()
                dbm.delete_card(delcno)
                status = dbm._out
                if status == 'SUCCESSED':
                    self.sb.SetStatusText(u'正常', 2)
                    dlg1 = wx.MessageDialog(None, u'删除成功', u'操作提示', wx.OK)
                    if (dlg1.ShowModal() == wx.OK):
                        dlg1.Destroy()
                else:
                    self.sb.SetStatusText(u'异常', 2)
                    dlg1 = wx.MessageDialog(None, u'有未处理的记录，删除失败！', u'操作提示', wx.OK)
                    if (dlg1.ShowModal() == wx.OK):
                        dlg1.Destroy()
            elif (dlg.ShowModal() == wx.ID_NO):
                dlg.Destroy()
            self._DestroyCardGrid()
            self._CreateCardGrid()

    def _CreateBorrowGrid(self):
        '''显示借书卡表格'''

        self.gridd = wx.grid.Grid(self, -1, pos=(25, 550), size=(800, 200))
        self.gridd.CreateGrid(20, 5)
        self.gridd.SetDefaultColSize(120, resizeExistingCols=True)
        self.gridd.SetDefaultCellOverflow(False)
        GridLabelToDBLabel = [(0, '卡号'), (1, '书号'), (2, '经手人'), (3, '借期'), (4,'还期')]
        for i, tup in enumerate(GridLabelToDBLabel):
            self.gridd.SetColLabelValue(i, tup[1])
        self.gridd.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.gridd.EnableEditing(False)
        self.tcc1 = wx.StaticText(self, -1, u'卡号：', pos=(1250, 200), size=(50, -1), style=wx.ALIGN_RIGHT)
        self.txx1 = wx.TextCtrl(self, -1, '', pos=(1300, 200), size=(150, -1), name='TXX01')
        self.btn_sea = wx.Button(self, -1, u'查询', pos=(1280, 300), size=(100, 25))
        self.tcc2 = wx.StaticText(self, -1, u'书号：', pos=(1250, 400), size=(50, -1), style=wx.ALIGN_RIGHT)
        self.txx2 = wx.TextCtrl(self, -1, '', pos=(1300, 400), size=(150, -1), name='TXX02')
        self.btn_bor = wx.Button(self, -1, u'借书', pos=(1280, 500), size=(100, 25))
        self.btn_ret = wx.Button(self, -1, u'还书', pos=(1280, 550), size=(100, 25))

        self.Bind(wx.EVT_BUTTON, self.OnSea, self.btn_sea)
        self.Bind(wx.EVT_BUTTON, self.OnBor, self.btn_bor)
        self.Bind(wx.EVT_BUTTON, self.OnRet, self.btn_ret)

    def OnSea(self, evt):
        '''查询借书记录'''
        cno = self.txx1.GetValue()
        dbm = select()
        data = dbm.select_borrow(cno)
        # print(data)
        if data == 'ERROR':
            dlg = wx.MessageDialog(None, u'没有这个卡号', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            self.gridd.ClearGrid()
            for row, ele in enumerate(data):
                l_ShowRow = row
                for col, value in enumerate(ele):
                    l_ShowCol = col
                    if l_ShowCol >= 0:
                        if type(value) is not str:
                            value = str(value)
                        self.gridd.SetCellValue(l_ShowRow, l_ShowCol, value)
            self.gridd.ForceRefresh()
            self.gridd.EnableEditing(False)
            self.sb.SetStatusText(u'正在处理：卡号为{}'.format(cno), 1)

    def OnBor(self, evt):
        '''借书'''
        f = open('mno.txt')
        mno = f.read()
        f.close()
        cno = self.txx1.GetValue()
        bno = self.txx2.GetValue()
        borrow_date = time.strftime("%Y-%m-%d", time.localtime())
        if cno == '' or bno == '':
            self.sb.SetStatusText(u'异常', 2)
            dlg = wx.MessageDialog(None, u'信息有误，借书失败！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            dbm = insert()
            dbm.borrow(cno, bno, mno, borrow_date)
            status = dbm._out
            if status == 'SUCCESSED':
                self.sb.SetStatusText(u'正常', 2)
                dlg = wx.MessageDialog(None, u'借书成功', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            elif status == 'NOBOOK':
                self.sb.SetStatusText(u'异常', 2)
                dlg = wx.MessageDialog(None, u'未找到该书，借书失败！', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            else:
                self.sb.SetStatusText(u'异常', 2)
                dbm = select()
                ret = dbm.select_return_date(bno)
                msg = u'库存不足或已拥有该书，借书失败！\n最近还书日期：{}'.format(ret)
                dlg = wx.MessageDialog(None, msg, u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            self.grid.Destroy()
            self._CreateGrid()
            self.OnSea('')

    def OnRet(self, evt):
        '''还书'''
        cno = self.txx1.GetValue()
        bno = self.txx2.GetValue()
        return_date = time.strftime("%Y-%m-%d", time.localtime())
        if cno == '' or bno == '':
            self.sb.SetStatusText(u'异常', 2)
            dlg = wx.MessageDialog(None, u'信息有误，还书失败！', u'操作提示', wx.OK)
            if (dlg.ShowModal() == wx.OK):
                dlg.Destroy()
        else:
            dbm = insert()
            dbm.ret(cno, bno, return_date)
            status = dbm._out
            if status == 'SUCCESSED':
                self.sb.SetStatusText(u'正常', 2)
                dlg = wx.MessageDialog(None, u'还书成功', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            else:
                self.sb.SetStatusText(u'异常', 2)
                dlg = wx.MessageDialog(None, u'信息有误，还书失败！', u'操作提示', wx.OK)
                if (dlg.ShowModal() == wx.OK):
                    dlg.Destroy()
            self.grid.Destroy()
            self._CreateGrid()
            self.OnSea('')

    def OnClose(self, evt):
        '''关闭窗口事件函数'''

        dlg = wx.MessageDialog(None, u'确定要退出系统？', u'操作提示', wx.YES_NO | wx.ICON_QUESTION)
        if (dlg.ShowModal() == wx.ID_YES):
            exit(0)




class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
