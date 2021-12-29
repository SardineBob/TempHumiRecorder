import tkinter as tk


class Tag():

    canvas = None
    relocate = None
    tagid = None
    bgid = None
    ringid = None
    pointid = None
    name = None
    tagX = 0  # 目前tag的座標位置
    tagY = 0
    tagW = 0
    tagH = 0
    oriTagX = 0  # 初始化時tag的座標位置，作為計算視窗縮放後新座標基準
    oriTagY = 0

    def __init__(self, canvas, relocate, pointid, name, x, y, picPhoto, tagName):
        self.canvas = canvas
        self.relocate = relocate
        self.pointid = pointid
        self.name = name
        self.tagX = self.oriTagX = x
        self.tagY = self.oriTagY = y
        self.tagW = picPhoto.width()
        self.tagH = picPhoto.height()
        # 繪製Tag背景圓型
        self.bgid = canvas.create_oval(
            self.getBGCoords(self.tagX, self.tagY),
            fill='#005AB5',
            tags=tagName
        )
        # 繪製Tag圖示
        self.tagid = canvas.create_image(
            x, y, image=picPhoto, anchor=tk.NW, tags=tagName)
        # 繪製Tag狀態環，可根據Tag特性，透過顏色識別目前物件的狀態
        self.ringid = self.canvas.create_oval(
            self.getRingCoords(self.tagX, self.tagY),
            outline='#ff0000',
            width=3
        )

    def Relocate(self):
        # 取得因為視窗縮放產生的新座標
        result = self.relocate.Relocate(self.oriTagX, self.oriTagY)
        self.tagX = result["newX"]
        self.tagY = result["newY"]
        # 重新定位tag(包含背景與狀態環)的位置
        self.canvas.coords(self.tagid, self.tagX, self.tagY)
        self.canvas.coords(self.bgid, self.getBGCoords(self.tagX, self.tagY))
        self.canvas.coords(
            self.ringid, self.getRingCoords(self.tagX, self.tagY))

    # 計算Tag背景的圓型位置，這邊只是微調一下，讓畫面好看
    def getBGCoords(self, tagX, tagY):
        return (
            tagX - 1,
            tagY + 1,
            tagX + self.tagW,
            tagY + 1 + self.tagH
        )

    # 計算狀態環的位置，只是微調，為了畫面呈現好看
    def getRingCoords(self, tagX, tagY):
        return (
            tagX - 2,
            tagY,
            tagX + self.tagW+1,
            tagY + 2 + self.tagH
        )
