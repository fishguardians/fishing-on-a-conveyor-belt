import os
import streamlit as st
import pandas as pd
import statistics as stats
import numpy as np
import plotly_express as px

global df
st.title("Data Visualization")
csv_path = "output"
file_list = os.listdir(csv_path)
print(file_list)

if len(file_list) == 0:
    st.error(""" Output CSV data folder is currently empty!""")

else:
    try:
        option = st.selectbox(
            'Which CSV file would you like to view?',
            file_list)

        df = pd.read_csv(f"{csv_path}\\{option}")
        st.write(df)
    except:
        st.text("This file is not a CSV file!")

# specifying the columns
col1, col2 = st.columns([5, 1])
col3, col4, col5 = st.columns(3)

try:
    weight_list = df['Weight(kg)'].tolist()
    length_list = df['Length(cm)'].tolist()
    depth_list = df['Depth(cm)'].tolist()
    num_samples = len(df['Fish#'].tolist())
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

    with col1:
        st.text(f"Number of Samples: {num_samples}")

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

    chart_select = st.selectbox(label="Select the chart type",
                                options=["Scatterplots", "Lineplots", "Histograms", "Boxplots"])

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
    st.plotly_chart(plot)  # display the chart

except:
    print("")
