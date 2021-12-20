import os
import subprocess
import tkinter as tk
from utilset.AbnormalUtil import AbnormalUtil


class VideoList():

    __layout = {
        'VideoLabel': {'row': 1, 'column': 1, 'sticky': 'EWNS'},
        'VideoList': {'row': 2, 'column': 1, 'sticky': 'EWNS'},
    }
    __listBox = None
    __videoList = None  # 目前載入的錄影片段清單

    # 初始化，建立容器
    def __init__(self, root):
        # ListBox初始設定
        self.__listBox = tk.Listbox(root)
        # 錄影片段清單標籤標題
        tk.Label(root,
                 text="錄影片段", font=("微軟正黑體", 12, "bold"), background="#DDDDDD").grid(self.__layout['VideoLabel'])
        # 建立錄影片段清單
        self.__Create()

    # 建立錄影片段清單
    def __Create(self):
        self.__listBox.configure(
            font=("微軟正黑體", 12), justify="center", highlightthickness=0)
        # 右邊版面內容，擺入選取之異常紀錄的錄影檔選單
        self.__listBox.grid(self.__layout['VideoList'])

    # 載入錄影片段資料
    def LoadData(self, AlertTime=None, AlertID=None):
        # 清空預備載入資料
        if self.__listBox is not None:
            self.__listBox.delete(0, tk.END)
        # 根據警示時間與警示器材代碼，取得錄影片段清單
        self.__videoList = AbnormalUtil().FindRecordList(AlertTime, AlertID)
        # 逐筆呈現於ListBox
        for item in self.__videoList:
            index = self.__videoList.index(item)
            cameraName = str(item['CameraID']) + "." + str(item['CameraName'])
            self.__listBox.insert(index, cameraName)
        # 綁定選取事件
        self.__listBox.bind('<Double-1>', self.__ListBoxSelectedEvent)

    # 點選錄影片事件，開啟該錄影片段影片檔案
    def __ListBoxSelectedEvent(self, event):
        # 擷取選取的錄影片段在ListBox的Index
        widget = event.widget
        index = widget.curselection()[0]
        # 根據index到List取得錄影片段檔名
        videoFileName = self.__videoList[index]['RecordFileName']
        # 透過Window Media Plyer播放影片
        playerPath = "C:/Program Files/Windows Media Player/wmplayer.exe"
        videoPath = os.path.join(
            os.path.abspath('.'), 'CameraRecord', videoFileName)
        subprocess.Popen(playerPath + ' ' + videoPath)
