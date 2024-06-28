import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import SmartDataframe
import io
import os
os.environ['PANDASAI_API_KEY'] = "$2a$10$WUXdxt0YBbsTbc2jkbLWx.gciPY7/6afonYh4PoOtwEI9bsTx9ZPe"

def main():
  """Streamlit app's main function."""
  st.set_page_config(layout='wide')
  st.title("Data Preprocessing Preview")
  st.info("Upload your CSV data for a preview.")

  uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    #Start of Upload
    st.header("Uploaded Data Preview :")
    st.dataframe(df)  # Show a preview of the rows
    st.write("**Note:** This is just a preview, scroll down for analysed & transformed dataset")
    #End of Upload

    #Start of Analysis
    st.header("Analyzed Data Preview :")
    st.info("**Basic Analysed Data :**")
    st.write (df.describe()) #Show basic analysed data

    st.info("**Sum of rows that are null :**")
    st.write (df.isnull().sum()) # Show sum of rows that are null
    #End of Analysis
    
    #Start of Transformation
    st.header("Transformed Data Preview :")
    st.info("**Preview after removing duplicates :**")
    df.drop_duplicates(inplace=True)
    st.write (df)
    #End of Transformation
    
    #Start of Gen-AI
    sdf = SmartDataframe(df)


    st.info("**Chat with your CSV**")
    input_text = st.text_area("Enter Prompt")
    if input_text is not None:
      if st.button("Chat with CSV"):
         st.info(f"Your Prompt: {input_text}")
         result = sdf.chat(input_text)
         st.success(result)

         if isinstance(result, pd.DataFrame):
                st.write("Result as a table:")
                st.dataframe(result)
         elif isinstance(result, str):
                # Try to interpret the string as a CSV
                try:
                    result_df = pd.read_csv(io.StringIO(result))
                    st.write("Result as a table:")
                    st.dataframe(result_df)
                except Exception as e:
                    st.write(result)
                    st.write(f"Could not convert result to DataFrame: {e}")
         elif isinstance(result, list):
                try:
                    result_df = pd.DataFrame(result)
                    st.write("Result as a table:")
                    st.dataframe(result_df)
                except Exception as e:
                    st.write(result)
                    st.write(f"Could not convert result to DataFrame: {e}")
    #End of Gen-AI
        
if __name__ == "__main__":
  main()