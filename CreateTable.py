import os
from utilset.SqlLiteUtil import SqlLiteUtil


# 偵測若DB檔案存在就不做Create Table的動作
if os.path.isfile('dbfile/AbnormalRecord.db'):
    print('DB檔案存在，不允許再次創建，請手動移除該檔案後再嘗試。')
    exit()

# create table for abnormal record
AbnormalListcommand = "CREATE TABLE AbnormalList(\
    AlertTime Text NOT NULL,\
    AlertID INTEGER NOT NULL,\
    AlertName Text NOT NULL,\
    PRIMARY KEY (AlertTime, AlertID)\
)"
RecordListcommand = "CREATE TABLE RecordList(\
    AlertTime Text NOT NULL,\
    AlertID INTEGER NOT NULL,\
    CameraID INTEGER NOT NULL,\
    CameraName Text NOT NULL,\
    RecordFileName Text NOT NULL,\
    PRIMARY KEY (AlertTime, AlertID, CameraID)\
)"

# go to execoute
SqlLiteUtil().Execute(AbnormalListcommand, [])
SqlLiteUtil().Execute(RecordListcommand, [])

print('DB創建成功。')
