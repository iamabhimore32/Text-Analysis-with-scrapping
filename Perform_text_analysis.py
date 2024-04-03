import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk
nltk.download('punkt')
nltk.download('stopwords')
# imported nltk librarie to perform text anlysis



# Created Function to extract title and text from a given URL
def extract_article_text(url):
    try:
        response = requests.get(url)
        #Parses the HTML using BeautifulSoup.
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title and article text
        title = soup.find('title').text.strip()
        article_text = '\n'.join([p.text for p in soup.find_all('p')])

        return title, article_text
    except Exception as e:
        # Handle any errors that may occur during the extraction
        print(f"Error extracting data from {url}: {e}")
        return None, None
    
# this function is created fro the text analysis on the article text.
def perform_text_analysis(article_text):
    # Tokenize words and sentences
    words = word_tokenize(article_text)
    sentences = sent_tokenize(article_text)

    # Remove common english stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Compute word frequency distribution
    word_freq_dist = FreqDist(filtered_words)

    # Compute variables text analysis metrics
    total_words = len(words)
    total_sentences = len(sentences)
    unique_words = len(set(filtered_words))
    most_common_word, most_common_word_freq = word_freq_dist.most_common(1)[0] if word_freq_dist else ('', 0)

    return total_words, total_sentences, unique_words, most_common_word, most_common_word_freq

# Main function to read input, perform analysis, and save results
def main():
    # Read the input Excel file containing URLs
    input_file_path = 'Input.xlsx'
    df_input = pd.read_excel(input_file_path)

    # Create an empty DataFrame to store analysis results
    columns = ['URL_ID', 'Total_Words', 'Total_Sentences', 'Unique_Words', 'Most_Common_Word', 'Most_Common_Word_Frequency']
    df_output = pd.DataFrame(columns=columns)

    # Loop through the URLs in the input file
    for index, row in df_input.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        # Extract article text
        title, article_text = extract_article_text(url)

        if title and article_text:
            # Perform text analysis on extracted articles text
            total_words, total_sentences, unique_words, most_common_word, most_common_word_freq = perform_text_analysis(article_text)

            # Append the analysis results to the output DataFrame
            df_output = df_output.append({
                'URL_ID': url_id,
                'Total_Words': total_words,
                'Total_Sentences': total_sentences,
                'Unique_Words': unique_words,
                'Most_Common_Word': most_common_word,
                'Most_Common_Word_Frequency': most_common_word_freq
            }, ignore_index=True)
            
            
            # Print a message indicating the completion of analysis for the current URL
            print(f"Textual analysis for {url} completed.")
    # Save the output DataFrame to the output structure Excel file
    output_structure_file = 'Output Data Structure.xlsx'
    df_output.to_excel(output_structure_file, index=False)
    print(f"Analysis results saved to {output_structure_file}")

if __name__ == "__main__":
    main()