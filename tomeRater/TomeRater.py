class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        temp = self.email
        self.email = address
        print('Email address changed from {old} to {new}'.format(old = temp, new = address))

    def read_book(self, book, rating = None):
        self.books[book] = rating
    
    def get_average_rating(self):
        if(len(self.books) == 0):
            return 0

        total = 0
        for rating in self.books.values():
            if rating is None:
                total += 0
            else:
                total += rating

        return total / len(self.books)

    def __repr__(self):
        return 'User: {name}, email: {email}, books read: {book_count}'.format(name = self.name, email = self.email, book_count = str(len(self.books)))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        return False

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
    
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        temp = self.isbn
        self.isbn = isbn
        print('ISBN changed from {old} to {new}'.format(old = temp, new = isbn))
    
    def add_rating(self, rating):
        if rating != None and rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print('{rating} is an invalid rating'.format(rating = rating))
        
    def get_average_rating(self):
        if(len(self.ratings) == 0):
            return 0

        total = 0
        for rating in self.ratings:
           total += rating

        return total / len(self.ratings)

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return '{title} has not been classified as fiction or non-fiction'.format(title = self.title)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author
    
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return '{title} by {author}'.format(title = self.title, author = self.author)
    
class NonFiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
    
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level
    
    def __repr__(self):
        return '{title}, a {level} manual on {subject}'.format(title = self.title, level = self.level, subject = self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)
    
    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)
    
    def create_non_fiction(self, title, subject, level, isbn):
        return NonFiction(title, subject, level, isbn)
    
    def add_book_to_user(self, book, email, rating = None):
        if email not in self.users:
            print('No user with email {email}!'.format(email = email))
            return
        
        for system_book in self.books:
            if system_book.isbn == book.isbn and system_book != book:
                print('Book with isbn {isbn} has already been added to the system as {book}'.format(isbn = book.isbn, book = system_book))
                return

        user = self.users[email]
        user.read_book(book, rating)

        if rating is not None:
            book.add_rating(rating)

        if book in self.books:
            self.books[book] += 1
        else:
            self.books[book] = 1

    def add_user(self, name, email, user_books = None):
        if email in self.users:
            print('User {email} has already been added to the system'.format(email = email))
            return

        if not '@' in email:
            print('Invalid email address {email}: must contain \'@\' symbol'.format(email = email))
            return
        
        found_valid_extension = False
        for extension in ['.com', '.edu', '.org']:
            if(extension in email):
                found_valid_extension = True
                break
        
        if(not found_valid_extension):
            print('Invalid email address {email}: must contain \'.com\', \'.edu\', or \'.org\''.format(email = email))
            return

        user = User(name, email)
        self.users[email] = user

        if user_books == None:
            return

        for book in user_books:
            self.add_book_to_user(book, email)
    
    def print_catalog(self):
        print('\nAll books in catalog:')
        for book in self.books:
            print(book)

    def print_users(self):
        print('\nAll users:')
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        top_count = 0
        book = None
        for ibook, icount in self.books.items():
            if icount > top_count:
                top_count = icount
                book = ibook
        return book
    
    def highest_rated_book(self):
        book = None
        top_avg = 0
        for ibook in self.books:
            curr_avg = ibook.get_average_rating()
            if curr_avg > top_avg:
                top_avg = curr_avg
                book = ibook
        return book

    def most_positive_user(self):
        user = None
        top_avg = 0
        for iuser in self.users.values():
            curr_avg = iuser.get_average_rating()
            if curr_avg > top_avg:
                top_avg = curr_avg
                user = iuser
        return user