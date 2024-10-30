# data_exporter.py
import pandas as pd
from io import BytesIO
import xml.etree.ElementTree as ET

def export_dataset(df, file_format):
    """
    Exports the DataFrame to the specified file format.
    Returns a tuple of (data, mime_type).
    """
    if file_format == 'CSV':
        return df.to_csv(index=False).encode('utf-8'), 'text/csv'
    elif file_format == 'Excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file_format == 'JSON':
        return df.to_json(orient='records').encode('utf-8'), 'application/json'
    elif file_format == 'XML':
        return df_to_xml_bytes(df), 'application/xml'
    elif file_format == 'Parquet':
        output = BytesIO()
        df.to_parquet(output, index=False)
        return output.getvalue(), 'application/octet-stream'
    else:
        raise ValueError("Unsupported file format.")

def df_to_xml_bytes(df):
    """
    Converts a DataFrame to XML bytes.
    """
    root = ET.Element('root')
    for _, row in df.iterrows():
        item = ET.SubElement(root, 'row')
        for col_name, value in row.items():
            col = ET.SubElement(item, col_name)
            col.text = str(value)
    tree = ET.ElementTree(root)
    output = BytesIO()
    tree.write(output, encoding='utf-8', xml_declaration=True)
    return output.getvalue()