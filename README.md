# 實作一套個人書籍管理系統的後端API

  
  如何將系統開發環境架設起來,需要寫到能讓我們看得懂如何架設你的系統
  
  API說明文件:總共有幾隻API、每個API的URL是什麼、怎麼帶入參數、預期的輸出是什麼、有哪些錯誤訊息

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
        - 預期輸出 ⇒ `return JsonResponse('修改成功', safe=False)`
        - 錯誤訊息 ⇒ `return JsonResponse({'message': 'Book not exists'}, status=404)`
5. 使用者可以為某一本書籍新增、刪除、編輯閱讀心得
    - `PUT DELETE /books/<str:user>/<str:title>/note`
        - 輸入書名後前端兩個按鈕分別接收 PUT / DELETE 給後端判斷
        - 
6. 使用者可以篩選出同個作者的書籍列表/使用者可以透過關鍵字在書名欄位中搜尋,找到他們要找的書籍
    - `GET /books/<str:user>/book_search/`
7. 使用者可以依照作者與出版年排列書籍列表
    - `GET /books/<str:user>/orderby/<str:sort>`
  
  資料庫說明文件:有幾張資料表、資料表欄位的資料型態是什麼、資料庫關聯圖
  
