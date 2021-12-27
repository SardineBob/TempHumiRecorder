import os
from datetime import datetime
from utilset.SqlLiteUtil import SqlLiteUtil


# 將讀取到的溫濕度紀錄在DB
# 每年的溫度紀錄，會集中在同一個sqlLite db 檔案，也就是每年都會開不同db檔案存放溫度紀錄
class DbAccessUtil():

    __dbPath = "dbfile"
    __dbFilePath = None
    __sqlLiteUtil = None

    def __init__(self):
        self.__sqlLiteUtil = SqlLiteUtil()
        # 先檢查dbfile是否存在
        self.__checkDB()

    # 將溫濕度寫入DB
    def writeTempHumi(self, para):
        # 將溫濕度insert到DB
        self.__insertTemperature(para)

    # 檢查今年的DB是否已產生
    def __checkDB(self):
        # 取得今年db檔案路徑
        dbFile = datetime.now().strftime('%Y') + '.db'
        # 檢查路徑是否存在，不存在則建立
        if os.path.exists(self.__dbPath) is False:
            os.makedirs(self.__dbPath)
        # 檢查今年DB檔案是否存在，不存在則開啟
        self.__dbFilePath = os.path.join(self.__dbPath, dbFile)
        if os.path.isfile(self.__dbFilePath) is False:
            self.__createDB()

    # 產生DB檔案
    def __createDB(self):
        # create RecorderList table
        command = "CREATE TABLE RecordList(\
            ID Text NOT NULL,\
            Name Text NOT NULL,\
            RecordTime Text NOT NULL,\
            Temperature REAL NOT NULL,\
            Humidity REAL NOT NULL,\
            IsTempUnusual INTEGER NOT NULL,\
            IsHumiUnusual INTEGER NOT NULL,\
            UpTempLimit REAL NOT NULL,\
            LowTempLimit REAL NOT NULL,\
            UpHumiLimit REAL NOT NULL,\
            LowHumiLimit REAL NOT NULL,\
            DeviceMac Text NOT NULL,\
            Battery REAL NOT NULL,\
            PRIMARY KEY (ID, RecordTime)\
        )"
        # do create db
        self.__sqlLiteUtil.Execute(self.__dbFilePath, command, [])

    # insert溫度資料
    def __insertTemperature(self, para):
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # insert 指令
        command = " INSERT INTO RecordList VALUES (:id, :name, :recordTime, :temperature, :humidity, :isTempUnusual, :isHumiUnusual, :upTempLimit, :lowTempLimit, :upHumiLimit, :lowHumiLimit, :deviceMac, :battery) "
        parameter = {
            'id': para['id'],
            'name': para['name'],
            'recordTime': now,
            'temperature': para['temperature'],
            'humidity': para['humidity'],
            'isTempUnusual': 1 if para['isTempUnusual'] is True else 0,
            'isHumiUnusual': 1 if para['isHumiUnusual'] is True else 0,
            'upTempLimit': para['upTempLimit'],
            'lowTempLimit': para['lowTempLimit'],
            'upHumiLimit': para['upHumiLimit'],
            'lowHumiLimit': para['lowHumiLimit'],
            'deviceMac': para['deviceMac'],
            'battery': para['battery']
        }
        # do insert to db
        self.__sqlLiteUtil.Execute(self.__dbFilePath, command, parameter)

    # 取得今日異常紀錄清單
    def getTodayUnusualRecord(self, **para):
        command = " SELECT Name, RecordTime, Temperature, Humidity, IsTempUnusual, IsHumiUnusual FROM RecordList WHERE 1=1 "
        parameter = {}
        # 取得查詢條件
        queryRecordDate = datetime.now().strftime('%Y/%m/%d') if "recordDate" not in para else para["recordDate"]
        queryID = None if "tagID" not in para else para["tagID"]
        queryTempUnusualStatus = None if "tempUnusualStatus" not in para else para["tempUnusualStatus"]
        queryHumiUnusualStatus = None if "humiUnusualStatus" not in para else para["humiUnusualStatus"]
        # 開始根據條件搜尋
        if queryRecordDate is not None:
            command += " AND RecordTime LIKE :date "
            parameter["date"] = queryRecordDate + "%"
        if queryID is not None:
            command += " AND ID= :id "
            parameter["id"] = queryID
        if queryTempUnusualStatus is not None:
            if queryTempUnusualStatus != "all":
                command += " AND IsTempUnusual= :isTempUnusual "
                parameter["isTempUnusual"] = 1 if queryTempUnusualStatus == "Y" else 0
        if queryHumiUnusualStatus is not None:
            if queryHumiUnusualStatus != "all":
                command += " AND IsHumiUnusual= :isHumiUnusual "
                parameter["isHumiUnusual"] = 1 if queryHumiUnusualStatus == "Y" else 0
        # 加入排序語法
        command += " ORDER BY RecordTime DESC "
        # 加工將List<tuple>轉List<Object>型態
        data = []
        result = SqlLiteUtil().Execute(self.__dbFilePath, command, parameter)
        for item in result:
            data.append({
                'Name': item[0],
                'RecordTime': item[1],
                'Temperature': item[2],
                'Humidity': item[3],
                'IsTempUnusual': item[4],
                'IsHumiUnusual': item[5]
            })
        return data

    # select溫度資料(目前for one year)
    def selectTemperature(self, para):
        # 回傳物件
        result = {
            'status': False,
            'message': '',
            'data': []
        }
        # 先判斷輸入查詢條件是否有效
        status, message = self.__checkQueryParameter(para)
        if status is False:
            result['message'] = message
            return result
        # 取出相關查詢參數值
        dbYear = str(para['DBYear']) if 'DBYear' in para else None
        id = str(para['ID']) if 'ID' in para else None
        dateTimeStart = str(para['DateTimeStart']
                            ) if 'DateTimeStart' in para else None
        dateTimeEnd = str(para['DateTimeEnd']
                          ) if 'DateTimeEnd' in para else None
        # 處理一下日期格式
        if dateTimeStart is not None or dateTimeEnd is not None:
            callback = self.__refinDateTime(dateTimeStart, dateTimeEnd)
            if callback['status'] is False:
                result['message'] = callback['message']
                return result
            dateTimeStart, dateTimeEnd = callback['data']
        # 產生DB路徑
        dbFile = dbYear + '.db'
        dbFilePath = os.path.join(self.__dbPath, dbFile)
        # 檢查有沒有這個年度的db file
        if os.path.isfile(dbFilePath) is False:
            result['message'] = str(dbYear) + "這個年度無溫度數據資料。"
            return result
        # select 指令
        sqlPara = {}
        command = " SELECT * FROM RecordList WHERE 1==1 "
        # 加入溫控棒ID查詢條件
        if id is not None:
            command += " AND ID=:ID "
            sqlPara['ID'] = id
        # 加入日期查詢條件
        if dateTimeStart is not None or dateTimeEnd is not None:
            command += " AND RecordTime BETWEEN :SDateTime AND :EDateTime "
            sqlPara['SDateTime'] = dateTimeStart
            sqlPara['EDateTime'] = dateTimeEnd
        # get data from db
        data = self.__sqlLiteUtil.Execute(dbFilePath, command, sqlPara)
        result['status'] = True
        result['data'] = data
        return result

    # 檢查傳入的查詢條件是否有效
    def __checkQueryParameter(self, para):
        # 查詢年份(DBYear)一定要給，才知道取得哪一年的DB
        if 'DBYear' not in para:
            return False, "請給予查詢年份(參數為DBYear)，且需為四碼西元年"
        # DateTimeStart最少需給到4碼年度
        if 'DateTimeStart' in para:
            if len(str(para['DateTimeStart'])) < 4:
                return False, "查詢條件DateTimeStart，至少需有四碼西元年。"
        # DateTimeEnd最少需給到4碼年度
        if 'DateTimeEnd' in para:
            if len(str(para['DateTimeEnd'])) < 4:
                return False, "查詢條件DateTimeEnd，至少需有四碼西元年。"
        # 驗證完成
        return True, ""

    # 處理日期格式
    def __refinDateTime(self, SDateTime, EDateTime):
        result = {
            'status': False,
            'message': '',
            'data': (None, None)
        }
        # 進來的時候，SDateTime與EDateTime一定是其中一個有值
        SDateTime = EDateTime if SDateTime is None else SDateTime
        EDateTime = SDateTime if EDateTime is None else EDateTime
        # 根據傳入的查詢時間，最少4碼年度(2020)，最多19碼完整日期時間格式(2020/06/23 09:58:00)，不足的處理補到19碼
        try:
            SDateTime = {
                4: lambda dt: dt + '/01/01 00:00:00',
                7: lambda dt: dt + '/01 00:00:00',
                10: lambda dt: dt + ' 00:00:00',
                13: lambda dt: dt + ':00:00',
                16: lambda dt: dt + ':00',
                19: lambda dt: dt,
            }[len(SDateTime)](SDateTime)
            EDateTime = {
                4: lambda dt: dt + '/12/31 23:59:59',
                7: lambda dt: dt + '/31 23:59:59',
                10: lambda dt: dt + ' 23:59:59',
                13: lambda dt: dt + ':59:59',
                16: lambda dt: dt + ':59',
                19: lambda dt: dt,
            }[len(EDateTime)](EDateTime)
        except Exception:
            result['message'] = "日期格式長度錯誤，支援的日期長度為；西元年度(2020)(4碼)、月份(2020/06)(7碼)、日期(2020/06/23)(10碼)、小時(2020/06/23 09)(13碼)、分鐘(2020/06/23 09:55)(16碼)、秒鐘(2020/06/23 09:55:00)(19碼)"
            return result
        # 處理完成
        result['status'] = True
        result['data'] = (SDateTime, EDateTime)
        return result