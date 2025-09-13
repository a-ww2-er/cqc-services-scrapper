import requests
from bs4 import BeautifulSoup

contact_url = 'https://www.cqc.org.uk/location/1-10023053398/contact'

response = requests.get(contact_url)

if response.status_code == 200:
    print("Successfully fetched the page!")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
   
    website_element = soup.find('a', class_='email-address') 
    
    if website_element:
        org_website = website_element.get('href')
        print(f"Extracted Website: {org_website}")
    else:
        print("Could not find the website link on the page.")
        
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")