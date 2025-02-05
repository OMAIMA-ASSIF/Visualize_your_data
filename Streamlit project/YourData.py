import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#This is the right version :)
# App title
st.title("**📂✨ CSV Explorer: Upload, Filter & Visualize 📊🔍**")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Navigation bar
    st.sidebar.title("Begin Your Exploration 👀")
    page = st.sidebar.radio("Go to:", ["🔍 Filter Data", "📈 Visualize Data", "🧹 Data Preprocessing", "📊 Data Summary"])
    st.sidebar.subheader("")
    st.sidebar.subheader("")
    st.sidebar.subheader("")
    st.sidebar.subheader("")

    st.sidebar.subheader("Created with 💗 by ASSIF OMAIMA")
    # Display the full DataFrame at the top of every page
    st.subheader("📋 Full Dataset")
    st.dataframe(df)

    if page == "🔍 Filter Data":
        st.header("🔍 Filter Data")

        # Data filtering
        st.subheader("Filter Options")
        columns_to_filter = st.multiselect("Choose columns to filter", df.columns)
        filters = {}
        for col in columns_to_filter:
            unique_values = df[col].unique()
            selected_values = st.multiselect(f"Filter values in {col}", unique_values)
            if selected_values:
                filters[col] = selected_values

        # Apply filters
        filtered_df = df.copy()
        for col, values in filters.items():
            filtered_df = filtered_df[filtered_df[col].isin(values)]

        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

    elif page == "📈 Visualize Data":
        st.header("📈 Visualize Data")

        # Visualization options
        column_options = df.columns
        if len(column_options) > 0:
            x_col = st.selectbox("Choose X-axis", column_options)
            y_col = st.selectbox("Choose Y-axis", column_options)

            chart_type = st.radio("Select Chart Type", ("Scatter Plot", "Line Plot", "Bar Plot", "Histogram"))

            if chart_type == "Scatter Plot":
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
                ax.set_title("Scatter Plot")
                st.pyplot(fig)

            elif chart_type == "Line Plot":
                fig, ax = plt.subplots()
                sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
                ax.set_title("Line Plot")
                st.pyplot(fig)

            elif chart_type == "Bar Plot":
                fig, ax = plt.subplots()
                sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
                ax.set_title("Bar Plot")
                st.pyplot(fig)

            elif chart_type == "Histogram":
                fig, ax = plt.subplots()
                sns.histplot(data=df, x=x_col, kde=True, ax=ax)
                ax.set_title("Histogram")
                st.pyplot(fig)

        else:
            st.warning("No columns available for visualization.")

    elif page == "🧹 Data Preprocessing":
        st.header("🧹 Data Preprocessing")

        # Show missing values
        st.subheader("Missing Data")
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        missing_summary = pd.DataFrame({"Missing Values": missing_data, "% Missing": missing_percentage})
        st.dataframe(missing_summary)

        # Options to handle missing values
        st.subheader("Handle Missing Values")
        handling_option = st.radio("Choose an option to handle missing values:", ["Fill with Custom Value", "Drop Rows"])

        if handling_option == "Fill with Custom Value":
            custom_value = st.text_input("Enter the value to fill missing values:")
            if custom_value:
                try:
                    custom_value = float(custom_value) if custom_value.replace('.', '', 1).isdigit() else custom_value
                    df = df.fillna(custom_value)
                    st.success(f"Missing values filled with custom value: {custom_value}")
                except ValueError:
                    st.error("Invalid custom value. Please enter a valid number or text.")
        elif handling_option == "Drop Rows":
            df = df.dropna()
            st.success("Rows with missing values dropped.")

        st.dataframe(df)

    elif page == "📊 Data Summary":
        st.header("📊 Data Summary")

        # Show statistical summary
        st.subheader("Statistical Summary")
        st.dataframe(df.describe())

        # Show data types and unique values
        st.subheader("Column Details")
        column_details = pd.DataFrame({
            "Data Type": df.dtypes,
            "Unique Values": df.nunique()
        })
        st.dataframe(column_details)

else:
    st.info("Please upload a CSV file to get started.")
