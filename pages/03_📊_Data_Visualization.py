#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem and Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import os
import streamlit as st
import pandas as pd
import statistics as stats
import numpy as np
import plotly_express as px
from sys import platform

from st_aggrid import AgGrid

global df

# Page Configs
st.set_page_config(
    page_title="Data Visualization",
    page_icon="🐠",
)

st.title("📊 Data Visualization 📊")
st.sidebar.info("This page allows visualize the data from your csv files")
csv_path = "results"
container1 = st.empty()
file_list = os.listdir(csv_path)

instruction_guide = st.expander("Expand or Collapse", True)
instruction_guide.write('###')  # Line break
instruction_guide.markdown("""
        ### Page Guide:
        1. Select the CSV file you would like to view from the dropdown menu. These are the data extracted from the processed videos. Or you can upload your own data\n
        2. To print a page of the selected data spread, press **'Ctrl'** & **'P'** on your keyboard. (Remember to close the sidebar tab first).
        3. You can also download the graph plots as an image file by hovering your mouse to the top of the graph and clicking on the camera icon.
        ###
        """)
st.markdown("###")

if len(file_list) == 0:
    st.warning("""The CSV results folder is currently **empty!**""")
    st.warning("""Please **process** some videos or add some CSV files to the
    **'results'** folder of the program directory.""")

else:
    try:
        option = st.selectbox(
            'Which CSV file would you like to view?',
            file_list)
        if platform == "win32" or platform == "win64":
            df = pd.read_csv(f"{csv_path}\\{option}")
            # st.dataframe(df)
            AgGrid(df, editable=False, enable_enterprise_modules=True, exportDataAsCsv=True,
                                 getDataAsCsv=True)
        elif platform == "darwin":
            df = pd.read_csv(f"{csv_path}/{option}")
            # st.dataframe(df)
            AgGrid(df, editable=False, enable_enterprise_modules=True, exportDataAsCsv=True,
                                 getDataAsCsv=True)
    except:
        st.text("This file is not a CSV file!")

# specifying the columns
col1, col2 = st.columns([5, 1])
col3, col4, col5 = st.columns(3)

