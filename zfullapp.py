import streamlit as st
import pandas as pd
import numpy as np
import certifi
import ssl
from urllib.request import urlopen
from urllib.error import URLError
from io import BytesIO

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    # Use certifi CA bundle to avoid macOS local issuer certificate issues.
    context = ssl.create_default_context(cafile=certifi.where())
    try:
        with urlopen(DATA_URL, context=context) as response:
            data = pd.read_csv(BytesIO(response.read()), nrows=nrows, compression='gzip')
    except URLError as exc:
        raise RuntimeError(
            'Unable to download data. SSL certificate validation failed or network is unavailable.'
        ) from exc

    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
try:
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache_data)")
except RuntimeError as err:
    data_load_state.text("Failed to load data")
    st.error(str(err))
    st.info("On macOS, you can also run: open /Applications/Python\\ 3*/Install\\ Certificates.command")
    st.stop()

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)