# import requests
# from bs4 import BeautifulSoup
# import re
# import csv
# import time
# from random import uniform
# from urllib.parse import urljoin

# # --- Configuration ---
# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
# DELAY = 1  # seconds between requests to be polite

# # --- Functions ---

# def get_website_from_contact_page(location_id):
#     """
#     If a website isn't in the CSV, use this function to get it from the CQC contact page.
#     Takes a CQC Location ID, builds the URL, and scrapes the website.
#     """
#     profile_url = f"https://www.cqc.org.uk/location/{location_id}"
#     contact_url = f"{profile_url}/contact"
#     print(f"    Fetching contact page: {contact_url}")

#     try:
#         response = requests.get(contact_url, headers=HEADERS)
#         response.raise_for_status()
#         time.sleep(uniform(DELAY-0.5, DELAY+0.5))

#     except requests.exceptions.RequestException as e:
#         print(f"    ERROR: Failed to retrieve contact page. {e}")
#         return None

#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # USE THE SELECTOR YOU FOUND THAT WORKS!
#     # Example: website_element = soup.find('a', class_='btn--website')
#     website_element = soup.find('a', class_='email-address') 
    
#     if website_element:
#         org_website = website_element.get('href')
#         print(f"    Found website via CQC: {org_website}")
#         return org_website
#     else:
#         print("    WARNING: The website link was not found on the CQC contact page.")
#         return None


# def scrape_emails_from_website(website_url):
#     """
#     Scrapes a given website URL for visible email addresses.
#     """
#     email = []
#     website_urls= [website_url,website_url+'/about',website_url+'/about-us',website_url+'/contact',website_url+'/contact-us']
#         # if not website_url:
#         #     return []
#     for url in website_urls:
            
#         print(f"    Scraping emails from: {url}")
        
#         try:
#             # Handle relative URLs (e.g., if the link is '/contact-us')
#             if not url.startswith(('http://', 'https://')):
#                 # If the URL in the CSV is just "www.example.com", this makes it "https://www.example.com"
#                 url = urljoin('https://', url)
                
#             response = requests.get(url, headers=HEADERS, timeout=10)
#             response.raise_for_status()
#             html_text = response.text

#         except requests.exceptions.RequestException as e:
#             print(f"      ERROR: Could not fetch the organization's website. {e}")
#             return []

#         # Use a regex pattern to find email addresses in the HTML
#         email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         found_emails = re.findall(email_pattern, html_text)
        
#         # Remove duplicates by converting to a set, then back to a list
#         unique_emails = list(set(found_emails))
        
#         if unique_emails:
#             print(f"      Found {len(unique_emails)} email(s): {', '.join(unique_emails)}")
#             email = unique_emails
#             break
#         else:
#             print(f"      No emails found on the {url} page")
#     return email        


# def main():
#     """
#     Main function to run the entire process using the pre-downloaded CSV.
#     """
#     input_csv = 'cqc_data_original_test.csv'  # Your downloaded CSV file
#     output_csv = 'cqc_data_with_emails.csv' # The new, enhanced file
    
#     # Read all data from the original CSV
#     print(f"Reading data from {input_csv}...")
#     with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
#         # The DictReader uses the first row as column names
#         reader = csv.DictReader(infile)
#         original_fieldnames = reader.fieldnames # Save the original column names
#         all_rows = list(reader) # Read all rows into a list

#     print(f"Found {len(all_rows)} records to process.")
    
#     # Define the new fieldnames for the output CSV (original + new columns)
#     new_fieldnames = original_fieldnames + ['Website Source', 'Emails']
    
#     # Open the output CSV for writing
#     with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
#         writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
#         writer.writeheader()
        
#         # Process each row from the original CSV
#         for index, row in enumerate(all_rows, start=1):
#             print(f"\n[{index}/{len(all_rows)}] Processing: {row.get('Name', 'N/A')}")
            
#             org_website = None
#             website_source = "CSV"
            
#             # Step 1: Try to get the website from the CSV first
#             org_website = row.get('Website', '').strip()
#             if not org_website:
#                 # Step 2: If CSV doesn't have it, try to get it from CQC using the Location ID
#                 location_id = row.get('CQC Location ID', '').strip()
#                 if location_id:
#                     org_website = get_website_from_contact_page(location_id)
#                     website_source = "CQC Scrape"
#                 else:
#                     print("    SKIP: No Website in CSV and no CQC Location ID to find it.")
#                     website_source = "Not Found"
            
#             # Step 3: Scrape emails from the website (if we have one)
#             emails = []
#             if org_website:
#                 emails = scrape_emails_from_website(org_website)
#             else:
#                 print("    SKIP: No website to scrape.")
            
