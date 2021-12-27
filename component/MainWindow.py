import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from utilset.ConfigUtil import ConfigUtil
import platform
from component.Map import Map
from component.WindowRelocate import WindowRelocate
from component.UnusualReportTag import UnusualReportTag
from component.AlertTag import AlertTag
from component.Abnormal.AbnormalWindow import AbnormalWindow


class MainWindow():
    __configUtil = None
    __originWidth = 640
    __originHeight = 480
    __curWidth = __originWidth
    __curHeight = __originHeight
    __mainWindow = None
    __canvas = None
    __map = None
    __windowRelocate = None
    __menuTags = []
    __alertTags = []
    __AbnormalWindow = None

    def __init__(self):
        # 讀取保全器材位置設定檔
        self.__configUtil = ConfigUtil()
        # 準備主要視窗設定
        self.__mainWindow = tk.Tk()
        self.__mainWindow.title("溫溼度監控器(ver.1.0.0)-" + self.__configUtil.DeviceName +
                                "(" + self.__configUtil.DeviceID + ")")
        self.__mainWindow.geometry("%dx%d" % (self.__originWidth, self.__originHeight))
        self.__mainWindow.protocol("WM_DELETE_WINDOW", False)  # 不允許使用者離開視窗
        # 判斷作業系統環境，Window則該程式屬性指定為toolwindow，反之指定為fullscreen
        if platform.system() is "Windows":
            self.__mainWindow.attributes("-toolwindow", True)  # in window
        else:
            self.__mainWindow.attributes("-fullscreen", True)  # in raspberrypi
        # 註冊視窗事件
        self.__mainWindow.bind('<Configure>', self.__windowResize)
        # 產生繪圖物件
        self.__canvas = tk.Canvas(
            width=self.__curWidth, height=self.__curHeight, bg="black")
        self.__canvas.pack(fill='both', expand=True)
        # 產生地圖物件
        self.__map = Map(self.__canvas)
        self.__map.Draw(self.__originWidth, self.__originHeight)
        # 產生視窗重新定位的物件
        self.__windowRelocate = WindowRelocate({
            'oriWindowWidth': self.__originWidth,
            'oriWindowHeight': self.__originHeight,
            'oriMapWidth': self.__map.mapOriginWidth,
            'oriMapHeight': self.__map.mapOriginHeight
        })
        # 執行刪除介接資料夾動作
        if os.path.exists(self.__configUtil.DeviceRootPath):
            shutil.rmtree(self.__configUtil.DeviceRootPath)
        # 產生Menu標籤
        self.__menuTags.append(UnusualReportTag(self.__canvas, self.__windowRelocate))
        # 產生溫溼度計標籤位置
        for item in self.__configUtil.TempHumiDevices:
            self.__alertTags.append(AlertTag(self.__canvas, self.__windowRelocate, item))
        # 建立溫溼度標籤與異常清單連結關係
        for item in self.__alertTags:
            item.linkAbnormalWindow(self.__openAbnormalWindow)
        # 開啟視窗
        self.__mainWindow.mainloop()

    def __windowResize(self, event):
        # 判斷事件是主要視窗所觸發
        if str(event.widget) == '.':
            # 判斷變動主要視窗寬高的操作
            if self.__curWidth != event.width or self.__curHeight != event.height:
                # 觸發執行Map Resize動作
                self.__map.Draw(event.width, event.height)
                # 設定目前Window Resize後的寬高大小
                self.__windowRelocate.SetCurrentSize(event.width, event.height)
                # 重新定位menu標籤位置
                for item in self.__menuTags:
                    item.Relocate()
                # 重新定位保全器材標籤位置
                for item in self.__alertTags:
                    item.Relocate()
                # 更新目前視窗寬高
                self.__curWidth = event.width
                self.__curHeight = event.height

    # 開啟異常紀錄清單視窗
    def __openAbnormalWindow(self):
        if self.__AbnormalWindow is None:
            self.__AbnormalWindow = AbnormalWindow({
                "closeMethod": self.__closeAbnormalWindow
            })
        # 這個return是提供外界去承接這個物件，呼叫裡面方法
        return self.__AbnormalWindow

    # 關閉異常紀錄清單視窗
    def __closeAbnormalWindow(self):
        if self.__AbnormalWindow is not None:
            self.__AbnormalWindow.WindowClose()
            self.__AbnormalWindow = None
