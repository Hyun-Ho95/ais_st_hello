# Q. Cache의 용도 ?

# A. 서버에서 요청을 많이 보낸다 => 비용
# 트래픽비용 증가 -> 서비스에 접속한 사람들에게 서비스속도 감속 -> 서비스 이용에 불편 
# cache ->  빈번하게 부르는 데이터를 cache 올려두고 사용하게 되면 트래픽 비용등을 절감

# Q.  CSV 파일들은 Upload 하지 않아도 되는건가 ?

# A. 데이터 올릴만한 서버존재 X  . 깃헙에 용량제한이 있어서 파일의 업로드 양 제한
# 큰 데이터를 사용하려면 어떻게 하면 좋을까요?
# 보통 실제 비즈니스에서는 데이터베이스 서버를 따로 사용
# ex) 빅쿼리 API 등을 사용

# + API 키는 서버에 따로 저장하여 서버에서 불러오기

import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)






DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

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


