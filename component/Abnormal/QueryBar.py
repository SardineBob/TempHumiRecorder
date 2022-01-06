import tkinter as tk
from tkinter import ttk, filedialog
from utilset.ConfigUtil import ConfigUtil
from utilset.DbAccessUtil import DbAccessUtil


class QueryBar():

    __layout = {
        # 只有這個是於root這個容器裡面的grid設定
        'QueryBar': {'row': 0, 'column': 0, 'sticky': 'EWNS', 'columnspan': 2},
        # 其他都是__QueryBar這個容器的grid設定
        'DateLabel': {'row': 0, 'column': 0, 'sticky': 'EWNS'},
        'AlertLabel': {'row': 1, 'column': 0, 'sticky': 'EWNS'},
        'DateBox': {'row': 0, 'column': 1, 'sticky': 'EWNS'},
        'AlertCombo': {'row': 1, 'column': 1, 'sticky': 'EWNS'},
        'TempUnusualLabel': {'row': 0, 'column': 2, 'sticky': 'EWNS'},
        'HumiUnusualLabel': {'row': 1, 'column': 2, 'sticky': 'EWNS'},
        'TempUnusualBlock': {'row': 0, 'column': 3, 'sticky': 'EWNS'},
        'HumiUnusualBlock': {'row': 1, 'column': 3, 'sticky': 'EWNS'},
        'CSVBlock': {'row': 0, 'column': 4, 'sticky': 'EWNS', 'rowspan': 2},
        # 下面是位於TempUnusualBlock裡面每個RadioButton的grid設定
        'TempUnusualRadioAll': {'row': 0, 'column': 0, 'sticky': 'W'},
        'TempUnusualRadioYes': {'row': 0, 'column': 1, 'sticky': 'W'},
        'TempUnusualRadioNo': {'row': 0, 'column': 2, 'sticky': 'W'},
        # 下面是位於HumiUnusualBlock裡面每個RadioButton的grid設定
        'HumiUnusualRadioAll': {'row': 0, 'column': 0, 'sticky': 'W'},
        'HumiUnusualRadioYes': {'row': 0, 'column': 1, 'sticky': 'W'},
        'HumiUnusualRadioNo': {'row': 0, 'column': 2, 'sticky': 'W'},
    }
    __QueryBar = None  # 查詢區塊容器
    # __TempUnusualBlock = None # 溫度異常單選項容器
    __AlertCombo = None  # 溫溼度計位置選取欄位
    __DateCondition = None  # 輸入的異常日期查詢條件
    __AlertCondition = None  # 選取的溫溼度計位置查詢條件
    __TempChooseVal = None  # 綁定溫度異常選項為一組的變數，選取項目的Value會被給予在這邊
    __HumiChooseVal = None  # 綁定濕度異常選項為一組的變數，選取項目的Value會被給予在這邊
    __TempUnusualCondition = None  # 選取的溫度異常查詢條件
    __HumiUnusualCondition = None  # 選取的濕度異常查詢條件
    __ReloadDataEvent = None  # 來自外部，在查詢條件變更時，要呼叫的動作
    __AlertTagList = None  # 溫溼度計位置清單

    # 初始化，建立容器
    def __init__(self, root, **para):
        # 建立一個查詢區塊容器，並建構在主容器中
        self.__QueryBar = tk.Frame(root)
        # 設定查詢區塊容器的版面配置比例
        self.__QueryBar.grid_columnconfigure(0, weight=1)
        self.__QueryBar.grid_columnconfigure(1, weight=4)
        self.__QueryBar.grid_columnconfigure(2, weight=1)
        self.__QueryBar.grid_columnconfigure(3, weight=4)
        self.__QueryBar.grid_columnconfigure(4, weight=1)
        self.__QueryBar.grid(self.__layout['QueryBar'])
        # 取出查詢條件變更時，要呼叫reload資料的動作
        self.__ReloadDataEvent = para.get('ReloadDataEvent')
        # 準備/建立/預設單選項所需變數
        self.__TempChooseVal = tk.StringVar()
        self.__TempChooseVal.set("all")
        self.__HumiChooseVal = tk.StringVar()
        self.__HumiChooseVal.set("all")
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
        # 建立異常狀態查詢控制選項
        self.__CreateUnusualRadio()
        # 建立匯出CSV報表
        self.__CreateExportCsvButton()

    # 建立控制項標題標籤
    def __CreateLabel(self):
        tk.Label(self.__QueryBar, text="異常日期(yyyy/mm/dd)", font=("微軟正黑體", 12, "bold"),
                 background="#DDDDDD").grid(self.__layout['DateLabel'])
        tk.Label(self.__QueryBar, text="溫溼度計位置", font=("微軟正黑體", 12, "bold"),
                 background="#DDDDDD").grid(self.__layout['AlertLabel'])
        tk.Label(self.__QueryBar, text="溫度異常", font=("微軟正黑體", 12, "bold"),
                 background="#DDDDDD").grid(self.__layout['TempUnusualLabel'])
        tk.Label(self.__QueryBar, text="濕度異常", font=("微軟正黑體", 12, "bold"),
                 background="#DDDDDD").grid(self.__layout['HumiUnusualLabel'])

    # 建立日期查詢控制項
    def __CreateDateBox(self):
        DateBox = tk.Entry(self.__QueryBar, font=("微軟正黑體", 12, "bold"))
        DateBox.grid(self.__layout['DateBox'])
        # 綁定loass focus跟按enter的事件
        DateBox.bind('<FocusOut>', lambda event, arg=DateBox: self.__DateBoxOnchangeEvent(event, arg))
        DateBox.bind('<Return>', lambda event, arg=DateBox: self.__DateBoxOnchangeEvent(event, arg))

    # 建立溫溼度計位置查詢控制項
    def __CreateAlertCombo(self):
        self.__AlertCombo = ttk.Combobox(self.__QueryBar, font=("微軟正黑體", 12, "bold"),
                                         state="readonly", values=self.__getAlertNameList())
        self.__AlertCombo.grid(self.__layout['AlertCombo'])
        # 綁定選取下拉選單事件
        self.__AlertCombo.bind("<<ComboboxSelected>>", self.__AlertComboOnchangeEvent)

    # 建立異常狀態查詢選項
    def __CreateUnusualRadio(self):
        # 建立一個溫度異常單選項容器，並建構在QueryBar容器中
        TempUnusualBlock = tk.Frame(self.__QueryBar)
        HumiUnusualBlock = tk.Frame(self.__QueryBar)
        # 設定查詢區塊容器的版面配置比例
        TempUnusualBlock.grid_columnconfigure(0, weight=1)
        TempUnusualBlock.grid_columnconfigure(1, weight=1)
        TempUnusualBlock.grid_columnconfigure(2, weight=1)
        TempUnusualBlock.grid(self.__layout['TempUnusualBlock'])
        HumiUnusualBlock.grid_columnconfigure(0, weight=1)
        HumiUnusualBlock.grid_columnconfigure(1, weight=1)
        HumiUnusualBlock.grid_columnconfigure(2, weight=1)
        HumiUnusualBlock.grid(self.__layout['HumiUnusualBlock'])
        # 產生單選項
        TempUnusualRadAll = tk.Radiobutton(TempUnusualBlock, text="全部", variable=self.__TempChooseVal, value="all")
        TempUnusualRadYes = tk.Radiobutton(TempUnusualBlock, text="是", variable=self.__TempChooseVal, value="Y")
        TempUnusualRadNo = tk.Radiobutton(TempUnusualBlock, text="否", variable=self.__TempChooseVal, value="N")
        HumiUnusualRadAll = tk.Radiobutton(HumiUnusualBlock, text="全部", variable=self.__HumiChooseVal, value="all")
        HumiUnusualRadYes = tk.Radiobutton(HumiUnusualBlock, text="是", variable=self.__HumiChooseVal, value="Y")
        HumiUnusualRadNo = tk.Radiobutton(HumiUnusualBlock, text="否", variable=self.__HumiChooseVal, value="N")
        TempUnusualRadAll.grid(self.__layout["TempUnusualRadioAll"])
        TempUnusualRadYes.grid(self.__layout["TempUnusualRadioYes"])
        TempUnusualRadNo.grid(self.__layout["TempUnusualRadioNo"])
        HumiUnusualRadAll.grid(self.__layout["HumiUnusualRadioAll"])
        HumiUnusualRadYes.grid(self.__layout["HumiUnusualRadioYes"])
        HumiUnusualRadNo.grid(self.__layout["HumiUnusualRadioNo"])
        # 綁定切換單選項事件
        TempUnusualRadAll.config(command=self.__TempUnusualRadioOnchangeEvent)
        TempUnusualRadYes.config(command=self.__TempUnusualRadioOnchangeEvent)
        TempUnusualRadNo.config(command=self.__TempUnusualRadioOnchangeEvent)
        HumiUnusualRadAll.config(command=self.__HumiUnusualRadioOnchangeEvent)
        HumiUnusualRadYes.config(command=self.__HumiUnusualRadioOnchangeEvent)
        HumiUnusualRadNo.config(command=self.__HumiUnusualRadioOnchangeEvent)

    # 建立匯出CSV報表
    def __CreateExportCsvButton(self):
        ExportCsvButton = tk.Button(self.__QueryBar, text="匯出CSV", command=self.__exportCsvClickEvent)
        ExportCsvButton.grid(self.__layout["CSVBlock"])

    # 日期查詢控制項onchange事件
    def __DateBoxOnchangeEvent(self, event, dateBox):
        # 值沒有變不需執行
        if self.__DateCondition == dateBox.get():
            return
        # 強制把輸入空值轉為None
        self.__DateCondition = None if dateBox.get() == '' else dateBox.get()
        # 更新異常紀錄清單
        self.__updateUnusualReport()

    # 警報位置控制項onchange事件
    def __AlertComboOnchangeEvent(self, event):
        # 值沒有變不需執行
        if self.__AlertCondition == self.__AlertCombo.get():
            return
        # 強制把輸入空值轉為None
        self.__AlertCondition = \
            None if self.__AlertCombo.get() == '' else self.__AlertCombo.get().split('.')[0]
        # 更新異常紀錄清單
        self.__updateUnusualReport()

    # 溫度異常狀態查詢控制項onchange事件
    def __TempUnusualRadioOnchangeEvent(self):
        # 值沒有變不需執行
        if self.__TempUnusualCondition == self.__TempChooseVal.get():
            return
        # 強制把輸入空值轉為None
        self.__TempUnusualCondition = None if self.__TempChooseVal.get() == '' else self.__TempChooseVal.get()
        # 更新異常紀錄清單
        self.__updateUnusualReport()

    # 濕度異常狀態查詢控制項onchange事件
    def __HumiUnusualRadioOnchangeEvent(self):
        # 值沒有變不需執行
        if self.__HumiUnusualCondition == self.__HumiChooseVal.get():
            return
        # 強制把輸入空值轉為None
        self.__HumiUnusualCondition = None if self.__HumiChooseVal.get() == '' else self.__HumiChooseVal.get()
        # 更新異常紀錄清單
        self.__updateUnusualReport()

    # 匯出CSV按鈕onclick事件
    def __exportCsvClickEvent(self):
        # 檔案路徑選取對話方塊
        csvFilePath = filedialog.asksaveasfilename(title="選取CSV儲存位置",
                                                   filetypes=(("CSV files", "*.csv"),),
                                                   defaultextension=".csv")
        # 根據目前條件，取得查詢結果
        data = DbAccessUtil().getTodayUnusualRecord(recordDate=self.__DateCondition,
                                                    tagID=self.__AlertCondition,
                                                    tempUnusualStatus=self.__TempUnusualCondition,
                                                    humiUnusualStatus=self.__HumiUnusualCondition)
        # 寫入檔案
        with open(csvFilePath, "w") as file:
            file.write("溫溼度計名稱,紀錄時間,溫度,濕度,溫度異常,濕度異常\n")
            for item in data:
                file.write(
                    f"{item['Name']},{item['RecordTime']},{item['Temperature']},{item['Humidity']},{'是' if item['IsTempUnusual'] == 1 else '否'},{'是' if item['IsHumiUnusual'] == 1 else '否'}\n")

    # 讀取警報點位置選取清單
    def __getAlertNameList(self):
        list = []
        list.append('')
        for point in ConfigUtil().TempHumiDevices:
            itemText = str(point['id']) + "." + str(point['name'])
            list.append(itemText)
        self.__AlertTagList = list
        return list

    # 更新異常清單
    def __updateUnusualReport(self):
        if self.__ReloadDataEvent is not None:
            self.__ReloadDataEvent(recordDate=self.__DateCondition,
                                   tagID=self.__AlertCondition,
                                   tempUnusualStatus=self.__TempUnusualCondition,
                                   humiUnusualStatus=self.__HumiUnusualCondition)

    # 提供外界直接切換至某警示點檢視異常紀錄的方法
    def QueryAlertCombo(self, tagID, tagName):
        index = self.__AlertTagList.index(tagID + "." + tagName)
        self.__AlertCombo.current(index)
        self.__AlertComboOnchangeEvent(None)
