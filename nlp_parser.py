# nlp_parser.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import traceback
import re
import time

# Load environment variables from .env file
load_dotenv(dotenv_path='key.env')

# Create OpenAI client instance using the API key from environment variables
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def parse_user_input(user_input):
    """
    Uses OpenAI's chat completion API to parse the user's textual input and extract dataset requirements.
    """
    system_message = """
    You are a helpful assistant that extracts detailed dataset requirements from user input.

    Given the user's request, extract the following information in valid JSON format:

    - domain: The domain or field of the dataset (e.g., retail, healthcare).
    - num_entries: The number of data entries required (default to 1000 if not specified).
    - fields: A list of dictionaries, each containing:
        - name: The field name (e.g., "age", "purchase date").
        - type: The data type (e.g., "integer", "float", "string", "date", "datetime", "categorical", "boolean").
    - constraints: Any constraints on the dataset (e.g., "age > 18", "price <= 1000").
    """

    try:
        # Using the OpenAI client to create a chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ]
        )
        
        # Extracting the content from the response
        response_content = response['choices'][0]['message']['content']
        return json.loads(response_content)  # Parse and return JSON

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    user_input = """
    I need a dataset for analyzing customer behavior in a retail store. 
    It should contain 2000 entries and include fields such as purchase date, product category, customer age, and total spent. 
    Make sure the age is over 18 and total spent is less than 1000.
    """
    
    # Call the function and print the results
    parsed_data = parse_user_input(user_input)
    print(json.dumps(parsed_data, indent=2))