try:
    weight_list = df['weight(kg)'].tolist()
    length_list = df['length(cm)'].tolist()
    depth_list = df['depth(cm)'].tolist()
    num_samples = len(df['weight(kg)'].tolist())
    # define function to calculate cv
    cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100

    # variables for weight stats
    weight_mean = stats.mean(weight_list)
    weight_mean = "{:.3f}".format(weight_mean)

    weight_median = stats.median(weight_list)
    weight_median = "{:.3f}".format(weight_median)

    weight_mode = stats.mode(weight_list)
    weight_mode = "{:.3f}".format(weight_mode)

    weight_min = min(weight_list)
    weight_max = max(weight_list)

    weight_range = weight_max - weight_min
    weight_range = "{:.3f}".format(weight_range)

    weight_sd = stats.stdev(weight_list)
    weight_sd = "{:.3f}".format(weight_sd)

    weight_variance = stats.variance(weight_list)
    weight_variance = "{:.6f}".format(weight_variance)

    weight_cv = cv(weight_list)
    weight_cv = "{:.3f}".format(weight_cv)

    weight_Q1 = np.percentile(weight_list, 25, method='midpoint')
    weight_Q3 = np.percentile(weight_list, 75, method='midpoint')
    weight_iqr = weight_Q3 - weight_Q1
    weight_iqr = "{:.3f}".format(weight_iqr)

    # variables for length stats
    length_mean = stats.mean(length_list)
    length_mean = "{:.3f}".format(length_mean)

    length_median = stats.median(length_list)
    length_median = "{:.3f}".format(length_median)

    length_mode = stats.mode(length_list)
    length_mode = "{:.3f}".format(length_mode)

    length_min = min(length_list)
    length_max = max(length_list)

    length_range = length_max - length_min
    length_range = "{:.3f}".format(length_range)

    length_sd = stats.stdev(length_list)
    length_sd = "{:.3f}".format(length_sd)

    length_variance = stats.variance(length_list)
    length_variance = "{:.6f}".format(length_variance)

    length_cv = cv(length_list)
    length_cv = "{:.3f}".format(length_cv)

    length_Q1 = np.percentile(length_list, 25, method='midpoint')
    length_Q3 = np.percentile(length_list, 75, method='midpoint')
    length_iqr = length_Q3 - length_Q1
    length_iqr = "{:.3f}".format(length_iqr)

    # variables for depth stats
    depth_mean = stats.mean(depth_list)
    depth_mean = "{:.3f}".format(depth_mean)

    depth_median = stats.median(depth_list)
    depth_median = "{:.3f}".format(depth_median)

    depth_mode = stats.mode(depth_list)
    depth_mode = "{:.3f}".format(depth_mode)

    depth_min = min(depth_list)
    depth_max = max(depth_list)

    depth_range = depth_max - depth_min
    depth_range = "{:.3f}".format(depth_range)

    depth_sd = stats.stdev(depth_list)
    depth_sd = "{:.3f}".format(depth_sd)

    depth_variance = stats.variance(depth_list)
    depth_variance = "{:.6f}".format(depth_variance)

    depth_cv = cv(depth_list)
    depth_cv = "{:.3f}".format(depth_cv)

    depth_Q1 = np.percentile(depth_list, 25, method='midpoint')
    depth_Q3 = np.percentile(depth_list, 75, method='midpoint')
    depth_iqr = depth_Q3 - depth_Q1
    depth_iqr = "{:.3f}".format(depth_iqr)

    with col1:
        st.text(f"Number of Samples: {num_samples}")
        st.markdown('***')

    with col3:
        st.subheader("Weight Stats(Kg)")
        st.text(f"Mean: {weight_mean}")
        st.text(f"Median: {weight_median}")
        st.text(f"Mode: {weight_mode}")
        st.text(f"Min: {weight_min}")
        st.text(f"Max: {weight_max}")
        st.text(f"Range: {weight_range}")
        st.text(f"Standard Deviation: {weight_sd}")
        st.text(f"Variance: {weight_variance}")
        st.text(f"C.V: {weight_cv}")
        st.text(f"IQR: {weight_iqr}")

    with col4:
        st.subheader("Length Stats(cm)")
        st.text(f"Mean: {length_mean}")
        st.text(f"Median: {length_median}")
        st.text(f"Mode: {length_mode}")
        st.text(f"Min: {length_min}")
        st.text(f"Max: {length_max}")
        st.text(f"Range: {length_range}")
        st.text(f"Standard Deviation: {length_sd}")
        st.text(f"Variance: {length_variance}")
        st.text(f"C.V: {length_cv}")
        st.text(f"IQR: {length_iqr}")

    with col5:
        st.subheader("Depth Stats(cm)")
        st.text(f"Mean: {depth_mean}")
        st.text(f"Median: {depth_median}")
        st.text(f"Mode: {depth_mode}")
        st.text(f"Min: {depth_min}")
        st.text(f"Max: {depth_max}")
        st.text(f"Range: {depth_range}")
        st.text(f"Standard Deviation: {depth_sd}")
        st.text(f"Variance: {depth_variance}")
        st.text(f"C.V: {depth_cv}")
        st.text(f"IQRe: {depth_iqr}")

    st.markdown('***')
    st.write('**Scatter Plot Axis selection:**')

    chart_select = "Scatterplots"

    # If scatterplot is selected
    if chart_select == 'Scatterplots':
        x_choice = st.selectbox('X axis', options=['Weight', 'Length', 'Depth'])
        y_choice = st.selectbox('Y axis', options=['Weight', 'Length', 'Depth'])

        if x_choice == 'Weight':
            x_label = "Weight(kg)"
            x_values = weight_list

        if x_choice == 'Length':
            x_label = "Length(cm)"
            x_values = length_list

        if x_choice == 'Depth':
            x_label = "Depth(cm)"
            x_values = depth_list

        if y_choice == 'Weight':
            y_label = "Weight(kg)"
            y_values = weight_list

        if y_choice == 'Length':
            y_label = "Length(cm)"
            y_values = length_list

        if y_choice == 'Depth':
            y_label = "Depth(cm)"
            y_values = depth_list

    plot = px.scatter(data_frame=df, x=x_values, y=y_values)
    plot.update_layout(

        xaxis_title=x_label,
        yaxis_title=y_label
    )
    st.plotly_chart(plot, use_container_width=True)  # display the chart

except:
    st.text("Error : Unable to load stats and graphs!")
