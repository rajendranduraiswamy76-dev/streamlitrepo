import streamlit as st


st.set_page_config(page_title="Session State Demo", page_icon="🧠", layout="centered")

st.title("Streamlit Session State Example")
st.write("Each browser session keeps its own state while the app reruns.")


if "count" not in st.session_state:
	st.session_state.count = 0

if "name" not in st.session_state:
	st.session_state.name = ""

if "saved_items" not in st.session_state:
	st.session_state.saved_items = []


def increment_count() -> None:
	st.session_state.count += 1


def add_item() -> None:
	item = st.session_state.new_item.strip()
	if item:
		st.session_state["saved_items"].append(item)
		st.session_state.new_item = ""


st.subheader("1. Saved per user session")
st.text_input("Enter your name", key="name")
st.write(f"Hello, {st.session_state.name or 'guest'}")


st.subheader("2. Counter that survives reruns")
st.button("Increase counter", on_click=increment_count)
st.write(f"Counter value: {st.session_state.count}")


st.subheader("3. Simple user list")
st.text_input("Add an item", key="new_item")
st.button("Save item", on_click=add_item)

if st.session_state["saved_items"]:
	st.write("Saved items:")
	st.write(st.session_state["saved_items"])
else:
	st.caption("No items saved yet.")


if st.button("Clear session state"):
	for key in ["count", "name", "saved_items", "new_item"]:
		if key in st.session_state:
			del st.session_state[key]
	st.rerun()
