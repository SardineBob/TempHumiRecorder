import tkinter as tk
from tkinter import ttk
from utilset.DbAccessUtil import DbAccessUtil


class AbnormalTable():

    __layout = {
        'AbnormalTable': {'row': 1, 'column': 0, 'sticky': 'EWNS', 'rowspan': 2},
    }
    __treeView = None
    # __ReloadDataEvent = None  # 來自外部，在選取異常時間時，更新異常錄影片段選單

    # 初始化，建立容器
    def __init__(self, root, **para):
        # 創建treeview widget (show="headings"可隱藏自動產生的第一列)
        self.__treeView = ttk.Treeview(root, show="headings")
        # 取出查詢條件變更時，要呼叫reload資料的動作
        # self.__ReloadDataEvent = para.get('ReloadDataEvent')
        # 建立異常紀錄清單表格
        self.__Create()

    # 建立異常紀錄清單表格
    def __Create(self):
        # 定義欄位
        self.__treeView["columns"] = ("Name", "RecordTime", "Temp", "Humi", "IsTempUnusual", "IsHumiUnusual")
        self.__treeView.column("Name", minwidth=100,
                               width=100, anchor=tk.CENTER)
        self.__treeView.column("RecordTime", minwidth=170,
                               width=170, anchor=tk.CENTER)
        self.__treeView.column("Temp", minwidth=100,
                               width=100, anchor=tk.CENTER)
        self.__treeView.column("Humi", minwidth=100,
                               width=100, anchor=tk.CENTER)
        self.__treeView.column("IsTempUnusual", minwidth=100,
                               width=100, anchor=tk.CENTER)
        self.__treeView.column("IsHumiUnusual", minwidth=100,
                               width=100, anchor=tk.CENTER)
        # 定義標題
        self.__treeView.heading("Name", text="設備名稱")
        self.__treeView.heading("RecordTime", text="紀錄時間")
        self.__treeView.heading("Temp", text="溫度")
        self.__treeView.heading("Humi", text="濕度")
        self.__treeView.heading("IsTempUnusual", text="溫度異常")
        self.__treeView.heading("IsHumiUnusual", text="濕度異常")
        # 設定treeview的樣式
        style = ttk.Style()
        style.configure("Treeview", font=("微軟正黑體", 12))
        style.configure("Treeview.Heading", font=("微軟正黑體", 14, "bold"))
        self.__treeView.tag_configure("odd", background="#FFFFFF")
        self.__treeView.tag_configure("even", background="#DDDDDD")
        # 左邊滿版，擺入異常紀錄清單
        self.__treeView.grid(self.__layout['AbnormalTable'])
        # 載入資料
        self.LoadData()

    # 載入異常清單資料
    def LoadData(self, **para):
        # 清空treeview(星號(*)，表示視為Tuple)
        self.__treeView.delete(*self.__treeView.get_children())
        # 撈取異常紀錄清單資料
        data = DbAccessUtil().getTodayUnusualRecord(**para)
        # 逐筆呈現在表格內
        for item in data:
            itemFormat = "even" if data.index(item) % 2 == 0 else "odd"
            # 取出各欄位資料
            Name = item['Name']
            RecordTime = item['RecordTime']
            Temperature = item['Temperature']
            Humidity = item['Humidity']
            IsTempUnusual = "是" if item['IsTempUnusual'] is 1 else "否"
            IsHumiUnusual = "是" if item['IsHumiUnusual'] is 1 else "否"
            # 透過treeview呈現
            self.__treeView.insert("", "end", value=(Name, RecordTime, Temperature,
                                   Humidity, IsTempUnusual, IsHumiUnusual), tags=(itemFormat))
