import pandas as pd
import re
import csv

class EmailCleaner:
    def __init__(self):
        # Define patterns for unwanted emails
        self.sentry_pattern = re.compile(r'^[a-f0-9]{32}@sentry', re.IGNORECASE)
        self.image_pattern = re.compile(r'\.(jpg|jpeg|png|gif|webp|bmp|tiff|svg|js|Pv|ai)$', re.IGNORECASE)
        self.generic_domain_pattern = re.compile(r'@(domain\.com|example\.com|test\.com|example\.org|mydomain\.com|godaddy\.com|email\.com|website\.com|mysite\.com|youremaildomain\.com|TheNameGuy\.com|domain\.co.uk|company\.com|provider\.com|doe\.com|freehtml5\.co|yourdomain\.com)$', re.IGNORECASE)
        
        # Role-based email patterns
        self.role_emails = {
            'abuse', 'admin', 'billing', 'compliance', 'devnull', 'dns', 'ftp', 
            'you','donotreply.myaccount','donotreply','yourename','sample','example',
            'hostmaster', 'inoc', 'ispfeedback', 'ispsupport', 'list-request', 
            'list', 'maildaemon', 'noc', 'no-reply', 'noreply', 'null', 'phish', 
            'phishing', 'postmaster', 'privacy', 'registrar', 'root', 'security', 
            'spam', 'support', 'sysadmin', 'tech', 'name', 'undisclosed-recipients', 
            'unsubscribe', 'usenet', 'uucp', 'webmaster', 'www'
        }
        
        # Marketing target patterns (priority emails to keep)
        self.marketing_targets = {
            'info', 'contact', 'hello', 'hello', 'enquiries', 'inquiry', 
            'sales', 'business', 'careers', 'jobs', 'hr', 'recruitment',
            'marketing', 'media', 'pr', 'press', 'partnership', 'collaboration'
        }
    
    def is_unwanted_email(self, email):
        """Check if email matches any unwanted patterns"""
        email = email.strip().lower()
        
        # Check for sentry-like emails (hex strings)
        if self.sentry_pattern.match(email):
            return True
            
        # Check for image filenames
        if self.image_pattern.search(email):
            return True
            
        # Check for generic domains
        if self.generic_domain_pattern.search(email):
            return True
            
        # Check for role-based emails
        username = email.split('@')[0] if '@' in email else ''
        if username in self.role_emails:
            return True
            
        return False
    
    def is_marketing_target(self, email):
        """Check if email is a marketing target"""
        email = email.strip().lower()
        if '@' not in email:
            return False
            
        username = email.split('@')[0]
        return username in self.marketing_targets
    
    def clean_email_list(self, emails_str):
        """Clean a comma-separated string of emails"""
        if not emails_str or pd.isna(emails_str):
            return [], []
            
        # Split and clean individual emails
        emails = [email.strip() for email in emails_str.split(',')]
        
        # Remove unwanted emails
        valid_emails = [email for email in emails if not self.is_unwanted_email(email)]
        
        return valid_emails
    
    def segregate_emails(self, emails):
        """Segregate emails into primary and other categories"""
        if not emails:
            return '', ''
        
        # Find marketing target emails
        marketing_emails = [email for email in emails if self.is_marketing_target(email)]
        other_emails = [email for email in emails if not self.is_marketing_target(email)]
        
        # Priority: marketing targets first, then first valid email
        if marketing_emails:
            primary_email = marketing_emails[0]
            # Combine remaining marketing emails with other emails
            remaining_emails = marketing_emails[1:] + other_emails
        elif emails:
            primary_email = emails[0]
            remaining_emails = emails[1:]
        else:
            primary_email = ''
            remaining_emails = []
        
        return primary_email, ', '.join(remaining_emails) if remaining_emails else ''
    
    def process_row(self, row):
        """Process a single row of data"""
        emails_str = row.get('Emails', '')
        
        # Clean the email list
        cleaned_emails = self.clean_email_list(emails_str)
        
        # Segregate into primary and other emails
        primary_email, other_emails = self.segregate_emails(cleaned_emails)
        
        # Update the row
        row['Emails'] = primary_email
        row['Other_Emails'] = other_emails
        
        return row
    
    def process_csv(self, input_file, output_file):
        """Process the entire CSV file"""
        print(f"Reading data from {input_file}...")
        
        # Read CSV
        df = pd.read_csv(input_file)
        
        # Add Other_Emails column if it doesn't exist
        if 'Other_Emails' not in df.columns:
            df['Other_Emails'] = ''
        
        original_count = len(df)
        print(f"Original records: {original_count}")
        
        # Process each row
        processed_rows = []
        emails_removed_count = 0
        
        for index, row in df.iterrows():
            original_emails = row.get('Emails', '')
            
            # Process the row
            processed_row = self.process_row(row.to_dict())
            
            # Check if emails were completely removed
            if original_emails and not processed_row['Emails'] and not processed_row['Other_Emails']:
                emails_removed_count += 1
                # Keep the row but mark it as having no valid emails
                processed_row['Emails'] = ''
                processed_row['Other_Emails'] = ''
                continue
            
            processed_rows.append(processed_row)
        
        # Create new DataFrame
        cleaned_df = pd.DataFrame(processed_rows)
        
        # Remove rows that have no emails at all (optional - you can comment this out if you want to keep them)
        # cleaned_df = cleaned_df[(cleaned_df['Emails'] != '') | (cleaned_df['Other_Emails'] != '')]
        
        print(f"Records with emails completely removed: {emails_removed_count}")
        print(f"Final records: {len(cleaned_df)}")
        
        # Save to CSV
        cleaned_df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to: {output_file}")
        
        return cleaned_df

def analyze_email_patterns(df):
    """Analyze the email patterns in the data"""
    print("\n=== Email Pattern Analysis ===")
    
    all_emails = []
    for emails_str in df['Emails'].dropna():
        if emails_str:
            all_emails.extend([email.strip() for email in emails_str.split(',')])
    
    if not all_emails:
        print("No emails found for analysis")
        return
    
    # Analyze usernames
    usernames = {}
    for email in all_emails:
        if '@' in email:
            username = email.split('@')[0].lower()
            usernames[username] = usernames.get(username, 0) + 1
    
    # Show most common usernames
    print("\nMost common email usernames:")
    for username, count in sorted(usernames.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {username}: {count} occurrences")

def main():
    # File paths
    input_file = 'cqc_data_cleaned.csv'  # Your cleaned CSV file
    output_file = 'cqc_data_final_cleaned.csv'
    
    # Initialize cleaner
    cleaner = EmailCleaner()
    
    # Process the CSV
    cleaned_df = cleaner.process_csv(input_file, output_file)
    
    # Analyze results
    analyze_email_patterns(cleaned_df)
    
    # Show sample of results
    print("\n=== Sample of Cleaned Data ===")
    sample_data = cleaned_df[['Name', 'Emails', 'Other_Emails']].head(10)
    for _, row in sample_data.iterrows():
        print(f"Organization: {row['Name']}")
        print(f"  Primary Email: {row['Emails']}")
        print(f"  Other Emails: {row['Other_Emails']}")
        print()

if __name__ == "__main__":
    main()