import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")
first_stream = st.Page("firststream.py", title="First Stream", icon="🧪")
full_app = st.Page("zfullapp.py", title="Uber Demo", icon="🚕")
progress_page = st.Page("progress_test.py", title="Progress Test", icon="⏳")

# Set up navigation
pg = st.navigation([
	main_page,
	page_2,
	page_3,
	first_stream,
	full_app,
	progress_page,
])

# Run the selected page
pg.run()