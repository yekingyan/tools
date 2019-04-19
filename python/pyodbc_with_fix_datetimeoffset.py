# -*- coding:utf-8 -*-

import struct
import pyodbc

class Db:
    @staticmethod
    def handle_datetimeoffset(dto_value):
        """
        add 转 datetimeoffset
        """
        # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
        tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
        tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

    def connect_db(self):
        """
        连接数据库
        """
        db = DATABASES['default']
        driver = db['OPTIONS']['driver']
        server = db['HOST']
        database = db['NAME']
        uid = db['USER']
        pwd = db['PASSWORD']
        cnxn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}")
        # cnxn = pyodbc.connect("DRIVER=ODBC Driver 17 for SQL Server;SERVER=yunzhusqlb2.database.chinacloudapi.cn;DATABASE=DataPool;UID=yzsqlb2;PWD=yz6699_2525")
        cnxn.add_output_converter(-155, self.handle_datetimeoffset)
        cursor = cnxn.cursor()
        return cursor

a = Db()
cursor = a.connect_db()
cursor.execute("select * from Wit_Key_Store")
rows = cursor.fetchall()
for row in rows:
    print(row.Store_Id, row.Create_Date, 1)
