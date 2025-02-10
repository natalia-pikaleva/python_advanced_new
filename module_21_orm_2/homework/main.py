from sqlalchemy import (Column, Integer, String, create_engine, Date, Float, Boolean, func, case,
                        ForeignKey, UniqueConstraint, select, extract)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy
from datetime import date
from flask import Flask, jsonify, request
from sqlalchemy.ext.associationproxy import association_proxy
import csv

app = Flask(__name__)

engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship("Author", back_populates="book")
    receiving_books = relationship("ReceivingBooks", back_populates="book", cascade="all, delete-orphan", lazy='joined')
    students = association_proxy("receiving_books", "student")

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


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)

    book = relationship("Book", back_populates="author", cascade="all, delete-orphan", lazy='subquery')

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

    receiving_books = relationship("ReceivingBooks", back_populates="student", cascade="all, delete-orphan",
                                   lazy='joined')
    books = association_proxy("receiving_books", "book")

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
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(Date, nullable=False)
    date_of_return = Column(Date)

    __table_args__ = (
        UniqueConstraint('book_id', 'student_id', name='unique_book_student'),
    )

    book = relationship("Book", back_populates="receiving_books", lazy='selectin')
    student = relationship("Student", back_populates="receiving_books", lazy='selectin')

    def __repr__(self):
        return f"{self.book_id}, {self.student_id}, {self.date_of_issue}, {self.date_of_return}"

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (date.today() - self.date_of_issue).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """Количество дней, которое читатель держит/держал книгу у себя"""
        end_date = sqlalchemy.case(
            (cls.date_of_return != None, cls.date_of_return),
            else_=sqlalchemy.func.now()
        )
        return sqlalchemy.func.julianday(end_date) - sqlalchemy.func.julianday(cls.date_of_issue)


def insert_students():
    with (open('students.csv', newline='', encoding='UTF-8') as csvfile):
        reader = csv.DictReader(csvfile)
        students_to_insert = []
        for row in reader:
            try:
                average_score = float(row['average_score'])
                scholarship = row['scholarship'].lower() in ['true', 'false']

            except ValueError as e:
                print(f"Ошибка при преобразовании данных: {e}. Строка пропущена: {row}")
                continue
            student = Student(
                name=row['name'],
                surname=row['surname'],
                phone=row['phone'],
                email=row['email'],
                average_score=average_score,
                scholarship=scholarship
            )
            students_to_insert.append(student)
        session.bulk_save_objects(students_to_insert)
        session.commit()
        print(f"Успешно вставлено {len(students_to_insert)} студентов из CSV файла.")


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)
    insert_students()


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
    receiving_books = session.query(ReceivingBooks).filter(ReceivingBooks.count_date_with_book > 14).all()
    debtors_list = [book.to_json for book in receiving_books]

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


@app.route('/authors/<int:id>', methods=['GET'])
def get_count_books_by_author_id(id: int):
    '''Получение количества книг автора по его id'''

    author = session.query(Author).filter(Author.id == id).one_or_none()
    if author:
        issued_count = session.query(func.count(ReceivingBooks.book_id)). \
            join(Book, ReceivingBooks.book_id == Book.id). \
            filter(Book.author_id == id, ReceivingBooks.date_of_return == None).scalar()

        total_count = session.query(func.coalesce(func.sum(Book.count), 0)).filter(Book.author_id == id).scalar()

        remaining_count = (total_count - issued_count) if total_count else 0

        return jsonify({'result': remaining_count}), 200

    return jsonify({'error': f'Author with id {id} do not find'}), 400


@app.route('/students/<int:student_id>', methods=['GET'])
def get_not_read_books_by_student_id(student_id: int):
    '''Получение количества книг автора по его id'''

    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student:
        subquery = (
            session.query(Book.author_id.distinct())
            .join(ReceivingBooks, Book.id == ReceivingBooks.book_id)
            .filter(ReceivingBooks.student_id == student_id)
            .subquery()
        )

        recommended_books = (
            session.query(Book.id, Book.name, Author.name, Author.surname)
            .join(Author, Book.author_id == Author.id)
            .filter(Book.author_id.in_(subquery))
            .filter(~Book.id.in_(
                session.query(ReceivingBooks.book_id)
                .filter(ReceivingBooks.student_id == student_id)
            ))
            .all()
        )

        result = [{'book_id': b_id, 'book_name': b_name, 'author_name': a_name, 'author_surname': a_surname}
                  for b_id, b_name, a_name, a_surname in recommended_books]

        return jsonify({'recommended_books': result}), 200

    return jsonify({'error': f'Student with id {id} do not find'}), 400


@app.route('/avg_books', methods=['GET'])
def get_average_count_books_in_this_month():
    '''Получение среднего количества прочитанных в текущем месяце книг'''
    subquery = session.query(ReceivingBooks.student_id, func.count(ReceivingBooks.book_id).label('count_books')).filter(
        extract('month', ReceivingBooks.date_of_issue) == extract('month', func.now()),
        extract('year', ReceivingBooks.date_of_issue) == extract('year', func.now())).group_by(
        ReceivingBooks.student_id).subquery()

    average_count = session.query(func.avg(subquery.c.count_books)).scalar()

    return jsonify({'result': average_count}), 200


@app.route('/popular_book', methods=['GET'])
def get_most_popular_book():
    '''Получение самой популярной книги среди студентов со среднем баллом более 4'''
    subquery_students_id = session.query(Student.id).filter(Student.average_score > 4.0).subquery()

    subquery_book_id = session.query(ReceivingBooks.book_id) \
        .filter(ReceivingBooks.student_id.in_(subquery_students_id)) \
        .group_by(ReceivingBooks.book_id) \
        .order_by(func.count(ReceivingBooks.student_id).desc()) \
        .limit(1).scalar()

    name_popular_book = session.query(Book.name).filter(Book.id == subquery_book_id).first()

    return jsonify({'result': name_popular_book[0]}), 200


@app.route('/most_reading', methods=['GET'])
def get_most_reading_students():
    '''Получение топ 10 самых читающих студентов'''
    subquery_students_id = session.query(ReceivingBooks.student_id) \
        .group_by(ReceivingBooks.student_id) \
        .order_by(func.count(ReceivingBooks.book_id).desc()).limit(10).subquery()

    students_name = session.query(Student.name, Student.surname).filter(Student.id.in_(subquery_students_id)).all()

    result = [{'name': name, 'surname': surname}
              for name, surname in students_name]

    return jsonify({'result': result}), 200


if __name__ == '__main__':
    app.run()
