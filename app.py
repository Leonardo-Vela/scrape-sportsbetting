import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load predefined CSV data
@st.cache
def load_data():
    return pd.read_csv("./scraped_data.csv")

# Main function to run the Streamlit app
def main():
    st.title("CSV Data Plotter")

    # Load predefined data
    data = load_data()

    # Display the raw data
    st.subheader("Raw Data")
    st.write(data)

    # Select columns for plotting
    st.sidebar.subheader("Select Columns for Plotting")
    selected_columns = st.sidebar.multiselect("Select columns", data.columns)

    if selected_columns:
        # Plot selected columns
        st.subheader("Plot")
        plt.figure(figsize=(10, 6))
        for column in selected_columns:
            plt.plot(data.index, data[column], label=column)
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.legend()
        st.pyplot()

if __name__ == "__main__":
    main()