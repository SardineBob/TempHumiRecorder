import tkinter as tk
from PIL import Image, ImageTk


class Map():
    __canvas = None
    mapOriginWidth = 0
    mapOriginHeight = 0
    __mapPath = './resource/map.jpg'
    __mapLoad = None

    def __init__(self, canvas):
        self.__canvas = canvas
        self.__mapLoad = Image.open(self.__mapPath)
        self.mapOriginWidth = self.__mapLoad.width
        self.mapOriginHeight = self.__mapLoad.height
        # 在canvas容器中產生影像物件
        self.__canvas.create_image(0, 0, anchor=tk.NW, tags="Map")

    def Draw(self, width=640, height=480):
        # 如果視窗寬高大於原圖，則圖片置中移動
        X = 0 if width <= self.mapOriginWidth else (
            width - self.mapOriginWidth) / 2
        Y = 0 if height <= self.mapOriginHeight else (
            height - self.mapOriginHeight) / 2
        self.__canvas.coords("Map", X, Y)
        # 視窗寬度(高度)小於Map圖片原寬(高)，resize成視窗寬度(高度)，否則維持圖片原寬(高)
        width = width if width <= self.mapOriginWidth else self.mapOriginWidth
        height = height if height <= self.mapOriginHeight else self.mapOriginHeight
        # Map異動為指定的大小
        mapImage = self.__mapLoad.resize((width, height))
        # 讀入放PhotoImage的容器
        photoImg = ImageTk.PhotoImage(mapImage)
        # 繪製地圖影像
        self.__canvas.itemconfig("Map", image=photoImg)
        # ↓avoid garbage collection(避免資源被回收)(把圖片註冊到canvas這種廣域物件中，並自訂屬性，避免被回收)
        self.__canvas.mapImg = photoImg
