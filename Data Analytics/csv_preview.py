import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import SmartDataframe
import io
import os

# Set the API key for PandasAI
os.environ['PANDASAI_API_KEY'] = "$2a$10$WUXdxt0YBbsTbc2jkbLWx.gciPY7/6afonYh4PoOtwEI9bsTx9ZPe"

def main():
    """Streamlit app's main function."""
    st.set_page_config(layout='wide')
    st.title("Data Preprocessing Preview")
    st.info("Upload your CSV data for a preview.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Start of Upload
        st.header("Uploaded Data Preview :")
        st.dataframe(df)  # Show a preview of the rows
        st.write("**Note:** This is just a preview, scroll down for analysed & transformed dataset")
        # End of Upload

        # Start of Analysis
        st.header("Analyzed Data Preview :")
        st.info("**Basic Analyzed Data :**")
        st.write(df.describe())  # Show basic analyzed data

        st.info("**Sum of rows that are null :**")
        st.write(df.isnull().sum())  # Show sum of rows that are null
        # End of Analysis
        
        # Start of Transformation
        st.header("Transformed Data Preview :")
        st.info("**Preview after removing duplicates :**")
        df.drop_duplicates(inplace=True)
        st.write(df)
        # End of Transformation
        
        # Start of Gen-AI
        sdf = SmartDataframe(df)

        st.info("**Chat with your CSV**")
        input_text = st.text_area("Enter Prompt")

        if input_text:
            if st.button("Chat with CSV"):
                st.info(f"Your Prompt: {input_text}")
                result = sdf.chat(input_text)
                
                if result:
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
                    else:
                        st.write(result)
                
                if 'plot' in input_text.lower() or 'chart' in input_text.lower():
                    # Example handling for basic plot requests
                    if 'pie' in input_text.lower():
                        st.info("Generating pie chart:")
                        fig, ax = plt.subplots()
                        df.iloc[:, 0].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
                        st.pyplot(fig)
                    else:
                        plot_type = 'line'  # Default plot type
                        if 'bar' in input_text.lower():
                            plot_type = 'bar'
                        if 'scatter' in input_text.lower():
                            plot_type = 'scatter'
                        if 'hist' in input_text.lower():
                            plot_type = 'hist'
                        
                        st.info(f"Generating {plot_type} plot:")
                        fig, ax = plt.subplots()
                        if plot_type == 'line':
                            df.plot(ax=ax)
                        elif plot_type == 'bar':
                            df.plot(kind='bar', ax=ax)
                        elif plot_type == 'scatter':
                            if 'x' in input_text and 'y' in input_text:
                                x_col = input_text.split('x=')[1].split()[0]
                                y_col = input_text.split('y=')[1].split()[0]
                                df.plot(kind='scatter', x=x_col, y=y_col, ax=ax)
                            else:
                                st.write("Please specify x and y columns for scatter plot.")
                                return
                        elif plot_type == 'hist':
                            df.plot(kind='hist', ax=ax)
                        
                        st.pyplot(fig)
                else:
                    st.write("Plot type not recognized.")
        # End of Gen-AI

if __name__ == "__main__":
    main()
