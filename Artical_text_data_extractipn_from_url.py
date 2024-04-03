# importing libraries
import os
import requests  # with this we can make http request to fetch web pages.
from bs4 import BeautifulSoup # we uses BeautifulSoup for the Parsing html content.
import pandas as pd

# by taking url as a input and by using requests we gets the html content of the page 
def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') #Parses the HTML using BeautifulSoup.

        # Extract title and article text (<p> tags)
        title = soup.find('title').text.strip()
        article_text = '\n'.join([p.text for p in soup.find_all('p')])

        return title, article_text
    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        return None, None

def main():
    # Read the input Excel file using pandas library
    input_file_path = 'Input.xlsx'
    df = pd.read_excel(input_file_path)

    # Create a directory to save text files
    output_directory = 'output_texts'
    os.makedirs(output_directory, exist_ok=True)

    # Loop through the URLs in the input file
    for index, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        # Extract article text
        title, article_text = extract_article_text(url)

        if title and article_text:
            # Save the extracted text to a file
            output_file_path = os.path.join(output_directory, f'{url_id}.txt') # here we takes the usrl_id as the name of output text file
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(f'Title: {title}\n\n{article_text}')

            print(f"Data extracted from {url} and saved to {output_file_path}")

if __name__ == "__main__":
    main()
