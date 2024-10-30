# app.py
import streamlit as st
from nlp_parser import parse_user_input
from data_generator import generate_sample_data_async, generate_full_dataset_async
from data_exporter import export_dataset
import asyncio

# Set page configuration
st.set_page_config(page_title="Synthetic Dataset Generator", page_icon="📊", layout="wide")

def main():
    st.title("📊 Synthetic Dataset Generator")
    st.markdown("""
    Welcome to the Synthetic Dataset Generator! This tool allows you to generate custom synthetic datasets for your machine learning projects. Simply describe the dataset you need, and we'll handle the rest.
    """)

    # Step 1: User Input
    st.header("📝 Enter Your Dataset Requirements")
    with st.form("dataset_form"):
        user_input = st.text_area("Describe the dataset you need:", height=150)
        formats = st.multiselect(
            "Select the desired file format(s):",
            ['CSV', 'Excel', 'JSON', 'XML', 'Parquet'],
            default=['CSV']
        )
        submitted = st.form_submit_button("Generate Sample")

    if submitted:
        if user_input.strip():
            # Step 2: Parse Input
            with st.spinner("Parsing your input..."):
                requirements = parse_user_input(user_input)
            if requirements:
                st.subheader("📄 Parsed Requirements")
                st.json(requirements)

                # Step 3: Generate Sample Data
                st.subheader("🔍 Sample Data Preview")
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    sample_df = loop.run_until_complete(generate_sample_data_async(requirements))
                    st.dataframe(sample_df)
                except Exception as e:
                    st.error(f"An error occurred while generating sample data: {e}")
                    return

                # Confirmation
                generate_full = st.button("Confirm and Generate Full Dataset")
                if generate_full:
                    # Step 4: Generate Full Dataset
                    st.subheader("⏳ Generating Full Dataset")
                    progress_bar = st.progress(0)
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        full_df = loop.run_until_complete(generate_full_dataset_async(requirements, progress_bar))
                        st.success("✅ Dataset Generated Successfully!")

                        # Step 5: Provide Download Links
                        st.subheader("💾 Download Dataset")
                        for file_format in formats:
                            dataset, mime_type = export_dataset(full_df, file_format)
                            st.download_button(
                                label=f"Download {file_format}",
                                data=dataset,
                                file_name=f"synthetic_dataset.{get_file_extension(file_format)}",
                                mime=mime_type
                            )
                    except Exception as e:
                        st.error(f"An error occurred while generating the full dataset: {e}")
            else:
                st.error("❌ Failed to parse the input. Please try again with a different description.")
        else:
            st.warning("⚠️ Please enter your dataset requirements.")

def get_file_extension(file_format):
    """
    Returns the appropriate file extension for a given file format.
    """
    extensions = {
        'CSV': 'csv',
        'Excel': 'xlsx',
        'JSON': 'json',
        'XML': 'xml',
        'Parquet': 'parquet'
    }
    return extensions.get(file_format, 'dat')

if __name__ == "__main__":
    main()