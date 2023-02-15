from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)
db = pymysql.connect(host='localhost', user='root',
                     password='passw0rd!', database='NTNU_books', charset='utf8mb4')


@app.route('/')
def index():
    return render_template('index.html')


# 使用者可新增書籍以及為該書籍建立書籍資訊,書籍資訊至少需包括作者、出版年、書名
@app.route('/books/<user>/add', methods=['POST'])
def book_add(user):
    book = request.get_json()
    # 檢查是否至少有書名、作者、出版年
    if not (book['title'] and book['author'] and book['published_year']):
        return 'Missing book data'

    cursor = db.cursor()

    # 使用者第一次使用就建立該使用者的table
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {user}_books_info (id INT(11) NOT NULL AUTO_INCREMENT,title VARCHAR(50) NOT NULL,author VARCHAR(50) NOT NULL,\
                   published_year INT(10) NOT NULL,note varchar(2000),PRIMARY KEY (id)) DEFAULT CHARSET=utf8mb4')
    db.commit()

    # 檢查書籍是否已存在
    cursor.execute(f'SELECT * FROM {user}_books_info WHERE title=%s AND author=%s AND published_year=%s', (book['title'], book['author'], book['published_year']))
    result = cursor.fetchone()
    if result:
        print('Data already exists')
        return jsonify('Book already exists')
    else:
        cursor.execute(f'INSERT INTO {user}_books_info (title, author, published_year) VALUES (%s, %s, %s)',
                       (book['title'], book['author'], book['published_year']))
        db.commit()
        print('Data inserted successfully')

        return jsonify('Book inserted successfully')

# 使用者可以刪除書籍
@app.route('/books/<user>/del_<int:id>', methods=['DELETE'])
def book_delete(user, id):
    print(user)
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM {user}_books_info WHERE id={id}')
    db.commit()
    
    return 'Book deleted'

# 使用者可以編輯書籍資訊
@app.route('/books/<user>/<string:title>', methods=['PUT'])
def update_book(user, title):
    book = request.get_json()
    cursor = db.cursor()
    cursor.execute(f'UPDATE {user}_books_info SET title = %s, author = %s, published_year = %s where title = %s',
                   (book['title'], book['author'], book['published_year'], title))
    db.commit()
    return 'Book updated'

# 使用者可以為某一本書籍新增、刪除、編輯閱讀心得
@app.route('/books/<user>/<string:title>/<note>', methods=['GET'])
def get_books(user):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {user}_books_info')
    books = cursor.fetchall()
    return jsonify(books)

# 使用者可以篩選出同個作者的書籍列表
@app.route('/books/<user>/<string:author>', methods=['GET'])
def get_author(user, author):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {user}_books_info where author = {author}')
    books = cursor.fetchall()
    return jsonify(books)

# # 使用者可以依照作者與出版年排列書籍列表
# @app.route('/books/<user>', methods=['GET'])
# def get_books(user):
#     author = request.args.get('author')
#     published_year = request.args.get('published_year')

#     cursor = db.cursor()
#     sql = f'SELECT * FROM {user}_books_info'
#     if author:
#         sql += f' WHERE author = "{author}"'
#     if published_year:
#         sql += f' WHERE published_year = {published_year}'
#     sql += ' ORDER BY author, published_year'
#     cursor.execute(sql)

#     books = cursor.fetchall()
#     return jsonify(books)

# 回傳該使用者的所有書籍
@app.route('/books/<user>', methods=['GET'])
def get_books_by_author(user):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM {user}_books_info')
    db.commit()
    books = cursor.fetchall()
    
    # 取得欄位名稱
    columns = [column[0] for column in cursor.description]
    # 將MySQL查詢結果轉換為字典
    books_dict = [dict(zip(columns, book)) for book in books]

    # 返回字典
    return jsonify(books_dict)

# @app.route('/books/<user>/<int:published_year>', methods=['GET'])
# def get_books_by_published_year(user,published_year):
#     cursor = db.cursor()
#     cursor.execute(f'SELECT * FROM {user}_books_info order by published_year')
#     books = cursor.fetchall()
#     return jsonify(books)

# 使用者可以透過關鍵字在書名欄位中搜尋,找到他們要找的書籍


@app.route('/books/<user>/<string:search_book>', methods=['GET'])
def get_books_by_title(user, search_book):
    cursor = db.cursor()
    cursor.execute(
        f'SELECT * FROM {user}_books_info where title like "%{search_book}%" ')
    books = cursor.fetchall()
    return jsonify(books)


if __name__ == '__main__':
    app.run(debug=True)
