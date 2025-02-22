import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="💽Data Sweeper", layout="wide")
st.title("💽Data Sweeper")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your file (CSV OR Excel):", type=['csv', 'xlsx'], accept_multiple_files=True)

# Check if files are uploaded
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)

        elif file_ext == ".xlsx":
            df = pd.read_excel(file)

        else:
            st.error(f"Invalid file format: {file_ext}. Please upload a CSV or Excel file.")
            continue
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
 
       #Data Preview
        st.write("### 🎬Data Preview")
        st.dataframe(df.head())
 
        #Data Cleaning
        st.subheader("🧹 Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
 
            with col1:
                if st.button(f"Remove Duplicates {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled with mean!")
         
            st.subheader("💡Select Columns to convert")
            columns = st.multiselect(f"choose columns to convert for {file.name}", df.columns, default=df.columns, key=f"multiselect_{file.name}")
            df = df[columns]

            # Create some visualizations
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Data Visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
             
            # Convert the file CSV to Excel
            st.subheader("⏳Convert File")    
            conversation_type = st.radio(f"convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            buffer = BytesIO()
            if conversation_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversation_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download the file
            st.download_button(
                label=f"Click here to download📥 {file_name} as {conversation_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
                key=f"download_button_{file.name}"
            )
st.success("🎀Done!")