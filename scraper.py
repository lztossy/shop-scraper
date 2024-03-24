from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
import sys

def print_green(text):
    print("\033[92m{}\033[0m".format(text))

def check_payment_method(url, payment_method):
    try:
        response = requests.get(url, timeout=10)  
        page_content = response.text.lower()

        payment_patterns = {
            'paypal': r'paypal',
            'card': r'visa|mastercard|amex|discover',
            'bitcoin': r'bitcoin',
        }

        if payment_method in payment_patterns:
            return re.search(payment_patterns[payment_method], page_content) is not None
        else:
            print_green(f"Payment method '{payment_method}' is not supported.")
            return False
    except Exception as e:
        print_green(f"An error occurred while checking the payment method at URL {url}: {e}")
        return False

country = input("Enter the country you want to scrape for: ")
product_genre = input("Enter the product genre you want to scrape for: ")
payment_method = input("What Payment method would you like to scrape for? ").lower()
amount_of_scrapes = int(input("Enter the number of search results you want to scrape: "))

query = f"buy {product_genre} online {country}"
print("Starting search...")

search_results = []
try:
    for url in search(query, num_results=amount_of_scrapes):
        search_results.append(url)
except Exception as e:
    print_green(f"An error occurred during the search: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

print("Search completed.")

save_path = 'scraped_urls.txt'

websites_with_payment_method = []

for url in search_results:
    if check_payment_method(url, payment_method):
        websites_with_payment_method.append(url)
        print_green(f"URL added: {url}")

with open(save_path, 'w') as file:
    for website in websites_with_payment_method:
        file.write(website + '\n')

print_green(f"\nSuccessfully scraped URLs and saved to {save_path}\n")

input("Press Enter to exit...")
