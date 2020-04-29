from dbapi.dbapi import sqlserverapi

class delete:
    def __init__(self, dbapi = sqlserverapi(), out = ''):
        self._dbapi = dbapi
        self._out = out

    def delete_card(self, cno):
        '''删除借书卡号'''
        sql = "DELETE FROM card WHERE cno='{}'".format(cno)
        self._out = self._dbapi.ExcuteDMLSQL(sql)
        #print(self._out)