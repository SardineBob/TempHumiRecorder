import tkinter as tk
from tkinter import ttk
from utilset.AbnormalUtil import AbnormalUtil


class AbnormalTable():

    __layout = {
        'AbnormalTable': {'row': 1, 'column': 0, 'sticky': 'EWNS', 'rowspan': 2},
    }
    __treeView = None
    __ReloadDataEvent = None  # 來自外部，在選取異常時間時，更新異常錄影片段選單

    # 初始化，建立容器
    def __init__(self, root, **para):
        # 創建treeview widget (show="headings"可隱藏自動產生的第一列)
        self.__treeView = ttk.Treeview(root, show="headings")
        # 取出查詢條件變更時，要呼叫reload資料的動作
        self.__ReloadDataEvent = para.get('ReloadDataEvent')
        # 建立異常紀錄清單表格
        self.__Create()

    # 建立異常紀錄清單表格
    def __Create(self):
        # 定義欄位
        self.__treeView["columns"] = ("TriggerTime", "AlertName")
        self.__treeView.column("TriggerTime", minwidth=170,
                               width=170, anchor=tk.CENTER)
        self.__treeView.column("AlertName", minwidth=100,
                               width=100, anchor=tk.CENTER)
        # 定義標題
        self.__treeView.heading("TriggerTime", text="異常觸發時間")
        self.__treeView.heading("AlertName", text="警報位置")
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
    def LoadData(self, AlertTime=None, AlertID=None):
        # 清空treeview(星號(*)，表示視為Tuple)
        self.__treeView.delete(*self.__treeView.get_children())
        # 撈取異常紀錄清單資料
        data = AbnormalUtil().FindAbnormalRecord(AlertTime, AlertID)
        # 逐筆呈現在表格內
        for item in data:
            itemFormat = "even" if data.index(item) % 2 == 0 else "odd"
            # 取出各欄位資料
            alertTime = item['AlertTime']
            alertName = str(item['AlertID']) + "." + str(item['AlertName'])
            # 透過treeview呈現
            self.__treeView.insert("", "end", value=(
                alertTime, alertName), tags=(itemFormat))
        # 綁定選取的事件
        self.__treeView.bind('<Button-1>', self.__TreeViewOnchangeEvent)

    # 選取異常清單項目事件，建立該異常時間發生之攝影機錄影片段
    def __TreeViewOnchangeEvent(self, event):
        # 擷取選取的警示時間與警示點為何
        selectedItem = self.__treeView.identify('item', event.x, event.y)
        selectedData = self.__treeView.item(selectedItem, 'values')
        if selectedData is '':
            return
        selectedAlertTime = selectedData[0]
        selectedAlertID = selectedData[1].split('.')[0]
        # 觸發更新錄影片段清單
        if self.__ReloadDataEvent is not None:
            self.__ReloadDataEvent(selectedAlertTime, selectedAlertID)
