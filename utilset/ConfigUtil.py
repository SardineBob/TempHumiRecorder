# coding=UTF-8
import os
from tkinter import messagebox
import configparser
import json


# 設定檔存取元件
class ConfigUtil():

    __filePath = 'config.ini'
    DeviceID = None
    DeviceName = None
    DeviceUrl = None
    CaptureTime = None
    TempHumiDevices = None
    # PostURL = None

    def __init__(self):
        # 判斷設定檔是否存在，不存在則給予預設參數值
        if os.path.exists(self.__filePath) is False:
            self.__saveConfig(self.__initConfig())
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取溫控設備設定
        self.DeviceID = json.loads(config["SystemConfig"]["DeviceID"])
        self.DeviceName = json.loads(config["SystemConfig"]["DeviceName"])
        self.DeviceUrl = json.loads(config["SystemConfig"]["DeviceUrl"])
        self.CaptureTime = json.loads(config["SystemConfig"]["CaptureTime"])
        self.TempHumiDevices = json.loads(config["SystemConfig"]["TempHumiDevices"])
        # self.PostURL = json.loads(config["SystemConfig"]["PostURL"])

    # 提供外部呼叫設定檔存檔
    def save(self):
        self.__saveConfig({
            "deviceID": self.DeviceID,
            "deviceName": self.DeviceName,
            "deviceUrl": self.DeviceUrl,
            "captureTime": self.CaptureTime,
            "tempHumiDevices": self.TempHumiDevices,
            # "postURL": self.PostURL,
        })

    # 設定檔存檔
    def __saveConfig(self, para):
        # 讀取設定參數
        deviceID = para["deviceID"]
        deviceName = para["deviceName"]
        deviceUrl = para["deviceUrl"]
        captureTime = para["captureTime"]
        tempHumiDevices = para["tempHumiDevices"]
        # postURL = para["postURL"]
        # 產生設定檔物件
        config = configparser.ConfigParser()
        # 產生系統設定參數
        config['SystemConfig'] = {
            'DeviceID': json.dumps(deviceID, ensure_ascii=False),
            'DeviceName': json.dumps(deviceName, ensure_ascii=False),
            'DeviceUrl': json.dumps(deviceUrl, ensure_ascii=False),
            'CaptureTime': json.dumps(captureTime),  # 擷取溫度循環時間，每N秒，讀取溫度，並寫入溫度紀錄
            'TempHumiDevices': json.dumps(tempHumiDevices, ensure_ascii=False),  # 溫度計硬體設備序號與名稱(陣列)
            # 'PostURL': json.dumps(postURL, ensure_ascii=False),  # 要發布溫度到後台的網址
        }
        # 寫入設定檔
        with open(self.__filePath, 'w', encoding='UTF8') as configFile:
            config.write(configFile)

    # 初始化設定檔
    def __initConfig(self):
        return {
            "deviceID": "0000",
            "deviceName": "星堡保全",
            "DeviceUrl": "http://raspberrypi:9453/TempHumi/",
            "captureTime": 5,
            "tempHumiDevices": [
                {'id': 'A01', 'name': '左側機房', 'mac': 'A4:C1:38:35:5C:24',
                 'tempuplimit': 30, 'templowlimit': 15,
                 'humiuplimit': 30, 'humilowlimit': 15,
                 'tagX': 125, 'tagY': 125},
                #{'id': 'A02', 'name': '中間冷凍櫃', 'serial': '28CEBD7D613CA6', 'initTemp': 10,  'uplimit': 15, 'lowlimit': 5},
                #{'id': 'A03', 'name': '右邊冷凍櫃', 'serial': '28177A7D613C87', 'initTemp': 60,  'uplimit': 70, 'lowlimit': 50},
            ],
            # "postURL": "http://59.125.33.102:2028"
        }
