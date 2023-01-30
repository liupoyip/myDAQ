# 量測系統建設

## **目標可用硬體**
- 任何支援PC的麥克風
  - USB
  - 3.5mm
- NI 9234 (with cDAQ-9171)
  - accelerometer
  - microphone
- 未來可擴充性
  - NI 相關產品
  - webcam

---

## **開發環境**
- **相容OS**
  - Windows / Linux(未來目標)
- **主要程式語言**
  - python
- **資料庫**
  - MongoDB
- **Packages**
  - Common data processing and scientific
    - numpy : array and math function
    - scipy : math function
    - matplotlib : mathematical visualization
    - pandas : Dataframe
  - NI
    - nidaqmx : NI DAQ裝置
  - Microphone (PC)
    - sounddevice : 麥克風
  - GUI framework
    - PyQt6 : 跨平台GUI介面，並支援許多數學圖形
  - Database
    - PyMongo : Control Mongo Database

---

# Roadmap

## **短期目標**
- 從 sensor 至 pc 紀錄資料
- 數學功能 function
  - 即時運算
    - 頻譜圖
    - 時頻圖
    - 統計特徵
- UI
  - 可選擇裝置
  - 即時顯示
    - 波形(waveform)
    - 頻譜圖 / 時頻圖
  - 對外參數
    - 資料擷取模式
      - 定時
      - 手動 on/off
    - Trigger : 即時顯示圖形
    - Triiger : 儲存資料
- 其他議題
  - UX
    - 思考UI面板在操作上的流程，愈簡單愈好。
    - 功能互鎖條件

---

## **長期目標**
- Local
  - 開放參數資料儲存路徑
  - 將資料串接上 MongoDB
- Remote
  - 將資料通過 internet (固定IP) 串接上 **MongoDB**