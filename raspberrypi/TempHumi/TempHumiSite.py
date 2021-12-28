from flask import Flask, request
from markupsafe import escape
import os
import subprocess

__rootPath = "/home/pi/Projects/TempHumiRecorder"
__deviceMacListFileName = f"{__rootPath}/deviceMacList.ini"
__deviceRootPath = f"{__rootPath}/devices"
app = Flask("TempHumiSite")


# 根據設定的Mac清單，逐一啟動第三方元件抓溫溼度數據
def actCaptrueTempHumi():
    # 讀出裝置MAC清單設定檔
    if not os.path.isfile(__deviceMacListFileName):
        print("尚未設定裝置Mac清單")
        return
    with open(__deviceMacListFileName, "r") as file:
        for mac in file.readlines():
            mac = mac.strip()
            # 開啟子程序，call第三方程式，擷取溫濕度計數值回來
            subprocess.Popen(f'python3 LYWSD03MMC.py -d {mac} -r -b -dp {__deviceRootPath} ', shell=True)


actCaptrueTempHumi()


# 存取設定頁面
@app.route("/TempHumi/setting")
def setting():
    macList = ""
    # 讀出裝置MAC清單設定檔
    if os.path.isfile(__deviceMacListFileName):
        with open(__deviceMacListFileName, "r") as file:
            macList = file.read()
    # 回應HTML頁面
    return """<script>
	            function button_onclick(){
		            var data = JSON.stringify({
		            	"deviceMacList": document.getElementById("deviceMacList").value
		            });
		            var xhr = new XMLHttpRequest();
		            xhr.withCredentials = true;
		            xhr.open("POST", "/TempHumi/setting/save");
		            xhr.setRequestHeader("Content-Type", "application/json");
		            xhr.send(data);
                    alert("設定存檔完成，將重啟樹梅派以載入新設定。");
	            }  
            </script>
            <form>
	            <p>溫溼度藍芽設備Mac清單(請使用enter區隔)</p>
	            <textarea id="deviceMacList" name="deviceMacList" rows="5" cols="50">""" + macList + """</textarea>
	            <br/>
	            <button type="button" onclick="button_onclick();">儲存</button>
            </form>"""


# 執行存檔
@app.route("/TempHumi/setting/save", methods=["POST"])
def settingSave():
    data = escape(request.get_json()["deviceMacList"])
    if data == "":
        return ""
    # 寫入裝置MAC清單設定檔
    with open(__deviceMacListFileName, "w") as file:
        file.write(data)
    # 重新啟動樹梅派
    os.system("sudo reboot")
    return ""


# 根據傳入藍芽裝置Mac，讀取溫濕度紀錄檔案
@app.route("/TempHumi/<MacAddress>")
def getTempHumi(MacAddress):
    macAddress = escape(MacAddress)
    macFile = macAddress.replace(":", "-")
    macFilePath = os.path.join(__deviceRootPath, macFile)
    # 找不到屬於該Mac的檔案，回傳none識別
    if not os.path.isfile(macFilePath):
        return "none"
    # 有找到檔案，將檔案內容拋出
    with open(macFilePath, "r") as file:
        return file.read()


app.run(host="0.0.0.0", port=9453)
