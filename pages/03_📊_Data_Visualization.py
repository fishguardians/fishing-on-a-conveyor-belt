import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Data Visualization",
    page_icon="📊",
)

st.write('# 📊 Data Visualization 📊')

st.sidebar.success("Select a demo above.")


# st.write("Session state is shared:", st.session_state["shared"])
# If page1 already executed, this should write True

st.markdown("""
### Client's wants:
- Basic Statistics (Table?)
    - Number of samples
    - S.D standard deviation
    - Variance
    - C.V 
    - etc
- Graphics
    - Box plot
    - Histogram
    - etc
""")

st.write("***")

# 2 column table
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.write("***")

# multi column example
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

st.write("***")

# Line graph
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.write("***")
