import os
import json
from urllib import request
from component.Tag import Tag
from PIL import Image, ImageTk
import time
import threading
from utilset.ConfigUtil import ConfigUtil
from utilset.DbAccessUtil import DbAccessUtil
from component.Buzzer import Buzzer

# 背景圓：平常為綠色，警報發生時，呈現紅色閃爍
# 狀態環：識別樹梅派WebSocket訊號是否連結的呈現(紅色：未連結，藍色：已連結)


class AlertTag(Tag):

    __picPath = './resource/IconAlert.png'
    __tagsName = "alert"  # 標籤名稱，綁定canvas繪製物件的標籤
    __task = None
    __flickerStatus = False  # 控制Tag閃爍的開關
    __dataTagBg = None  # 溫溼度標籤背景
    __dataTag = None  # 溫溼度標籤
    __deviceMac = None  # 屬於這顆標籤對應的小米溫溼度藍芽位址
    __upLimitTemp = None  # 上限警報溫度
    __lowLimitTemp = None  # 下限警報溫度
    __upLimitHumi = None  # 上限警報濕度
    __lowLimitHumi = None  # 下限警報濕度
    __deviceRootPath = None  # 與第三方元件取得小米溫濕度數值後，寫入的檔案root位置
    __buzzer = None  # 蜂鳴警報器物件
    __dbAccessUtil = None  # sqlite db物件
    __raspberryUrl = "http://raspberrypi:9453/TempHumi/"  # 架設溫溼度數據於樹梅派站台URL

    def __init__(self, canvas, relocate, configItem):
        # 取出需用到的設定值
        pointid = configItem["id"]
        name = configItem["name"]
        x = configItem["tagX"]
        y = configItem["tagY"]
        self.__deviceMac = configItem["mac"]
        self.__upLimitTemp = configItem["tempuplimit"]
        self.__lowLimitTemp = configItem["templowlimit"]
        self.__upLimitHumi = configItem["humiuplimit"]
        self.__lowLimitHumi = configItem["humilowlimit"]
        self.__deviceRootPath = ConfigUtil().DeviceRootPath
        self.__buzzer = Buzzer()
        self.__dbAccessUtil = DbAccessUtil()
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
        # 建立溫溼度訊號執行緒
        self.createThreadTask()

    # 在Tag下方顯示溫溼度標籤
    def CreateDataTag(self):
        # 繪製背景
        bgX1, bgY1, bgX2, bgY2 = self.getDataTagBGCoords(self.tagX, self.tagY)
        bgImg = ImageTk.PhotoImage(Image.new(mode="RGBA", size=(bgX2-bgX1, bgY2-bgY1), color=(0, 0, 0, 125)))
        self.__dataTagBg = self.canvas.create_image(bgX1, bgY1, image=bgImg, anchor='nw', tags=self.__tagsName)
        self.canvas.dataTagBg = bgImg
        # 繪製資料
        self.__dataTag = self.canvas.create_text(
            self.getDataTagCoords(self.tagX, self.tagY),
            text="電量:??%\n溫度:??℃\n濕度:??%",
            fill='#FFFFFF',
            font=("Arial", 12),
            tags=self.__tagsName
        )

    # 建立執行緒動作
    def createThreadTask(self):
        # 建立一個執行緒，觸發透過溫溼度數值檔案，將最新數據呈現
        readTempHumiDataTask = threading.Thread(target=self.readTempHumiData)
        readTempHumiDataTask.setDaemon(True)
        readTempHumiDataTask.start()

    # 讀取溫溼度檔案，呈現最新數據
    def readTempHumiData(self):
        offlineCount = 0  # 讀取不到檔案幾次顯示離線(6次，6*5=30秒)
        captureTime = ConfigUtil().CaptureTime
        # 每設定秒數讀取一次檔案的數值
        while True:
            # 向樹梅派溫溼度數據站台取得資料
            try:
                with request.urlopen(f"{self.__raspberryUrl}{self.__deviceMac}") as res:
                    resData = str(res.read().decode("utf-8"))
            except:
                print(offlineCount, '無法連線，嘗試重連。')
                resData = "none"
            # 站台回傳none訊息，表示無此Mac的溫溼度數據檔案資料，則表示離線狀態
            if resData == "none":
                if(offlineCount >= 5):
                    self.setOnlineStatus(False)
                    self.TriggerAlert()
                offlineCount = offlineCount + 1
                time.sleep(captureTime)
                continue
            # 讀取最新數值，只有一行，json資料結構
            data = json.loads(resData)
            # 於畫面上更新數值
            self.canvas.itemconfig(self.__dataTag, text="電量:%s%%\n溫度:%s℃\n濕度:%s%%" %
                                   (data["Battery"], data["Temp"], data["Humi"]))
            # 檢查目前溫溼度數值是否異常
            tempIsOK = self.checkTemp(data["Temp"])
            humiIsOK = self.checkTemp(data["Humi"])
            # 執行寫入db
            self.insertTempHumiData({
                "Temp": data["Temp"],
                "Humi": data["Humi"],
                "Battery": data["Battery"],
                "TempIsOK": tempIsOK,
                "HumiIsOK": humiIsOK
            })
            # 溫溼度其中一個異常，觸發告警
            if tempIsOK is False or humiIsOK is False:
                self.TriggerAlert()
            else:
                self.TriggerStop()  # 異常恢復，自動關閉告警
            # 成功讀取最新數值，offline狀態清空
            offlineCount = 0
            self.setOnlineStatus(True)
            time.sleep(captureTime)

    # 判斷目前溫度，是否異常，超出設定界線則觸發告警
    def checkTemp(self, nowTemp):
        return float(nowTemp) >= float(self.__lowLimitTemp) and float(nowTemp) <= float(self.__upLimitTemp)

    # 判斷目前濕度，是否異常，超出設定界線則觸發告警
    def checkHumi(self, nowHumi):
        return float(nowHumi) >= float(self.__lowLimitHumi) and float(nowHumi) <= float(self.__upLimitHumi)

    # 將收到的溫溼度寫入sqlite db
    def insertTempHumiData(self, data):
        self.__dbAccessUtil.writeTempHumi({
            'id': self.pointid,
            'name': self.name,
            'temperature': data['Temp'],
            'humidity': data['Humi'],
            'isTempUnusual': not data['TempIsOK'],
            'isHumiUnusual': not data['HumiIsOK'],
            'upTempLimit': self.__upLimitTemp,
            'lowTempLimit': self.__lowLimitTemp,
            'upHumiLimit': self.__upLimitHumi,
            'lowHumiLimit': self.__lowLimitHumi,
            'deviceMac': self.__deviceMac,
            'battery': data['Battery']
        })

    # 標籤觸發警報動作，閃爍背景(紅色)來達到視覺注目效果(使用執行序來跑，以免畫面lock)
    def TriggerAlert(self):
        if self.__task is None:
            # 建立執行序實體
            self.__task = threading.Thread(target=self.__TagFlicker)
            self.__task.setDaemon(True)  # 設定保護執行序，會隨著主視窗關閉，執行序會跟著kill
            self.__flickerStatus = True  # 開啟背景閃爍
            self.__task.start()
            # 啟動異常警示語音播報
            self.__buzzer.trigger()

    # 停止警報觸發動作，停止背景閃爍
    def TriggerStop(self):
        self.__flickerStatus = False
        self.__task = None  # 停止閃爍，執行序清掉(等待python程序GC)，以利下一次觸發
        self.__buzzer.close()  # 停止警示語音播報
        self.__buzzer.switchOnOff(True)  # 異常排除，恢復警報器

    # 執行背景閃爍的特效(紅藍背景互換)
    def __TagFlicker(self):
        while self.__flickerStatus is True:
            self.canvas.itemconfig(self.bgid, fill='#ff0000')
            time.sleep(0.25)
            self.canvas.itemconfig(self.bgid, fill='#005AB5')
            time.sleep(0.25)

    # 連結異常紀錄清單，點擊該AlertTag的時候，開啟異常紀錄視窗，並直接切換到這一個溫溼度計的異常紀錄清單
    def linkAbnormalWindow(self, openMethod):
        # 註冊開啟異常紀錄視窗事件
        self.canvas.tag_bind(self.tagid, '<Double-Button-1>',
                             lambda event: openMethod().queryBar.QueryAlertCombo(self.pointid, self.name))

    # 點擊該AlertTag動作，告警發生時，可關閉告警；無告景下點擊則開啟紀錄清單視窗，並直接切換到這一個警示點的異常紀錄清單
    def __TagClick(self):
        if self.__flickerStatus is True:
            self.TriggerStop()
        self.__buzzer.close()  # 停止警示語音播報
        self.__buzzer.switchOnOff(False)  # 暫時關閉警報器

    # 讓外界呼叫，根據與小米溫濕度計藍芽連接之上線狀況，切換狀態環的顏色
    def setOnlineStatus(self, onlineStatus):
        if onlineStatus:
            self.canvas.itemconfig(self.ringid, outline="#00ff00")
            self.__buzzer.switchOnOff(True)  # 恢復連線，恢復警報器
        else:
            self.canvas.itemconfig(self.ringid, outline="#ff0000")
            self.__buzzer.trigger()  # 啟動離線警示語音播報
            # 離線時更新數值為問號
            self.canvas.itemconfig(self.__dataTag, text="電量:??%\n溫度:??℃\n濕度:??%")

    # 視窗大小異動時，更新座標位置
    def Relocate(self):
        super().Relocate()
        bgX1, bgY1, bgX2, bgY2 = self.getDataTagBGCoords(self.tagX, self.tagY)
        self.canvas.coords(self.__dataTagBg, bgX1, bgY1)
        self.canvas.coords(self.__dataTag, self.getDataTagCoords(self.tagX, self.tagY))

    # 計算溫溼度數值標籤背景圖位置，這邊只是微調一下，讓畫面好看
    def getDataTagBGCoords(self, tagX, tagY):
        return (tagX - 40, tagY + 30, tagX + 60, tagY + 90)

    # 計算溫溼度數值標籤文字位置，這邊只是微調一下，讓畫面好看
    def getDataTagCoords(self, tagX, tagY):
        return (tagX + 10, tagY + 60)
