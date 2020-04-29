from dbapi.dbapi import sqlserverapi

class trigger:
    def __init__(self, dbapi = sqlserverapi()):
        self._dbapi = dbapi

    def delete_card_check(self):
        '''检查注销借书证时该证有无未还记录'''
        tr_del_card = """
                CREATE TRIGGER tr_del_card
                ON card
                INSTEAD OF DELETE AS
                IF EXISTS(SELECT * FROM deleted, borrow
                        WHERE deleted.cno=borrow.cno AND borrow.return_date IS NULL)        
                BEGIN 
                    RAISERROR ('有记录未处理不可注销',16,1)
                    ROLLBACK
				END
				ELSE
				BEGIN
					DELETE FROM card WHERE cno=(SELECT cno FROM deleted)
                END 
                """

        out = self._dbapi.ExcuteDMLSQL(tr_del_card)
        print(out)

    def borrow_check(self):
        '''余量检查，重复借检查'''
        tr_borrow_check = """
                    CREATE TRIGGER tr_borrow_check
                    ON borrow
                    INSTEAD OF INSERT AS
                    IF 0=(SELECT stock FROM inserted, book
                            WHERE inserted.bno=book.bno)                            
                    BEGIN 
                        RAISERROR('库存不足',16,1)
                        ROLLBACK 
					END
					ELSE IF	
						EXISTS (SELECT * FROM borrow, inserted
                            WHERE borrow.bno=inserted.bno AND borrow.cno=inserted.cno 
                            AND borrow.return_date is null) 
					BEGIN 
                        RAISERROR('已经借入',16,1)
                        ROLLBACK 
					END
					ELSE
					BEGIN				
						INSERT INTO borrow SELECT * FROM inserted
                    END
                    """

        out = self._dbapi.ExcuteDMLSQL(tr_borrow_check)
        print(out)

    def borrow_update(self):
        '''借出数据更新'''
        tr_borrow_update = """
                    CREATE TRIGGER tr_borrow_update
                    FOR borrow
                    AFTER INSERT AS      
                    BEGIN 
                        UPDATE book 
                        SET stock = (SELECT stock - 1 FROM book, inserted
                                    WHERE book.bno = inserted.bno)
									WHERE book.bno = (SELECT bno FROM inserted)
                    END
                    """

        out = self._dbapi.ExcuteDMLSQL(tr_borrow_update)
        print(out)

    def return_update(self):
        '''还书数据更新'''
        tr_return_update = """
                    CREATE TRIGGER tr_return_update
                    ON borrow
                    AFTER UPDATE AS 
                    IF UPDATE(return_date)     
                    BEGIN 
                        UPDATE book 
                        SET stock = (SELECT stock + 1 FROM book, inserted
                                    WHERE book.bno = inserted.bno)
                                    WHERE book.bno = (SELECT bno FROM inserted)
                    END
                    """

        out = self._dbapi.ExcuteDMLSQL(tr_return_update)
        print(out)

