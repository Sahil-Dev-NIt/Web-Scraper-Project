import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
BASE_URL = "http://quotes.toscrape.com/page/{}/"

# Store data
quotes_data = []

def scrape_page(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return False
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    quotes = soup.find_all("div", class_="quote")
    
    for quote in quotes:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        
        quotes_data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })
    
    return True


def main():
    page = 1
    
    while True:
        url = BASE_URL.format(page)
        print(f"Scraping page {page}...")
        
        success = scrape_page(url)
        
        if not success:
            break
        
        page += 1
        
        # Stop after 10 pages (safe limit)
        if page > 10:
            break

    # Convert to DataFrame
    df = pd.DataFrame(quotes_data)
    
    # Save to CSV
    df.to_csv("output.csv", index=False)
    
    print("Data saved to output.csv")


if __name__ == "__main__":
    main()
