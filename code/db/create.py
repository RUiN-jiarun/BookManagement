from dbapi.dbapi import sqlserverapi

class create:
    def __init__(self, dbapi = sqlserverapi()):
        self._dbapi = dbapi

    def create_book(self):
        book = """
        IF OBJECT_ID('book', 'U') IS NOT NULL
          DROP TABLE book
        CREATE TABLE book(
        bno 		varchar(20) PRIMARY KEY, 
        category 	varchar(30),
        title 		varchar(40),
        press		varchar(30),
        year		int,
        author		varchar(20),
        price		decimal(7,2),
        total		int,
        stock		int)
        """

        out = self._dbapi.ExcuteDMLSQL(book)
        print(out)

    def create_card(self):
        card = """
        IF OBJECT_ID('card', 'U') IS NOT NULL
          DROP TABLE card
        CREATE TABLE card(
        cno			varchar(20) PRIMARY KEY,
        name		varchar(10),
        department	varchar(40),
        type		char(1),
        CHECK (type IN ('T','S','M'))) 
        """

        out = self._dbapi.ExcuteDMLSQL(card)
        print(out)

    def create_manager(self):
        manager= """
        IF OBJECT_ID('manager', 'U') IS NOT NULL
          DROP TABLE manager
        CREATE TABLE manager(
        mno         varchar(20) PRIMARY KEY,
        password    varchar(20),
        name        varchar(10),
        tel         varchar(20))
        """

        out = self._dbapi.ExcuteDMLSQL(manager)
        print(out)

    def create_borrow(self):
        borrow = """
        IF OBJECT_ID('borrow', 'U') IS NOT NULL
          DROP TABLE borrow
        CREATE TABLE borrow(
        cno				varchar(20),
        bno				varchar(20),      
        mno             varchar(20),
        borrow_date		varchar(30),
        return_date		varchar(30),
        FOREIGN KEY (bno)
            REFERENCES book(bno)
            ON DELETE CASCADE,
        FOREIGN KEY (cno)
            REFERENCES card(cno)
            ON DELETE CASCADE,
        FOREIGN KEY (mno)
            REFERENCES manager(mno)
            ON DELETE CASCADE)
        """

        out = self._dbapi.ExcuteDMLSQL(borrow)
        print(out)
