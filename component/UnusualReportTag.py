import os
import json
from component.Tag import Tag
from PIL import Image, ImageTk
import time
import threading
from datetime import datetime
from utilset.ConfigUtil import ConfigUtil
from utilset.AbnormalUtil import AbnormalUtil
from utilset.DbAccessUtil import DbAccessUtil
from component.Abnormal.AbnormalWindow import AbnormalWindow


# 背景圓：均為綠色
# 狀態環：識別是否開啟異常報表(紅色：已開啟，綠色：未開啟)
class UnusualReportTag(Tag):

    __picPath = './resource/IconReport.png'
    __tagsName = "report"  # 標籤名稱，綁定canvas繪製物件的標籤
    __openReportStatus = False  # 開啟報表視窗狀態
    __reportWindow = None  # 報表視窗物件

    def __init__(self, canvas, relocate):
        # open警報點標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "reportIcon") is False:
            canvas.reportIcon = []
        canvas.reportIcon.append(picPhoto)
        # 傳入父類別，建立警報點標籤物件
        super().__init__(canvas, relocate, "R01", "UnusualReport", 610, 10, picPhoto, self.__tagsName)
        # 改變異常清單背景色
        canvas.itemconfig(self.bgid, fill="#00ff00")
        # 綁定標籤點擊事件
        self.canvas.tag_bind(self.__tagsName, '<Button-1>', lambda event: self.__tagClick())
        # 預設狀態環為未開啟報表
        self.setOpenReportStatus(False)

    # 點擊異常報表事件
    def __tagClick(self):
        self.__openReportStatus = not self.__openReportStatus
        self.setOpenReportStatus(self.__openReportStatus)
        # 報表打開狀態
        if self.__openReportStatus is True and self.__reportWindow is None:
            self.__reportWindow = AbnormalWindow({"closeMethod": self.close})
        # 報表關閉狀態
        if self.__openReportStatus is False:
            self.close()

    # 根據開啟報表狀態，切換狀態環的顏色
    def setOpenReportStatus(self, onlineStatus):
        self.canvas.itemconfig(self.ringid, outline="#ff0000" if onlineStatus is True else "#00ff00")

    # 提供外界呼叫tag關閉事件
    def close(self):
        self.__openReportStatus = False
        self.setOpenReportStatus(self.__openReportStatus)
        if self.__reportWindow is not None:
            self.__reportWindow.WindowClose()
            self.__reportWindow = None
