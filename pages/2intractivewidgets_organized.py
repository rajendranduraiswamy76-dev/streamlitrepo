import streamlit as st
import pandas as pd

st.title("Interactive Widgets Reference 👋")
st.caption("All Streamlit widgets grouped by category — with descriptions and live demos.")

# Helper to render a compact description table for a widget group.
def desc_table(rows):
    st.dataframe(
        pd.DataFrame(rows, columns=["Widget", "Returns", "Description"]),
        use_container_width=True,
        hide_index=True,
    )

st.header("1 · Button Controls")
desc_table([
    ("st.button", "bool", "Simple clickable button. Returns True on the frame it is clicked."),
    ("st.download_button", "bool", "Triggers a file download when clicked. Accepts bytes or string data."),
    ("st.link_button", "None", "Opens an external URL in a new browser tab."),
    ("st.menu_button", "str", "Dropdown menu button; returns the selected option string."),
    ("st.page_link", "None", "Navigation link to another registered page in a multipage app."),
])
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Click me", key="btn_click")
    st.download_button("Download file", data="Hello, world!", file_name="hello.txt", key="btn_download")
with col2:
    st.link_button("Go to gallery", "https://gallery.streamlit.io", key="btn_link")
    st.menu_button("Export", options=["CSV", "JSON", "PDF"], key="btn_menu")
with col3:
    st.page_link("pages/subpage1_organized.py", label="Subpage 1")

st.divider()

st.header("2 · Selection Controls")
desc_table([
    ("st.checkbox", "bool", "On/off boolean checkbox."),
    ("st.feedback", "str | None", "Thumbs up/down or star rating widget."),
    ("st.pills", "list", "Pill-style multi-tag selector."),
    ("st.radio", "str", "Single-choice radio button group."),
    ("st.segmented_control", "str", "Horizontal segmented bar for mutually exclusive options."),
    ("st.toggle", "bool", "Styled on/off toggle switch."),
])
col1, col2, col3 = st.columns(3)
with col1:
    st.checkbox("I agree", key="chk_agree")
    st.feedback("thumbs", key="fbk_thumbs")
with col2:
    st.pills("Tags", ["Sports", "Politics"], key="pills_tags")
    st.radio("Pick one", ["cats", "dogs"], key="radio_pick")
with col3:
    st.segmented_control("Filter", ["Open", "Closed"], key="seg_filter")
    st.toggle("Enable", key="tgl_enable")

st.divider()

st.header("3 · Dropdown & Multi-select")
desc_table([
    ("st.selectbox", "any", "Dropdown to pick exactly one item from a list."),
    ("st.multiselect", "list", "Dropdown allowing multiple simultaneous selections."),
])
col1, col2 = st.columns(2)
with col1:
    st.selectbox("Pick one", ["cats", "dogs"], key="sel_pick")
with col2:
    st.multiselect("Buy", ["milk", "apples", "potatoes"], key="msel_buy")

st.divider()

st.header("4 · Sliders")
desc_table([
    ("st.slider", "int / float / date", "Numeric or date range slider with draggable handle."),
    ("st.select_slider", "any", "Slider that snaps to discrete options from a list."),
])
col1, col2 = st.columns(2)
with col1:
    st.slider("Pick a number", 0, 100, key="slider_demo")
with col2:
    st.select_slider("Pick a size", ["S", "M", "L"], key="ssel_size")

st.divider()

st.header("5 · Text & Numeric Input")
desc_table([
    ("st.text_input", "str", "Single-line text field."),
    ("st.number_input", "float", "Numeric input with optional min, max, and step controls."),
    ("st.text_area", "str", "Multi-line text area for longer input."),
])
col1, col2, col3 = st.columns(3)
with col1:
    st.text_input("First name", key="txt_firstname")
with col2:
    st.number_input("Pick a number", 0, 10, key="number_input_demo")
with col3:
    st.text_area("Text to translate", key="txtarea_translate")

st.divider()

st.header("6 · Date & Time Input")
desc_table([
    ("st.date_input", "date", "Calendar picker returning a date object."),
    ("st.datetime_input", "datetime", "Combined date and time picker."),
    ("st.time_input", "time", "Time-only picker returning a time object."),
])
col1, col2, col3 = st.columns(3)
with col1:
    st.date_input("Your birthday", key="date_birthday")
with col2:
    st.datetime_input("Event date and time", key="datetime_event")
with col3:
    st.time_input("Meeting time", key="time_meeting")

st.divider()

st.header("7 · Data Editor")
desc_table([
    ("st.data_editor", "DataFrame", "Editable table — users can modify cell values directly in the UI."),
])
st.data_editor({"Name": ["Alice", "Bob"], "Age": [25, 30]}, key="de_names", use_container_width=True)

st.divider()

st.header("8 · Media & File Input")
desc_table([
    ("st.file_uploader", "UploadedFile", "File upload widget; accepts one or multiple files."),
    ("st.audio_input", "bytes", "Records audio from the user's microphone."),
    ("st.camera_input", "UploadedFile", "Captures a photo from the user's webcam."),
    ("st.color_picker", "str (hex)", "Color palette picker returning the selected hex value."),
])
col1, col2 = st.columns(2)
with col1:
    st.file_uploader("Upload a CSV", key="fu_csv")
    st.audio_input("Record a voice message", key="aud_voice")
with col2:
    st.camera_input("Take a picture", key="cam_photo")
    st.color_picker("Pick a color", key="cp_color")

st.divider()

st.header("9 · Widget Return Values in Code")
st.markdown("Every widget returns a value you can store and use directly in your logic.")

num = int(st.number_input("How many iterations?", min_value=0, value=0, key="num_iterations"))
for i in range(num):
    st.write(f"Iteration {i + 1}")

selected_value = st.sidebar.selectbox("Sidebar select:", ["f", "g", "h"], key="sb_sidebar_sel")
if selected_value == "f":
    st.info("You selected **f** from the sidebar.")

my_slider_val = st.slider("Quinn Mallory", 1, 88, key="slider_quinn")
st.write(f"Slider value: **{my_slider_val}**")

st.divider()

st.header("10 · Disabled Widgets")
st.markdown("Pass disabled=True to any widget to make it read-only.")
st.slider("Pick a number (disabled)", 0, 100, disabled=True, key="slider_disabled")
