import os
import re

import pandas as pd
import streamlit as st
from sqlalchemy import Column, DateTime, Integer, Text, create_engine, func, select, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import CreateSchema


st.set_page_config(page_title="Library Books", page_icon="📚", layout="wide")


TABLE_NAME = "library_books"
DEFAULT_SCHEMA = "library_mgmt"
Base = declarative_base()


def _secret_or_env(key: str, default: str = "") -> str:
	if key in st.secrets:
		return str(st.secrets[key])
	return os.getenv(key, default)


def _safe_sql_identifier(value: str, fallback: str) -> str:
	if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
		return value
	return fallback


def get_db_schema() -> str:
	raw_schema = _secret_or_env("DB_SCHEMA", DEFAULT_SCHEMA)
	return _safe_sql_identifier(raw_schema, DEFAULT_SCHEMA)


def get_db_config() -> dict[str, str]:
	schema_name = get_db_schema()
	return {
		"host": _secret_or_env("DB_HOST", "localhost"),
		"port": _secret_or_env("DB_PORT", "5432"),
		"dbname": _secret_or_env("DB_NAME", "library_db"),
		"user": _secret_or_env("DB_USER", "postgres"),
		"password": _secret_or_env("DB_PASSWORD", ""),
		"options": f"-c search_path={schema_name},public",
	}


@st.cache_resource
def get_engine():
	config = get_db_config()
	dsn = (
		f"postgresql+psycopg2://{config['user']}:{config['password']}"
		f"@{config['host']}:{config['port']}/{config['dbname']}"
	)
	return create_engine(dsn, connect_args={"options": config["options"]}, future=True)


@st.cache_resource
def get_session_factory():
	return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, future=True)


class LibraryBook(Base):
	__tablename__ = TABLE_NAME
	__table_args__ = {"schema": get_db_schema()}

	id = Column(Integer, primary_key=True)
	title = Column(Text, nullable=False)
	author = Column(Text, nullable=False)
	genre = Column(Text)
	published_year = Column(Integer)
	available_copies = Column(Integer, nullable=False, server_default=text("1"))
	created_at = Column(DateTime, nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


def _book_to_dict(book: LibraryBook) -> dict[str, object]:
	return {
		"id": book.id,
		"title": book.title,
		"author": book.author,
		"genre": book.genre,
		"published_year": book.published_year,
		"available_copies": book.available_copies,
		"created_at": book.created_at,
		"updated_at": book.updated_at,
	}


def init_db() -> None:
	engine = get_engine()
	with engine.begin() as connection:
		connection.execute(CreateSchema(get_db_schema(), if_not_exists=True))
		Base.metadata.create_all(connection)


def add_book(title: str, author: str, genre: str, published_year: int | None, available_copies: int) -> None:
	book = LibraryBook(
		title=title,
		author=author,
		genre=genre,
		published_year=published_year,
		available_copies=available_copies,
	)
	session_factory = get_session_factory()
	with session_factory() as session:
		session.add(book)
		session.commit()


def update_book(book_id: int, title: str, author: str, genre: str, published_year: int | None, available_copies: int) -> None:
	session_factory = get_session_factory()
	with session_factory() as session:
		book = session.get(LibraryBook, book_id)
		if not book:
			raise ValueError(f"Book with id {book_id} not found")
		book.title = title
		book.author = author
		book.genre = genre
		book.published_year = published_year
		book.available_copies = available_copies
		session.commit()


def fetch_books():
	stmt = select(LibraryBook).order_by(LibraryBook.id.desc())
	with get_session_factory()() as session:
		books = session.scalars(stmt).all()
		rows = [_book_to_dict(book) for book in books]
	columns = ["id", "title", "author", "genre", "published_year", "available_copies", "created_at", "updated_at"]
	return rows, columns


def fetch_book_by_id(book_id: int):
	with get_session_factory()() as session:
		return session.get(LibraryBook, book_id)
st.title("Library Books Manager")
st.write("Add, update, and view books stored in PostgreSQL using SQLAlchemy ORM.")


with st.sidebar:
	st.header("Database Settings")
	st.code(
		"DB_HOST=localhost\nDB_PORT=5432\nDB_NAME=library_db\nDB_USER=postgres\nDB_PASSWORD=your_password\nDB_SCHEMA=library_mgmt",
		language="text",
	)
	if st.button("Initialize table"):
		try:
			init_db()
			st.success(f"Table {get_db_schema()}.{TABLE_NAME} is ready.")
		except Exception as exc:
			st.error(f"Unable to initialize table: {exc}")


try:
	init_db()
	except_message = None
except Exception as exc:
	except_message = str(exc)

if except_message:
	st.error(f"Database connection failed: {except_message}")
	st.stop()


tab_add, tab_update, tab_view = st.tabs(["Add Book", "Update Book", "View Books"])


with tab_add:
	st.subheader("Add a new book")
	with st.form("add_book_form", clear_on_submit=True):
		title = st.text_input("Title")
		author = st.text_input("Author")
		genre = st.text_input("Genre")
		published_year = st.number_input("Published year", min_value=0, max_value=3000, value=2024, step=1)
		available_copies = st.number_input("Available copies", min_value=0, value=1, step=1)
		submitted = st.form_submit_button("Save book")
		if submitted:
			if not title or not author:
				st.warning("Title and author are required.")
			else:
				try:
					add_book(title, author, genre, int(published_year), int(available_copies))
					st.success("Book added successfully.")
				except Exception as exc:
					st.error(f"Failed to add book: {exc}")


with tab_update:
	st.subheader("Update an existing book")
	book_id = st.number_input("Book ID", min_value=1, step=1, key="book_id")
	book = fetch_book_by_id(int(book_id)) if book_id else None

	if book:
		st.info(f"Editing: {book.title} by {book.author}")
	else:
		st.caption("Enter a valid ID to load a book for editing.")

	with st.form("update_book_form"):
		title = st.text_input("Title", value=book.title if book else "")
		author = st.text_input("Author", value=book.author if book else "")
		genre = st.text_input("Genre", value=book.genre if book else "")
		published_year = st.number_input(
			"Published year",
			min_value=0,
			max_value=3000,
			value=int(book.published_year) if book and book.published_year is not None else 2024,
			step=1,
		)
		available_copies = st.number_input(
			"Available copies",
			min_value=0,
			value=int(book.available_copies) if book else 1,
			step=1,
		)
		update_submitted = st.form_submit_button("Update book")
		if update_submitted:
			if not book:
				st.warning("Select a valid book ID first.")
			elif not title or not author:
				st.warning("Title and author are required.")
			else:
				try:
					update_book(int(book_id), title, author, genre, int(published_year), int(available_copies))
					st.success("Book updated successfully.")
				except Exception as exc:
					st.error(f"Failed to update book: {exc}")


with tab_view:
	st.subheader("Books in the library table")
	if st.button("Refresh books"):
		st.rerun()
	books, columns = fetch_books()
	if books:
		book_frame = pd.DataFrame(books, columns=columns)
		st.dataframe(book_frame, use_container_width=True)
		st.caption(f"{len(books)} book(s) found in {get_db_schema()}.{TABLE_NAME}.")
	else:
		st.info("No books found yet. Add one in the Add Book tab.")

