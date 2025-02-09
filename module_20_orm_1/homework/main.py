from sqlalchemy import Column, Integer, String, create_engine, Date, Float, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date
from flask import Flask, jsonify, request

app = Flask(__name__)

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.name}, {self.count}, {self.release_date}, {self.author_id}"

    def to_json(self):
        """Преобразует объект Book в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'count': self.count,
            'release_date': self.release_date.isoformat(),
            'author_id': self.author_id
        }


class Autor(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)

    def __repr__(self):
        return f"{self.name}, {self.surname}"


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)
    phone = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"{self.name}, {self.surname}, {self.phone}, {self.email}, {self.average_score}, {self.scholarship}"

    @classmethod
    def get_students_with_scholarship(cls, session):
        students = session.query(cls).filter(cls.scholarship == True).all()
        return [student.name for student in students]

    @classmethod
    def get_students_with_high_average_score(cls, session, score):
        students = session.query(cls).filter(cls.average_score > score).all()
        return [student.name for student in students]


class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(Date, nullable=False)
    date_of_return = Column(Date)

    def __repr__(self):
        return f"{self.book_id}, {self.student_id}, {self.date_of_issue}, {self.date_of_return}"

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (date.today() - self.date_of_issue).days


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route('/books', methods=['GET'])
def get_all_books():
    '''Получение списка всех книг в библиотеке'''
    books = session.query(Book).all()
    books_list = []
    for book in books:
        book_as_dict = book.to_json()
        books_list.append(book_as_dict)
    return jsonify(books_list=books_list), 200


@app.route('/debtors', methods=['GET'])
def get_debtors():
    '''Получение списка должников'''
    receiving_books = session.query(ReceivingBooks).all()
    # TODO Чтобы в запросе использовать гибридное свойство (с целью получить все данные не прибегая к python, а просто
    #  одним запросом) и нужно добавить в модель ReceivingBook и так называемое "выражение" (expression) - см. пример
    #  кода выражения (возможно он не согласован с вашим проектом - это просто пример, а не готовый код)
    #     @count_date_with_book.expression
    #     def count_date_with_book(cls):
    #         """Количество дней, которое читатель держит/держал книгу у себя"""
    #         end_date = sqlalchemy.case(
    #             (cls.date_of_return != None, cls.date_of_return),
    #             else_=sqlalchemy.func.now()
    #         )
    #         return sqlalchemy.func.julianday(end_date) - sqlalchemy.func.julianday(cls.date_of_issue)
    debtors_list = []
    for book in receiving_books:
        if book.count_date_with_book > 14:
            book_as_dict = book.to_json()
            debtors_list.append(book_as_dict)
    return jsonify(debtors_list=debtors_list), 200


@app.route('/issue_book', methods=['POST'])
def issue_book_of_library():
    '''Выдать книгу'''
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)

    book = session.query(ReceivingBooks).filter(ReceivingBooks.book_id == book_id,
                                                ReceivingBooks.student_id == student_id,
                                                ReceivingBooks.date_of_return.is_(None)).one_or_none()
    if not book:
        issue_book = ReceivingBooks(book_id=book_id, student_id=student_id, date_of_issue=date.today())

        session.add(issue_book)
        session.commit()
        return 'Книга успешно выдана', 201

    return f'Ошибка, книга с id {book_id} ранее выдана студенту с id {student_id} и еще не возвращена', 500


@app.route('/return_book', methods=['POST'])
def return_book_in_library():
    '''Вернуть книгу'''
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)

    return_book = session.query(ReceivingBooks).filter(ReceivingBooks.book_id == book_id,
                                                       ReceivingBooks.student_id == student_id,
                                                       ReceivingBooks.date_of_return.is_(None)).one_or_none()

    if return_book:
        return_book.date_of_return = date.today()
        session.commit()
        return 'Книга успешно возвращена в библиотеку', 201

    return f'Ошибка, книга с id {book_id} не выдана студенту с id {student_id}', 500


@app.route('/find_book', methods=['POST'])
def find_book():
    '''Найти книгу по названию'''
    name = request.form.get('name', type=str)
    name_lower = name.lower()

    books = session.query(Book).filter(
        func.lower(Book.name).like(f'%{name_lower}%')).all()

    books_list = [book.to_json() for book in books]

    return jsonify(books_list=books_list), 200


if __name__ == '__main__':
    app.run()
