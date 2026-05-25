import os
import re
from contextlib import contextmanager

import pandas as pd
import psycopg2  # type: ignore[import-not-found]
import streamlit as st
from psycopg2 import sql  # type: ignore[import-not-found]


st.set_page_config(page_title="Library Books", page_icon="📚", layout="wide")


TABLE_NAME = "library_books"
DEFAULT_SCHEMA = "library_mgmt"


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
def get_connection():
	config = get_db_config()
	connection = psycopg2.connect(**config)
	connection.autocommit = True
	return connection


@contextmanager
def get_cursor():
	connection = get_connection()
	cursor = connection.cursor()
	try:
		yield cursor
	finally:
		cursor.close()


def init_db() -> None:
	schema_name = get_db_schema()
	create_schema_query = sql.SQL("CREATE SCHEMA IF NOT EXISTS {schema_name}").format(
		schema_name=sql.Identifier(schema_name)
	)
	create_table_query = sql.SQL(
		"""
		CREATE TABLE IF NOT EXISTS {table_name} (
			id SERIAL PRIMARY KEY,
			title TEXT NOT NULL,
			author TEXT NOT NULL,
			genre TEXT,
			published_year INTEGER,
			available_copies INTEGER NOT NULL DEFAULT 1,
			created_at TIMESTAMP NOT NULL DEFAULT NOW(),
			updated_at TIMESTAMP NOT NULL DEFAULT NOW()
		)
		"""
	).format(table_name=sql.Identifier(TABLE_NAME))
	with get_cursor() as cursor:
		cursor.execute(create_schema_query)
		cursor.execute(create_table_query)


def add_book(title: str, author: str, genre: str, published_year: int | None, available_copies: int) -> None:
	insert_query = sql.SQL(
		"""
		INSERT INTO {table_name} (title, author, genre, published_year, available_copies)
		VALUES (%s, %s, %s, %s, %s)
		"""
	).format(table_name=sql.Identifier(TABLE_NAME))
	with get_cursor() as cursor:
		cursor.execute(insert_query, (title, author, genre, published_year, available_copies))


def update_book(book_id: int, title: str, author: str, genre: str, published_year: int | None, available_copies: int) -> None:
	update_query = sql.SQL(
		"""
		UPDATE {table_name}
		SET title = %s,
			author = %s,
			genre = %s,
			published_year = %s,
			available_copies = %s,
			updated_at = NOW()
		WHERE id = %s
		"""
	).format(table_name=sql.Identifier(TABLE_NAME))
	with get_cursor() as cursor:
		cursor.execute(update_query, (title, author, genre, published_year, available_copies, book_id))


def fetch_books():
	select_query = sql.SQL(
		"""
		SELECT id, title, author, genre, published_year, available_copies, created_at, updated_at
		FROM {table_name}
		ORDER BY id DESC
		"""
	).format(table_name=sql.Identifier(TABLE_NAME))
	with get_cursor() as cursor:
		cursor.execute(select_query)
		rows = cursor.fetchall()
	columns = [desc[0] for desc in cursor.description]
	return rows, columns


def fetch_book_by_id(book_id: int):
	select_query = sql.SQL(
		"""
		SELECT id, title, author, genre, published_year, available_copies
		FROM {table_name}
		WHERE id = %s
		"""
	).format(table_name=sql.Identifier(TABLE_NAME))
	with get_cursor() as cursor:
		cursor.execute(select_query, (book_id,))
		return cursor.fetchone()
st.title("Library Books Manager")
st.write("Add, update, and view books stored in PostgreSQL using psycopg2.")


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
		st.info(f"Editing: {book[1]} by {book[2]}")
	else:
		st.caption("Enter a valid ID to load a book for editing.")

	with st.form("update_book_form"):
		title = st.text_input("Title", value=book[1] if book else "")
		author = st.text_input("Author", value=book[2] if book else "")
		genre = st.text_input("Genre", value=book[3] if book else "")
		published_year = st.number_input(
			"Published year",
			min_value=0,
			max_value=3000,
			value=int(book[4]) if book and book[4] is not None else 2024,
			step=1,
		)
		available_copies = st.number_input(
			"Available copies",
			min_value=0,
			value=int(book[5]) if book else 1,
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

