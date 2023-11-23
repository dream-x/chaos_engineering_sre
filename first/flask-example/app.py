from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

from pdchaos.middleware.contrib.flask.flask_middleware import FlaskMiddleware

app = Flask(__name__)
app.config['CHAOS_MIDDLEWARE_APPLICATION_NAME'] = 'bookstore'
app.config['CHAOS_MIDDLEWARE_APPLICATION_ENV'] = 'dev'

middleware = FlaskMiddleware(app)

metrics = PrometheusMetrics(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

metrics.info('app_info', 'Application info', version='1.0.3')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added'}), 201
    elif request.method == 'GET':
        books = Book.query.all()
        return jsonify([{'title': book.title, 'author': book.author} for book in books])

def initialize_db():
    books = [
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': '1984', 'author': 'George Orwell'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
    ]
    for book_data in books:
        book = Book(title=book_data['title'], author=book_data['author'])
        db.session.add(book)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_db()
    app.run(debug=True, port=4000)