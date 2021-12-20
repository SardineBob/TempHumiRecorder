class WindowRelocate():

    __curWindowWidth = None
    __curWindowHeight = None
    __oriWindowWidth = None
    __oriWindowHeight = None
    __oriMapWidth = None
    __oriMapHeight = None

    def __init__(self, para):
        # 取出KV結構內資料待處理
        self.__oriWindowWidth = para['oriWindowWidth'] if 'oriWindowWidth' in para else 640
        self.__oriWindowHeight = para['oriWindowHeight'] if 'oriWindowHeight' in para else 480
        self.__oriMapWidth = para['oriMapWidth'] if 'oriMapWidth' in para else 640
        self.__oriMapHeight = para['oriMapHeight'] if 'oriMapHeight' in para else 480
        self.__curWindowWidth = self.__oriWindowWidth
        self.__curWindowHeight = self.__oriWindowHeight

    # 設定縮放後目前視窗寬高
    def SetCurrentSize(self, newWidth, newHeight):
        self.__curWindowWidth = newWidth
        self.__curWindowHeight = newHeight

    # 根據目前視窗的縮放比例，計算出新的座標位置
    def Relocate(self, oriX, oriY):
        # 計算目前視窗寬高與原寬高異動比率(ex.據比例調整保全器材位置)
        ratioWidth = self.__curWindowWidth / self.__oriWindowWidth if self.__curWindowWidth <= self.__oriMapWidth \
            else self.__oriMapWidth / self.__oriWindowWidth
        ratioHeight = self.__curWindowHeight / self.__oriWindowHeight if self.__curWindowHeight <= self.__oriMapHeight \
            else self.__oriMapHeight / self.__oriWindowHeight
        # 判斷視窗放大超過原始地圖寬高，則增加空白偏移量(因地圖在視窗置中，故(視窗寬高-地圖寬高) / 2)
        offsetX = 0 if self.__curWindowWidth <= self.__oriMapWidth \
            else (self.__curWindowWidth - self.__oriMapWidth) / 2
        offsetY = 0 if self.__curWindowHeight <= self.__oriMapHeight \
            else (self.__curWindowHeight - self.__oriMapHeight) / 2
        # 計算新的座標位置
        newX = oriX * ratioWidth + offsetX
        newY = oriY * ratioHeight + offsetY
        # 回傳一份新座標位置的物件
        return {"newX": newX, "newY": newY}
