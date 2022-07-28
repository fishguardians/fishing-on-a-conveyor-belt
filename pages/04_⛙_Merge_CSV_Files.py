import streamlit as st
import pandas as pd
import scripts.generate_csv as generate_csv

# Page Configs
from st_aggrid import AgGrid

st.set_page_config(
    page_title="Merging CSV data",
    page_icon="🐠️",
)

st.title("🗃️️ Merging CSV data 🗃️️")
st.sidebar.info("This page allows you to upload and merge multiple CSV files")
# st.text("This page allows you to upload and merge multiple CSV files")
instruction_guide = st.expander("Expand or Collapse", True)
instruction_guide.write('###')  # Line break
instruction_guide.markdown("""
        ### Page Guide:
        1. Click on the browse files button.
        2. Hold the **'Ctrl'** key while selecting which files you want to merge with your mouse.
        3. When you're done with your selection, click on the open button.
        4. You will see the list of CSV files that is going to be merged. You can choose to remove a file by clicking on the **'X'** button beside it.
        5. Once you confirmed the files you want to merge, click on the **'Download Merged CSV File'** button.
        ###
        """)
st.markdown("###")

new_df = pd.DataFrame()
master_df = pd.DataFrame()  # the final output CSV after merge
merged_file_name = ""

# Setup file upload
uploaded_files = st.file_uploader(label="Upload CSV files to merge.",
                                  help="Upload CSV files to merge together the data of 2 or more files",
                                  accept_multiple_files=True,
                                  type=['csv'])  # Upload file for CSV

def convert_df(df):
    return df.to_csv().encode('utf-8')

# check if files are uploaded
if uploaded_files is not None:
    for file in uploaded_files:
        df_list = pd.read_csv(file)
        df_list = df_list.iloc[: , :-3]
        master_df = master_df.append(df_list)

        new_list = master_df.values.tolist()
        extra_list = []
        for item_in_list in new_list:
            extra_list.append([str(i) for i in item_in_list])

        new_df = pd.DataFrame(generate_csv.check_iqr_data(extra_list), columns = ["fish", "idtag", "weight(kg)", "length(cm)", "depth(cm)", "weight diff(iqr)", "length diff(iqr)", "depth diff(iqr)"])
        st.text(file.name)
        # st.dataframe(df_list)
        AgGrid(df_list, editable=False, enable_enterprise_modules=True, exportDataAsCsv=True,
               getDataAsCsv=True)
        merged_file_name = merged_file_name + "-" + file.name  # Name of the output file when download

    st.text("Merged Data")

    AgGrid(new_df, editable=False, enable_enterprise_modules=True, exportDataAsCsv=True,
           getDataAsCsv=True)
    merged_csv = convert_df(new_df)
    st.download_button(
        "Download Merged CSV file",
        merged_csv,
        f"{merged_file_name}",
        "text/csv",
        key='download-csv'
    )
