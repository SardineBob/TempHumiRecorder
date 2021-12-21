from component.Tag import Tag
from PIL import Image, ImageTk
import time
import threading
from datetime import datetime
from utilset.AbnormalUtil import AbnormalUtil
# from component.RtspRecord import RtspRecord

# 背景圓：平常為綠色，警報發生時，呈現紅色閃爍
# 狀態環：識別樹梅派WebSocket訊號是否連結的呈現(紅色：未連結，藍色：已連結)


class AlertTag(Tag):

    __picPath = './resource/IconAlert.png'
    __tagsName = "alert"  # 標籤名稱，綁定canvas繪製物件的標籤
    __task = None
    __flickerStatus = False  # 控制Tag閃爍的開關
    __dataTagBg = None  # 溫溼度標籤背景
    __dataTag = None  # 溫溼度標籤

    def __init__(self, canvas, relocate, configItem):
        # 取出需用到的設定值
        pointid = configItem["id"]
        name = configItem["name"]
        x = configItem["tagX"]
        y = configItem["tagY"]
        # open警報點標籤的icon image
        picLoad = Image.open(self.__picPath)
        picPhoto = ImageTk.PhotoImage(picLoad)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        if hasattr(canvas, "alertIcon") is False:
            canvas.alertIcon = []
        canvas.alertIcon.append(picPhoto)
        # 傳入父類別，建立警報點標籤物件
        super().__init__(canvas, relocate, pointid, name, x, y, picPhoto, self.__tagsName)
        # 新增繪製溫溼度數值標籤
        self.CreateDataTag()
        # 綁定標籤點擊事件
        self.canvas.tag_bind(self.__tagsName, '<Button-1>', lambda event: self.__TagClick())
        # 預設狀態環為未與小米溫度計藍芽連接
        self.setOnlineStatus(False)

    # 在Tag下方顯示溫溼度標籤
    def CreateDataTag(self):
        self.__dataTagBg = self.canvas.create_rectangle(
            self.getDataTagBGCoords(self.tagX, self.tagY),
            fill='#000000',
            tags=self.__tagsName
        )
        self.__dataTag = self.canvas.create_text(
            self.getDataTagCoords(self.tagX, self.tagY),
            text="溫度:36.6℃\n濕度:52%",
            fill='#ffffff',
            font=("Arial", 12),
            tags=self.__tagsName
        )

    def Relocate(self):
        super().Relocate()
        self.canvas.coords(self.__dataTagBg, self.getDataTagBGCoords(self.tagX, self.tagY))
        self.canvas.coords(self.__dataTag, self.getDataTagCoords(self.tagX, self.tagY))
        self.TriggerAlert()
#        self.canvas.itemconfig(self.__dataTag, text="溫度:50℃\n濕度:39%")

    # 標籤觸發警報動作，閃爍背景(紅色)來達到視覺注目效果(使用執行序來跑，以免畫面lock)
    def TriggerAlert(self):
        if self.__task is None:
            # 建立執行序實體
            self.__task = threading.Thread(target=self.__TagFlicker)
            self.__task.setDaemon(True)  # 設定保護執行序，會隨著主視窗關閉，執行序會跟著kill
            self.__flickerStatus = True  # 開啟背景閃爍
            self.__task.start()
            # 產生觸發時間與錄影檔名
            #nowTime = datetime.now()
            #cameraInfo = []
            # 觸發啟動攝影機動作
            # for camera in self.__cameraMappingTag:
            #    # 開啟攝影機畫面
            #    camera.openRtspBox()
            #    # 觸發錄影動作
            #    filename = nowTime.strftime('%Y%m%d%H%M%S') + \
            #        "-Alert" + str(self.pointid) + \
            #        "-Camera" + str(camera.pointid) + ".avi"
            #    RtspRecord({'cameraTagID': camera.pointid,
            #                'recordFileName': filename})
            #    # 蒐集錄影檔名，準備寫入DB
            #    cameraInfo.append({
            #        'cameraID': camera.pointid,
            #        'cameraName': camera.name,
            #        'recordFileName': filename
            #    })
            # 警示觸發時，記錄一筆異常紀錄
            #triggerTime = nowTime.strftime('%Y/%m/%d %H:%M:%S')
            # AbnormalUtil().InsertAbnormalRecord({
            #    'alertTime': triggerTime,
            #    'alertID': self.pointid,
            #    'alertName': self.name,
            #    'cameraInfo': cameraInfo
            # })

    # 停止警報觸發動作，停止背景閃爍
    def TriggerStop(self):
        self.__flickerStatus = False
        self.__task = None  # 停止閃爍，執行序清掉(等待python程序GC)，以利下一次觸發

    # 執行背景閃爍的特效(紅綠背景互換)
    def __TagFlicker(self):
        while self.__flickerStatus is True:
            self.canvas.itemconfig(self.bgid, fill='#ff0000')
            time.sleep(0.25)
            self.canvas.itemconfig(self.bgid, fill='#00ff00')
            time.sleep(0.25)

    # 連結異常紀錄清單，點擊該AlertTag的時候，開啟異常紀錄視窗，並直接切換到這一個警示點的異常紀錄清單
    # def linkAbnormalWindow(self, openMethod):
    #    # 註冊開啟異常紀錄視窗事件
    #    self.canvas.tag_bind(self.tagid, '<Button-1>',
    #                         lambda event: openMethod().queryBar.QueryAlertCombo(self.pointid))

    # 點擊該AlertTag動作，告警發生時，可關閉告警；無告景下點擊則開啟紀錄清單視窗，並直接切換到這一個警示點的異常紀錄清單
    def __TagClick(self):
        if self.__flickerStatus is True:
            self.TriggerStop()

    # 讓外界呼叫，根據與小米溫濕度計藍芽連接之上線狀況，切換狀態環的顏色
    def setOnlineStatus(self, onlineStatus):
        if onlineStatus:
            self.canvas.itemconfig(self.ringid, outline="#0000ff")
        else:
            self.canvas.itemconfig(self.ringid, outline="#ff0000")

    # 計算溫溼度數值標籤背景圖位置，這邊只是微調一下，讓畫面好看
    def getDataTagBGCoords(self, tagX, tagY):
        return (tagX - 40, tagY + 30, tagX + 60, tagY + 80)

    # 計算溫溼度數值標籤文字位置，這邊只是微調一下，讓畫面好看
    def getDataTagCoords(self, tagX, tagY):
        return (tagX + 10, tagY + 55)
