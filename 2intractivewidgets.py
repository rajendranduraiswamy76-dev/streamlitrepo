import streamlit as st

st.title("Hello Streamlit-er 👋")

st.button("Click me", key="btn_click")
st.download_button("Download file", data="Hello, world!", file_name="hello.txt", key="btn_download")
st.link_button("Go to gallery", "https://gallery.streamlit.io", key="btn_link")
st.menu_button("Export", options=["CSV", "JSON", "PDF"], key="btn_menu")

st.page_link("pages/subpage1.py", label="Subpage 1")



st.checkbox("I agree", key="chk_agree")
st.feedback("thumbs", key="fbk_thumbs")
st.pills("Tags", ["Sports", "Politics"], key="pills_tags")
st.radio("Pick one", ["cats", "dogs"], key="radio_pick")

st.segmented_control("Filter", ["Open", "Closed"], key="seg_filter")
st.toggle("Enable", key="tgl_enable")

st.selectbox("Pick one", ["cats", "dogs"], key="sel_pick")
st.multiselect("Buy", ["milk", "apples", "potatoes"], key="msel_buy")

st.slider("Pick a number", 0, 100, key="slider_demo")
st.select_slider("Pick a size", ["S", "M", "L"], key="ssel_size")

st.text_input("First name", key="txt_firstname")
st.number_input("Pick a number", 0, 10, key="number_input_demo")
st.text_area("Text to translate", key="txtarea_translate")
st.date_input("Your birthday", key="date_birthday")
st.datetime_input("Event date and time", key="datetime_event")
st.time_input("Meeting time", key="time_meeting")

st.caption("Edit data")
st.data_editor({"Name": ["Alice", "Bob"], "Age": [25, 30]}, key="de_names")

st.file_uploader("Upload a CSV", key="fu_csv")

st.audio_input("Record a voice message", key="aud_voice")
st.camera_input("Take a picture", key="cam_photo")
st.color_picker("Pick a color", key="cp_color")

# Use widgets' returned values in variables:
num = int(st.number_input("Num:", min_value=0, value=0, key="num_iterations"))
for i in range(num):
    st.write(f"Iteration {i + 1}")

selected_value = st.sidebar.selectbox("I:", ["f"], key="sb_sidebar_sel")
if selected_value == "f":
    st.write("You selected f")

my_slider_val = st.slider("Quinn Mallory", 1, 88, key="slider_quinn")
st.write(my_slider_val)

# Disable widgets to remove interactivity:
st.slider("Pick a number", 0, 100, disabled=True, key="slider_disabled")