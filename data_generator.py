# data_generator.py
import pandas as pd
from faker import Faker
import asyncio
import random
from datetime import datetime, timedelta
from dateutil import parser as date_parser

fake = Faker()

async def generate_sample_data_async(requirements, num_samples=5):
    """
    Asynchronously generates a sample dataset based on the requirements.
    """
    return await generate_data_async(requirements, num_samples)

async def generate_full_dataset_async(requirements, progress_bar=None):
    """
    Asynchronously generates the full dataset based on the requirements.
    """
    return await generate_data_async(requirements, requirements['num_entries'], progress_bar)

async def generate_data_async(requirements, num_entries, progress_bar=None):
    """
    Core asynchronous data generation function.
    """
    data = {field['name']: [] for field in requirements['fields']}
    total_entries = num_entries
    batch_size = 1000  # Adjust based on performance
    batches = total_entries // batch_size + 1

    for batch_num in range(batches):
        tasks = []
        current_batch_size = min(batch_size, total_entries - batch_num * batch_size)
        for _ in range(current_batch_size):
            tasks.append(asyncio.create_task(generate_single_entry(requirements)))
        results = await asyncio.gather(*tasks)
        for entry in results:
            for field_name, value in entry.items():
                data[field_name].append(value)

        # Update progress bar if provided
        if progress_bar:
            progress = (batch_num + 1) / batches
            progress_bar.progress(progress)

    df = pd.DataFrame(data)
    return df

async def generate_single_entry(requirements):
    """
    Generates a single data entry asynchronously.
    """
    entry = {}
    for field in requirements['fields']:
        field_name = field['name']
        field_type = field.get('type', 'string').lower()
        constraints = field.get('constraints', '')
        entry[field_name] = await generate_field_data_async(field_name, field_type, constraints)
    return entry

async def generate_field_data_async(field_name, field_type, constraints):
    """
    Asynchronously generates data for a specific field based on its type and constraints.
    """
    await asyncio.sleep(0)  # Yield control to the event loop

    if field_type == 'integer':
        return generate_integer(constraints)
    elif field_type == 'float':
        return generate_float(constraints)
    elif field_type == 'string':
        return generate_string(constraints)
    elif field_type == 'date':
        return generate_date(constraints)
    elif field_type == 'datetime':
        return generate_datetime(constraints)
    elif field_type == 'categorical':
        return generate_categorical(constraints)
    elif field_type == 'boolean':
        return generate_boolean()
    else:
        # Default to string if type is unknown
        return generate_string(constraints)

def generate_integer(constraints):
    min_value, max_value = parse_min_max_constraints(constraints, default_min=0, default_max=100)
    return random.randint(int(min_value), int(max_value))

def generate_float(constraints):
    min_value, max_value = parse_min_max_constraints(constraints, default_min=0.0, default_max=100.0)
    return random.uniform(min_value, max_value)

def generate_string(constraints):
    if 'options:' in constraints.lower():
        options = parse_options(constraints)
        return random.choice(options)
    else:
        return fake.word()

def generate_categorical(constraints):
    if 'categories:' in constraints.lower():
        categories = parse_options(constraints)
        return random.choice(categories)
    else:
        # Default categories if none provided
        default_categories = ['Category A', 'Category B', 'Category C']
        return random.choice(default_categories)

def generate_date(constraints):
    start_date, end_date = parse_date_constraints(constraints)
    return fake.date_between(start_date=start_date, end_date=end_date)

def generate_datetime(constraints):
    start_date, end_date = parse_date_constraints(constraints)
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def generate_boolean():
    return random.choice([True, False])

def parse_min_max_constraints(constraints_str, default_min, default_max):
    """
    Parses constraints like 'between 18 and 65' to extract min and max values.
    """
    try:
        import re
        match = re.search(r'between\s+([\d\.]+)\s+and\s+([\d\.]+)', constraints_str, re.IGNORECASE)
        if match:
            min_value = float(match.group(1))
            max_value = float(match.group(2))
            return min_value, max_value
    except:
        pass
    return default_min, default_max

def parse_options(constraints_str):
    """
    Parses options or categories from constraints like 'options: red, green, blue'
    """
    try:
        import re
        match = re.search(r'(options|categories):\s*(.+)', constraints_str, re.IGNORECASE)
        if match:
            options_str = match.group(2)
            options = [option.strip() for option in options_str.split(',')]
            return options
    except:
        pass
    return []

def parse_date_constraints(constraints_str):
    """
    Parses date constraints to extract start and end dates.
    """
    default_start = datetime.now() - timedelta(days=365 * 5)
    default_end = datetime.now()

    try:
        import re
        match = re.search(r'between\s+([\w\s,0-9-]+)\s+and\s+([\w\s,0-9-]+)', constraints_str, re.IGNORECASE)
        if match:
            start_date_str = match.group(1).strip()
            end_date_str = match.group(2).strip()
            start_date = date_parser.parse(start_date_str)
            end_date = date_parser.parse(end_date_str)
            return start_date, end_date
    except:
        pass
    return default_start, default_end

