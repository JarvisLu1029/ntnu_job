from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db import connection
from django.http import JsonResponse , HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.utils import ProgrammingError, OperationalError

# Create your views here.

def indexTest(request):
    return HttpResponse('Hello HttpResponse !')


def index(request):
    context = {}
    context["name"] = "測試"
    return render(request, "index.html", context)

# 使用者所有書籍
def get_books_by_user(request, user):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"SELECT title, author, published_year, note FROM {user}_books_info")
                books = cursor.fetchall()
                # 取得欄位名稱
                columns = [column[0] for column in cursor.description]
                # 將MySQL查詢結果轉換為字典
                books_dict = [dict(zip(columns, book)) for book in books]
                return JsonResponse(books_dict, safe=False)
            
            except:
                return HttpResponseBadRequest('No User')
    else:
        return HttpResponseBadRequest('無效的請求方法')

# 作者或關鍵字搜尋
def get_books_by_search(request, user):
    if request.method == 'GET':
        # 建立資料庫連接
        with connection.cursor() as cursor:
            try:
                # 取得前端網頁的欄位資料
                book_title = request.GET.get('book_title')
                author = request.GET.get('author')
                # 用作者篩選書籍列表
                if author and not book_title:
                    cursor.execute(f'SELECT title, author, published_year, note FROM {user}_books_info WHERE author = "{author}"')
                # 用書名關鍵字做篩選
                elif book_title:
                    cursor.execute(f'SELECT title, author, published_year, note FROM {user}_books_info WHERE title LIKE %s', ('%' + book_title + '%',))

                books = cursor.fetchall()
                # 取得欄位名稱
                columns = [column[0] for column in cursor.description]
                # 將MySQL查詢結果轉換為字典
                books_dict = [dict(zip(columns, book)) for book in books]
                # 返回字典
                return JsonResponse(books_dict, safe=False)
            except:
                return JsonResponse('查無資料',safe=False)
    else:
        return HttpResponseBadRequest('無效的請求方法')

# 排序查詢
def get_books_orderby(request,user,sort):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            try:
                if sort == "asc":
                    cursor.execute(f"SELECT title, author, published_year, note FROM {user}_books_info order by published_year,author")
                else:
                    cursor.execute(f"SELECT title, author, published_year, note FROM {user}_books_info order by published_year,author desc")
                books = cursor.fetchall()
                # 取得欄位名稱
                columns = [column[0] for column in cursor.description]
                # 將MySQL查詢結果轉換為字典
                books_dict = [dict(zip(columns, book)) for book in books]
                return JsonResponse(books_dict, safe=False)
            
            except:
                return HttpResponseBadRequest('No User')
    else:
        return HttpResponseBadRequest('無效的請求方法')

# 新增書籍
@csrf_exempt  # 必要的 POST 請求 CSRF 豁免權限
def book_add(request, user):
    if request.method == 'POST':
        body = json.loads(request.body)
        title = body.get('title')
        author = body.get('author')
        published_year = body.get('published_year')
        # 檢查必要的欄位是否存在
        if not (title and author and published_year):
            return HttpResponseBadRequest('缺少書籍資料')

        with connection.cursor() as cursor:
            # 如果使用者的表不存在，則創建該表
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {user}_books_info \
                             (id INT(11) NOT NULL AUTO_INCREMENT, \
                              title VARCHAR(50) NOT NULL, \
                              author VARCHAR(50) NOT NULL, \
                              published_year INT(4) NOT NULL, \
                              note varchar(2000), \
                              PRIMARY KEY (id)) \
                              DEFAULT CHARSET=utf8mb4")
            # 檢查書籍是否已存在
            cursor.execute(f"SELECT * FROM {user}_books_info WHERE title=%s",
                           (title,))
            result = cursor.fetchone()
            if result:
                print('資料已存在')
                return JsonResponse('書籍已存在', safe=False)
            else:
                # 插入新書籍到數據庫
                cursor.execute(f"INSERT INTO {user}_books_info (title, author, published_year) \
                                 VALUES (%s, %s, %s)",
                               (title, author, published_year))
                print('資料新增成功')
                return JsonResponse(f'{title}新增成功', safe=False)
    else:
        return HttpResponseBadRequest('無效的請求方法')


# 刪除書籍
@csrf_exempt  # 請求 CSRF 豁免權限    
def book_delete(request, user, title):
    if request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {user}_books_info WHERE title=%s", [title])
        return HttpResponse("Book deleted")
    else:
        return HttpResponseBadRequest('無效的請求方法')
    

# 編輯書籍
@csrf_exempt  # 請求 CSRF 豁免權限
def book_update(request, user, title):
    if request.method == 'PUT':
        book = json.loads(request.body)
        with connection.cursor() as cursor:
            # 檢查書籍是否已存在
            cursor.execute(f"SELECT * FROM {user}_books_info WHERE title=%s", [title])
            result = cursor.fetchone()
            if not result:
                print('Book not exists')
                return JsonResponse('書籍清單找不到這本書' ,safe=False)

            # 判斷要修改的資料有哪些    
            update_values = {}
            if 'title' in book:
                if isinstance(book['title'], str) and book['title'] != '':
                    update_values['title'] = book['title']
            if 'author' in book:
                if isinstance(book['author'], str) and book['author'] != '':
                    update_values['author'] = book['author']
            if 'published_year' in book:
                if isinstance(book['published_year'], str) and book['published_year'] != '':
                    update_values['published_year'] = book['published_year']
            # 檢查傳送修改的資料
            print(book)
            print(update_values)

            if update_values:
                set_clause = ', '.join([f"{key} = %s" for key in update_values.keys()])
                values = list(update_values.values()) + [title]
                query = f"UPDATE {user}_books_info SET {set_clause} WHERE title=%s"
                cursor.execute(query, values)
                return JsonResponse(f'{title}修改成功', safe=False)
            else:
                return JsonResponse(f'{title}修改失敗', safe=False)
    else:
        return HttpResponseBadRequest('無效的請求方法')
    
# 編輯心得    
@csrf_exempt  # 請求 CSRF 豁免權限   
def book_note_update(request, user, title):
    if request.method == 'PUT':
        with connection.cursor() as cursor:
            # 檢查書籍是否已存在
            cursor.execute(f"SELECT * FROM {user}_books_info WHERE title=%s", [title])
            result = cursor.fetchone()
            if not result:
                print('Book not exists')
                return JsonResponse('書籍清單找不到這本書' ,safe=False)
            body = json.loads(request.body)
            note = body.get('note')
            if note:
                cursor.execute(f"UPDATE {user}_books_info SET note = %s WHERE title = %s", [note, title])
                return JsonResponse(f'{title}心得更新成功' ,safe=False)
            else:
                return JsonResponse('請輸入心得',safe=False, status=400)

    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            # 檢查書籍是否已存在
            cursor.execute(f"SELECT * FROM {user}_books_info WHERE title=%s", [title])
            result = cursor.fetchone()
            if not result:
                print('Book not exists')
                return JsonResponse('書籍清單找不到這本書' ,safe=False)
            cursor.execute(f"UPDATE {user}_books_info SET note = null WHERE title = %s", [title])
        return JsonResponse(f'{title}心得刪除成功',safe=False)
    else:
        return HttpResponseBadRequest('無效的請求方法')




