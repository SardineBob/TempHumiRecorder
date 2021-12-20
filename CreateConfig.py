import configparser
import json

filePath = 'config.ini'
config = configparser.ConfigParser()

# 產生系統設定參數
# config['SystemConfig'] = {
#    'IsLinkRaspberry': json.dumps(True),  # 連結樹梅派Websocket訊號開關
#    'VideoTime': json.dumps(10),  # 錄影片段時間(以秒為單位，0秒為影片關閉後才停止錄影)
# }

# 產生樹梅派URL位址資料
# config['RaspberryPiWebsocket'] = {
#    'device': json.dumps([
#        {'number': 1, 'url': 'ws://localhost:9453', 'alertLink': [2, 3]},
#        {'number': 2, 'url': 'ws://localhost:9453', 'alertLink': [1]},
#        {'number': 3, 'url': 'ws://localhost:9453', 'alertLink': [4, 5]},
#    ], ensure_ascii=False)
# }

# 產生警報點位置資料
# config['AlertPoint'] = {
#    'point': json.dumps([
#        {'number': 1, 'name': 'A棟地下前門', 'X': 25,
#            'Y': 25, 'cameraLink': [2, 4]},
#        {'number': 2, 'name': 'A棟地下後門', 'X': 50,
#            'Y': 50, 'cameraLink': [1, 5]},
#        {'number': 3, 'name': 'B棟東邊前門', 'X': 75, 'Y': 75, 'cameraLink': [3]},
#        {'number': 4, 'name': 'B棟西邊前門', 'X': 100,
#            'Y': 100, 'cameraLink': [1, 3]},
#        {'number': 5, 'name': 'C棟大門', 'X': 125,
#            'Y': 125, 'cameraLink': [2, 3, 5]}
#    ], ensure_ascii=False)
# }
# 產生攝影機位置資料
# config['CameraPoint'] = {
#    'point': json.dumps([
#        {'number': 1, 'name': 'A棟地下前門右側', 'X': 125, 'Y': 25,
#            'rtspUrl': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'},
#        {'number': 2, 'name': 'A棟地下前門左側', 'X': 150, 'Y': 50,
#            'rtspUrl': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'},
#        {'number': 3, 'name': 'B棟西邊前門正對面', 'X': 175, 'Y': 75,
#            'rtspUrl': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'},
#        {'number': 4, 'name': 'C棟大門前方', 'X': 200, 'Y': 100,
#            'rtspUrl': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'},
#        {'number': 5, 'name': 'C棟大門左側', 'X': 225, 'Y': 125,
#            'rtspUrl': 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'}
#    ], ensure_ascii=False)
# }

# 產生溫溼度監控位置資料
config['AlertPoint'] = {
    'point': json.dumps([
        {'number': 1, 'name': 'A棟地下前門', 'X': 25, 'Y': 25},
        {'number': 2, 'name': 'A棟地下後門', 'X': 50, 'Y': 50},
        {'number': 3, 'name': 'B棟東邊前門', 'X': 75, 'Y': 75},
        {'number': 4, 'name': 'B棟西邊前門', 'X': 100, 'Y': 100},
        {'number': 5, 'name': 'C棟大門', 'X': 125, 'Y': 125}
    ], ensure_ascii=False)
}

# 寫入設定檔
with open('config.ini', 'w', encoding='UTF8') as configFile:
    config.write(configFile)
