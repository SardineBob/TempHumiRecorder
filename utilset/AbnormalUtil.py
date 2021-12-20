from utilset.SqlLiteUtil import SqlLiteUtil

# 處理異常紀錄寫DB的Util


class AbnormalUtil:

    # 新增一筆異常紀錄
    def InsertAbnormalRecord(self, para):
        # 取出相關資訊，準備Insert資料
        AlertTime = para["alertTime"]
        AlertID = para["alertID"]
        AlertName = para["alertName"]
        CameraInfos = para["cameraInfo"]  # this is array
        # 準備Insert INTO指令，並執行
        commands = []
        # insert into AbnormalList
        commands.append({
            'command': " INSERT INTO AbnormalList VALUES (:alerttime, :alertid, :alertname) ",
            'parameter': {
                'alerttime': AlertTime,
                'alertid': AlertID,
                'alertname': AlertName
            }
        })
        # insert into RecordList
        for camera in CameraInfos:
            commands.append({
                'command': " INSERT INTO RecordList VALUES (:alerttime, :alertid, :cameraid, :cameraname, :recordfilename) ",
                'parameter': {
                    'alerttime': AlertTime,
                    'alertid': AlertID,
                    'cameraid': camera['cameraID'],
                    'cameraname': camera['cameraName'],
                    'recordfilename': camera['recordFileName'],
                }
            })
        for command in commands:
            SqlLiteUtil().Execute(command['command'], command['parameter'])

    # 根據條件搜尋需要的異常紀錄
    def FindAbnormalRecord(self, AlertTime=None, AlertID=None):
        # 先取得異常紀錄清單，即保全器材的觸發時間點
        command = " SELECT AlertTime, AlertID, AlertName FROM AbnormalList WHERE 1=1 "
        parameter = {}
        # 開始根據條件搜尋
        if AlertTime is not None:
            command += " AND AlertTime LIKE :alerttime "
            parameter["alerttime"] = AlertTime + "%"
        if AlertID is not None:
            command += " AND AlertID=:alertid "
            parameter["alertid"] = AlertID
        # 加入排序語法
        command += " ORDER BY AlertTime DESC "
        # 加工將List<tuple>轉List<Object>型態
        data = []
        result = SqlLiteUtil().Execute(command, parameter)
        for item in result:
            data.append({
                'AlertTime': item[0],
                'AlertID': item[1],
                'AlertName': item[2]
            })

        return data

    # 根據警示時間以及警示點ID，查詢可查看的錄影片段清單
    def FindRecordList(self, AlertTime, AlertID):
        command = " SELECT CameraID, CameraName, RecordFileName FROM RecordList WHERE AlertTime=:alerttime AND AlertID=:alertid "
        parameter = {
            'alerttime': AlertTime,
            'alertid': AlertID
        }
        # 加工將List<tuple>轉List<Object>型態
        data = []
        result = SqlLiteUtil().Execute(command, parameter)
        for item in result:
            data.append({
                'CameraID': item[0],
                'CameraName': item[1],
                'RecordFileName': item[2]
            })

        return data
