from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(80), nullable=False)
    year_of_publication = db.Column(db.Integer, nullable=False)
    number_of_copies = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f'Student({self.id}, {self.book_title}, {self.year_of_publication}, {self.number_of_copies})'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    second_name = db.Column(db.String(80), nullable=False)
    book = db.relationship('Books', backref='author', lazy=True)

    def __repr__(self):
        return f'Faculty({self.id}, {self.first_name}, {self.last_name})'
