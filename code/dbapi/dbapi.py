import pymssql

class sqlserverapi:
    def __init__(self,server='localhost',user='sa',password='jiarun20010308',dbname='bmg'):
        self._server = server
        self._user = user
        self._password = password
        self._dbname = dbname

    def ExcuteDMLSQL(self,sql):
        """
        执行DML操作
        :return:
        """
        try:
            conn = pymssql.connect(self._server, self._user, self._password, self._dbname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 'SUCCESSED'
        except pymssql.Error as err:
            print(err)
            return 'FAILED'

    def ExcuteDMLSQLSelect(self,sql):
        """
        执行DML查询操作
        :return:
        """
        try:
            conn = pymssql.connect(self._server, self._user, self._password, self._dbname)
            cursor = conn.cursor()
            cursor.execute(sql)

            data = cursor.fetchall()

            return data
        except pymssql.Error as err:
            return err
