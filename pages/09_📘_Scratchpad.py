import streamlit as st
import pandas as pd
import numpy as np
import time
import csv

st.write("""
# Scratchpad to show possible functions
""")

# Slider input
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.write("***")

# Button input
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

st.write("***")

# Select box
option = st.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)

st.write("***")

# checkboxes to show/hide data
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    chart_data

# selectbox for options
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.write("***")

option = st.selectbox(
    'Which number do you like best?',
    df['first column'])

'You selected: ', option

st.write("***")

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted again?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

# Column layout
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

st.write("***")
