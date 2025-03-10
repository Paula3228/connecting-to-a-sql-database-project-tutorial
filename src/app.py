import os
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# 1) Connect to the database here using the SQLAlchemy's create_engine function

connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"

engine = create_engine(connection_string).execution_options(autocommit=True)
conn = engine.connect()

conn.execute(text(''' DROP TABLE IF EXISTS book_authors;
                DROP TABLE IF EXISTS books;
                DROP TABLE IF EXISTS authors;
                DROP TABLE IF EXISTS publishers;
                '''))

# 2) Execute the SQL sentences to create your tables using the SQLAlchemy's execute function
conn.execute.text("""CREATE TABLE publishers(
    publisher_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(publisher_id)
);

CREATE TABLE authors(
    author_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(50) NULL,
    last_name VARCHAR(100) NULL,
    PRIMARY KEY(author_id)
);

CREATE TABLE books(
    book_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    total_pages INT NULL,
    rating DECIMAL(4, 2) NULL,
    isbn VARCHAR(13) NULL,
    published_date DATE,
    publisher_id INT NULL,
    PRIMARY KEY(book_id),
    CONSTRAINT fk_publisher FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
);

CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY(book_id, author_id),
    CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
); """))

# 4) Use pandas to print one of the tables as dataframes using read_sql function
dataframe = pd.read_sql("Select * from books;", conn)
print(dataframe.describe())