from flask import Flask, request, jsonify, render_template
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = db.create_engine("mysql+pymysql://root:passw0rd!@localhost/NTNU_books")
# metadata = db.MetaData()
# connection = engine.connect()

Base = declarative_base()

# 創建session
Session = sessionmaker(bind=engine)
session = Session()  

class Book(Base):
    __tablename__ = 'books_info'

    id = Column(Integer, primary_key=True)
    book = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    published_year = Column(Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'book': self.book, 'author': self.author, 'published_year': self.published_year}

@app.route('/books' , methods=['POST'])
def add_book():
    data = request.get_json()
    book = data['book']
    author = data['author']
    published_year = data['published_year']
    book = Book(book=book, author=author, published_year=published_year)
    session.add(book)
    session.commit()
    # 關閉連結
    session.close()
    return jsonify({'message': 'Book added successfully.', 'book': book.to_dict()})

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = data['book']
    author = data['author']
    published_year = data['published_year']
    book = Book.query.filter_by(id=id).first()
    book.book = book
    book.author = author
    book.published_year = published_year
    session.commit()
    # 關閉連結
    session.close()
    return jsonify({'message': 'Book updated successfully.', 'book': book.to_dict()})

@app.route('/books/<user>/del_<int:id>', methods=['DELETE'])
def delete_book(id):
    book = session.query(Book).filter_by(id=id).first()
    if not book:
        return jsonify({'message': 'Book not found.'}), 404
    
    session.delete(book)
    session.commit()
    return jsonify({'message': 'Book deleted successfully.'}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)