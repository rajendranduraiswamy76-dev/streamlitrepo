"""
# My first app
Here's our first attempt at using data to create a table:
"""

import threading
import time

import streamlit as st
import pandas as pd
import numpy as np

st.write("Here's our first attempt at using data to create a table:")

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)


chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)


# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)



left_column, right_column = st.columns(2)

# Left column — plain button (outside form, immediate rerun)
left_column.button('Press me!')

# Right column — form so radio + slider only rerun on submit
with right_column:
    with st.form("sorting_form"):
        st.subheader("Sorting Hat Form")
        chosen = st.radio(
            'Sorting hat',
            ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"),
            key="form_house"
        )
        house_slider = st.slider(
            "How strongly do you feel about it?",
            1, 10, 5,
            key="form_strength"
        )
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"You are in **{chosen}** house! Confidence: {house_slider}/10")

