import os
from tkinter import messagebox
import configparser
import json


# 設定檔存取元件
class ConfigUtil():

    __filePath = 'config.ini'
    SystemConfig = None
    AlertPoints = None
    cameraPoints = None
    RaspberryPis = None

    def __init__(self):
        # 判斷設定檔是否存在
        if os.path.exists(self.__filePath) is False:
            messagebox.showinfo("error", "設定檔不存在。")
            exit()
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取系統參數設定
        #self.SystemConfig = SystemConfig(config)
        # 讀取警報器材位置
        self.AlertPoints = json.loads(config["AlertPoint"]["point"])
        # 讀取攝影機位置
        #self.cameraPoints = json.loads(config["CameraPoint"]["point"])
        # 讀取樹梅派Websocket位址
        #self.RaspberryPis = json.loads(config["RaspberryPiWebsocket"]["device"])

    # 根據Point ID取得Camera Point Config Item
    #def getCameraPoint(self, pointID):
    #    for item in self.cameraPoints:
    #        if(item['number'] is pointID):
    #            return item


# 設定檔中，系統參數設定存取元件
#class SystemConfig():
#
#    IsLinkRaspberry = None
#    VideoTime = None
#
#    def __init__(self, config):
#        self.IsLinkRaspberry = json.loads(config["SystemConfig"]["islinkraspberry"])
#        self.VideoTime = json.loads(config["SystemConfig"]["videotime"])