#             # Step 4: Prepare the new row for the output CSV
#             # Copy all original data
#             new_row = row
#             # Add our new data
#             new_row['Website Source'] = website_source
#             new_row['Emails'] = ', '.join(emails)
            
#             # Step 5: Write the updated row to the new CSV
#             writer.writerow(new_row)
            
#             # A small delay to be polite to both CQC and the organization's websites
#             time.sleep(0.5)
    
#     print(f"\nAll done! Results saved to {output_csv}")

# # --- Run the Script ---
# if __name__ == "__main__":
#     main()

import requests
from bs4 import BeautifulSoup
import re
import csv
import time
from random import uniform
from urllib.parse import urljoin

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
DELAY = 1  


def get_website_from_contact_page(location_id):
    """
    If a website isn't in the CSV, use this function to get it from the CQC contact page.
    Takes a CQC Location ID, builds the URL, and scrapes the website.
    """
    profile_url = f"https://www.cqc.org.uk/location/{location_id}"
    contact_url = f"{profile_url}/contact"
    print(f"    Fetching contact page: {contact_url}")

    try:
        response = requests.get(contact_url, headers=HEADERS)
        response.raise_for_status()
        time.sleep(uniform(DELAY-0.5, DELAY+0.5))

    except requests.exceptions.RequestException as e:
        print(f"    ERROR: Failed to retrieve contact page. {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    website_element = soup.find('a', class_='email-address') 
    
    if website_element:
        org_website = website_element.get('href')
        print(f"    Found website via CQC: {org_website}")
        return org_website
    else:
        print("    WARNING: The website link was not found on the CQC contact page.")
        return None

def scrape_page_for_emails(url):
    """
    Helper function to scrape emails from a single specific URL.
    Returns a set of emails found on that page.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        found_emails = re.findall(email_pattern, response.text)
        
        return set(found_emails)  
        
    except requests.exceptions.RequestException:
        return set()

def scrape_emails_from_website(website_url):
    """
    Scrapes a given website URL for visible email addresses.
    Checks the homepage first, then common contact-related pages if none found.
    """
    if not website_url:
        return []
        
    print(f"    Scraping emails from: {website_url}")
    
    CONTACT_PATHS = [
        '/contact',
        '/contact-us',
        '/contact.html',
        '/our-services',
        '/about',
        '/about-us',
        '/about.html',
        '/support',
        '/get-in-touch',
        '/connect',
        '/reach-us'
    ]
    
    all_emails = set() 
    
    try:
        if not website_url.startswith(('http://', 'https://')):
            website_url = urljoin('https://', website_url)
            
        print(f"      Trying homepage...")
        homepage_emails = scrape_page_for_emails(website_url)
        all_emails.update(homepage_emails)
        
        if not homepage_emails:
            print(f"      No emails on homepage. Trying contact pages...")
            
            for path in CONTACT_PATHS:
                contact_url = urljoin(website_url, path)
                print(f"      Trying {path}...")
                
                try:
                    page_emails = scrape_page_for_emails(contact_url)
                    all_emails.update(page_emails)
                    
                    
                    if page_emails:
                        print(f"        Found emails on {path}!") 
                        break  
                        
                except requests.exceptions.RequestException:
                    continue
                    
               
                time.sleep(0.2)

    except requests.exceptions.RequestException as e:
        print(f"      ERROR: Could not process website. {e}")
        return list(all_emails)  

    unique_emails = list(all_emails)
    
    if unique_emails:
        print(f"      Found {len(unique_emails)} unique email(s): {', '.join(unique_emails)}")
    else:
        print("      No emails found on any pages.")
        
    return unique_emails

def main():
    """
    Main function to run the entire process using the pre-downloaded CSV.
    Includes resume functionality to continue from where it left off.
    """
    input_csv = 'cqc_data_original.csv'  
    output_csv = 'cqc_data_with_emails.csv'   
    
    # Read all data from the original CSV
    print(f"Reading data from {input_csv}...")
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        original_fieldnames = reader.fieldnames
        all_rows = list(reader)

    print(f"Found {len(all_rows)} total records in input file.")
    
    # --- RESUME FUNCTIONALITY ---
    # Check if output file exists and get already processed IDs
    processed_ids = set()
    output_exists = False
    
    try:
        with open(output_csv, 'r', newline='', encoding='utf-8') as check_file:
            output_reader = csv.DictReader(check_file)
            if output_reader.fieldnames:  # File exists and has content
                output_exists = True
                for row in output_reader:
                    # Use CQC Location ID to track what's been processed
                    processed_id = row.get('CQC Location ID', '').strip()
                    if processed_id:
                        processed_ids.add(processed_id)
                print(f"Found {len(processed_ids)} already processed records in output file.")
    except FileNotFoundError:
        print("No existing output file found. Starting from scratch.")
    
    # Filter out already processed rows
    rows_to_process = []
    for row in all_rows:
        location_id = row.get('CQC Location ID', '').strip()
        if location_id not in processed_ids:
            rows_to_process.append(row)
    
    print(f"{len(rows_to_process)} records remaining to process.")
    
    if not rows_to_process:
        print("All records have already been processed. Exiting.")
        return
    
    # --- PREPARE OUTPUT FILE ---
    new_fieldnames = original_fieldnames + ['Website Source', 'Emails']
    
    # Open file in appropriate mode: append if exists, write new if not
    file_mode = 'a' if output_exists else 'w'
    
    with open(output_csv, file_mode, newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
        
        # Write header only if creating a new file
        if not output_exists:
            writer.writeheader()
        
        # Process each remaining row
        for index, row in enumerate(rows_to_process, start=1):
            print(f"\n[{index}/{len(rows_to_process)}] Processing: {row.get('Name', 'N/A')}")
            
            org_website = None
            website_source = "CSV"
            
            # Step 1: Try to get the website from the CSV first
            org_website = row.get('Website', '').strip()
            if not org_website:
                # Step 2: If CSV doesn't have it, try to get it from CQC using the Location ID
                location_id = row.get('CQC Location ID', '').strip()
                if location_id:
                    org_website = get_website_from_contact_page(location_id)
                    website_source = "CQC Scrape"
                else:
                    print("    SKIP: No Website in CSV and no CQC Location ID to find it.")
                    website_source = "Not Found"
            
            # Step 3: Scrape emails from the website (if we have one)
            emails = []
            if org_website:
                emails = scrape_emails_from_website(org_website)
            else:
                print("    SKIP: No website to scrape.")
            
            # Step 4: Prepare the new row for the output CSV
            new_row = row.copy()  # Important: create a copy to avoid modifying the original
            new_row['Website Source'] = website_source
            new_row['Emails'] = ', '.join(emails)
            
            # Step 5: Write the updated row to the new CSV
            writer.writerow(new_row)
            
            # Flush the buffer to ensure data is written to disk immediately
            outfile.flush()
            
            # A small delay to be polite to both CQC and the organization's websites
            time.sleep(0.5)
            
            # Progress update every 10 records
            if index % 10 == 0:
                print(f"\n=== Progress: {index}/{len(rows_to_process)} ({index/len(rows_to_process)*100:.1f}%) ===")
    
    print(f"\nAll done! Results saved to {output_csv}")
    # """
    # Main function to run the entire process using the pre-downloaded CSV.
    # """
    # input_csv = 'cqc_data_original.csv'  
    # output_csv = 'cqc_data_with_emails.csv' 
    
    
    # print(f"Reading data from {input_csv}...")
    # with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
    #     reader = csv.DictReader(infile)
    #     original_fieldnames = reader.fieldnames
    #     all_rows = list(reader)

    # print(f"Found {len(all_rows)} records to process.")
    
    # new_fieldnames = original_fieldnames + ['Website Source', 'Emails']
    
    # with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    #     writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
    #     writer.writeheader()
        
    #     for index, row in enumerate(all_rows, start=1):
    #         print(f"\n[{index}/{len(all_rows)}] Processing: {row.get('Name', 'N/A')}")
            
    #         org_website = None
    #         website_source = "CSV"
            
    #         # Step 1: 
    #         org_website = row.get('Website', '').strip()
    #         if not org_website:
    #             # Step 2: 
    #             location_id = row.get('CQC Location ID', '').strip()
    #             if location_id:
    #                 org_website = get_website_from_contact_page(location_id)
    #                 website_source = "CQC Scrape"
    #             else:
    #                 print("    SKIP: No Website in CSV and no CQC Location ID to find it.")
    #                 website_source = "Not Found"
            
    #         # Scrape emails 
    #         emails = []
    #         if org_website:
    #             emails = scrape_emails_from_website(org_website)
    #         else:
    #             print("    SKIP: No website to scrape.")
            
    #         new_row = row
    #         new_row['Website Source'] = website_source
    #         new_row['Emails'] = ', '.join(emails)
            
    #         writer.writerow(new_row)
            
    #         time.sleep(0.5)
    
    # print(f"\nAll done! Results saved to {output_csv}")

if __name__ == "__main__":
    main()