#streamlit

import streamlit as st
import pandas as pd
import os
from io import BytesIO

#set up page

st.set_page_config(page_title="🧠 Growth Mind Set Challenge- By SUA", layout= 'wide')
st.title("🧠 Growth Mind Set Challenge- By SUA")
st.write("🔄 Inter-Conversion between XLSX and CSV files")

uploaded_files = st.file_uploader("⬆️ up-load your files (XLSX or CSV):", type=["csv","xlsl"],
                                   accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Un-Supported File-Type: {file_ext}")
            continue

        #Display File Information
        st.write(f"--File Name:-- {file.name}")
        st.write(f"--File Size:-- {file.size/1024}")

        #Show 5-Rows of DF
        st.write("👁‍🗨 Preview the Head of the Data Frame")
        st.dataframe(df.head())

        #Options for Data Cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"clean data for {file.name}:"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicate from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")

            with col2:
                 if st.button(f"Fill Missing Values for {file.name}"):
                     numeric_cols = df.select_dtypes(include=['number']).columns
                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                     st.write("Missing Values have been Filled..")

        #Choose Specific Columns to keep or convert
        st.subheader("Select columns to convert")
        columns = st.multiselect(f"choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #Create Visualization
        st.subheader("📉 Data Visualization")
        if st.checkbox(f"show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        #Convert the file -> CSV to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"convert {file.name} to", ["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type =="CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type =="Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data= buffer,
                file_name= file_name,
                mime= mime_type
            )

st.success("🎆 All Files Processed 🎆")



