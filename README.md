# Dataset-Generator-using-OpenAI-API
This project provides a tool for generating custom synthetic datasets based on user-specified requirements. Built with `Streamlit` as a frontend interface, users can describe their dataset needs, and the application will generate and allow downloads in various formats (CSV, Excel, JSON, XML, Parquet).

## Components

1. **app.py**: The main application interface built with Streamlit. Users input dataset specifications, view parsed requirements, and download generated datasets.
2. **nlp_parser.py**: Uses OpenAI API to parse user input, extracting dataset fields and constraints.
3. **data_generator.py**: Asynchronous functions to generate sample or full datasets based on parsed requirements.
4. **data_exporter.py**: Exports the dataset to the requested file format.

## Features

- **Natural Language Input**: Parse user input using OpenAI's API.
- **Dataset Generation**: Create sample and full datasets asynchronously.
- **Download in Multiple Formats**: CSV, Excel, JSON, XML, and Parquet.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API Key (stored in `.env` file as `OPENAI_API_KEY`)

### Installation

1. **Clone this repository**:
   ```bash
   git clone <repo-url>
   cd synthetic-dataset-generator

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Add your OpenAI API key**:
   ```bash
   OPENAI_API_KEY=your_openai_api_key

4. **Running the Application**:
   ```bash
   streamlit run app.py

## Usage

1.	Enter Dataset Requirements: Describe the dataset you need in the text box (e.g., “I need a dataset for analyzing customer behavior in retail. It should have 2000 entries with fields like purchase date, product category, customer age (over 18), and amount spent (under 1000)”).
2.	Generate Sample: Submit the form to parse your input. The application will display the interpreted requirements in JSON format.
3.	View and Confirm: Preview a sample dataset based on your input, and confirm if it meets your needs.
4.	Download: After confirming, generate the full dataset and download it in your selected format(s).
   


