import tkinter as tk
from tkinter import ttk, messagebox
from utilset.ConfigUtil import ConfigUtil
from component.Map import Map
from component.WindowRelocate import WindowRelocate
from component.AlertTag import AlertTag
# from component.Abnormal.AbnormalWindow import AbnormalWindow


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
    __alertTags = []
    __cameraTags = []
    __raspberryPi = []
    __AbnormalWindow = None
    __RtspWindow = None

    # 測試用
    __window = None
    __window1 = None
    __window2 = None
    __window3 = None

    def __init__(self):
        # 準備主要視窗設定
        self.__mainWindow = tk.Tk()
        self.__mainWindow.title("溫溼度監控器(ver.0.1.0)")
        self.__mainWindow.geometry("%dx%d" % (
            self.__originWidth, self.__originHeight))
        # 註冊視窗事件
        self.__mainWindow.bind('<Configure>', self.__windowResize)
        # 讀取保全器材位置設定檔
        self.__configUtil = ConfigUtil()
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
        # 產生RTSP視窗物件
        # self.__RtspWindow = RtspWindow()
        # self.__RtspWindow.SetCameraTag(self.__cameraTags)
        # 產生溫溼度計標籤位置
        for item in self.__configUtil.TempHumiDevices:
            self.__alertTags.append(
                AlertTag(self.__canvas, self.__windowRelocate, item))
        # 產生攝影機標籤位置
        # for item in self.__configUtil.cameraPoints:
        #    self.__cameraTags.append(
        #        CameraTag(self.__canvas, self.__windowRelocate, item))
        # 建立保全器材(警報點)與其他組件連結關係
        # for item in self.__alertTags:
        #    # 建立保全器材(警報點)與攝影機的連結關係
        #    item.linkCamera(self.__cameraTags)
        #    # 建立保全器材(警報點)與異常紀錄視窗的連結關係
        #    item.linkAbnormalWindow(self.__openAbnormalWindow)
        # 建立攝影機與RTSP視窗的連結關係
        # for item in self.__cameraTags:
        #    item.linkRtspWindow(self.__RtspWindow)
        # 設定開啟與樹梅派建立連線時，才去連線，避免開發過程中一直連線
        # if self.__configUtil.SystemConfig.IsLinkRaspberry:
        #    # 建立與多台樹梅派的WebSocket連線物件
        #    for item in self.__configUtil.RaspberryPis:
        #        self.__raspberryPi.append(RaspberryPiSignal(item))
        #    # 建立樹梅派與其他組件的連結關係
        #    for item in self.__raspberryPi:
        #        item.linkAlert(self.__alertTags)

        # 給兩個按鈕來測試閃爍
        def click1():
            self.__alertTags[4].TriggerAlert()

        def click2():
            for tag in self.__alertTags:
                tag.TriggerStop()
            # self.__alertTags[2].TriggerStop()
            # for item in self.__cameraTags:
            #    item.RtspStop()
            # self.__test.closeTask()

        def click3():
            self.__test = RaspberryPiSignal(self.__alertTags)

        def click4():
            self.__openAbnormalWindow()
            # 自訂一個dialog box
            #test = tk.Tk()
            #test.master = self.__mainWindow
            # test.mainloop()
            # messagebox.showinfo('555')
            #test = tk.Frame(self.__mainWindow)
            # tk.Label(test,text="testestse").pack()
            #test.place(x=150, y=10)
            # test.pack()
            #self.newfream = tk.Toplevel()
            # self.newfream.resizable(0,0)
            # self.newfream.attributes('-toolwindow',True)
            # self.newfream.wm_attributes('-topmost',True)
            # self.newfream.wm_overrideredirect(True)
            # self.newfream.geometry("640x480+50+50")

        def click5():
            self.__closeAbnormalWindow()
            # test.mainloop()

            # def click3():
            # self.__window = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 100, 100)
            # self.__window1 = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 100, 270)
            # self.__window2 = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 350, 100)
            # self.__window3 = CameraWindow(
            #    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov', 350, 270)
            # self.__window.Start()
            # self.__window1.Start()
            # self.__window2.Start()
            # self.__window3.Start()

        # def click6():
            # self.__openRtspBox()

        # def click7():
            # self.__closeRtspWindow()

        #button1 = tk.Button(text='啟動', command=click1)
        #button1.place(x=10, y=10)
        #button2 = tk.Button(text='停止', command=click2)
        #button2.place(x=50, y=10)
        #button3 = tk.Button(text='連線', command=click3)
        #button3.place(x=90, y=10)
        #button4 = tk.Button(text='開啟報表', command=click4)
        #button4.place(x=130, y=10)
        #button5 = tk.Button(text='關閉報表', command=click5)
        #button5.place(x=200, y=10)
        #button4 = tk.Button(text='開啟攝影機畫面', command=click6)
        #button4.place(x=270, y=10)
        #button5 = tk.Button(text='關閉攝影機畫面', command=click7)
        #button5.place(x=370, y=10)
        #button3 = tk.Button(text='播放', command=click3)
        #button3.place(x=90, y=10)

        # 測試表格
        #treeview = ttk.Treeview()
        # treeview["columns"]=("colume1","colume2","colume3")
#
        # treeview.heading("#0",text="OK", anchor=tk.W)
        # treeview.heading("colume1",text="OK")
        # treeview.heading("colume2",text="OK1")
        # treeview.heading("colume3",text="OK3")
        #treeview.place(x=300, y=300)

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
                # 重新定位保全器材標籤位置
                for item in self.__alertTags:
                    item.Relocate()
                for item in self.__cameraTags:
                    item.Relocate()
                # 更新目前視窗寬高
                self.__curWidth = event.width
                self.__curHeight = event.height

    # 開啟異常紀錄清單視窗
    # def __openAbnormalWindow(self):
    #    if self.__AbnormalWindow is None:
    #        self.__AbnormalWindow = AbnormalWindow({
    #            "closeMethod": self.__closeAbnormalWindow
    #        })
    #    # 這個return是提供外界去承接這個物件，呼叫裡面方法
    #    return self.__AbnormalWindow

    # 關閉異常紀錄清單視窗
    # def __closeAbnormalWindow(self):
    #    if self.__AbnormalWindow is not None:
    #        self.__AbnormalWindow.WindowClose()
    #        self.__AbnormalWindow = None
