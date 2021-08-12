# 目的
實作旅遊電商平台，包含展示、會員、金流等功能，做為前後端學習的專案練習。<br>
1. 利用政府提供的台北景點資訊API取得資料，存入AWS RDS- MySQL，讓前端透過AJAX技術，取得景點資料並展示<br>
2. 建立會員註冊、登入、登出等功能，讓會員能夠建立自己的訂單<br>
3. 訂單建立後，串接TapPay金流API，提供付款服務<br>

***

# Demo

click <a href="https://taipei-travel.blucas0707.com/">here</a><br>
test account:123123123123@gmail.com<br>
test password:123123123123<br>

***

# 功能
1. 會員：會員註冊（前後端資料錯誤驗證提醒、加密）／登入／登出
2. 展示：景點展示、捲動式呈現、淡出淡入、
3. 景點：日期選擇(過期日期判斷)、圖片輪轉式呈現
4. 金流：信用卡付款（信用卡資訊驗證）

***

# 流程圖

<div align=center><img src="https://github.com/Blucas0707/taipei-day-trip-website/blob/develop/README/Flow/flowpng.png" alt="" width="100%"/></div>

### 資料收集＆儲存

利用政府開放API取得台北景點資訊，並存入AWS RDS MySQL中。

___

#### 資料庫配置

共只有一個Database: travel_info <br>
包含五個table: 
1. taipei_travel_info: 景點資訊
2. taipei_travel_booking: 預定資訊
3. taipei_travel_orders: 訂單資訊
4. taipei_travel_images: 景點圖片資訊
6. taipei_travel_user_info: 會員資訊

<div align=center><img src="https://github.com/Blucas0707/taipei-day-trip-website/blob/develop/README/Flow/SQL_tables.png" alt="" width="40%"/></div>
<div align=center><img src="https://github.com/Blucas0707/taipei-day-trip-website/blob/develop/README/Flow/user.png" alt="" width="30%"/></div>

___

#### TapPay 

<div align=center><img src="https://github.com/Blucas0707/taipei-day-trip-website/blob/develop/README/Flow/TapPay.png" alt="" width="50%"/></div>

共分成4步驟：
1. Client 會去跟TapPay Server 取得一組專屬Prime
2. 將Prime 傳到後端Server作處理
3. 後端Server 會用這組Prime，去跟TapPay Server 要求付款(TapPay 會去跟Bank Server去請求付款)
4. 後端Server會接收TapPay付款結果，並回傳付款狀態回Client

