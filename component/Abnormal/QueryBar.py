import tkinter as tk
from tkinter import ttk
from utilset.ConfigUtil import ConfigUtil


class QueryBar():

    __layout = {
        # 只有這個是於root這個容器裡面的grid設定
        'QueryBar': {'row': 0, 'column': 0, 'sticky': 'EWNS', 'columnspan': 2},
        # 其他都是__QueryBar這個容器的grid設定
        'DateLabel': {'row': 0, 'column': 0, 'sticky': 'EWNS'},
        'AlertLabel': {'row': 1, 'column': 0, 'sticky': 'EWNS'},
        'DateBox': {'row': 0, 'column': 1, 'sticky': 'EWNS'},
        'AlertCombo': {'row': 1, 'column': 1, 'sticky': 'EWNS'},
    }
    __QueryBar = None  # 查詢區塊容器
    __DateBox = None  # 異常日期查詢欄位
    __AlertCombo = None  # 警報位置選取欄位
    __DateCondition = None  # 輸入的異常日期查詢條件
    __AlertCondition = None  # 選取的警報位置查詢條件
    __ReloadDataEvent = None  # 來自外部，在查詢條件變更時，要呼叫的動作

    # 初始化，建立容器
    def __init__(self, root, **para):
        # 建立一個查詢區塊容器，並建構在主容器中
        self.__QueryBar = tk.Frame(root)
        # 設定查詢區塊容器的版面配置比例
        self.__QueryBar.grid_columnconfigure(0, weight=1)
        self.__QueryBar.grid_columnconfigure(1, weight=4)
        self.__QueryBar.grid(self.__layout['QueryBar'])
        # 取出查詢條件變更時，要呼叫reload資料的動作
        self.__ReloadDataEvent = para.get('ReloadDataEvent')
        # 建立物件
        self.__Create()

    # 建立物件
    def __Create(self):
        # 建立控制項標題標籤
        self.__CreateLabel()
        # 建立日期查詢控制項
        self.__CreateDateBox()
        # 建立警報位置查詢控制項
        self.__CreateAlertCombo()

    # 建立控制項標題標籤
    def __CreateLabel(self):
        tk.Label(self.__QueryBar,
                 text="異常日期(yyyy/mm/dd)", font=("微軟正黑體", 12, "bold"), background="#DDDDDD").grid(self.__layout['DateLabel'])
        tk.Label(self.__QueryBar,
                 text="警報位置", font=("微軟正黑體", 12, "bold"), background="#DDDDDD").grid(self.__layout['AlertLabel'])

    # 建立日期查詢控制項
    def __CreateDateBox(self):
        self.__DateBox = tk.Entry(self.__QueryBar, font=("微軟正黑體", 12, "bold"))
        self.__DateBox.grid(self.__layout['DateBox'])
        # 綁定loass focus跟按enter的事件
        self.__DateBox.bind('<FocusOut>', self.__DateBoxOnchangeEvent)
        self.__DateBox.bind('<Return>', self.__DateBoxOnchangeEvent)

    # 建立警報位置查詢控制項
    def __CreateAlertCombo(self):
        self.__AlertCombo = ttk.Combobox(self.__QueryBar,
                                         font=("微軟正黑體", 12, "bold"), state="readonly",
                                         values=self.__getAlertNameList())
        self.__AlertCombo.grid(self.__layout['AlertCombo'])
        # 綁定選取下拉選單事件
        self.__AlertCombo.bind("<<ComboboxSelected>>",
                               self.__AlertComboOnchangeEvent)

    # 日期查詢控制項onchange事件
    def __DateBoxOnchangeEvent(self, event):
        # 值沒有變不需執行
        if self.__DateCondition == self.__DateBox.get():
            return
        # 強制把輸入空值轉為None
        self.__DateCondition = None if self.__DateBox.get() == '' else self.__DateBox.get()
        # 更新異常紀錄清單
        if self.__ReloadDataEvent is not None:
            self.__ReloadDataEvent(self.__DateCondition, self.__AlertCondition)

    # 警報位置控制項onchange事件
    def __AlertComboOnchangeEvent(self, event):
        # 值沒有變不需執行
        if self.__AlertCondition == self.__AlertCombo.get():
            return
        # 強制把輸入空值轉為None
        self.__AlertCondition = \
            None if self.__AlertCombo.get() == '' else self.__AlertCombo.get().split('.')[0]
        # 更新異常紀錄清單
        if self.__ReloadDataEvent is not None:
            self.__ReloadDataEvent(self.__DateCondition, self.__AlertCondition)

    # 讀取警報點位置選取清單
    def __getAlertNameList(self):
        list = []
        list.append('')
        for point in ConfigUtil().AlertPoints:
            itemText = str(point['number']) + "." + str(point['name'])
            list.append(itemText)
        return list

    # 提供外界直接切換至某警示點檢視異常紀錄的方法
    def QueryAlertCombo(self, AlertID):
        self.__AlertCombo.current(AlertID)
        self.__AlertComboOnchangeEvent(None)

