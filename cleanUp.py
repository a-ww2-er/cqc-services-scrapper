import csv
import re
from collections import defaultdict

def clean_csv(input_file, output_file):
    """
    Clean the CSV file by:
    1. Removing rows without emails
    2. Removing duplicate rows based on email addresses
    3. Saving the cleaned data to a new file
    """
    
    # Read the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    print(f"Original number of rows: {len(rows)}")
    
    # Track seen emails to identify duplicates
    seen_emails = defaultdict(list)
    cleaned_rows = []
    rows_without_emails = 0
    
    for row in rows:
        emails = row.get('Emails', '').strip()
        
        # Skip rows without emails
        if not emails:
            rows_without_emails += 1
            continue
        
        # Extract individual emails from the comma-separated string
        email_list = [email.strip() for email in emails.split(',')]
        
        # Check if any of these emails have been seen before
        is_duplicate = False
        for email in email_list:
            if email in seen_emails:
                is_duplicate = True
                break
        
        # If not a duplicate, add to cleaned rows and mark emails as seen
        if not is_duplicate:
            cleaned_rows.append(row)
            for email in email_list:
                seen_emails[email].append(len(cleaned_rows) - 1)
    
    print(f"Rows without emails: {rows_without_emails}")
    print(f"Duplicate rows removed: {len(rows) - len(cleaned_rows) - rows_without_emails}")
    print(f"Final number of rows: {len(cleaned_rows)}")
    
    # Write the cleaned data to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print(f"Cleaned data saved to: {output_file}")

def clean_csv_advanced(input_file, output_file, dedupe_by='Emails'):
    """
    Advanced cleaning with more options:
    1. Remove rows without emails
    2. Remove duplicate rows based on specified column(s)
    3. Save the cleaned data to a new file
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        dedupe_by: Column name to use for deduplication (default: 'Emails')
    """
    
    # Read the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    print(f"Original number of rows: {len(rows)}")
    
    # Track seen values to identify duplicates
    seen_values = set()
    cleaned_rows = []
    rows_without_emails = 0
    
    for row in rows:
        # Check if row has emails
        emails = row.get('Emails', '').strip()
        if not emails:
            rows_without_emails += 1
            continue
        
        # Get the value to use for deduplication
        dedupe_value = row.get(dedupe_by, '').strip()
        
        # Skip if no deduplication value found
        if not dedupe_value:
            continue
        
        # Check if this is a duplicate
        if dedupe_value not in seen_values:
            cleaned_rows.append(row)
            seen_values.add(dedupe_value)
    
    print(f"Rows without emails: {rows_without_emails}")
    print(f"Duplicate rows removed: {len(rows) - len(cleaned_rows) - rows_without_emails}")
    print(f"Final number of rows: {len(cleaned_rows)}")
    
    # Write the cleaned data to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print(f"Cleaned data saved to: {output_file}")

if __name__ == "__main__":
    input_csv = 'cqc_data_with_emails.csv'
    output_csv = 'cqc_data_cleaned.csv'
    
    # Simple cleaning
    # clean_csv(input_csv, output_csv)
    
    # For more advanced deduplication (e.g., by organization name or ID)
    clean_csv_advanced(input_csv, output_csv, dedupe_by='Emails')