import streamlit as st
import pandas as pd


def convert_df(df):
    return df.to_csv().encode('utf-8')


st.title("🗃️️ Merging CSV data 🗃️️")
st.text("This page allows you to upload and merge multiple CSV files")
instruction_guide = st.expander("Expand or Collapse", True)
instruction_guide.write('###')  # Line break
instruction_guide.markdown("""
        ### Page Guide:
        1. Click on the browse files button.
        2. Hold the ctrl key while selecting which files you want to merge with your mouse.
        3. When you're done with your selection, click on the open button.
        4. You will see the list of CSV files that is going to be merged. You can choose to remove a file by clicking on the X button beside it.
        5. Once you confirmed the files you want to merge, click on the 'Download Merged CSV File' button.
        """)
st.markdown("###")

master_df = pd.DataFrame()  # the final output CSV after merge
merged_file_name = ""

# Setup file upload
uploaded_files = st.file_uploader(label="Upload CSV files to merge.",
                                  help="Upload CSV files to merge together the data of 2 or more files",
                                  accept_multiple_files=True,
                                  type=['csv'])  # Upload file for CSV

# check if files are uploaded
if uploaded_files is not None:
    for file in uploaded_files:
        df_list = pd.read_csv(file)
        master_df = master_df.append(df_list)
        st.text(file.name)
        st.write(df_list)
        merged_file_name = merged_file_name + "-" + file.name  # Name of the output file when download

    st.text("Merged Data")
    st.write(master_df)
    merged_csv = convert_df(master_df)
    st.download_button(
        "Download Merged CSV file",
        merged_csv,
        f"{merged_file_name}",
        "text/csv",
        key='download-csv'
    )


