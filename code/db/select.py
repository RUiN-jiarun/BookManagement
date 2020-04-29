from dbapi.dbapi import sqlserverapi

class select:
    def __init__(self, dbapi = sqlserverapi()):
        self._dbapi = dbapi

    def select_all(self):
        '''构建图书总表'''
        sql = "SELECT * FROM book"
        out = self._dbapi.ExcuteDMLSQLSelect(sql)
        return(out)

    def select_attr(self, title='', category='', press='', author='', year_s=1800, year_e=2020, price_s=0.00, price_e=999.99, attrname='', method=''):
        '''按属性查询书籍'''
        if attrname == '书名':
            attr = 'title'
        elif attrname == '类别':
            attr = 'category'
        elif attrname == '作者':
            attr = 'author'
        elif attrname == '年份':
            attr = 'year'
        elif attrname == '价格':
            attr = 'price'
        elif attrname == '库存':
            attr = 'stock'
        sql = "SELECT * FROM book WHERE "
        if title != '':
            sql += "title LIKE '%{}%' AND ".format(title)
        if category != '':
            sql += "category LIKE '%{}%' AND ".format(category)
        if press != '':
            sql += "press LIKE '%{}%' AND ".format(press)
        if author != '':
            sql += "author LIKE '%{}%' AND ".format(author)
        sql += "year BETWEEN {} AND {} AND ".format(int(year_s), int(year_e))
        sql += "price BETWEEN {} AND {} ".format(float(price_s), float(price_e))
        sql += "ORDER BY {} ".format(attr)
        if method == '升序':
            sql += "ASC"
        elif method == '降序':
            sql += "DESC"
        out = self._dbapi.ExcuteDMLSQLSelect(sql)
        return (out)

    def select_card(self):
        '''构建借书卡副表'''
        sql = "SELECT * FROM card"
        out = self._dbapi.ExcuteDMLSQLSelect(sql)
        return (out)

    def check_manager(self, mno=''):
        '''管理员密码检验'''
        sql = "SELECT password FROM manager WHERE mno='{}'".format(mno)
        out = self._dbapi.ExcuteDMLSQLSelect(sql)
        return (out)

    def get_manager_name(self, mno=''):
        '''管理员名字获取'''
        sql = "SELECT name FROM manager WHERE mno='{}'".format(mno)
        out = self._dbapi.ExcuteDMLSQLSelect(sql)
        return (out)

    def select_borrow(self, cno=''):
        '''借书记录查询'''
        sql_pre = "SELECT * FROM card WHERE card.cno='{}'".format(cno)
        if self._dbapi.ExcuteDMLSQLSelect(sql_pre) == []:
            return('ERROR')
        else:
            sql = "SELECT * FROM borrow WHERE borrow.cno='{}'".format(cno)
            out = self._dbapi.ExcuteDMLSQLSelect(sql)
            return (out)

    def select_return_date(self, bno=''):
        '''最近还书日期查询'''
        sql = "SELECT TOP 1 return_date FROM borrow WHERE borrow.bno='{}' " \
              "ORDER BY return_date DESC".format(bno)
        out = self._dbapi.ExcuteDMLSQLSelect(sql)
        return (str(out))




