import threading
import time
from playsound import playsound


# 警報器，當溫度/濕度或離線時超出正常範圍時觸發
class Buzzer():

    __alertSoundTask = None  # 警報進行中的執行緒，負責不斷撥放警報語音
    __alertUnusual = False
    __alertSoundPath = "./resource/alert.mp3"
    __alertOn = False  # 是否啟動警報機制，預設關閉

    # 初始化，建立警報語音撥放執行緒
    def __init__(self):
        # 判斷如果執行緒沒開啟，則建立播放警報語音的執行緒
        if self.__alertSoundTask is None:
            self.__alertSoundTask = threading.Thread(target=self.__alertSoundEvent)
            self.__alertSoundTask.setDaemon(True)
            self.__alertSoundTask.start()

    # 觸發溫度異常警報，播放語音
    def trigger(self):
        # 判斷如果關閉警報，則不觸發
        if self.__alertOn is False:
            return
        # 啟動播放告警語音
        self.__alertUnusual = True

    # 關閉警報，停止撥放語音
    def close(self):
        # 清空狀態
        self.__alertUnusual = False

    # 執行不斷撥放警報語音動作
    def __alertSoundEvent(self):
        while True:
            if self.__alertUnusual is True:
                playsound(self.__alertSoundPath)
            time.sleep(1)

    # 給予外界判斷，是否關閉該警報器
    def switchOnOff(self, switch):
        self.__alertOn = switch
