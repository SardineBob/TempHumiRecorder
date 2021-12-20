import sqlite3


class SqlLiteUtil():

    def __init__(self):
        self.__dbFile = "dbfile/AbnormalRecord.db"

    # 執行SQL Lite指令
    def Execute(self, sqlcommand, sqlparamter):
        with sqlite3.connect(self.__dbFile) as conn:
            cur = conn.cursor()
            cur.execute(sqlcommand, sqlparamter)
            conn.commit()
            # 把結果轉為List<tuple>
            data = []
            for row in cur:
                data.append(row)
            return data
