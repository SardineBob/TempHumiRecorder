from websocket import enableTrace, WebSocketApp
import threading
import time


class RaspberryPiSignal:

    __id = None
    __wsUrl = None
    __alertMappingID = None  # 這支樹梅派對應的「AlertPoint」ID
    __alertMappingObj = None  # 這支樹梅派對應的「AlertPoint」實體物件，用於訊號觸發時，驅動物件某個動作
    __ws = None
    __task = None

    def __init__(self, configItem):
        # enableTrace(True)  # 啟動偵錯模式
        # 取出需用到的設定值
        self.__id = configItem['number']
        self.__wsUrl = configItem['url']
        self.__alertMappingID = configItem['alertLink']
        self.__createTask()

    # 將接收websocket訊號的方法，使用執行序背景執行
    def __createTask(self):
        if self.__task is None:
            self.__task = threading.Thread(target=self.__createWebsocket)
            self.__task.setDaemon(True)  # 設定保護執行序，會隨著主視窗關閉，執行序會跟著kill
            self.__task.start()

    # 關閉執行序
    def closeTask(self):
        self.__ws.close()
        self.__ws = None
        self.__task = None
        # 更新AlertTag的連線狀態
        if self.__alertMappingObj is not None:
            for item in self.__alertMappingObj:
                item.setOnlineStatus(False)
        # 五秒後重新嘗試連線
        time.sleep(5)
        self.__createTask()

    # 產生WebSocket連線
    def __createWebsocket(self):
        if self.__ws is not None:
            return
        self.__ws = WebSocketApp(
            self.__wsUrl,
            on_open=self.__onOpen,
            on_message=self.__onMessage,
            on_error=self.__onError,
            on_close=self.__onClose
        )
        self.__ws.run_forever()

    def __onMessage(self, message):
        if self.__alertMappingObj is None:
            return
        # 根據收到的Websocket哪一個Alert設備，去執行這一個AlertTag觸發警報事件
        self.__alertMappingObj[int(message)].TriggerAlert()
        print("收到的Alert Tag號碼" + message)

    def __onError(self, error):
        print('---id:{},URL:{}，發生連線錯誤，錯誤訊息：{}---'.format(self.__id, self.__wsUrl, error))
        # self.closeTask()

    def __onClose(self):
        print('---id:{},URL:{}，已斷線(五秒後重新連線)---'.format(self.__id, self.__wsUrl))
        self.closeTask()

    def __onOpen(self):
        print('---id:{},URL:{}，已連線---'.format(self.__id, self.__wsUrl))
        # 更新AlertTag的連線狀態
        if self.__alertMappingObj is not None:
            for item in self.__alertMappingObj:
                item.setOnlineStatus(True)

    # 連結警示點，根據設定檔中這支樹梅派連接的警示點ID，取出實體物件，準備訊號觸發時，啟動警報動作
    def linkAlert(self, alertTagCollection):
        self.__alertMappingObj = []
        for id in self.__alertMappingID:
            self.__alertMappingObj.append(alertTagCollection[id-1])
