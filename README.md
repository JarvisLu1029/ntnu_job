# 實作一套個人書籍管理系統的後端API

### 如何將系統開發環境架設起來,需要寫到能讓我們看得懂如何架設你的系統
1. 使用 VMware 啟動一台虛擬機 ( Ubuntu 22.04 )
2. 使用 VS code Remote SSH 至 VMware 撰寫文件
3. 使用 Docker (23.0.1) 建立 Dockerfile 架設 Python ( 3.11 ) 安裝Django、PyMySQL套件
4. 使用 Docker-compose (2.16.0) 啟動 Python、MySQL ( 8.0 ) 部屬至 GCP 啟動服務
5. 網站連結 : <http://35.236.155.54/index/>    使用者可輸入範例 : 小明

### API說明文件:總共有幾隻API、每個API的URL是什麼、怎麼帶入參數、預期的輸出是什麼、有哪些錯誤訊息

API說明文件:總共有幾隻API、每個API的URL是什麼、怎麼帶入參數、預期的輸出是什麼、有哪些錯誤訊息

1. 使用者輸入姓名查詢可以查看該使用者的書籍列表
    - `GET /books/<str:user>`
        - 預期輸出 ⇒ `return JsonResponse(books_dict, safe=False)`
        - 錯誤訊息 ⇒ `return HttpResponseBadRequest('No User')` ⇒ 前端網頁顯示『該使用者尚未建立書籍，請新增第一本書籍』
2. 使用者可新增書籍以及為該書籍建立書籍資訊,書籍資訊至少需包括作者、出版年、書名 
    - `POST /books/<str:user>/add/`
        - 前端有三個 input 讓使用者輸入作者、出版年、書名 ，皆須輸入才可送出
        - 預期輸出 ⇒ `return JsonResponse('書籍新增成功', safe=False)`
        - 錯誤訊息 ⇒ `JsonResponse('書籍已存在', safe=False)`
3. 使用者可以刪除書籍
    - `DELETE /books/<str:user>/del_<str:title>`
        - 前端有按鈕讓使用者針對書籍查詢結果做刪除
        - 預期輸出 ⇒ `return HttpResponse("Book deleted")`
        - 錯誤訊息 ⇒ `return HttpResponseBadRequest('無效的請求方法')`
4. 使用者可以編輯書籍資訊
    - `PUT /books/<str:user>/update_<str:title>`
        - 前端讓使用者先輸入欲修改書籍名稱 ⇒ 新的書名、作者、出版年 可擇一輸入
        - 預期輸出 ⇒ `return JsonResponse(f'{title}修改成功', safe=False)`
        - 錯誤訊息 ⇒ `return JsonResponse('書籍清單找不到這本書' ,safe=False)`
5. 使用者可以為某一本書籍新增、刪除、編輯閱讀心得
    - `PUT DELETE /books/<str:user>/<str:title>/note`
        - 輸入書名給前端兩個按鈕分別接收 PUT / DELETE 給後端判斷
        - PUT 預期輸出 ⇒ `return JsonResponse(f'{title}心得更新成功' ,safe=False)`
        - DELETE 預期輸出 ⇒ `return JsonResponse(f'{title}心得刪除成功',safe=False)`
        - 錯誤訊息 ⇒ `return HttpResponseBadRequest('無效的請求方法')`
6. 使用者可以篩選出同個作者的書籍列表/使用者可以透過關鍵字在書名欄位中搜尋,找到他們要找的書籍
    - `GET /books/<str:user>/book_search/`
        - 前端分別有『書名關鍵字 』及 『作者』兩個欄位 ⇒ 依據給的資料回傳不同的資料庫篩選方式
        - 預期輸出 ⇒ `return JsonResponse(books_dict, safe=False)`
        - 錯誤訊息 ⇒ `return HttpResponseBadRequest('無效的請求方法')`
7. 使用者可以依照作者與出版年排列書籍列表
    - `GET /books/<str:user>/orderby/<str:sort>`
        - 提供排序查詢按鈕
        - 預期輸出 ⇒ `return JsonResponse(books_dict, safe=False)`
        - 錯誤訊息 ⇒ `return HttpResponseBadRequest('無效的請求方法')`
  
### 資料庫說明文件:有幾張資料表、資料表欄位的資料型態是什麼、資料庫關聯圖
  有新的使用者就會建立新的Table ⇒ 用 **<使用者名稱>_books_info** 命名
  - ID INT(11)
  - 書名(title) VARCHAR(50)
  - 作者(author) VARCHAR(50)
  - 出版年(published_year) INT(4)
  - 讀書心得(note) VARCHAR(2000)
