from dbapi.dbapi import sqlserverapi

class insert:
    def __init__(self, dbapi = sqlserverapi(), out = ''):
        self._dbapi = dbapi
        self._out = ''

    def insert_single(self, bno, category, title, press, year, author, price, num):
        '''单本入库'''
        sql_pre = "SELECT * FROM book WHERE bno='{}'".format(bno)
        if self._dbapi.ExcuteDMLSQLSelect(sql_pre)!=[]:
            sql = "UPDATE book " \
                  "SET total = (SELECT total+{} FROM book WHERE bno='{}') " \
                  "WHERE bno='{}'\n" \
                  "UPDATE book " \
                  "SET stock = (SELECT stock+{} FROM book WHERE bno='{}') " \
                  "WHERE bno='{}'".format(num,bno,bno,num,bno,bno)
            self._out = self._dbapi.ExcuteDMLSQL(sql)
        else:
            sql = "INSERT INTO book(bno, category, title, press, year, author, price, total, stock)" \
              " VALUES ('{}','{}','{}','{}',{},'{}',{},{},{})".format(bno, category, title, press, year, author, price, num, num)
            self._out = self._dbapi.ExcuteDMLSQL(sql)

    def insert_multi(self, info):
        '''批量入库'''
        num = len(info)
        for i in range(num):
            handled = info[i].lstrip('( ').rstrip(')\n').split(', ')
            sql_pre = "SELECT * FROM book WHERE bno='{}'".format(handled[0])
            if self._dbapi.ExcuteDMLSQLSelect(sql_pre) != []:
                sql = "UPDATE book " \
                      "SET total = (SELECT total+{} FROM book WHERE bno='{}') " \
                      "WHERE bno='{}'\n" \
                      "UPDATE book " \
                      "SET stock = (SELECT stock+{} FROM book WHERE bno='{}') " \
                      "WHERE bno='{}'".format(handled[7], handled[0], handled[0], handled[7], handled[0], handled[0])

            else:
                sql = "INSERT INTO book(bno, category, title, press, year, author, price, total, stock)" \
                  " VALUES ('{}','{}','{}','{}',{},'{}',{},{},{})".format(handled[0],handled[1],handled[2],
                                                                          handled[3],handled[4],handled[5],
                                                                          handled[6],handled[7],handled[7])
            sta = self._dbapi.ExcuteDMLSQL(sql)
            if sta == 'SUCCESSED':
                self._out += 'SUCCESSED '
            else:
                self._out += 'FAILED '

    def insert_card(self, info):
        '''添加借书卡'''
        sql = "INSERT INTO card(cno, name, department, type)" \
              " VALUES {}".format(info)
        self._out = self._dbapi.ExcuteDMLSQL(sql)

    def borrow(self, cno, bno, mno, borrow_date):
        '''添加借书记录'''
        sql_pre = "SELECT * FROM book WHERE bno='{}' ".format(bno)
        if self._dbapi.ExcuteDMLSQLSelect(sql_pre) == []:
            self._out = 'NOBOOK'
        else:
            sql = "INSERT INTO borrow(cno, bno, mno, borrow_date, return_date)" \
                " VALUES ('{}','{}','{}','{}',null)".format(cno, bno, mno, borrow_date)
            self._out = self._dbapi.ExcuteDMLSQL(sql)


    def ret(self, cno, bno, return_date):
        '''更新还书记录'''
        sql_pre = "SELECT * FROM borrow WHERE cno='{}' AND bno='{}' " \
                  "AND borrow_date is not null AND return_date is null".format(cno, bno)
        if self._dbapi.ExcuteDMLSQLSelect(sql_pre) == []:
            self._out = 'ERROR'
        else:
            sql = "UPDATE borrow " \
              "SET return_date = '{}' " \
              "WHERE cno = '{}' AND bno = '{}' AND return_date is null".format(return_date, cno, bno)
            self._out = self._dbapi.ExcuteDMLSQL(sql)
