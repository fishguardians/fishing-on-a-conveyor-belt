import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Data Visualization",
    page_icon="📊",
)

st.write('# Data Visualization')

st.sidebar.success("Select a demo above.")

st.markdown(
    """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard 
dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen 
book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially 
unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""
)

st.write("***") # Horizontal line in Markdown

st.write("Session state is shared:", st.session_state["shared"])
# If page1 already executed, this should write True

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
