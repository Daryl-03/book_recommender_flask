import sqlite3
import pandas as pd

df = pd.read_csv('books.csv')

# Connect to the SQLite database
conn = sqlite3.connect('f_books.db')
cursor = conn.cursor()

# Create the tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS book (
    bookId VARCHAR(100) PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    rating FLOAT DEFAULT 0,
    description TEXT DEFAULT '',
    isbn CHAR(13) NOT NULL,
    numRatings BIGINT DEFAULT 0,
    coverImg VARCHAR(100) DEFAULT ' ',
    pages INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_history (
    id INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    bookId VARCHAR(100) NOT NULL,
    bookStateId INTEGER NOT NULL,
    bookmark INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ratings (
    userId INTEGER NOT NULL,
    bookId VARCHAR(100) NOT NULL,
    rating INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS genres (
    genreId INTEGER PRIMARY KEY,
    name VARCHAR(15) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS authors (
    authorId INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS book_state (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS book_author (
    id INTEGER PRIMARY KEY,
    bookId VARCHAR(100) NOT NULL,
    authorId INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS book_genre (
    id INTEGER PRIMARY KEY,
    bookId VARCHAR(100) NOT NULL,
    genreId INTEGER NOT NULL
)
''')

# Commit the changes to the database
conn.commit()

# Iterate through rows in the DataFrame
for index, row in df.iterrows():
    # Insert book record into the 'book' table
    cursor.execute('INSERT INTO book (bookId, title, rating, description, isbn, numRatings, coverImg, pages) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (row['bookId'], row['title'], 0, row['description'], row['isbn'], 0, row['coverImg'], row['pages']))
    
    # Commit the book insertion
    conn.commit()
    
    # Insert authors into 'authors' and 'book_author' tables
    authors = [author.strip() for author in row['author'].split(',')]
    for author in authors:
        cursor.execute('SELECT authorId FROM authors WHERE name = ?', (author,))
        author_id = cursor.fetchone()
        if author_id is None:
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (author,))
            conn.commit()
            author_id = cursor.lastrowid
        else:
            author_id = author_id[0]

        cursor.execute('INSERT INTO book_author (bookId, authorId) VALUES (?, ?)', (row['bookId'], author_id))

    # Insert genres into 'genres' and 'book_genre' tables
    genres = [genre.strip() for genre in row['genres'].strip("[]").replace("'", "").split(',')]
    for genre in genres:
        cursor.execute('SELECT genreId FROM genres WHERE name = ?', (genre,))
        genre_id = cursor.fetchone()
        if genre_id is None:
            cursor.execute('INSERT INTO genres (name) VALUES (?)', (genre,))
            conn.commit()
            genre_id = cursor.lastrowid
        else:
            genre_id = genre_id[0]

        cursor.execute('INSERT INTO book_genre (bookId, genreId) VALUES (?, ?)', (row['bookId'], genre_id))

# Close the database connection
conn.close()
