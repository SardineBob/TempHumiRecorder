import tkinter as tk
from component.Abnormal.QueryBar import QueryBar
from component.Abnormal.AbnormalTable import AbnormalTable
from component.Abnormal.VideoList import VideoList


class AbnormalWindow():

    __window = None
    __closeMethod = None  # 呼叫端關閉本視窗的方法，通常包含呼叫本class的close event，以及呼叫端管理class關閉的實作方法
    queryBar = None  # 提供外界可透過自己的程式操作查詢條件

    def __init__(self, para):
        # 取出需使用的設定值
        self.__closeMethod = para["closeMethod"]
        # 開始建立一個子視窗
        self.__window = tk.Toplevel()
        self.__window.geometry("480x480+50+50")
        # 註冊視窗關閉事件，使用者點擊視窗的X，會觸發
        self.__window.protocol("WM_DELETE_WINDOW", self.__closeMethod)
        # 產生版面
        self.__CreatePanel()

    # 產生版面(左版面：異常紀錄清單，右版面：選取異常紀錄之對應的錄影檔)
    def __CreatePanel(self):
        # 設定Grid版面配置比例(最外層主要容器)
        self.__window.grid_columnconfigure(0, weight=1)
        self.__window.grid_columnconfigure(1, weight=1)
        self.__window.grid_rowconfigure(2, weight=1)
        # 建立錄影片段選單
        videoList = VideoList(self.__window)
        # 建立異常紀錄清單
        abnormalTable = AbnormalTable(
            self.__window, ReloadDataEvent=videoList.LoadData)
        # 建立查詢區塊
        self.queryBar = QueryBar(
            self.__window, ReloadDataEvent=abnormalTable.LoadData)

    # 視窗關閉，用於外部呼叫
    def WindowClose(self):
        self.__window.destroy()
        self.__window = None
